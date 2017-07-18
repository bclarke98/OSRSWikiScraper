# OSRS Wiki Scraper

Python3 script that allows for easy access to Oldschool Runescape NPC drops.


This script was designed to help developers dynamically pull RuneScape NPC drops from the wiki. It runs a Flask server that receives input via GET requests and outputs directly to the page.


If you want to use host your own version, take note that it runs on port 8000.


If you don't want to host your own server, use the following request: rs.d3x.me:8000/droptable?npc=NPC_NAME

The NPC_NAME must match the wiki URL. For example, a green dragon's wiki page is oldschoolrunescape.wikia.com/wiki/Green_dragon

Therefore, NPC_NAME must be Green_dragon.



Required Modules: Requests, lxml, Flask


# Known Issues: 


- Unable to load data from certain mirror wiki pages (/wiki/Fanatic vs. /wiki/Chaos_Fanatic)
