const { PythonShell } = require('python-shell');

module.exports = function(RED) {
    function SpoofingIOT(config) {
        RED.nodes.createNode(this, config);
        var node = this;
        node.on('input', function(msg) {
            // Tạo một tùy chọn để gọi mã Pythonmp
            let pyshell = new PythonShell('node_modules/node-red-contrib-attack-spoofing-iot/spoofing-iot.py');
            pyshell.send([msg.payload]);
            pyshell.on('message', function (message) {
            msg.payload = message;
            node.send(msg);
            console.log(message);
            });

            // end the input stream and allow the process to exit
            pyshell.end(function (err,code,signal) {
            if (err) throw err;
                console.log('The exit code was: ' + code);
                console.log('The exit signal was: ' + signal);
                console.log('finished');
            });
            // var options = {
            //     mode: 'text',
            //     pythonOptions: ['-u'], // unbuffered output
            //     scriptPath: './node-red-contrib-attack-spoofing-iot', // Đường dẫn đến script Python của bạn
            //     args: [msg.payload] // Các đối số truyền vào cho script Python
            // };
            // PythonShell.run('spoofing-iot.py', options).then(messages=>{
            //     // results is an array consisting of messages collected during execution
            //     msg.payload = messages;
            //     console.log("Messages: ",messages)
            //     node.send(msg);
            //   });
        });
    }
    RED.nodes.registerType("spoofing-iot", SpoofingIOT);
}
