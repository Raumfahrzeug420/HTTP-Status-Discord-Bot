# HTTP-Status-Discord-Bot
This bot changes a channel's name based on the parameters given. It has two commands ping & status. Ping, pings the discord bot and sends the delay in ms. Status pings the HTTP server in config.py and checks if it's online or offline. This does not work on websites that use cloudflare as cloudflare responds back when the server is down.

# Hosting the Bot
Requires Python 3.9.0 or greater. Not sure if it works with previous versions!

Clone this repository. CMD: ```git clone https://github.com/Raumfahrzeug420/HTTP-Status-Discord-Bot```

Create a Discord Bot: https://discord.com/developers/applications

Install the required dependencies: CMD: ```python3 -m pip install discord```

Start the bot from the project folder: ```main.py```
