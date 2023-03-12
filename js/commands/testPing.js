// THIS FILE IS A TEST, IT IS ONLY MEANT TO SHOW HOW SLASH COMMANDS CAN BE BUILT

const { SlashCommandBuilder } = require('discord.js')
const wait = require('node:timers/promises').setTimeout;

const { Client, Events, GatewayIntentBits, Collection } = require('discord.js');
module.exports = {
    data: new SlashCommandBuilder()
        .setName('ping')
        .setDescription('Replies with Pong!'),
    async execute(interaction) {
        await interaction.reply({ content: 'Pong!', ephemeral: true });
        //wait a second then edit the reply to say pong again
        await wait(1000);
        await interaction.editReply({ content: 'Pong again!' });
    },
};
;
