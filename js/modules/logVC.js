import fs from 'fs';

// import prisma client
import { PrismaClient } from '@prisma/client';

// create a new prisma client
const prisma = new PrismaClient();


const user_logs = './../file_Logs/user_logs.json'
const user_today = './../file_logs/user_time_today.json'
// get json as js object

//edit a json file
function readJSONFile(path) {
    fs.readFile(path    , (err, data) => {
        if (err) {
            throw err;
        }
        return JSON.parse(data);
    });
}
function writeintoJSONFile(path, data) {
    // prisma create a new line in the logsNow table
    prisma.logsNow.create({
        data: {
            user : data.user_id,
            // TODO: activity
            // TODO: type
            
            timestamp: data.time,

}

const getUserFromJSON = (user_id, json) => {
    let user = readJSONFile(json);
    if(user[user_id] == undefined){
        return null;
    }
    return user[user_id];
}

function compareTime(time1, time2){
    return time1.getTime() - time2.getTime();
}

//get time difference in minutes
function getTimeDifference(time1, time2){
    return Math.abs(compareTime(time1, time2)/60000);
}

//
function deleteUserFromJSON(user_id, json){
    let user = readJSONFile(json);
    delete user[user_id];
    writeintoJSONFile(json, user);
}


export function userEnteredVC(client) {
    function getMinutesInVC(newState) {
        const time = getUserFromJSON(newState.id, user_logs).time;
        const timeDifference = getTimeDifference(time, new Date());
        // delete the user from the database
        return timeDifference;
    }

    function userIsInTodayLog(id) {
        return getUserFromJSON(id, user_today) == null;
    }

    client.on('voiceStateUpdate', (oldState, newState) => {

        if (joinedChannel()) {
            // create a new entry in the database
            const log = returnUserjoinedObject(newState);
            writeintoJSONFile(user_logs, log);
        }

        function userTimeLogExists() {
            return getUserFromJSON(newState.id) != null;
        }

        if (leftChannel()) {

            if(userTimeLogExists()){


                //get time from user
                const timeDifference = getMinutesInVC(newState);
                //update time in user_today
                // if there is not a user entry in user_today yet, create one with the time difference, id and name

                if(userIsInTodayLog(newState.id)){
                    const user = returnUserObject(newState, timeDifference);
                    writeintoJSONFile(user_today, user);
                }
                //if there is a user entry in user_time_day.json then update the time
                else{
                    const user = getUserFromJSON(newState.id, user_today);
                    user.time += timeDifference;
                    writeintoJSONFile(user_today, user);
                    }
                }
            deleteUserFromJSON(newState.id, user_logs);

        }
        if (switchedChannel()) {

        }


        function joinedChannel() {
            return oldState.channelID === null && newState.channelID !== null;
        }
        function switchedChannel() {
            return oldState.channelID !== null && newState.channelID !== null;
        }
        // if the client just left a channel
        function leftChannel() {
            return oldState.channelID !== null && newState.channelID === null;
        }


        function returnUserObject(member) {
            const userID = member.id;
            const userName = member.user.username;
        }

        function createUserToday(member, channel, time) {
            const user = returnUserObject(member);
            user.channel = channel;
            user.time = time;
            return user;
        }

        function returnUserjoinedObject() {
            const {userID, name}  = returnUserObject(newState.member);
            const time = new Date();
            const channel = newState.channel.name;
            const guild = newState.guild.name;
            //return an object with name of user, time, channel, and guild
            return ({name, time, channel, guild, userID});
        }


        function leftObject() {
            const userID = oldState.member.id;
            const name = oldState.member.user.username;
            const time = new Date();
            const channel = oldState.channel.name;
            const guild = oldState.guild.name;
            //return an object with name of user, time, channel, and guild
            return ({name, time, channel, guild, userID});
        }
    });}
