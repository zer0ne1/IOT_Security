const { PythonShell } = require('python-shell');
const multer = require('multer');

module.exports = function(RED) {
    function SpoofingNew(config) {
        RED.nodes.createNode(this, config);
        var node = this;
        // Cấu hình multer để lưu trữ tệp trong bộ nhớ
        const storage = multer.memoryStorage();
        const upload = multer({ storage: storage });

        // Đường dẫn để xử lý tải lên tệp
        RED.httpAdmin.post("/spoofing-new", upload.single('file'), function(req, res) {
            const data = req.body;
            const file = req.file;

            if (file) {
                // Đọc nội dung tệp từ bộ nhớ
                const fileBuffer = file.buffer;
                // Nếu muốn hiển thị dưới dạng chuỗi hex
                const fileHex = fileBuffer.toString('hex');
                dataEnd={
                    content:fileHex,
                    ipserver:data.ipserver,
                    port:data.port,
                    time:data.time
                }
                const jsonPayload = JSON.stringify(dataEnd);
            let pyshell = new PythonShell('node_modules/node-red-contrib-attack-spoofing-new/spoofing-new.py');
            pyshell.send(jsonPayload);
            pyshell.on('message', function (message) {
                node.send({ payload: message });
                node.warn(message)
            });

            pyshell.end(function (err, code, signal) {
                if (err) throw err;
                console.log('The exit code was: ' + code);
                console.log('The exit signal was: ' + signal);
                console.log('finished');
            });
                
            } else {
                console.log("No file received");
            }
        });
    }
    RED.nodes.registerType("spoofing-new", SpoofingNew);
}
