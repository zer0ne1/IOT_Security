const { PythonShell } = require('python-shell');

module.exports = function(RED) {
    function DetectXSS(config) {
        RED.nodes.createNode(this, config);
        var node = this;
        RED.httpAdmin.post("/detect-xss", function(req, res) {
            var data = req.body;
            console.log("Received data:", data);
            var options = {
                mode: 'text',
                pythonOptions: ['-u'], // unbuffered output
                scriptPath: './node-red-contrib-attack-detect-xss', // Đường dẫn đến script Python của bạn
                args: [data?.url] // Các đối số truyền vào cho script Python
            };
            PythonShell.run('xss.py', options).then(messages=>{
                // results is an array consisting of messages collected during execution
                
                node.send({payload:messages});
              });
            
     
            
        });

      
    }
    RED.nodes.registerType("detect-xss", DetectXSS);
}
