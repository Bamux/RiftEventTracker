# -*- coding: utf-8 -*-

import requests
import json
import time
import win32com.client
import pythoncom
from threading import Thread
import os
import math
import configparser
from tkinter import *
import codecs


def read_config(file):
    if os.path.isfile(file):
        config = configparser.ConfigParser()
        config.read(configfile)
    else:
        config = write_new_config(configfile)
    return config


def write_new_config(file):
    config = configparser.ConfigParser()
    config['Settings'] = {}
    settings = config['Settings']
    settings['serverlocation'] = 'eu'
    settings['language'] = 'eng'
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
    with open(file, 'w') as file:
        config.write(file)
    return config


def zones_to_track(config):
    zone_id = {}

    for item in config:
        if item != "Settings" and item != "GUI":
            for key, value in config[item].items():
                if ", " in value:
                    value = value.split(", ")
                    if config['Settings']['language'] == "ger":
                        zone_id[key] = value[1]
                    elif config['Settings']['language'] == "fr":
                        zone_id[key] = value[2]
                    else:
                        zone_id[key] = value[0]
                else:
                    zone_id[key] = value
    return zone_id


def get_data(zone_id, serverlocation, url, unstable_events):
    data_output = []
    for shardid in shards[serverlocation]:
        data = json.loads(requests.get(url + str(shardid)).text)['data']
        if data:
            for zone in data:
                if 'started' in zone:
                    condition = False
                    if unstable_events == "no"  or unstable_events == "only":
                        if 'Unstable' in zone['name'] or 'Instabil' in zone['name'] or 'instable' in zone['name']:
                            if unstable_events == "no":
                                condition = False
                            else:
                                condition = True
                    else:
                        condition = True
                    if condition:
                        for item in zoneid:
                            if item == str(zone['zoneId']):
                                data_output += [[zone['started'], zone_id[item], shards[serverlocation][shardid],
                                                 zone['name']]]
        else:
            data_output += [[0, shards[serverlocation][shardid]]]
    data_output.sort(reverse=True)
    return data_output


def outputloop(zone_id, serverlocation, url, unstable_events, voice):
    eventlist = []
    first_run = True
    if serverlocation == "prime" or serverlocation == "log":
        logfile_analysis(serverlocation, unstable_events)
    while True:
        if not root:
            break
        data_output = get_data(zone_id, serverlocation, url, unstable_events)
        unavailable_servers = 0
        if data_output:
            guioutput = ""
            for item in data_output:
                if item[0] == 0:
                    unavailable_servers += 1
                    guioutput += " " + item[1] + " not available\n"
                else:
                    m = int(math.floor((time.time() - item[0]) / 60))
                    if m < 0:
                        m = 0
                    if m < 100:
                        m = '{:02}'.format(m)
                        guioutput += (" " + m + " m  " + item[1] + " | " + item[2] + " | " + item[3] + '\n')
                    if voice == "yes":
                        eventexist = False
                        for started in eventlist:
                            if item[0] == started[0]:
                                eventexist = True
                        if not eventexist:
                            eventlist += [(item[0], item[1])]
                            if not first_run:
                                beginning = "Event in"
                                end = "on"
                                if config_var['Settings']['language'] == 'ger':
                                    end = "auf"
                                elif config_var['Settings']['language'] == 'fr':
                                    beginning = "Événement en"
                                    end = "au"
                                text = beginning + " " + item[1] + " " + end + " " + item[2]
                                Thread(target=saytext, args=(text,)).start()
            if first_run:
                first_run = False
            if root:
                v.set(guioutput)
        else:
            v.set(" No event running")
        if unavailable_servers == len(shards[serverlocation]):
            logfile_analysis(serverlocation, unstable_events)
        time.sleep(15)


def saytext(text):
    if root and config_var['Settings']['voice'] == "yes":
        try:
            pythoncom.CoInitializeEx(pythoncom.COINIT_MULTITHREADED)
            speak.Speak(text)
        except:
            pass


def close():
    file = configfile
    config = ""
    if os.path.isfile(configfile):
        config = configparser.ConfigParser()
        config.read(configfile)
    zones_id = zones_to_track(config)
    config['GUI']['x'] = (str(root.winfo_x()))
    config['GUI']['y'] = (str(root.winfo_y()))
    config['GUI']['width'] = (str(root.winfo_width()))
    config['GUI']['height'] = (str(root.winfo_height()))
    config["GUI"]['borderless'] = borderless
    expansions = sorted(zones.keys())
    for expansion in expansions:
        sorted_zones = sorted(zones[expansion].items(), key=lambda x: x[1])
        config[expansion] = {}
        for zone in sorted_zones:
            zoneexist = False
            for zone_id in zones_id:
                if str(zone[0]) == zone_id:
                    zoneexist = True
            if zoneexist:
                config[expansion][str(zone[0])] = str(zone[1])
            else:
                config[expansion][";" + str(zone[0])] = str(zone[1])
    with open(file, 'w') as file:
        config.write(file)
    root.destroy()
    os._exit(1)


