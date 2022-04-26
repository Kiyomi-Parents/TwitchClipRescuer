# Overview

Discord bot that monitors specified text channels for posted Twitch clip links and downloads them to an FTP server.</br>


### Install dependencies
    # Install requirements  
	python3 -m pip install -r requirements.txt  

### Fill out config.json
Create a file called config.json and fill it out with your configuration details.
(You can use config_example.json to help you with this.)<br>
    
    "DISCORD_TOKEN" (string) - your Discord bot's token.
    "CLIPS_CHANNEL_IDS" (list of integers) - the Discord channel IDs that the bot should monitor.
    "ALLOW_UNKNOWN_SOURCES" (boolean) - if enabled, the bot will try to pass the message content directly to yt-dlp if no known url pattern is matched.
    "ENABLED_MODES" (list of strings) - enabled download modes, possible options: "FTP", "LOCAL".
    "CREATE_PLATFORM_SUBDIRECTORY" (boolean) - whether the bot should create a subdirectory for each source platform. For example, "Twitch/downloaded_clip.mp4".
    "CREATE_DISCORD_CHANNEL_SUBDIRECTORY" (boolean) - whether the bot should create a subdirectory for the discord channel it was called from.
    "OUTPUT_TEMPLATE" (string) - custom yt-dlp output template. Determines the format of the downloaded filenames.
    "PATH" (string) - the path of the directory where clips will be downloaded (both local and FTP).
    "FTP": {
        "HOST" (string) - the hostname/address of the FTP server,
        "PORT" (integer) - the port that the FTP server is running on,
        "SUBDIRECTORY" (string) - the path of the directory that the bot should use on the FTP server,
        "USERNAME" (string) - username of the account to use on the FTP server,
        "PASSWORD" (string) - password of the account to use on the FTP server
    }

### Start bot  
	python3 main.py

### More about config.json

Further info on the "OUTPUT_TEMPLATE" option: https://github.com/yt-dlp/yt-dlp#output-template

#### File structure example
Settings file (only relevant settings shown):<br>

    ...
    "ALLOW_UNKNOWN_SOURCES": true,
    "CREATE_DISCORD_CHANNEL_SUBDIRECTORY": true,    
    "CREATE_PLATFORM_SUBDIRECTORY": true,
    "OUTPUT_TEMPLATE": "%(creator)s/%(title)s-%(id)s.%(ext)s",
    "PATH": "Clips",
    "FTP": {
        ...
        "SUBDIRECTORY": "Data/ClipDownloader"
        ...
    }

File structure that would be created with these settings after some videos have been submitted:

Local file structure:
```
└── Clips
    ├── clips-channel-1
    │   ├── Twitch
    │   │   ├── CreatorName2
    │   │   │   └── myvideo-1304897.mp4
    │   │   └── creatorname1
    │   │       ├── coolvideo1-12345678910.mp4
    │   │       └── sadvideo-12341234123.mp4
    │   └── Unknown
    │       └── iamalsoacreator
    │           └── weirdvideofromweirdplatform-NA.webm
    └── clips-submission
        └── Twitch
            └── creatorname1
                └── coolvideo1-12345678910.mp4
```
FTP server file structure:
```
└── Data
    └── ClipDownloader
        └── Clips
            ├── clips-channel-1
            │   ├── Twitch
            │   │   ├── CreatorName2
            │   │   │   └── myvideo-1304897.mp4
            │   │   └── creatorname1
            │   │       ├── coolvideo1-12345678910.mp4
            │   │       └── sadvideo-12341234123.mp4
            │   └── Unknown
            │       └── iamalsoacreator
            │           └── weirdvideofromweirdplatform-NA.webm
            └── clips-submission
                └── Twitch
                    └── creatorname1
                        └── coolvideo1-12345678910.mp4
```
