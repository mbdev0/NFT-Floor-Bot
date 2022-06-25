from discord_webhook import DiscordWebhook, DiscordEmbed
import requests
import json
LAMPORTS_PER_SOL = 1000000000
ALERT_WEBHOOK = '' #Place DiscordWebhook here
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

    def magic_eden(self,user):
        prev = 0
        while self.running:

            url = f"https://api-mainnet.magiceden.dev/v2/collections/{self.collectionName}/stats"
            payload={}
            headers={}
            response = requests.get(url, headers=headers, data=payload)

            floorP = float(response.json()['floorPrice']/LAMPORTS_PER_SOL)
            prev = floorP


            if self.floorprice == floorP or (floorP>prev and self.floorprice<floorP) or (prev>floorP and floorP>self.floorprice):
                mWebhook = DiscordWebhook(
                    url=ALERT_WEBHOOK,
                    rate_limit_retry=True,
                    content = user
                    )
                    
                embed = DiscordEmbed(
                    title = "Alert FP Hit",
                    description = f"[{self.collectionName}](https://magiceden.io/marketplace/{self.collectionName})",
                    color = 6710937

                    )
                embed.set_author(icon_url=WEBHOOK_IMAGE)
                embed.add_embed_field(name='Collection',value=self.collectionName,inline = True)
                embed.add_embed_field(name='Floor Price To be alerted at',value=str(self.floorprice),inline = True)
                embed.add_embed_field(name='Current Floor Price',value=str(floorP),inline = True)
                embed.set_footer(text='Floor Watcher - by mbdev0')
                mWebhook.add_embed(embed)
                mWebhook.execute()

                currently_running.remove(self)
                return None