def leftclick(event):
    global borderless
    if borderless == "no":
        root.overrideredirect(1)
        borderless = "yes"
    else:
        root.overrideredirect(0)  # Remove border
        borderless = "no"


def rightclick(event):
    time.sleep(0.3)
    close()


def logfilecheck():
    while True:
        log_exists = False
        log_file = ""
        if os.path.isfile(os.path.expanduser('~\Documents\RIFT\Log.txt')):
            log_file = os.path.expanduser('~\Documents\RIFT\Log.txt')
            log_exists = True
        elif os.path.isfile('C:\Program Files (x86)\RIFT Game\Log.txt'):
            log_file = 'C:\Program Files (x86)\RIFT Game\Log.txt'
            log_exists = True
        elif os.path.isfile('C:\Programs\RIFT~1\Log.txt'):
            log_file = 'C:\Programs\RIFT~1\Log.txt'
            log_exists = True
        if log_exists:
            logtext = codecs.open(log_file, 'r', "utf-8")
            return logtext
        time.sleep(10)


def lofile_output(serverlocation, data_output):
    guioutput = ""
    i = 0
    for item in data_output:
        if i < 15:
            m = int(math.floor((time.time() - item[0]) / 60))
            if m < 0:
                m = 0
            if m < 100:
                m = '{:02}'.format(m)
            if serverlocation == "prime":
                guioutput += (" " + m + " m  " + item[1] + " | " + item[3] + "\n")
            else:
                guioutput += (" " + m + " m  " + item[1] + " | " + item[2] + " | " + item[3] + '\n')
        else:
            break
    v.set(guioutput)


def logfile_analysis(serverlocation, unstable_events):  # analyzes each new line in the Log.txt
    guioutput = " WebApi not aviable!\n Use /log in Rift as an alternative data source for running events."
    v.set(guioutput)
    logtext = logfilecheck()
    logtext.seek(0, 2)  # jumps to the end of the Log.txt
    data_output = []
    zone = ""
    shardname = ""
    running_log = False
    previous_event = []
    while True:
        line = ""
        log = ""
        line = logtext.readline()  # read new line
        if line:
            if not running_log:
                running_log = True
                v.set(" Logfile found. Search for events started.")
            if "[" in line and "]" in line and "!" in line:
                for shardname in shards[serverlocation].values():
                    if shardname in line:
                        for zone in zoneid.values():
                            if zone in line:
                                condition = False
                                if unstable_events == "no" or unstable_events == "only":
                                    if 'Unstable' in zone['name'] or 'Instabil' in zone['name'] or 'instable' in zone[
                                        'name']:
                                        if unstable_events == "no":
                                            condition = False
                                        else:
                                            condition = True
                                else:
                                    condition = True
                                if condition:
                                    event = line.split("[")[2]
                                    event = event.split("]")[0]
                                    timestamp = int(math.floor(time.time()))
                                    event = [timestamp, zone, shardname, event]
                                    if previous_event and event[3] == previous_event[3] and timestamp - previous_event[0] < 10:
                                        condition = False
                                    if condition:
                                        previous_event = event
                                        data_output += [event]
                                        data_output.sort(reverse=True)
                                        event = ()
                                        lofile_output(serverlocation, data_output)
                                        beginning = "Event in"
                                        end = "on"
                                        if config_var['Settings']['language'] == 'ger':
                                            end = "auf"
                                        elif config_var['Settings']['language'] == 'fr':
                                            beginning = "Événement en"
                                            end = "au"
                                        if serverlocation == "prime":
                                            text = beginning + " " + zone
                                        else:
                                            text = beginning + " " + zone + " " + end + " " + shardname
                                        Thread(target=saytext, args=(text,)).start()
                                break
                        break
        else:
            if data_output:
                lofile_output(serverlocation, data_output)
            time.sleep(1)  # waiting for a new input


