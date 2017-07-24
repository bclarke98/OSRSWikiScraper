#!/usr/bin/env python3
import argparse
import requests
import sys
import os
import datetime
import json
from lxml import html

# handle command line arguments
parser = argparse.ArgumentParser()

parser.add_argument('-s', help='runs flask server on local computer to handle GET requests', action='store_true')
parser.add_argument('-i', help='specify local ip to run the server on (default 0.0.0.0)', default='0.0.0.0')
parser.add_argument('-p', help='specify port to run the server on (default 8000)', type=int, default=8000)
parser.add_argument('-n', help='npc name to search (does not run flask server, saves CSV with output)')
parser.add_argument('-o', help='specifies file output path (default NPC_NAME.csv/.json)')
parser.add_argument('-w', help='add this parameter if running from a Windows machine', action='store_true')
parser.add_argument('-c', help='if included, CSV output will not contain icon image URLs', action='store_true')
parser.add_argument('-e', help='equipment item name to search (does not run flask server, saves JSON with output)')
# parser.add_argument('-aw', help='saves JSON file with every weapon in the game as allweapons.json', action='store_true')

args = parser.parse_args()


# handles the wiki parsing, basically the backbone of this whole script
def get_drop_table(boss, icons=True):
    wiki = 'http://oldschoolrunescape.wikia.com/wiki/'
    # send a request to get the raw HTML of the wiki page
    r = requests.get(wiki + boss)
    # pass the raw HTML to the lxml module so that it can be parsed later
    content = html.fromstring(r.content)
    # create the NPC Image variable (not sure if this is necessary... I'm not up to date on how Python3 handles scope with try/except
    ni = ''
    try:
        # I'm new to lxml, so I'll try to explain this as best as I can:
        # '//table[contains(@class, "wikitable infobox")]'
        #     grab the information inside of tables that have the 'wikitable infobox' classes
        # '//td[contains(@style, "text-align")]'
        #     only show the information within <td> tags that have "text-align" in the styling
        # '//img[contains(@alt, "' + boss.replace('_', ' ') + '")]/@src'
        #     only grab <img> tags with 'alt=[NPC_NAME]'
        #     then grab the first item in the array of 'src' elements
        ni = content.xpath('//table[contains(@class, "wikitable infobox")]//td[contains(@style, "text-align")]//img[contains(@alt, "' + boss.replace('_', ' ') + '")]/@src')[0]
    except:
        ni = 'i.imgur.com/ghLHiQZ.png' # not found thumbnail
    # grab the item images
    ii = content.xpath('//table[contains(@class, "wikitable sortable dropstable")]//tr[@style="text-align:center;"]//td[1]//img[1]/@src')
    # grab the item names
    n = content.xpath('//table[contains(@class, "wikitable sortable dropstable")]//tr[@style="text-align:center;"]//td[2]//a/text()')
    # grab the quantities
    q = content.xpath('//table[contains(@class, "wikitable sortable dropstable")]//tr[@style="text-align:center;"]//td[3]/text()')
    # grab the rarities
    h = content.xpath('//table[contains(@class, "wikitable sortable dropstable")]//tr[@style="text-align:center;"]//td[4]/text()')
    # item images kept giving 2 sources per item, we only want odd numbered indices 
    ii = ii[1::2]
    # remove any entries that are empty
    ii = [zz for zz in ii if len(zz.strip()) > 0]
    n = [zz for zz in n if len(zz.strip().replace('[','').replace(']','')) > 2]
    # the wiki uses the unicode character '–' to separate a range of drops and unicode likes to break other peoples' programs, so it's getting replaced with the normal '-'
    q = [zz.replace('–','-') for zz in q if len(zz.strip()) > 0]
    h = [zz for zz in h if len(zz.strip()) > 0]
    # first line is the NPC Name, NPC Image
    csv = '%s,%s \n' % (boss, ni)
    # if there are no items in the array, it couldnt find the NPC
    if len(n) == 0:
        return 'Found no results for query: "%s"' % boss
    # format the string based on whether or not the user wants icons included
    for i in range(len(n)):
        csv += '%s,%s,%s,%s \n' % (ii[i].strip(), n[i].strip(), q[i].strip().replace(',', ''), h[i].strip().replace(',', '')) if icons else '%s,%s,%s \n' % (n[i].strip(), q[i].strip().replace(',', ''), h[i].strip().replace(',', ''))
    # return the drops
    return csv

