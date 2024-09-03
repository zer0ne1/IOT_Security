const { PythonShell } = require('python-shell');

module.exports = function(RED) {
    function DetectXSS(config) {
        RED.nodes.createNode(this, config);
        var node = this;
        RED.httpAdmin.post("/detect-xss",  function(req, res) {
            var data = req.body;
            
            console.log("Received data:", data);
            var jsonPayload = JSON.stringify(data);
            let pyshell = new PythonShell('node_modules/node-red-contrib-attack-detect-xss/xss.py');
            pyshell.send(jsonPayload);
            pyshell.on('message', function (message) {
                console.log("Kiêm rtra ", message)
                node.send({ payload: message });
                node.warn(message)
            });
            pyshell.end(function (err,code,signal) {
            if (err) throw err;
                console.log('The exit code was: ' + code);
                console.log('The exit signal was: ' + signal);
                console.log('finished');
            });



            // var data = req.body;
            // console.log("Received data:", data);
            // var options = {
            //     mode: 'text',
            //     pythonOptions: ['-u'], // unbuffered output
            //     scriptPath: './node-red-contrib-attack-detect-xss', // Đường dẫn đến script Python của bạn
            //     args: [data?.url] // Các đối số truyền vào cho script Python
            // };
            // const mess= await PythonShell.run('xss.py', options)
            // console.log(mess)
            // node.send({payload:mess})
                
                 
        });

      
    }
    RED.nodes.registerType("detect-xss", DetectXSS);
}
