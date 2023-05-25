import { TOKEN } from 'config.json';
// const TOKEN = "MTA1MDQ3Njg1MTcxOTU4OTk0OA.GWEG5N.t2nNYP_Lv79SxEoOu7P9p8VmxzmmjPfLWmo5-A"


// const CLIENT_ID = 1050476851719589948
import { Client, Events, GatewayIntentBits } from 'discord.js';

// const rest = new REST({ version: '10' }).setToken(TOKEN);


const client = new Client({ intents: [GatewayIntentBits.Guilds] });

client.once(Events.ClientReady, c => {
  console.log(`Ready! logged in as ${c.user.tag}`)
})

client.login(TOKEN)