def get_item_stats(itemname):
    wiki = 'http://oldschoolrunescape.wikia.com/wiki/'
    r = requests.get(wiki + itemname)
    content = html.fromstring(r.content)
    try:
        n = content.xpath('//table[contains(@class, "wikitable infobox")]//caption/text()')[0].strip()
    except:
        n = itemname
    rjson = {'_name':n, 'offensive':{}, 'defensive':{}, 'misc':{}}
    ts = '//table[contains(@class, "wikitable smallpadding")]'
    titles = content.xpath(ts + '//tr[3]//a/@title')
    titles = [i for i in titles if len(i.strip()) > 0]
    atkv = content.xpath(ts + '//tr[4]//td/text()')
    atkv = [i for i in atkv if len(i.strip()) > 0]
    defv = content.xpath(ts + '//tr[7]//td/text()')
    defv = [i for i in defv if len(i.strip()) > 0]
    for i in range(len(titles)):
        rjson['offensive'][titles[i].strip()] = atkv[i].strip()
        rjson['defensive'][titles[i].strip()] = defv[i].strip()
    misct = content.xpath(ts + '//tr[9]//a/@title')
    misct = [i for i in misct if len(i.strip()) > 0]
    misct = [j for j in misct if 'eapon' not in j and 'slot' not in j]
    miscv = content.xpath(ts + '/tr[10]//td/text()')
    miscv = [i for i in miscv if len(i.strip()) > 0]
    for i in range(len(misct)):
        rjson['misc'][misct[i].strip()] = miscv[i].strip()
    return rjson

def get_all_weapons():
    onehandweapons = 'http://oldschoolrunescape.wikia.com/wiki/Weapons_table'
    twohandweapons = 'http://oldschoolrunescape.wikia.com/wiki/Two-handed_slot_table'
    r1 = requests.get(onehandweapons)
    r1c = html.fromstring(r1.content)
    r2 = requests.get(twohandweapons)
    r2c = html.fromstring(r2.content)
    ts = '//table[contains(@class, "wikitable sortable")]//td//a/@title'
    n = r1c.xpath(ts)
    # continue here
    # Note: only 2h ranged weapons have Ranged Strength stat

# if the user wants to run the server
if args.s:
    print('Attempting to run server on [%s:%d]' % (args.i, args.p))
    try:
        from flask import Flask
        from flask import request
    except:
        print('Error importing Flask module.')
        sys.exit()
    if not args.w:
        # saves a shell script to stop the server if you decide to run it with 'nohup'
        with open('stop.sh', 'w') as pw:
            pw.write('echo "Stopping Server..."\nkill ' + str(os.getpid()) + '\nrm stop.sh')

    # formatted EST string for logging 
    def est_time():
        s = str(datetime.datetime.utcnow())
        n = int(s[11:13])
        n = n - 4 if n - 4 > 0 else 24 - n
        return '[' + s[:11] + str(n) + s[13:-7] + ' (EST)]: '
    
    # create flask object
    app = Flask(__name__)
     
    @app.route('/item', methods=['GET'])
    def handle_i():
        # log request IPs to see how much this is actually used by the community
        with open('connections.dat', 'a') as fw:
            fw.write(est_time() + str(request.environ['REMOTE_ADDR']) + '\n')
        r = ''
        if request.method == 'GET':
            resp = request.args.getlist('name')
            # if there's a value for ?name=, grab it and pass it to get_item_stats
            if len(resp) == 1:
                r = resp[0].capitalize()
        return json.dumps(get_item_stats(r), sort_keys=True, indent=4) 
         
    # accept connections at HOSTNAME:8000/droptable
    @app.route('/droptable', methods=['GET'])
    def handle():
        # log request IPs to see how much this is actually used by the community
        with open('connections.dat', 'a') as fw:
            fw.write(est_time() + str(request.environ['REMOTE_ADDR']) + '\n')
        r = ''
        icon = True
        if request.method == 'GET':
            resp = request.args.getlist('npc')
            icons = request.args.getlist('icons')
            # if theres a value for ?icons=0, don't return icon links
            if len(icons) == 1 and icons[0] == '0':
                icon = False
            # if there's a value for ?npc=, grab it and pass it to get_drop_table
            if len(resp) == 1:
                r = resp[0].capitalize()
        return get_drop_table(r, icon)

    if __name__ == '__main__':
        app.run(host=args.i, port=args.p)
elif args.n: # if the user only wants to run the script locally
    print('Searching for drop table of NPC "%s"' % args.n)
    # create default path based on whether or not the script is running on a windows system
    path = str(os.getcwd().replace('\\','/')) + '/' + args.n + '.csv' if args.w else args.n + '.csv'
    # change path if the user specified a custom path
    if args.o:
        path = args.o if '.csv' in args.o else args.o + '.csv'
    # save data file
    with open(path, 'w') as fw:
        fw.write(get_drop_table(args.n.capitalize(), not args.c))
        print('Saved file to "%s"' % path)
elif args.e:
    print('Searching for stats for item "%s"' % args.e)
    # create default path based on whether or not the script is running on a windows system
    path = str(os.getcwd().replace('\\','/')) + '/' + args.e + '.json' if args.w else args.e + '.json'
    # change path if the user specified a custom path
    if args.o:
        path = args.o if '.json' in args.o else args.o + '.json'
    # save data file
    with open(path, 'w') as fw:
        fw.write(json.dumps(get_item_stats(args.e), sort_keys=True, indent=4)) 
        print('Saved file to "%s"' % path)
elif args.aw:
    print('Attempting to pull stats for all weapons in OSRS...')
    get_all_weapons()
    print('Saved weapon data to "allweapons.json"')
else:
    print('Please specify how you would like to run this script.\nUse -h or --help to list the options.')


