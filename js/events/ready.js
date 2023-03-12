const { Events } = require('discord.js');
const {createJSONFile} = require("../serverConfig/createServerConfigFile");

planner = require('./../actions/vcPlanMessage.js');
serverconfig = require('../serverConfig/createServerConfigFile.js');
module.exports = {
    name: Events.ClientReady,
    once: true,
    async execute(client) {
        console.log(`Ready! Logged in as ${client.user.tag}`);
        serverconfig.createServerConfigs(client);
        // console.log(planner)
        planner.writeMessage(client)
    },
};
