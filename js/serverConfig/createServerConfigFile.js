// get fs as async
const fs = require('fs').promises;


async function createServerConfigs(client) {
 client.guilds.cache.forEach((guild) => {
    if(!checkIfJSONExists(guild)){
        createJSONFile(guild);
    }
    else{
        checkIfAllFilesAreInConfig(guild);
    }
});
}
// function that checks if a json with the name exists
function checkIfJSONExists(guild) {
    // get fs
    const fs = require('fs');
    const path = `./serverConfig/${guild.id}.json`;
    // check if the file exists
    if (fs.existsSync(path)) {
        return true;
    }
}
// create a function that creates a json file
// with name = input of the function

async function getFeaturesFromJSON() {
    const path = `./serverConfig/features.json`;
    const data = await fs.readFile
    (path,
        'utf8',
        (err, jsonString) => {
            if (err) {
                console.log("File read failed:", err)
                return
            }
            return jsonString;
        }
    );
    const obj = JSON.parse(data);
    const features = obj['features'];
    return features;
}
async function getAllFiles() {
    // path to actions folder
    const path = `./actions`;
    const files = [];
    // console log the files
    // get fs as async function

    const feats = await fs.readdir (path, (err, files) => {
        if(err) {
            console.log(err);
        }
    });
    return feats;
}
async function createNewConfig(guild) {
    // create an object with one attribute for every file in the folder actions
    // the attribute is the name of the file and the value is a false boolean

    // get the files in the actions folder as array
    const data = {}
    data['feats']= await getFeaturesFromJSON();
    function createToggleAttributes(files) {
        const data = {};
        files.forEach((file) => {
            data[file] = false;
        });
        return data;
    }
// create an object with the name of the file as attribute and false as value
    const info = {}
    // add the server id and name to the object
    info['server_id'] = guild.id;
    info['server_name'] = guild.name;
    // add the info object to the data object
    data['info'] = info;
    return data;
}

async function getJSONFile(guild) {
    const path = `./serverConfig/${guild.id}.json`;
const data = await fs
.readFile(path
    , 'utf8', (err, jsonString) => {
        if (err) {
            console.log("File read failed:", err)
            return
        }
        return jsonString;
    }
);
return JSON.parse(data);
}

async function checkIfAllFilesAreInConfig(guild) {
    // get the files in the actions folder
    const files = await getFeaturesFromJSON();
    // get the config file
    let config = await getJSONFile(guild);
    let feats = config['feats'];

    // check if the config file has all the files in the actions folder
    // for every file in the actions folder
    Object.entries(files).forEach((file) => {
        // if hasFeature
        if(!hasFeature(feats, file[0])){
            let name = file[0];
            feats[name] = file[1];

        }
    });

    function hasFeature(config, file) {
        return config[file] != undefined;
    }
    // write the config file
    await replaceJSONFile(guild, config);
}

async function replaceJSONFile(guild, data) {
    // path to the file
    const path = `./serverConfig/${guild.id}.json`;
    // write the file
    const jsonData = JSON.stringify(data, null, 2);
    await fswriteFile(path, jsonData);
}

async function createJSONFile(guild) {
    console.log('creating json file');
    const data = await createNewConfig(guild);
    // data to json with line breaks
    const jsonData = JSON.stringify(data, null, 2);
    // const jsonData = JSON.stringify(data);
    // path to the file
    const path = `./serverConfig/${guild.id}.json`;
    // write the file
    await fs.writeFile
    (path,
        jsonData,
        (err) => {
            if (err) {
                throw err;
            }
            console.log("JSON data is saved.");
        }
    );

}

async function writeAsGuildID(guild, data) {
    const path = `./serverConfig/${guild.id}.json`;
    await fswriteFile(path, data)
};


async function fswriteFile(path, data) {
    await fs.writeFile
    (path,
        data,
        (err) => {
            if (err) {
                throw err;
            }
            console.log("JSON data is saved.");
        }
    );
}

// export all functions
module.exports = {
    createServerConfigs: createServerConfigs,
    createJSONFile: createJSONFile

}