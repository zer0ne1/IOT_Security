const { PythonShell } = require('python-shell');

module.exports = function(RED) {
    function DetectXSS(config) {
        RED.nodes.createNode(this, config);
        var node = this;

        node.on('input', function(msg) {
            // Tạo một tùy chọn để gọi mã Python
            var options = {
                mode: 'text',
                pythonOptions: ['-u'], // unbuffered output
                scriptPath: './node-red-contrib-attack-detect-xss', // Đường dẫn đến script Python của bạn
                args: [msg.payload] // Các đối số truyền vào cho script Python
            };
            PythonShell.run('xss.py', options).then(messages=>{
                // results is an array consisting of messages collected during execution
                msg.payload = messages;
                node.send(msg);
              });
        });
    }
    RED.nodes.registerType("detect-xss", DetectXSS);
}
