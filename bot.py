import nextcord
from nextcord import Interaction
from nextcord.ext import commands
import os

from apikeys import *

intents = nextcord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix= '$', intents=intents)

serverId = 481883505727635456

@client.event
async def on_ready():
    print('''
    BOT IS WORKING
    ===================================
    ''')
    
@client.slash_command(name="command",description='A test Description',guild_ids=[serverId])
async def test(interaction:Interaction):
    await interaction.response.send_message("Testing")


client.run(BOTTOKEN)