# Epic Games Store Scraper and Embed Poster
 This repository contains the scripts I used to create an automated web scraping pipeline that checks if the Epic Games Store has new free games. 
 The data I gather is then processed and posted to a Discord server in the form of an embed. 
## Introduction
Epic Games, a development studio best known for creating Fortnite, runs an online games store. One of the ways they encourage people to use the store is to offer free games every week. 

While it's not exactly hard to manually check the store every week, I decided to automate the process through and package it in a nice embed.
## Data Extraction
The data that we want is loaded in dynamically via JavaScript. As such, the usual combo of Requests + BeautifulSoup won't work, as that's only grabbing the raw HTML. Instead, we'll be using Selenium, and finding the element by its XPath. Here's an example of the element we're grabbing:

><a aria-label="Free Games, 1 of 3, Free Now, Paladins Epic Pack, Free Now - Oct 21 at 11:00 AM" role="link" href="/store/en-US/p/paladins--paladins-epic-pack"\>

This has most the data we need. The name of the game, how long it'll be free for, and a link to the store page. We'll do something similar to grab the link to the promotional image they use.
All of this data and when we found it is then saved to a CSV file, which also doubles as a way to check if we've already scraped for these games before.

## Posting the Content
The content is posted to a Discord server via [Discordpy's embed creation methods](https://discordpy.readthedocs.io/en/stable/api.html#embed). Here's what the final product looks like:

![embed](README_Images/Embed_Example.png)

## Automation

We'll use Apache Airflow to schedule the scraper and embed poster. We'll have it set to run everyday at noon. We'll prevent the embed poster from posting any repeats by having it check if the game title was written on the same day the program was run. If it isn't it'll simply exit the program with nothing posted.
