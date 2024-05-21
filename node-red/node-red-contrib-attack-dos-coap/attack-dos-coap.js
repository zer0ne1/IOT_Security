const { PythonShell } = require('python-shell');

module.exports = function(RED) {
    function AttackDOSCoAP(config) {
        RED.nodes.createNode(this, config);
        var node = this;
        node.on('input', function(msg) {
            var jsonPayload = JSON.stringify(msg.payload);
            // Tạo một tùy chọn để gọi mã Pythonmp
            let pyshell = new PythonShell('node_modules/node-red-contrib-attack-dos-coap/dos.py');
            pyshell.send(jsonPayload);
            
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
        });

        // node.on('input', function(msg) {
        //     // Tạo một tùy chọn để gọi mã Python
        //     var jsonPayload = JSON.stringify(msg.payload);
        //     var options = {
        //         mode: 'text',
        //         pythonOptions: ['-u'], // unbuffered output
        //         scriptPath: './node-red-contrib-attack-dos-coap', // Đường dẫn đến script Python của bạn
        //         args: [jsonPayload] // Các đối số truyền vào cho script Python
        //     };
        //     PythonShell.run('dos.py', options).then(messages=>{
        //         // results is an array consisting of messages collected during execution
        //         msg.payload = messages;
        //         node.send(msg);
        //       });
        // });
    }
    RED.nodes.registerType("attack-dos-coap", AttackDOSCoAP);
}
