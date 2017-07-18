#!usr/bin/env python3

# @author /u/overlysalty

# this script was designed to help developers dynamically pull RuneScape NPC drops from the wiki
# it runs a flask server that receives input via GET requests and outputs directly to the page

# If you want to use host your own version, take note that it runs on port 8000

# If you don't want to host your own server, use the following request:
# rs.d3x.me:8000/droptable?npc=NPC_NAME

# Return Format:
# [LINE 1]:      NPC_NAME       ,  NPC_IMAGE_LINK   
# [LINES 2+]:    ITEM_IMAGE_LINK,  ITEM_NAME     ,  QUANTITY,  RARITY

# If you don't want to item image links, add &icons=0 to the end of your request

import os
import datetime
import requests
from lxml import html
from flask import Flask
from flask import request

# saves a shell script to stop the server if you decide to run it with 'nohup'
with open('stop.sh', 'w') as pw:
    pw.write('echo "Stopping Server..."\nkill ' + str(os.getpid()) + '\nrm stop.sh')

# formatted UTC time string for logging
def utc_time():
    return '[' + str(datetime.datetime.utcnow())[:-7] + ' (UTC)]: '

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
    n = [zz for zz in n if len(zz.strip()) > 0]
    q = [zz for zz in q if len(zz.strip()) > 0]
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

# create flask object
app = Flask(__name__)

# accept connections at HOSTNAME:8000/droptable
@app.route('/droptable', methods=['GET'])
def handle():
    # log request IPs to see how much this is actually used by the community
    with open('connections.dat', 'a') as fw:
        fw.write(utc_time() + str(request.environ['REMOTE_ADDR']) + '\n')
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
    app.run(host='0.0.0.0', port=8000)
