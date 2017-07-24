# OSRS Wiki Scraper

This script was designed to help developers dynamically pull RuneScape NPC drops from the wiki.  
It has been updated to pull item statistics as well.  

It can be run in one of two ways:
- as Flask server that receives input via GET requests and outputs directly to the page 
- as a normal Python script that outputs results as a CSV/JSON file


# Usage & Requirements

```
You can use this script without having to download anything.

Simply send a request to "rs.d3x.me:8000/droptable?npc=NPC_NAME"

Please note that 'NPC_NAME' must match the OSRS wiki URL for that NPC.
For example, the wiki URL for green dragons is oldschoolrunescape.wikia.com/wiki/Green_dragon
If you wanted the drop table for green dragons, you would replace 'NPC_NAME' with Green_dragon.

The first line of the data is formatted as [NPC_NAME],[NPC_IMAGE_URL]
Subsequent lines are formatted as [ITEM_IMAGE_URL],[ITEM_NAME],[QUANTITY],[RARITY]

If you want to get item stats, change "/droptable?npc=" to "/item?name="
The stats are returned in JSON format.

If you want the stats for every weapon in OSRS, don't add "?name=" to the request.

Unfortunately, this is not being run on a dedicated server, so uptime is not always guarenteed.
If the server is down and you need it up, feel free to contact me. Details are below.

If you prefer to run the script locally, you must have:
    - Python 3.x
    - Requests module
    - lxml module (comes pre-installed with some versions of Python)

If you want to run your own server to guarentee uptime when you need it, you also must have:
    - flask module
    - access to port forwarding (default port is 8000, see command line parameters below)


Command Line Parameters
------------------------------------------------------------------------------------------
-h        prints parameters to console
-s        runs flask server on local computer to handle GET requests
-i        specify local ip to run the server on (default 0.0.0.0)
-p        specify port to run the server on (default 8000)
-n        specify npc name to search for (does not run flask server, saves CSV with output)
-o        specify file output path (default NPC_NAME.csv/.json)
-w        add this parameter if running from a Windows machine
-c        if included, CSV output will not contain image icon URLs
-e        specify equipment item name to search (does not run flask server, saves JSON with output)
-aw       locally save a JSON file with stats for every weapon in OSRS (warning: takes a long time to run)
```


# Future Features

- support for weapon/equipment stats [IN PROGRESS]
- multiple formats for returned values (csv, json, etc)
- web front-end for loot tracker + virtual loadouts


# Known Issues: 


- Unable to load data from certain mirror wiki pages (/wiki/Fanatic vs. /wiki/Chaos_Fanatic)


# Contact Me
**Want to request a feature, report a bug, or give general feedback?**  
Send me a message on Reddit -  */u/overlysalty*


# Credits
Huge thanks to /u/artpicks for inspiring this project. Go check out his loot tracking program!

