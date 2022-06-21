import requests
import json
import threading
from discord_webhook import DiscordWebhook, DiscordEmbed
LAMPORTS_PER_SOL = 1000000000

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

            floorP = float(response.json()['floorPrice']/LAMPORTS_PER_SOL)
            prev = floorP


            if self.floorprice == floorP or (floorP>prev and self.floorprice<floorP) or (prev>floorP and floorP>self.floorprice):
                mWebhook = DiscordWebhook(
                    url='https://discord.com/api/webhooks/814320851930841109/PzSxpUmTSN46nCvEhHMziNmVc6-pFoNYCVIaSfWhSbPclB-bjDnYNrhVIYR9uNU0NfSF',
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

        def delete_task(self):
            pass
finished = False

while not finished:
    choice = input(
    '''
    1. Floor Watcher
    2. Delete Collection
    Option: ''')
    if choice == '1':

        collection = input("    Enter Collection: ")
        floor = float(input("    Enter floor price to get alert: "))

        url = f"https://api-mainnet.magiceden.dev/v2/collections/{collection}/stats"
        payload={}
        headers = {}

        response = requests.get(url, headers=headers, data=payload)
        json_data = json.loads(response.text)

        if len(json_data) == 1:
            print("Incorrect Collection")
            continue

        sniper = floor_watcher(collection,floor)
        threading.Thread(target=sniper.magic_eden,args=(response,)).start()

        for i in threading.enumerate():
            print(i.name)

        currently_running.append(sniper)

    elif choice == '2':
        print('\n')
        for count,i in enumerate(currently_running):
            print(f'    {count+1}: {i.collectionName} - {i.floorprice}')

        delete_input = int(input('\n\n\nItem: '))

        delete_task= currently_running[delete_input-1]
        delete_task.terminate_task()
        print(f'\nSuccessfully deleted {delete_task.collectionName}')
        
        currently_running.pop(delete_input-1)

        
    else:
        print("\nInput 1 or 2")