# TeruhashiBot
A Discord bot for League, Anime, Manga, and more!

## Inviting Teruhashi Bot to your Discord Server
* Visit the link https://discordapp.com/oauth2/authorize?&client_id=459135751632846868&scope=bot&permissions=0, and follow the instructions on the webpage.

## Running and modifying a local Teruhashi Bot
* Three files are required for Teruhashi Bot to run properly:
    * `secrets.py`: Contains API keys and other authorization tokens.
    * `blacklist.txt`: Contains Discord channelId's seperated by newlines.
    * `debug.log`: Contains all commands and replies handled by Teruhashi Bot.
* To start Teruhashi Bot, ensure all API keys in `secrets.py` are valid, then run `login.py`.
* To stop Teruhashi Bot, force quit the program and allow the event loop to finish. 
    * If you do not wait for the event loop to finish, Teruhashi Bot may remain logged in! To fix this, start and stop Teruhashi Bot again.
