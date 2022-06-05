import requests
import threading
from discord_webhook import DiscordWebhook, DiscordEmbed

def magic_eden(collectionName,floorprice,user='329651231272337418'):
    prev = 0
    s = False
    while not s:
        url = f"https://api-mainnet.magiceden.dev/v2/collections/{collectionName}/stats"

        payload={}
        headers = {}

        response = requests.get(url, headers=headers, data=payload)
        floorP = float(response.json()['floorPrice']/1000000000)
        prev = floorP

        if floorprice == floorP or (floorP>prev and floorprice<floorP) or (prev>floorP and floorP>floorprice):
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
            print("True")
            s = True
            return ""

        
finished = False

while not finished:
    collection = input("Enter Collection: ")
    floor = float(input("Enter floor price to get alert: "))
    threading.Thread(target=magic_eden,args=(collection,floor)).start()
    for i in threading.enumerate():
        print(i.name)