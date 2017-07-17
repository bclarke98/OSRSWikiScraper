# OSRS Wiki Scraper

Python3 script that allows for easy access to Oldschool Runescape NPC drops.


This script was designed to help developers dynamically pull RuneScape NPC drops from the wiki. It runs a Flask server that receives input via GET requests and outputs directly to the page.


If you want to use host your own version, take note that it runs on port 8000.


If you don't want to host your own server, use the following request: rs.d3x.me:8000/droptable?=NPC_NAME


Required Modules: Requests, lxml, Flask
