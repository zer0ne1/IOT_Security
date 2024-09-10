var DataTypes = require("sequelize").DataTypes;
var _permissions = require("./permissions");
var _users = require("./users");

function initModels(sequelize) {
  var permissions = _permissions(sequelize, DataTypes);
  var users = _users(sequelize, DataTypes);

  users.belongsTo(permissions, { as: "permission", foreignKey: "permission_id"});
  permissions.hasMany(users, { as: "users", foreignKey: "permission_id"});

  return {
    permissions,
    users,
  };
}
module.exports = initModels;
module.exports.initModels = initModels;
module.exports.default = initModels;
