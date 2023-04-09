import os
import discord
import platform
from discord.ext import tasks, commands
from config import seconds, server, token, channelid, offlinename, onlinename
intents = discord.Intents.all()
client = commands.Bot(command_prefix=";",intents=intents)

@client.event
async def on_ready():
    status = "Checking..."
    await client.change_presence(activity=discord.Game(name=f"{server} Status: {status}"))
    try:
        await client.tree.sync()
    except Exception as Error:
        print(Error)
    print('[SUCCESS] : Logged in as ' + format(client.user))
    await ServerCheckLoop.start()

# RobloxGameClient
@tasks.loop(seconds=int(seconds))
async def ServerCheckLoop():
    print("Checking Server Status...")
    mainChannel = client.get_channel(int(channelid))
    param = "-n" if platform.system().lower()=="windows" else "-c"
    check = os.system(f"ping {param} 1 {server}")
    if check == 0:
        print("[PASSED] Server is online.")
        await mainChannel.edit(name = onlinename)
        status = "Online."
    else:
        print("[FAILED] Server is offline!")
        await mainChannel.edit(name = offlinename)
        status = "Offline!"
    await client.change_presence(activity=discord.Game(name=f"{server} Status: {status}"))

@client.command(pass_context=True)
async def ping(ctx):
	await ctx.send("> `Pong! " + str(round(client.latency * 1000)) + "ms`")

@client.command(pass_context=True)
async def status(ctx):
    param = "-n" if platform.system().lower()=="windows" else "-c"
    check = os.system(f"ping {param} 1 {server}")
    if check == "0":
        status = "Online"
    else:
        status = "Offline!" 
    await ctx.send(f"Server Status: {status}")

@client.tree.command(name="ping")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("> `Pong! " + str(round(client.latency * 1000)) + "ms`")

@client.tree.command(name="status")
async def ping(interaction: discord.Interaction):
    param = "-n" if platform.system().lower()=="windows" else "-c"
    check = os.system(f"ping {param} 1 {server}")
    if check == "0":
        status = "Online"
    else:
        status = "Offline!" 
    await interaction.response.send_message(f"Server Status: {status}")

@ServerCheckLoop.before_loop
async def before_some_task():
  await client.wait_until_ready()

client.run(token)
