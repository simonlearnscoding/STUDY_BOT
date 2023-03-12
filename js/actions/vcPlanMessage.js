const testID = '1053329872115744808'
// require embedbuilder
const { MessageEmbed, EmbedBuilder} = require('discord.js');
const { ActionRowBuilder, ButtonBuilder, ButtonStyle, Events } = require('discord.js');
function writeMessage(client) {
    const channel = client.channels.cache.get(testID);
    // send embed message to channel
    const components = componentCreator()
    const embed = embedCreator()
    const message = channel.send({
        embeds: [embed],
        components: [components]
    });
}

const activities = [
    'meditate',
    'workout',
    'read',
    'study',
    'journal',
]

const peopleDoingThings = {
    'meditate': [],
    'workout': [],
    'read': [],
    'study': [],
    'journal': [],
}

// when a button is clicked, add the user to the list of people doing that activity

const activityEmojies = {
    'meditate': '🧘',
    'workout': '🏋️',
    'read': '📚',
    'study': '📝',
    'journal': '📒',
}

function componentCreator() {
    const components = new ActionRowBuilder()

    buttonCreator(components)
    // components.addComponents(buttons[0])
    return components


    function buttonCreator(components) {
        for(const activity of activities) {
            const button = new ButtonBuilder()
            .setCustomId(`${activity}`)
            .setLabel(`${activity}`)
                .setStyle(ButtonStyle.Primary)
            .setEmoji(activityEmojies[activity])
            components.addComponents(button)

        }
    }
}

function embedCreator() {
    const fields = fieldCreator()
    const color = '#0099ff'
    const embed = new EmbedBuilder()
        .setColor(color)
        .setDescription('react to the message with what you want to get done today')
        .setTitle('Today I will...')
        .setImage("https://c4.wallpaperflare.com/wallpaper/667/4/23/statue-sculpture-black-background-philosophy-black-background-hd-wallpaper-preview.jpg")
        .addFields(fields)
    // add fields to embed
    // for(const field of fields) {
    //     embed.addFields(field)
    // }
    return embed
}

module.exports = {
    writeMessage
}

function fieldCreator() {
    arr = []

    for(const activity of activities) {
        const obj = {
            name: `${activityEmojies[activity]} - ${activity}`,
            // inline: true,
            value: '.'

        }
        arr.push(obj)
    }
    return arr
}

