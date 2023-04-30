import os, platform
def clear():
    if platform.system().lower()=="windows":
        os.system('cls')
    else:
        os.system('clear')

if platform.system().lower()=="windows":
    ossys = "python.exe -m pip install"
else:
    ossys = "python3 -m pip install"

try:
    import discord
except ImportError:
    os.system(f"{ossys} discord"), clear()
    
import discord
from discord.ext import tasks, commands

if str(os.path.exists("config.py")) == "False":
    print("config.py not detected! \n Creating config.py.")
    token = input("Token: ")
    channelid = input("ChannelID: ")
    server = input("What to Ping: ")
    seconds = input("(How often to ping) Seconds: ")
    offlinename = input("What to name the channel when offline: ")
    onlinename = input("What to name the channel when online: ")
    prefix = input("Prefix: ")
    with open("config.py", "w") as file:
        file.write(f'token = "{token}" \nchannelid = "{channelid}" \nserver = "{server}" \nseconds = "{seconds}" \nprefix = "{prefix}" \nofflinename = "{offlinename}" \nonlinename = "onlinename"')
    file.close
from config import seconds, server, token, channelid, offlinename, onlinename, prefix

intents = discord.Intents.all()
client = commands.Bot(command_prefix=prefix,intents=intents)

dir = os.path.dirname(os.path.realpath(__file__))
wdir = os.getcwd()
if dir != wdir:
    os.chdir(dir)

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name=f"{server} Status: Checking..."))
    try:
        await client.tree.sync()
    except Exception as Error:
        print(Error)
    print(f'[SUCCESS] : Logged in as {client.user}\n')
    await ServerCheckLoop.start()

@tasks.loop(seconds=int(seconds))
async def ServerCheckLoop():
    print("Checking Server Status...")
    mainChannel = client.get_channel(int(channelid))
    param = "-n" if platform.system().lower()=="windows" else "-c"
    check = os.system(f"ping {param} 1 {server}")
    if check == 0:
        print("\n[PASSED] Server is online.\n")
        await mainChannel.edit(name = onlinename)
        status = "Online."
    else:
        print("\n[FAILED] Server is offline!\n")
        await mainChannel.edit(name = offlinename)
        status = "Offline!"
    await client.change_presence(activity=discord.Game(name=f"{server} Status: {status}"))

@client.hybrid_command(pass_context=True)
async def ping(ctx):
	await ctx.send("> `Pong! " + str(round(client.latency * 1000)) + "ms`")

@client.hybrid_command(pass_context=True)
async def status(ctx):
    param = "-n" if platform.system().lower()=="windows" else "-c"
    check = os.system(f"ping {param} 1 {server}")
    if check == 0:
        status = "Online"
    else:
        status = "Offline!" 
    await ctx.send(f"Server Status: {status}")

@ServerCheckLoop.before_loop
async def before_some_task():
  await client.wait_until_ready()

client.run(token)
