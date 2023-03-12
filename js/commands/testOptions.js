const { SlashCommandBuilder } = require('discord.js');

module.exports = {
    data: new SlashCommandBuilder()
        .setName('test')
        .setDescription('test command')
        .addStringOption(option => option.setName('test').setDescription('test option').setRequired(true))
    .addMentionableOption(option => option.setName('test2').setDescription('test option 2').setRequired(true)),

    async execute(interaction) {
        await interaction.reply({content: 'test', ephemeral : true});
    }

}
