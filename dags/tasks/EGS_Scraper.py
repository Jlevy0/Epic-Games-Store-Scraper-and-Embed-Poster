"""
Author: Jacob Levy
This program scrapes the Epic Games Store for new free games.
Program is run daily via Free_Games_Scraper.py Airflow DAG.
"""
from selenium import webdriver
import csv
from datetime import date

def scrape_data():
    """
    Utilizes Selenium to find elements on the Epic Games Store that advertise free games.
    """
    #We'll begin by initializing our dictionary which will store some of the scraped data.
    games = {'game_name': [], 'offer_period': [], 
    'store_link': [], 'date_written':date.today(), 'logo_link':[]}

    url = "https://www.epicgames.com/store/en-US/free-games"

    driver = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver')
    driver.get(url)
    #Finding our element(s). There can be more than one game available at a time.
    elementInfo = driver.find_elements_by_xpath("//a[contains(@aria-label, 'Free Now')]")
    elementImages = driver.find_elements_by_xpath("//a[contains(@aria-label, 'Free Now')]//img")

    for  info, image in zip(elementInfo, elementImages):
        #Splitting the info for each game by newline character,
        #and removing "FREE NOW" since we don't need it.
        infoList = info.text.split('\n')
        infoList.remove("FREE NOW")

        #Checking if it's been offered before. If it has, we'll ignore it.
        game_name = infoList[0]
        if check_duplicate(game_name):
            continue

        #Filling out our dictionary.
        games['game_name'].append(game_name)
        games['offer_period'].append(infoList[1])
        games['store_link'].append(info.get_attribute('href'))

        #Grabbing the url for the promotional image.
        games['logo_link'].append(image.get_attribute('src'))


    #Lastly, we'll close the driver and write what data we have to the CSV.
    driver.quit()
    write_data(games)
    return

def check_duplicate(game_name):
    """
    We want to avoid duplicate offerings, since we don't need them.
    So, we'll be checking to see if the 
    games offered have already been written to EGS_Data.csv
    Arguments:
        game_name: The name of the game, to be searched for in the csv.
    Returns:
        True, if it finds the game's name in the CSV already
        False, if no duplicate is found.
    """
    #The field names we'll use to when opening up the csv.
    fieldnames = ['game_name','offer_period', 'store_link', 'date_written', 'logo_link']

    with open('EGS_Data.csv', 'r', newline='') as f:
        reader = csv.DictReader(f, fieldnames=fieldnames)
        for line in reader:
            #Checking if the game has already been written to the file. If it has, we'll return true.
            if line['game_name'] == game_name:
                return True
    #If we didn't find the game name in the file, we'll return false. 
    return False

def write_data(games):
    """
    Writing our data to a CSV. 
    The CSV will then be read by Embed_Poster.py in order to populate the embed.
    Arguments:
        games(dict): Our dictionary holding the scraped store data.
    """
    #Like in check_duplicate(), these will be used when opening our csv. They are also our csv's headers.
    fieldnames = ['game_name','offer_period', 'store_link', 'date_written', 'logo_link']

    with open('EGS_Data.csv', 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        for element in range(len(games['game_name'])):
            #Writing all the values from our games dictionary to the csv. 
            writer.writerow({'game_name': games['game_name'][element], 
            'offer_period': games['offer_period'][element], 
            'store_link': games['store_link'][element],
            'date_written':games['date_written'],
            'logo_link':games['logo_link'][element]})

if __name__ == '__main__':
    scrape_data()