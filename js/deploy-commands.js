// ONLY RUN THIS FILE AFTER YOU DEPLOYED A NEW COMMAND

const { REST, Routes } = require("discord.js");
const { clientId, guildId, TOKEN } = require("./config.json");
const fs = require("node:fs");

// GRAB ALL THE COMMAND FILES FROM THE COMMANDS DIRECTORY YOU CREATED EARLIER
const commands = [];
const commandFiles = fs
    .readdirSync("./commands")
    .filter((file) => file.endsWith(".js"));

// GRAB THE SLASHCOMMANDBUILDER#TOJSON() OUTPUT OF EACH COMMAND'S DATA FOR DEPLOYMENT
for (const file of commandFiles) {
    const command = require(`./commands/${file}`);
    commands.push(command.data.toJSON());
}

// CONSTRUCT AND PREPARE AN INSTANCE OF THE rest MODULE
const rest = new REST({ version: "10" }).setToken(TOKEN);

// And deploy your commands!
(async () => {
    try {
        console.log(
            `Started refreshing ${commands.length} application (/) commands.`
        );

        // The put method is used to fully refresh all commands in the guild with the current set
        const data = await rest.put(
            Routes.applicationCommands(clientId), // global commands
            // Routes.applicationGuildCommands(clientId, guildId), // guild commands
            { body: commands }
        );

        console.log(
            `Successfully reloaded ${data.length} application (/) commands.`
        );
    } catch (error) {
        // And of course, make sure you catch and log any errors!
        console.error(error);
    }
})();
