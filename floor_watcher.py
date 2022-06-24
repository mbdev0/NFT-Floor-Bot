from discord_webhook import DiscordWebhook, DiscordEmbed
import requests
import json
LAMPORTS_PER_SOL = 1000000000
ALERT_WEBHOOK = 'https://discord.com/api/webhooks/814320851930841109/PzSxpUmTSN46nCvEhHMziNmVc6-pFoNYCVIaSfWhSbPclB-bjDnYNrhVIYR9uNU0NfSF'
WEBHOOK_IMAGE='https://scx2.b-cdn.net/gfx/news/2017/2-nasaastronau.jpg'

currently_running = []


class floor_watcher():

    def __init__(self,collectionname,floorprice) -> None:
        self.running = True
        self.valid = True
        self.collectionName = collectionname
        self.floorprice = floorprice

    def terminate_task(self):
        self.running = False

    def magic_eden(self,response,user='329651231272337418'):
        prev = 0
        while self.running:

            url = f"https://api-mainnet.magiceden.dev/v2/collections/{self.collectionName}/stats"
            payload={}
            headers={}
            response = requests.get(url, headers=headers, data=payload)

            floorP = float(response.json()['floorPrice']/LAMPORTS_PER_SOL)
            print(floorP)
            prev = floorP


            if self.floorprice == floorP or (floorP>prev and self.floorprice<floorP) or (prev>floorP and floorP>self.floorprice):
                mWebhook = DiscordWebhook(
                    url=ALERT_WEBHOOK,
                    rate_limit_retry=True,
                    content = f"<@{user}>",
                    allowed_mentions = {'users': [user]}
                    )
                    
                embed = DiscordEmbed(
                    title = "Alert FP Hit",
                    description = f"[{self.collectionName}](https://magiceden.io/marketplace/{self.collectionName})",
                    color = 6710937
                    )
                embed.add_embed_field(name='Collection',value=self.collectionName,inline = True)
                embed.add_embed_field(name='Floor Price To be alerted at',value=str(self.floorprice),inline = True)
                embed.add_embed_field(name='Current Floor Price',value=str(floorP),inline = True)
                mWebhook.add_embed(embed)
                mWebhook.execute()
                print("True")
                s = True
                return ""