# Overview

Discord bot that monitors specified text channels for posted Twitch clip links and downloads them to an FTP server.</br>


### Install dependencies
    # Install requirements  
	python3 -m pip install -r requirements.txt  

### Fill out config.json
Create a file called config.json and fill it out with your configuration details.
(You can use config_example.json to help you with this.)<br>
    
    "DISCORD_TOKEN" - your Discord bot's token, as a string
    "CLIPS_CHANNEL_IDS" - the Discord channel IDs that the bot should monitor, as a list of integers
    "FTP_HOST" - the hostname/address of your FTP server, as a string
    "FTP_PORT" - the port that the FTP server is running on, as an integer
    "FTP_DIRECTORY" - the path of the directory that the bot should use on the FTP server, as a string
                      (leave blank to use the root directory)
    "FTP_USERNAME" - username of the account to use on the FTP server, as a string
    "FTP_PASSWORD" - password of the account to use on the FTP server, as a string
  
### Start bot  
	python3 main.py
