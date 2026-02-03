import epicstore_api
import os
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()

store = epicstore_api.EpicGamesStoreAPI()

games = store.get_free_games()["data"]["Catalog"]["searchStore"]["elements"]

free_games = []

print("Finding free games on Epic Games Store.")

for game in games:
    if game["price"]["totalPrice"]["discountPrice"] == 0:
        with open(file="games_notified.txt", mode="r") as file:
            if game["title"] not in file.read():
                game_name = game["title"]
                game_description = game["description"]
                end_date = game["promotions"]["promotionalOffers"][0]["promotionalOffers"][0]["endDate"]
                end_date = end_date[0:9]
                free_games.append({
                    "game_name" : game_name,
                    "game_description" : game_description,
                    "end_date" : end_date
                })

print(f"Found {len(free_games)} free games.")

if len(free_games) == 0:
    quit()
    
account_sid = os.environ["TWILIO_ACCOUNT_SID"]
auth_token = os.environ["TWILIO_AUTH_TOKEN"]
twilio_number = os.environ["TWILIO_NUMBER"]
my_number = os.environ["MY_NUMBER"]


for game in free_games:
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body=f"Free Game Alert!\n{game["game_name"]} is free on Epic Games Store until {game["end_date"]}!\n{game["game_description"]}",
        from_=twilio_number,
        to=my_number,
    )

    print("Message Sent!")

    with open(file="games_notified.txt", mode="a") as file:
        file.write(game_name + "\n")