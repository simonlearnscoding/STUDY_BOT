import {ClientToExport} from "./clientConnector.js";
const client = ClientToExport;
import { EmbedBuilder } from 'discord.js';


// inside a command, event listener, etc.
const embed = new EmbedBuilder()
//create and embed object
    .setColor('#0099ff')

    // .setTitle('Some title')
    // .setURL('https://discord.js.org/')
    // .setAuthor
    // ('Some name', 'https://i.imgur.com/wSTFkRM.png', 'https://discord.js.org')
    // .setDescription('Some description here')
    // .setThumbnail('https://i.imgur.com/wSTFkRM.png')
    // .addFields(
    //     { name: 'Regular field title', value: 'Some value here' },
    //     { name: '\u200B', value: '\u200B' },
    //     { name: 'Inline field title', value: 'Some value here', inline: true },
    //     { name: 'Inline field title', value: 'Some value here', inline: true },
    // )

export async function testMessage(CHANNEL_ID) {
    const channel = client.channels.cache.get(CHANNEL_ID);
// send embed message to channel
    await channel.send('Hello world!');
//     channel.send({embeds: [embed]});
}

//get text channel by id


// discord get textchannel by id
// https://stackoverflow.com/questions/59202075/how-to-get-a-text-channel-by-id-in-discord-js
