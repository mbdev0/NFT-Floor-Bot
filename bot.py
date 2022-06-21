import nextcord
from nextcord import Interaction
from nextcord.ext import commands
import os
from floor_watcher import *
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
    
@client.slash_command(name="floor-alert",description='Alerts you when a collection hits a certain FP',guild_ids=[serverId])
async def test(interaction:Interaction,collection_name:str,floor_price:float):


    print(type(interaction.user.mention))
    url = f"https://api-mainnet.magiceden.dev/v2/collections/{collection_name}/stats"
    payload={}
    headers = {}

    response = requests.get(url, headers=headers, data=payload)
    json_data = json.loads(response.text)

    if len(json_data) == 1:
        await interaction.response.send_message(f"Collection: {collection_name} is invalid/does not exist")
    else:  
        sniper = floor_watcher(collection_name,floor_price)
        threading.Thread(target=sniper.magic_eden,args=(response,),daemon=True).start()

        for i in threading.enumerate():
            print(i.name)

        currently_running.append(sniper)
        await interaction.response.send_message(f"You've added {collection_name}: {floor_price} to the alert list")

@client.slash_command(name='list-all-alerts',description='Shows you the entire list of alerts created by you',guild_ids=[serverId])
async def list_all(interaction:Interaction):
    string = ""
    for count,i in enumerate(currently_running):
        string+= f"{count+1}: {i.collectionName} - {i.floorprice}\n"

    await interaction.response.send_message(string)

@client.slash_command(name='delete_task',description='Deletes collection specified',guild_ids=[serverId])
async def delete_task(interaction:Interaction,collection_id:int):
    delete_task = currently_running[collection_id-1]
    delete_task.terminate_task()
    currently_running.pop(collection_id-1)

    await interaction.response.send_message(f'Successfully deleted {delete_task.collectionName}')

client.run(BOTTOKEN)