const { PythonShell } = require('python-shell');

module.exports = function(RED) {
    function AttackDictionary(config) {
        RED.nodes.createNode(this, config);
        var node = this;
        RED.httpAdmin.post("/attack-dic", function(req, res) {
            var data = req.body;
            console.log("Received data:", data);
            var jsonPayload = JSON.stringify(data);
            let pyshell = new PythonShell('node_modules/node-red-contrib-attack-dictionary/attack-dictionary.py');
            pyshell.send(jsonPayload);
            pyshell.on('message', function (message) {
                
                node.send({ payload: message });
                node.warn(message)
            });
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
