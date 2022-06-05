from math import floor
import requests
import threading

def magic_eden(collectionName,floorprice,user=None):
    s = False
    while not s:
        url = f"https://api-mainnet.magiceden.dev/v2/collections/{collectionName}/stats"

        payload={}
        headers = {}

        response = requests.get(url, headers=headers, data=payload)
        floorP = float(response.json()['floorPrice']/1000000000)

        if floorprice == floorP:
            print('ALERT ALERT ALERT\nCollection: {} has hit FLOORPRICE: {}'.format(response.json()['symbol'],floorP))
            s = True
            return ""

        
finished = False

while not finished:
    collection = input("Enter Collection: ")
    floor = float(input("Enter floor price to get alert: "))
    threading.Thread(target=magic_eden,args=(collection,floor)).start()
    for i in threading.enumerate():
        print(i.name)