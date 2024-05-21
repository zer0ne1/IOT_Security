const { PythonShell } = require('python-shell');

module.exports = function(RED) {
    function AttackDictionary(config) {
        RED.nodes.createNode(this, config);
        var node = this;

        node.on('input', function(msg) {
            var jsonPayload = JSON.stringify(msg.payload);
            // Tạo một tùy chọn để gọi mã Pythonmp
            let pyshell = new PythonShell('node_modules/node-red-contrib-attack-dictionary/attack-dictionary.py');
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
    }
    RED.nodes.registerType("attack-dictionary", AttackDictionary);
}
