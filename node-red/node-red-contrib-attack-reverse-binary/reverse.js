const { PythonShell } = require('python-shell');
const multer = require('multer');

module.exports = function(RED) {
    function AttackReverse(config) {
        RED.nodes.createNode(this, config);
        var node = this;

        // Cấu hình multer để lưu trữ tệp trong bộ nhớ
        const storage = multer.memoryStorage();
        const upload = multer({ storage: storage });

        // Đường dẫn để xử lý tải lên tệp
        RED.httpAdmin.post("/reverse-binary", upload.single('file'), function(req, res) {
            const data = req.body;
            const file = req.file;

            if (file) {
                // Đọc nội dung tệp từ bộ nhớ
                const fileBuffer = file.buffer;
                // Nếu muốn hiển thị dưới dạng chuỗi hex
                const fileHex = fileBuffer.toString('hex');
                dataEnd={
                    content:fileHex,
                    architectures:data.architectures,
                    mode:data.mode
                }
                
                const jsonPayload = JSON.stringify(dataEnd);

            let pyshell = new PythonShell('node_modules/node-red-contrib-attack-reverse-binary/reverse.py');
            console.log("alo",jsonPayload)
            pyshell.send(jsonPayload);
            console.log("alo123",jsonPayload)
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
    RED.nodes.registerType("attack-reverse-binary", AttackReverse);
}
