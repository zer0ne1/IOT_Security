const { PythonShell } = require('python-shell');

module.exports = function(RED) {
    function SpoofingIOT(config) {
        RED.nodes.createNode(this, config);
        var node = this;
        RED.httpAdmin.post("/inject-data", function(req, res) {
            var data = req.body;
            console.log("Received data:", data);
            var jsonPayload = JSON.stringify(data);
            let pyshell = new PythonShell('node_modules/node-red-contrib-attack-spoofing-iot/spoofing-iot.py');
            pyshell.send(jsonPayload);
            pyshell.on('message', function (message) {
                console.log("Kiểm tra message",message)
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
    RED.nodes.registerType("spoofing-iot", SpoofingIOT);
}
