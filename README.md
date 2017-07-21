# OSRS Wiki Scraper

Python3 script that allows for easy access to Oldschool Runescape NPC drops.


This script was designed to help developers dynamically pull RuneScape NPC drops from the wiki.  
It can either run a Flask server that receives input via GET requests and outputs directly to the page or can be simply output the drops as a CSV file.


# Usage & Requirements

```
You can use this script without having to download anything.

Simply send a request to "rs.d3x.me:8000/droptable?npc=NPC_NAME"

Please note that 'NPC_NAME' must match the OSRS wiki URL for that NPC.
For example, the wiki URL for green dragons is oldschoolrunescape.wikia.com/wiki/Green_dragon
If you wanted the drop table for green dragons, you would replace 'NPC_NAME' with Green_dragon.

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
-o        specify file output path (default NPC_NAME.csv)
-w        add this parameter if running from a Windows machine
-c        if included, CSV output will not contain image icon URLs
```


# Future Features

- support for weapon/equipment stats  
- multiple formats for returned values (csv, json, etc)
- web front-end for loot tracker + virtual loadouts


# Known Issues: 


- Unable to load data from certain mirror wiki pages (/wiki/Fanatic vs. /wiki/Chaos_Fanatic)


# Contact Me
**Want to request a feature, report a bug, or give general feedback?**  
Send me a message on Reddit -  */u/overlysalty*

