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
            node.send({ payload: "9999999999999" }); 
            PythonShell.run('xss.py', options)
                .then(messages => {
                    console.log("Result from Python script:", messages);
                    node.send({ payload: messages });  // Gửi kết quả thực tế từ Python script
                })
                .catch(err => {
                    console.error("Error running Python script:", err);
                    node.error(err);
                });
            // PythonShell.run('xss.py', options, function (err, messages) {
            //     if (err) {
            //         console.error(err);
            //         node.error(err);
            //     } else {
            //         console.log("alooooooo", messages);
            //         node.send({payload: messages});
            //         console.log("alooooooo123", messages);
            //     }
            // });
     
            
        });

      
    }
    RED.nodes.registerType("detect-xss", DetectXSS);
}
