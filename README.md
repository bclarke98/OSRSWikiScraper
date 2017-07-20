# OSRS Wiki Scraper

Python3 script that allows for easy access to Oldschool Runescape NPC drops.


This script was designed to help developers dynamically pull RuneScape NPC drops from the wiki. It can either run a Flask server that receives input via GET requests and outputs directly to the page or can be simply output the drops as a CSV file.


If you don't want to run anything locally, you can use the following request: rs.d3x.me:8000/droptable?npc=NPC_NAME


The NPC_NAME must match the wiki URL. For example, a green dragon's wiki page is oldschoolrunescape.wikia.com/wiki/Green_dragon

Therefore, NPC_NAME must be Green_dragon.


Required Modules: Requests, lxml, Flask (only necessary if you want to actually run the flask server)


# Future Features
### Want to request a feature, report a bug, or give general feedback? Send me a message on Reddit - /u/overlysalty
- support for weapon/equipment stats



# Command Line Parameters

```
-h        prints parameters to console
-s        runs flask server on local computer to handle GET requests
-i        specify local ip to run the server on (default 0.0.0.0)
-p        specify port to run the server on (default 8000)
-n        specify npc name to search for (does not run flask server, saves CSV with output)
-o        specify file output path (default NPC_NAME.csv)
-w        add this parameter if running from a Windows machine
-c        if included, CSV output will not contain image icon URLs
```

# Known Issues: 


- Unable to load data from certain mirror wiki pages (/wiki/Fanatic vs. /wiki/Chaos_Fanatic)
