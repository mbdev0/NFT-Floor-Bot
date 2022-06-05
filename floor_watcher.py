import requests
import threading
from discord_webhook import DiscordWebhook, DiscordEmbed

def webhooks(user,collectionName,floorprice,floorP):
        mWebhook = DiscordWebhook(
            url='https://discord.com/api/webhooks/814320851930841109/PzSxpUmTSN46nCvEhHMziNmVc6-pFoNYCVIaSfWhSbPclB-bjDnYNrhVIYR9uNU0NfSF',
            rate_limit_retry=True,
            content = f"<@{user}>",
            allowed_mentions = {'users': [user]}
            )
            
        embed = DiscordEmbed(
            title = "Alert FP Hit",
            description = f"[{collectionName}](https://magiceden.io/marketplace/{collectionName})",
            color = 6710937
            )
        embed.add_embed_field(name='Collection',value=collectionName,inline = True)
        embed.add_embed_field(name='Floor Price To be alerted at',value=str(floorprice),inline = True)
        embed.add_embed_field(name='Current Floor Price',value=str(floorP),inline = True)
        mWebhook.add_embed(embed)
        mWebhook.execute()

def magic_eden(collectionName,floorprice,user='329651231272337418'):
    prev = None
    url = f"https://api-mainnet.magiceden.dev/v2/collections/{collectionName}/stats"
    final = 0
    while True:
        payload={}
        headers = {}

        response = requests.get(url, headers=headers, data=payload)
        floorP = float(response.json()['floorPrice']/1000000000)
        
        if prev == None:
            prev=floorP

        if floorprice == floorP or (floorP>prev and floorprice<floorP) or (prev>floorP and floorP<floorprice):
            webhooks(user,collectionName,floorprice,floorP)
            return None
        prev=floorP

finished = False
while not finished:
    collection = input("Enter Collection: ")
    floor = float(input("Enter floor price to get alert: "))
    threading.Thread(target=magic_eden,args=(collection,floor)).start()
    for i in threading.enumerate():
        print(i.name)