import nextcord
from nextcord import Interaction
from nextcord.ext import commands
import threading
from floor_watcher import *
from apikeys import *
import json

intents = nextcord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix= '$', intents=intents)

serverId = '' #Place your server ID here

def webhook(title:str, description:str=None):
    embed = nextcord.Embed(title=title,description=description,colour=3093117)
    embed.set_thumbnail(url=WEBHOOK_IMAGE)
    embed.set_footer(text='Floor Watcher - by mbdev0')
    return embed

@client.event
async def on_ready():
    print('''
    BOT IS WORKING
    ===================================
    ''')
    
@client.slash_command(name="alert",description='Alerts you when a collection hits a certain FP',guild_ids=[serverId])
async def add_task(interaction:Interaction,collection_name:str,floor_price:float):

    url = f"https://api-mainnet.magiceden.dev/v2/collections/{collection_name}/stats"
    payload={}
    headersForApi = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
    }
    headers={}
    response = requests.get(url, headers=headers, data=payload)
    json_data = json.loads(response.text)

    if len(json_data) == 1:
        await interaction.response.send_message(f"Collection: **{collection_name}** is invalid/does not exist")
    else:  
        sniper = floor_watcher(collection_name,floor_price)
        threading.Thread(target=sniper.magic_eden,args=(interaction.user.mention,),daemon=True).start()

        currently_running.append(sniper)
        await interaction.response.defer()
        get_aggregate = requests.get(f'https://cors.ryanking13.workers.dev/?u=https://api-mainnet.magiceden.io/rpc/getAggregatedCollectionMetricsBySymbol?symbols={collection_name}',headers=headersForApi)
        aggregate = json.loads(get_aggregate.text)
        collection_image = aggregate['results'][0]['image']


        added_webhook=webhook(title="Added Collection",description=f'Successfully added collection **{collection_name}** with FP: **{floor_price}**')
        added_webhook.set_thumbnail(url=collection_image)

        await interaction.followup.send(embed=added_webhook)

@client.slash_command(name='list-all-alerts',description='Shows you the entire list of alerts created by you',guild_ids=[serverId])
async def list_all(interaction:Interaction):
    if not currently_running:
        error_embed=webhook(title="List Alerts",description="There are no currently running tasks")
        await interaction.response.send_message(embed=error_embed)


    list_embed = webhook(title='List Alerts',description='All Alerts')

    for count,i in enumerate(currently_running):
        list_embed.add_field(name=f'**{count+1}**: {i.collectionName}', value=f'Floor Price: {i.floorprice}',inline=False)

    await interaction.response.send_message(embed=list_embed)

@client.slash_command(name='delete_task',description='Deletes collection specified',guild_ids=[serverId])
async def delete_task(interaction:Interaction,collection_id:int):
    delete_task = currently_running[collection_id-1]
    delete_task.terminate_task()
    currently_running.pop(collection_id-1)

    delete_task_embed = webhook(title='Delete Task',description=f'Successfully deleted: \n**{delete_task.collectionName} FP: {delete_task.floorprice}**')

    await interaction.response.send_message(embed=delete_task_embed)


client.run(BOTTOKEN)