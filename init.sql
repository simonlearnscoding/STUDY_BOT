-- init.sql
CREATE DATABASE IF NOT EXISTS discordjs;
GRANT ALL PRIVILEGES ON discordjs.* TO 'simon'@'%' IDENTIFIED BY '3112';
FLUSH PRIVILEGES;
