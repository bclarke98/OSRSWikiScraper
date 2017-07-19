# OSRS Wiki Scraper

Python3 script that allows for easy access to Oldschool Runescape NPC drops.


This script was designed to help developers dynamically pull RuneScape NPC drops from the wiki. It can either run a Flask server that receives input via GET requests and outputs directly to the page or can be simply output the drops as a CSV file.


If you don't want to run anything locally, you can use the following request: rs.d3x.me:8000/droptable?npc=NPC_NAME


The NPC_NAME must match the wiki URL. For example, a green dragon's wiki page is oldschoolrunescape.wikia.com/wiki/Green_dragon

Therefore, NPC_NAME must be Green_dragon.


Required Modules: Requests, lxml, Flask (only necessary if you want to actually run the flask server)


# Command Line Parameters


- -h,       &nbsp;&nbsp;&nbsp;prints parameters to console
- -s        &nbsp;&nbsp;&nbsp;runs flask server on local computer to handle GET requests
- -i        &nbsp;&nbsp;&nbsp;specify local ip to run the server on (default 0.0.0.0)
- -p        &nbsp;&nbsp;&nbsp;specify port to run the server on (default 8000)
- -n        &nbsp;&nbsp;&nbsp;specify npc name to search for (does not run flask server, saves CSV with output)
- -o        &nbsp;&nbsp;&nbsp;specify file output path (default NPC_NAME.csv)
- -w        &nbsp;&nbsp;&nbsp;add this parameter if running from a Windows machine
- -c        &nbsp;&nbsp;&nbsp;if included, CSV output will not contain image icon URLs


# Known Issues: 


- Unable to load data from certain mirror wiki pages (/wiki/Fanatic vs. /wiki/Chaos_Fanatic)
