"""
Author: Jacob Levy
This program posts an embed to Discord if there's a free new game on the Epic Games Store.
Program is run daily via Free_Games_Scraper.py Airflow DAG.
"""
import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import csv
from datetime import date
import sys

#Loading in our API token, the connection to the server, and the server's announcement channel
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
ANNOUNCEMENT_CHANNEL_ID = int(os.getenv('ANNOUNCEMENT_CHANNEL_ID'))
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)



@bot.event
async def on_ready():
    #Loading into our server.
    for guild in bot.guilds:
        if guild.name == GUILD:
            break
    #Now we'll be loading in our games dictionary - just like in EGS_Scraper.py
    games = get_games_data()
    #We'll get this channel object so that we'll have a place to post the embed message.
    channel = guild.get_channel(ANNOUNCEMENT_CHANNEL_ID)

    embedColor = discord.Colour.from_rgb(255, 215, 0)
    #And now what we've been waiting for: posting our data to Discord!
    for element in range(len(games['game_name'])):
        embedMessage = discord.Embed(
            title = f"Free on the Epic Games Store:\n{games['game_name'][element]}",
            color = embedColor)

        embedMessage.add_field(name='Offer Period', 
            value = games['offer_period'][element], inline=False)

        embedMessage.add_field(name='Store Link', value = games['store_link'][element],
            inline=True)

        
        embedMessage.set_image(url = games['logo_link'][element])
        #Lastly, we'll send our message to the server's announcement channel.
        await channel.send(embed=embedMessage)
    #Discordpy wants to run forever, and there's no 
    #really elegant way to end it, so we'll just use sys.exit().
    sys.exit(0)

def get_games_data():
    """
    Grabs the data from the csv, checks that data was written today.
    Returns:
        games (dict): dictionary populated with the data about the offered games.
    """
    #Declaring our dictionary to be loaded in and our fieldnames to read the csv.
    games = {'game_name': [], 'offer_period': [], 
    'store_link': [], 'date_written':str(date.today()), 'logo_link': []}

    fieldnames = ['game_name','offer_period', 'store_link', 'date_written', 'logo_link']

    with open ('EGS_Data.csv', 'r', newline='') as f:
        reader = csv.DictReader(f, fieldnames=fieldnames)
        #Skipping over the header.
        next(reader)
        for line in reader:
            #Checking that data was written today.
            if line['date_written'] == games['date_written']:
                #Reading the csv back into a dictionary.
                games['game_name'].append(line['game_name'])
                games['offer_period'].append(line['offer_period'])
                games['store_link'].append(line['store_link'])
                games['logo_link'].append(line['logo_link'])
        return games

def start_bot():
    """
    An odd function, but it's something that Airflow can call on.
    We'll use this in the DAG file.
    You could also use a bash operator for this purpose.
    """
    #Running our bot.
    bot.run(TOKEN)

if __name__ == '__main__':
    start_bot()