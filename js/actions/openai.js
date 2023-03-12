const { Configuration, OpenAIApi } = require("openai");
const { OPENAI_API_KEY } = require("../config");
const configuration = new Configuration({
    organization: "org-3nSfb95y9IB3QAqKTWSRrCw5",
    apiKey: OPENAI_API_KEY,
});



const openai = new OpenAIApi(configuration);


async function askQuestion(prompt) {
    // const response = await openai.listEngines();
    // send a request to the API

    const response = await openai.createCompletion({
        prompt: `${prompt}`,
        temperature: 0.5,
        n: 1,
        stream: false,
        max_tokens: 400,
        model: 'text-davinci-003',
        // make it answer the question
        // stop: ["\n", "AI:"],
    });

    return response.data.choices[0].text;
}

let pirate = ' Talk like a pirate'
let bratty = 'Talk in a bratty way'
let peterson = ' Talk like Jordan Peterson'
let trump = ' Talk like Donald Trump'
let prompt = " and answer to the question: "
let question = "Greater axons are recruited at low values of current, axons with smaller diameter are recruited only" +
    " at relatively greater current values but Contraction force is increased by recruiting the smallest motor neurons first. " +
    "This is because the smallest motor neurons have the greatest number of axons per motor unit. " +
let question1 = prompt + question








askQuestion(question1).then((res) => { console.log(res) })
