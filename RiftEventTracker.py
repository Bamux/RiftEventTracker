import requests
import json
import time
import win32com.client
import pythoncom
from threading import Thread
import os
import math
import codecs
import configparser
from collections import OrderedDict
from tkinter import *

def read_config(configfile):
    if os.path.isfile(configfile):
        config = configparser.ConfigParser()
        config.read(configfile)
        return config
    else:
        config = write_new_config(configfile)
        return config

def write_new_config(configfile):
    config = configparser.ConfigParser()
    config['Settings'] = {}
    settings = config['Settings']
    settings['serverlocation'] = 'eu'
    settings['voice'] = 'yes'
    settings['volume'] = '100'
    settings['unstable_events'] = 'no'
    config['GUI'] = {}
    gui = config['GUI']
    gui['x'] = '325'
    gui['y'] = '200'
    gui['width'] = '400'
    gui['height'] = '154'
    gui['background'] = 'black'
    gui['foreground'] = 'white'
    gui['alpha'] = '0.7'
    gui['borderless'] = 'no'
    expansions = sorted(zones.keys())
    for expansion in expansions:
        sorted_zones = sorted(zones[expansion].items(), key=lambda x: x[1])
        config[expansion] = {}
        for zone in sorted_zones:
            config[expansion][str(zone[0])] = str(zone[1])
    with open(configfile, 'w') as configfile:
        config.write(configfile)
    return config


def zones_to_track():
    zoneid = {}
    for item in config:
        if item != "Settings" and item != "GUI":
            for key, value in config[item].items():
                zoneid[key] = value
    return zoneid

def webapi(zoneid):
    eventlist = []
    first_run = True
    unstable_events = config['Settings']['unstable_events']
    serverlocation = config['Settings']['serverlocation']
    if serverlocation == 'eu':
        url = "http://web-api-eu.riftgame.com:8080/chatservice/zoneevent/list?shardId="
    else:
        serverlocation = 'na'
        url = "http://web-api-us.riftgame.com:8080/chatservice/zoneevent/list?shardId="
    while True:
        output = []
        for shardid in shards[serverlocation]:
            data = json.loads(requests.get(url + str(shardid)).text)['data']
            if data:
                for zone in data:
                    if 'started' in zone:
                        condition = False
                        if unstable_events == "no":
                            if 'Unstable' in zone['name'] or 'Instabil' in zone['name'] or 'instable' in zone['name']:
                                condition = True
                        if not condition:
                            for item in zoneid:
                                if item == str(zone['zoneId']):
                                    output += [[zone['started'], zoneid[item], shards[serverlocation][shardid],
                                                zone['name']]]
        output.sort(reverse=True)
        guioutput = ""
        for item in output:
            min = str(int( math.floor((time.time() - item[0]) / 60) ))
            min = '{:02}'.format(int(min))
            guioutput += (" " +  min + " m  " + item[1] + " | " + item[2] + " | " + item[3] + '\n')
            if config['Settings']['voice'] == "yes":
                eventexist = False
                for started in eventlist:
                    if item[0] == started[0]:
                        eventexist = True
                if not eventexist:
                    eventlist += [(item[0], item[1])]
                    if not first_run:
                        text = "Event in " + item[1] + " on " + item[2]
                        Thread(target=saytext, args=(text,)).start()
        if first_run:
            first_run = False
        v.set(guioutput)
        time.sleep(15)

def saytext(say):
    pythoncom.CoInitializeEx(pythoncom.COINIT_MULTITHREADED)
    speak.Volume = int(config['Settings']['volume'])
    speak.Speak(say)

def ask_quit():
    global configfile
    config['GUI']['x'] = (str(root.winfo_x()))
    config['GUI']['y'] = (str(root.winfo_y()))
    config['GUI']['width'] = (str(root.winfo_width()))
    config['GUI']['height'] = (str(root.winfo_height()))
    with open(configfile, 'w') as configfile:
        config.write(configfile)
    root.destroy()
    os._exit(1)

def leftclick(event):
    if config["GUI"]['borderless'] == "no":
        root.overrideredirect(1)
        config["GUI"]['borderless'] = "yes"
    else:
        root.overrideredirect(0)  # Remove border
        config["GUI"]['borderless'] = "no"

def middleclick(event):
    pass

def rightclick(event):
    time.sleep(0.3)
    ask_quit()

zones = {
    'Prophecy of Ahnket': {
        2007770238: 'Ashenfell',
        788055204: 'Gedlo Badlands',
        2066418614: 'Scatherran Forest',
        511816852: 'Vostigar Peaks',
        1208799201: 'Xarth Mire',
    },
    'Nightmare Tide': {
        302: 'Draumheim',
        301: 'Goboro Reef',
        28: 'Planetouched Wilds',
        303: 'Tarken Glacier',
        426135797: "Tyrant's Throne",
    },
    'Storm Legion': {
        1446819710: 'Ardent Domain',
        790513416: 'Ashora',
        1213399942: 'Eastern Holdings',
        1770829751: 'Cape Jule',
        1967477725: 'City Core',
        479431687: 'Kingdom of Pelladane',
        1300766935: 'Kingsward',
        956914599: 'Morban',
        282584906: 'The Dendrome',
        1494372221: 'Seratos',
        798793247: 'Steppes of Infinity',
    },
    'Classic': {
        336995470: 'Droughtlands',
        19: 'Freemarch',
        22: 'Iron Pine Peak',
        27: 'Gloamwood',
        1992854106: 'Ember Isle',
        24: 'Moonshade Highlands',
        26580443: 'Scarlet Gorge',
        20: 'Scarwood Reach',
        6: 'Shimmersand',
        12: 'Silverwood',
        26: 'Stillmoor',
        1481781477: 'Stonefield',
    },
}

shards = {
  'na': {
    1704: 'Deepwood',
    1707: 'Faeblight',
    1702: 'Greybriar',
    1721: 'Hailol',
    1708: 'Laethys',
    1701: 'Seastone',
    1706: 'Wolfsbane',
  },
  'eu': {
    2702: 'Bloodiron',
    2714: 'Brisesol',
    2711: 'Brutwacht',
    2721: 'Gelidra',
    2741: 'Typhiria',
    2722: 'Zaviel',
  }
}

configfile = "config.ini"
config = read_config(configfile)
speak = win32com.client.Dispatch('Sapi.SpVoice')
zoneid = zones_to_track()


# GUI
root = Tk()
COLOR = "black"
root.title("Rift Event Tracker v0.4")
root.geometry(config['GUI']['width'] + "x" + config['GUI']['height'])
root.geometry("+" + config['GUI']['x'] + "+" + config['GUI']['y'])
root.bind("<Button-1>", leftclick)
root.bind("<Button-2>", middleclick)
test = root.bind("<Button-3>", rightclick)
v = StringVar()
Label(root, textvariable=v, anchor=NW, justify=LEFT,width=config['GUI']['width'],height=config['GUI']['height'],
      bg=config['GUI']['background'], fg=config['GUI']['foreground']).pack()
root.protocol("WM_DELETE_WINDOW", ask_quit)
root.attributes('-alpha',config['GUI']['alpha'])
root.wm_attributes("-topmost", 1)
if config["GUI"]['borderless'] == "yes":
    root.overrideredirect(1)
Thread(target=webapi, args=(zoneid,)).start()
mainloop()
