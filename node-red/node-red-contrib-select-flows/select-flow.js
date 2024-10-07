module.exports = function(RED) {
    function SelectFlow(config) {
        RED.nodes.createNode(this, config);
        var node = this;
        node.on('input', function(msg) {
            if (Array.isArray(msg.payload)) {
                const flowArray = msg.payload;
           
                RED.httpAdmin.get("/select-flow-data", function(req, res) {
                    // Giả sử bạn muốn trả về một mảng các flo
                    res.json(flowArray);
                })

                RED.httpAdmin.post("/select-flow", function(req, res) {
                    var data = req.body;
                    msg.payload= data.flow
                    console.log("Kiểm tra be",data )
                    node.send(msg);
                    node.warn(msg)
                })

                
        
                // Gửi mảng flow về frontend để cập nhật thẻ select
               
            } else {
                node.error("Payload is not an array of flows");
            }
        });
    }
    RED.nodes.registerType("select-flow", SelectFlow);
}
