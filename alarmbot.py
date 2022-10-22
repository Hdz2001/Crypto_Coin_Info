import discord 
from discord.ext import commands

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='.',intents=intents)
client = discord.Client(intents=discord.Intents.default())

@client.event
async def on_ready(): 
    print('Hi!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
 
    if message.content.startswith('hi'):
        await message.channel.send('Hello!') 

bot.run('MTAyODgwNDM3OTU4MDU3NTc2NQ.GHxpTZ.Igteuz0PSqvCYfGGCOoRqERupecsb4P79oollo')

# @bot.command(): 