zones = {
    'Prophecy of Ahnket': {
        2007770238: 'Ashenfell, Aschenfall, Chutecendres',
        788055204: 'Gedlo Badlands, Gedlonianisches Ödland, Maleterres de Gedlo',
        2066418614: 'Scatherran Forest, Skatherran-Wald, Forêt des Bourreaux',
        511816852: 'Vostigar Peaks, Vostigar-Gipfel, Pics de Vostigar',
        1208799201: 'Xarth Mire, Xarth-Sumpf, Bourbier de Xarth',
    },
    'Nightmare Tide': {
        302: 'Draumheim, Draumheim, Draumheim',
        301: 'Goboro Reef, Goboro-Riff, Récif de Goboro',
        28: 'Planetouched Wilds, Ebenenberührte Wildnis, Étendues marquées par les Plans',
        303: 'Tarken Glacier, Tarken-Gletscher, Glacier de Tarken',
        426135797: "Tyrant's Throne, Tyrannenthron, Trône du Tyran",
    },
    'Storm Legion': {
        1446819710: 'Ardent Domain, Eiferer-Reich, Contrée Ardente',
        790513416: 'Ashora',
        1213399942: "Eastern Holdings, Östliche Besitztümer, Fiefs de l'Orient",
        1770829751: 'Cape Jule, Kap Jul, Cap Yule',
        1967477725: 'City Core, Stadtkern, Cœur de la Cité',
        479431687: 'Kingdom of Pelladane, Königreich Pelladane, Royaume de Pelladane',
        1300766935: 'Kingsward, Königszirkel, Protectorat du Roi',
        956914599: 'Morban',
        282584906: 'The Dendrome, Das Dendrom, The Dendrome',
        1494372221: 'Seratos, Seratos, Serratos',
        798793247: "Steppes of Infinity, Steppen der Unendlichkeit, Steppes de l'Infini",
    },
    'Classic': {
        336995470: 'Droughtlands, Ödlande, Plaines Arides',
        19: 'Freemarch, Freimark, Libremarche',
        22: 'Iron Pine Peak, Eisenkieferngipfel, Pic du Pin de fer',
        27: 'Gloamwood, Dämmerwald, Bois du Crépuscule',
        1992854106: 'Ember Isle, Glutinsel, Île de Braise',
        24: "Moonshade Highlands, Mondschattenberge, Hautes-Terres d'Ombrelune",
        26580443: 'Scarlet Gorge, Scharlachrote Schlucht, Gorges Écarlates',
        20: 'Scarwood Reach, Wundwaldregion, Étendue de Bois Meurtris',
        6: 'Shimmersand, Schimmersand, Sable-chatoyant',
        12: "Silverwood, Silberwald, Bois d'Argent'",
        26: 'Stillmoor, Stillmoor, Mornelande',
        1481781477: 'Stonefield, Steinfeld, Champ de Pierre',
    },
}

shards = {
  'us': {
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
    },
    'prime': {
        0: 'Virgil',
    },
}

configfile = "config.ini"
config_var = read_config(configfile)
if config_var['Settings']['serverlocation'] != 'eu' and config_var['Settings']['serverlocation'] != 'prime':
    config_var['Settings']['serverlocation'] = 'us'
try:
    speak = win32com.client.Dispatch('Sapi.SpVoice')
    speak.Volume = int(config_var['Settings']['volume'])
except:
    pass
webapi = "http://web-api-" + config_var['Settings']['serverlocation'] \
         + ".riftgame.com:8080/chatservice/zoneevent/list?shardId="
zoneid = zones_to_track(config_var)
borderless = config_var["GUI"]['borderless']

# GUI
root = Tk()
root.title("Rift Event Tracker 0.5")
root.geometry(config_var['GUI']['width'] + "x" + config_var['GUI']['height'])
root.geometry("+" + config_var['GUI']['x'] + "+" + config_var['GUI']['y'])
root.bind("<Button-1>", leftclick)
test = root.bind("<Button-3>", rightclick)
v = StringVar()
Label(root, textvariable=v, anchor=NW, justify=LEFT, width=config_var['GUI']['width'],
      height=config_var['GUI']['height'], bg=config_var['GUI']['background'], fg=config_var['GUI']['foreground']).pack()
v.set("loading data ...")
root.protocol("WM_DELETE_WINDOW", close)
root.attributes('-alpha', config_var['GUI']['alpha'])
root.wm_attributes("-topmost", 1)
if config_var["GUI"]['borderless'] == "yes":
    root.overrideredirect(1)

Thread(target=outputloop, args=(zoneid, config_var['Settings']['serverlocation'], webapi,
                                config_var['Settings']['unstable_events'], config_var['Settings']['voice'])).start()
mainloop()
