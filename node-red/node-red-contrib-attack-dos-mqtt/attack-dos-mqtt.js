const { PythonShell } = require('python-shell');

module.exports = function(RED) {
    function AttackDOS(config) {
        RED.nodes.createNode(this, config);
        var node = this;
        RED.httpAdmin.post("/dos-mqtt", function(req, res) {
            var data = req.body;
            console.log("Received data:", data);
            var jsonPayload = JSON.stringify(data);
            let pyshell = new PythonShell('node_modules/node-red-contrib-attack-dos-mqtt/dos.py');
            pyshell.send(jsonPayload);
            pyshell.on('message', function (message) {
                console.log(message)
                
                node.send({ payload: message });
            });
            pyshell.end(function (err,code,signal) {
            if (err) throw err;
                console.log('The exit code was: ' + code);
                console.log('The exit signal was: ' + signal);
                console.log('finished');
            });
     
            
        });

    }
    RED.nodes.registerType("attack-dos-mqtt", AttackDOS);
}
