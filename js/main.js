// Require the necessary discord.js classes
const fs = require('node:fs');
const path = require('node:path');
const { Client, Events, GatewayIntentBits, Collection} = require('discord.js');
const { TOKEN } = require('./config.json');
console.log({TOKEN});
// Create a new client instance
const client = new Client({ intents: [GatewayIntentBits.Guilds] });
client.commands = new Collection();

const commandsPath = path.join(__dirname, 'commands');
const commandFiles = fs.readdirSync(commandsPath).filter(file => file.endsWith('.js'));

for (const file of commandFiles) {
    const filePath = path.join(commandsPath, file);
    const command = require(filePath);
    // Set a new item in the Collection with the key as the command name and the value as the exported module
    if ('data' in command && 'execute' in command) {
        client.commands.set(command.data.name, command);
    } else {
        console.log(`[WARNING] The command at ${filePath} is missing a required "data" or "execute" property.`);
    }
}
const eventsPath = path.join(__dirname, 'events');
const eventFiles = fs.readdirSync(eventsPath).filter(file => file.endsWith('.js'));

for (const file of eventFiles) {
    const filePath = path.join(eventsPath, file);
    const event = require(filePath);
    if (event.once) {
        client.once(event.name, (...args) => event.execute(...args));
    } else {
        client.on(event.name, (...args) => event.execute(...args));
    }
}
// client.on(Events.InteractionCreate, async interaction => {
//     if (!interaction.isChatInputCommand()) return;
//     console.log(interaction);
//     const command = interaction.client.commands.get(interaction.commandName);
//
//     if (!command) {
//         console.error(`No command matching ${interaction.commandName} was found.`);
//         return;
//     }
//
//
//     try {
//         await command.execute(interaction);
//     } catch (error) {
//         console.error(error);
//         await interaction.reply({ content: 'There was an error while executing this command!', ephemeral: true });
//     }
//
// });

// When the client is ready, run this code (only once)
// We use 'c' for the event parameter to keep it separate from the already defined 'client'
// client.once(Events.ClientReady, c => {
//     console.log(`Ready! Logged in as ${c.user.tag}`);
// });

// Log in to Discord with your client's token
client.login(TOKEN);



















// import { clientExporter } from "./modules/clientConnector.js";
// // import { userEnteredVC } from "./modules/logVC.js";
// // import { testMessage } from "./modules/joinpeople.js";
// import fs from 'fs';
// import path from 'path';
// import {fileURLToPath} from 'url';
// import token from './config.json' assert {type: 'json'};
// import { Client, Collection, Events, GatewayIntentBits } from 'discord.js';
// import { createRequire } from 'node:module';
// //rewrite all import statements to require statements for cjs
// const require = createRequire(import.meta.url);
// const __dirname = path.dirname(fileURLToPath(import.meta.url));
// const client = new Client({ intents: [GatewayIntentBits.Guilds] });
// const commandFiles = fs.readdirSync(path.join(__dirname, 'commands')).filter(file => file.endsWith('.cjs'));
// client.commands = new Collection();
// for (const file of commandFiles) {
//     const command = require(`./commands/
// ${file}`);
//     client.commands.set(command.data.name, command);
//
// }
//
// const TOKEN = token.TOKEN.toString()
// console.log(TOKEN)
// // const CLIENT_ID = 1050476851719589948
// // const require = createRequire(import.meta.url);
//
//
// // const rest = new REST({ version: '10' }).setToken(TOKEN
// // );
// // const client = new Client({ intents: [GatewayIntentBits.Guilds] });
//
//
//
//
//
// // const __filename = fileURLToPath(import.meta.url);
// // const __dirname = path.dirname(__filename);
// //
// // client.commands = new Collection();
// // const commandsPath = path.join(__dirname, 'commands');
// // const commandFiles = fs.readdirSync(commandsPath).filter(file =>file.endsWith('.js'));
// //
// // for (const file of commandFiles) {
// //     const filePath = path.join(commandsPath, file);
// //     import (filePath).then((command) => {
// //         client.commands.set(command.data.name, command);
// //     }
// //     );
// //
// //     // const command = require(filePath);
// //     // if ('data' in command && 'execute' in command) {
// //     //     client.commands.set(command.data.name, command);
// //     // }
// //     // else {
// //     //     console.log(`Command ${file} does not have data or execute`);
// //     // }
// // }
//
//
// client.once(Events.ClientReady, c => {
//     console.log(`Ready! logged in as ${c.user.tag}`)
// })
//
// client.login(TOKEN)
