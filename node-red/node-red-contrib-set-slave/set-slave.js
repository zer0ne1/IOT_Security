module.exports = function(RED) {
    function SetSlave(config) {
        RED.nodes.createNode(this, config);
        var node = this;
        node.on('input', function(msg) {
            if (Array.isArray(msg.payload)) {
                const flowArray = msg.payload;
                RED.httpAdmin.get("/select-flow-set-slave", function(req, res) {
                    // Giả sử bạn muốn trả về một mảng các flo
                    res.json(flowArray);
                })

                RED.httpAdmin.post("/set-slave", function(req, res) {
                    var data = req.body;
                    msg.payload= data.flow
                    console.log("Kiểm tra be",data )
                    node.send(msg);
                })

                
        
                // Gửi mảng flow về frontend để cập nhật thẻ select
               
            } else {
                node.error("Payload is not an array of flows");
            }
        });
    }
    RED.nodes.registerType("set-slave", SetSlave);
}
