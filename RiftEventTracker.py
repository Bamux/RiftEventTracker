# -*- coding: utf-8 -*-

import json
import time
try:
    import requests
except:
    print("Please Install the requests library (pip install requests)")
try:
    import win32com.client
    import win32clipboard
    import pythoncom
except:
    print("Please Install the pywin 32 library (pip install pywin32)")
from threading import Thread
import os
import math
import configparser
from tkinter import *
import codecs
import subprocess

version = "0.9.9"


def read_config(file):
    if os.path.isfile(file):
        try:
            config = configparser.ConfigParser()
            config.read(configfile, encoding="utf-8-sig")
            if int(config['Settings']['volume']) > 100:
                config['Settings']['volume'] = "100"
            elif int(config['Settings']['volume']) < 0:
                config['Settings']['volume'] = "0"
            config['Settings']['lfm'] = config['Settings'].get("lfm", "no")
            config['Settings']['auto_update'] = config['Settings'].get("auto_update", "yes")
            config['Settings']['logfile'] = config['Settings'].get("logfile", "Log.txt")
            config['GUI']['always_on_top'] = config['GUI'].get("always_on_top", "no")
            config['GUI']['fire'] = config['GUI'].get("fire", "red")
            config['GUI']['air'] = config['GUI'].get("air", "deep sky blue")
            config['GUI']['water'] = config['GUI'].get("water", "cornflower blue")
            config['GUI']['earth'] = config['GUI'].get("earth", "peru")
            config['GUI']['life'] = config['GUI'].get("life", "spring green")
            config['GUI']['death'] = config['GUI'].get("death", "medium purple")
            config['GUI']['unstable'] = config['GUI'].get("unstable", "white")
            config['GUI']['lfm'] = config['GUI'].get("lfm", "gold")
        except Exception as e:
            print(e)
            config = write_new_config(configfile)
    else:
        config = write_new_config(configfile)
    return config


def eventnames():
    event = []
    if os.path.isfile("eventnames.txt"):
        event_names = codecs.open("eventnames.txt", 'r', "utf-8")
        for item in event_names:
            item = item.strip()
            item = item.split(", ")
            event += [item]
    return event


def write_new_config(file):
    config = configparser.ConfigParser()
    config['Settings'] = {}
    settings = config['Settings']
    settings['serverlocation'] = 'us'
    settings['language'] = 'eng'
    settings['voice'] = 'yes'
    settings['volume'] = '100'
    settings['unstable_events'] = 'no'
    settings['lfm'] = 'no'
    settings['auto_update'] = 'yes'
    settings['logfile'] = 'Log.txt'
    config['GUI'] = {}
    gui = config['GUI']
    gui['background'] = 'black'
    gui['foreground'] = 'white'
    gui['fire'] = 'red'
    gui['air'] = 'deep sky blue'
    gui['water'] = 'cornflower blue'
    gui['earth'] = 'peru'
    gui['life'] = 'spring green'
    gui['death'] = 'medium purple'
    gui['unstable'] = 'white'
    gui['lfm'] = 'gold'
    gui['alpha'] = '0.7'
    gui['borderless'] = 'no'
    gui['always_on_top'] = 'yes'
    gui['font_size'] = '9'
    gui['x'] = '325'
    gui['y'] = '200'
    gui['width'] = '400'
    gui['height'] = '154'
    expansions = sorted(zones.keys())
    for expansion in expansions:
        sorted_zones = sorted(zones[expansion].items(), key=lambda x: x[1])
        config[expansion] = {}
        for zone_id, zone_all_languages in sorted_zones:
            config[expansion][str(zone_id)] = str(zone_all_languages)
    with open(file, 'w', encoding="utf-8") as file:
        config.write(file)
    return config


def zones_to_track(config):
    zone_id = {}
    for item in config:
        if item != "Settings" and item != "GUI":
            for key, value in config[item].items():
                if ", " in value:
                    value = value.split(",")
                    if config['Settings']['language'] == "ger":
                        zone_id[key] = value[1].strip()
                    elif config['Settings']['language'] == "fr":
                        zone_id[key] = value[2].strip()
                    else:
                        zone_id[key] = value[0].strip()
                else:
                    zone_id[key] = value.strip()
    return zone_id


def get_data(zone_id, serverlocation, url, unstable_events):
    data_output = []
    for shardid in shards[serverlocation]:
        data = json.loads(requests.get(url + str(shardid)).text)['data']
        if data:
            for zone in data:
                if 'started' in zone:
                    condition = True
                    if unstable_events == "no" or unstable_events == "only":
                        if unstable_events == "only":
                            condition = False
                        if 'Unstable' in zone['name'] or 'Instabil' in zone['name'] or 'instable' in zone['name']:
                            if unstable_events == "only":
                                condition = True
                            else:
                                condition = False
                    if condition:
                        for item in zoneid:
                            if item == str(zone['zoneId']):
                                data_output += [[zone['started'], zone_id[item], shards[serverlocation][shardid],
                                                 zone['name']]]
        else:
            data_output += [[0, shards[serverlocation][shardid]]]
    return data_output


def web_api(zone_id, serverlocation, url, unstable_events, voice, first_run, eventlist):
    data_output = get_data(zone_id, serverlocation, url, unstable_events)
    events = []
    if data_output:
        for item in data_output:
            eventexist = False
            events += [[item[0], item[1], item[2], item[3]]]
            for key in eventlist:
                if item[0] == key[0]:
                    eventexist = True
                    break
            if not eventexist:
                if voice == "yes":
                    if not first_run:
                        beginning = "Event in"
                        end = "on"
                        if config_var['Settings']['language'] == 'ger':
                            end = "auf"
                        elif config_var['Settings']['language'] == 'fr':
                            beginning = "Événement en"
                            end = "au"
                        if serverlocation == "prime":
                            text = beginning + " " + item[1]
                        else:
                            text = beginning + " " + item[1] + " " + end + " " + item[2]
                        Thread(target=saytext, args=(text,)).start()
    return events


def show_text(text):
    txt.config(state=NORMAL)
    txt.delete(1.0, END)
    txt.insert('end', text)
    txt.config(state=DISABLED)


def show_text_with_colour(events):
    txt.config(state=NORMAL)
    txt.delete(1.0, END)
    for event in events:
        if "(fire)" in event:
            txt.insert('end', event, 'fire')
        elif "(air)" in event:
            txt.insert('end', event, 'air')
        elif "(life)" in event:
            txt.insert('end', event, 'life')
        elif "(death)" in event:
            txt.insert('end', event, 'death')
        elif "(earth)" in event:
            txt.insert('end', event, 'earth')
        elif "(water)" in event:
            txt.insert('end', event, 'water')
        elif "Unstable" in event:
            txt.insert('end', event, 'unstable')
        elif "LFM" in event:
            txt.insert('end', event, 'lfm')
        else:
            txt.insert('end', event)
    txt.config(state=DISABLED)


def outputloop(zone_id, url, unstable_events, voice, language, zonenames, lfm):
    update()
    show_text("Loading data ...\nIt may take a few seconds to connect to the Web API.\nPlease wait ...")
    logtext = ""
    running_log = False
    lfm_trigger = lfmtrigger()
    data_output = []
    eventlist = []
    old_events = (0, "")
    eventtimestamp = 0
    serverlocation = "log"
    if serverlocation == "log" or lfm != "no":
        guioutput = " Use /log in Rift to start tracking."
        show_text(guioutput)
        logtext = logfilecheck()
        logtext.seek(0, 2)  # jumps to the end of the Log.txt
    while True:
        if serverlocation == "log" or lfm != "no":
            if not logtext:
                logtext = logfilecheck()
            logtext.seek(0, 1)  # reset EOF status on some python versions
            line = logtext.readline()  # read new line
            line = line.strip()
            lfm_zone = ""
            shardname = ""
            timestamp = int(math.floor(time.time()))
            if line:
                low_line = line.lower()
                if "]: " in low_line:
                    low_line = low_line.split("]: ")[1]
                if not running_log:
                    running_log = True
                    show_text(" Logfile found. Search for events started.")
                if lfm != "no":
                    if "lf" in low_line or "looking" in low_line or "/5" in low_line or "/10" \
                            in low_line or "/20" in low_line:
                        found = False
                        for trigger in lfm_trigger:
                            if "," in trigger[1]:
                                triggers = trigger[1].split(",")
                                for item in triggers:
                                    if item.strip() in low_line:
                                        found = True
                                        lfm_zone = trigger[0]
                                        break
                            else:
                                if trigger[1] in low_line:
                                    found = True
                                    lfm_zone = trigger[0]
                                    break
                        if found:
                            found = False
                            try:
                                player_name = line.split("][")[1]
                                player_name = player_name.split("]:")[0]
                                event = [timestamp, lfm_zone + " LFM", player_name]
                                for item in data_output:
                                    if item[2] == player_name and lfm_zone in item[1]:
                                        found = True
                                        break
                                if not found:
                                    data_output += [event]
                                    text = lfm_zone + " looking for more"
                                    Thread(target=saytext, args=(text,)).start()
                                    set_clipboard("/tell " + player_name + " +")
                            except Exception as e:
                                print(e)
                                pass
                if lfm != "only" and serverlocation != "eu" and serverlocation != "us" and line[-1] == "!":
                    if language == "fr":
                        if "serveur " in line:
                            shardname = line.split("serveur ")[1]
                            shardname = shardname.split()[0]
                    elif language == "ger":
                        if " begonnen!" in line and " hat auf " in line:
                            shardname = line.split(" begonnen!")[0]
                            shardname = shardname.split(" hat auf ")[1]
                    else:
                        shardname = line.split()[-1].split("!")[0]
                    for zone in zoneid.values():
                        if "[" + zone + "]" in line:
                            condition = True
                            if unstable_events == "no" or unstable_events == "only":
                                if unstable_events == "only":
                                    condition = False
                                if 'Unstable' in line or 'Instabil' in line or 'instable' in line:
                                    if unstable_events == "only":
                                        condition = True
                                    else:
                                        condition = False
                            if condition:
                                event = line.split("[")[2]
                                event = event.split("]")[0]
                                event = [timestamp, zone, shardname, event]
                                for *_, shardname_data_output, event_data_output in data_output:
                                    if event[3] in event_data_output and event[2] == shardname_data_output:
                                        condition = False
                                if condition:
                                    data_output += [event]
                                    beginning = "Event in"
                                    end = "on"
                                    if config_var['Settings']['language'] == 'ger':
                                        end = "auf"
                                    elif config_var['Settings']['language'] == 'fr':
                                        beginning = "Événement en"
                                        end = "au"
                                    text = beginning + " " + zone + " " + end + " " + shardname
                                    Thread(target=saytext, args=(text,)).start()
                            break
            else:
                if data_output:
                    i = 0
                    for item in data_output:
                        if len(item) == 3:
                            if timestamp - item[0] > 600:
                                del data_output[i]
                        else:
                            if timestamp - item[0] > 3600:
                                del data_output[i]
                        i += 1
                if lfm != "only" and serverlocation != "log" and timestamp - eventtimestamp > 15:
                    eventtimestamp = timestamp
                    try:
                        eventlist = web_api(zone_id, serverlocation, url, unstable_events, voice, language, zonenames)
                    except Exception as e:
                        print(e)
                        show_text(" Web API not available.\n "
                                  "RiftEventTracker switches to logfile mode! Please wait ...")
                        time.sleep(3)
                        serverlocation = "log"
                old_events = lofile_output(serverlocation, data_output, eventlist, zonenames, language,
                                           running_log, old_events)
                time.sleep(1)  # waiting for a new input
        else:
            try:
                eventlist = web_api(zone_id, serverlocation, url, unstable_events, voice, language, zonenames)
                running_log = True
                if eventlist:
                    old_events = lofile_output(serverlocation, data_output, eventlist, zonenames, language,
                                               running_log, old_events)
                else:
                    show_text(" No event running")
                time.sleep(15)
            except Exception as e:
                print(e)
                show_text(" Web API not available.\n RiftEventTracker switches to logfile mode!")
                time.sleep(3)
                serverlocation = "log"
                logtext = logfilecheck()
                logtext.seek(0, 2)  # jumps to the end of the Log.txt


def saytext(text):
    if root and config_var['Settings']['voice'] == "yes":
        try:
            pythoncom.CoInitializeEx(pythoncom.COINIT_MULTITHREADED)
            speak.Speak(text)
        except Exception as e:
            print(e)


def set_clipboard(text):  # add to windows clipboard
    try:
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardText(text)
        win32clipboard.CloseClipboard()
    except Exception as e:
        print(e)


def close():
    file = configfile
    config = ""
    if os.path.isfile(configfile):
        config = configparser.ConfigParser()
        config.read(configfile, encoding="utf-8-sig")
    zones_id = zones_to_track(config)
    config['Settings']['lfm'] = config['Settings'].get("lfm", "no")
    config['Settings']['auto_update'] = config['Settings'].get("auto_update", "yes")
    config['Settings']['logfile'] = config_var['Settings']['logfile']

    config['GUI']['x'] = (str(root.winfo_x()))
    config['GUI']['y'] = (str(root.winfo_y()))
    config['GUI']['width'] = (str(root.winfo_width()))
    config['GUI']['height'] = (str(root.winfo_height()))
    config["GUI"]['borderless'] = borderless
    config['GUI']['always_on_top'] = config_var['GUI']['always_on_top']
    config['GUI']['font_size'] = config['GUI'].get("font_size", "9")

    config['GUI']['fire'] = config['GUI'].get("fire", "red")
    config['GUI']['air'] = config['GUI'].get("air", "deep sky blue")
    config['GUI']['water'] = config['GUI'].get("water", "cornflower blue")
    config['GUI']['earth'] = config['GUI'].get("earth", "peru")
    config['GUI']['life'] = config['GUI'].get("life", "spring green")
    config['GUI']['death'] = config['GUI'].get("death", "medium purple")
    config['GUI']['unstable'] = config['GUI'].get("unstable", "white")
    config['GUI']['lfm'] = config['GUI'].get("lfm", "gold")

    expansions = sorted(zones.keys())
    for expansion in expansions:
        sorted_zones = sorted(zones[expansion].items(), key=lambda x: x[1])
        config[expansion] = {}
        for id_zone, zone_all_languages in sorted_zones:
            zoneexist = False
            for zone_id in zones_id:
                if str(id_zone) == zone_id:
                    zoneexist = True
            if zoneexist:
                config[expansion][str(id_zone)] = str(zone_all_languages)
            else:
                config[expansion][";" + str(id_zone)] = str(zone_all_languages)
    with open(file, 'w', encoding="utf-8") as file:
        config.write(file)
    root.destroy()
    os._exit(1)


def leftclick(event):
    print(event)
    global borderless
    if borderless == "no":
        root.overrideredirect(1)
        borderless = "yes"
    else:
        root.overrideredirect(0)  # Remove border
        borderless = "no"


def rightclick(event):
    print(event)
    time.sleep(0.3)
    close()


def logfilecheck():
    log_exists = False
    log_file = ""
    if os.path.isfile(os.path.expanduser(config_var['Settings']['logfile'])):
        log_file = os.path.expanduser(config_var['Settings']['logfile'])
        log_exists = True
    elif os.path.isfile(os.path.expanduser('~/Documents/RIFT/Log.txt')):
        log_file = os.path.expanduser('~/Documents/RIFT/Log.txt')
        log_exists = True
    elif os.path.isfile('C:/Program Files (x86)/RIFT Game/Log.txt'):
        log_file = 'C:/Program Files (x86)/RIFT Game/Log.txt'
        log_exists = True
    elif os.path.isfile('C:/Programs/RIFT~1/Log.txt'):
        log_file = 'C:/Programs/RIFT~1/Log.txt'
        log_exists = True
    elif os.path.isfile('C:/Documents/RIFT/Log.txt'):
        log_file = 'C:/Documents/RIFT/Log.txt'
        log_exists = True
    elif os.path.isfile('C:/Dokumente/RIFT/Log.txt'):
        log_file = 'C:/Dokumente/RIFT/Log.txt'
        log_exists = True
    if log_exists:
        config_var['Settings']['logfile'] = log_file
        logtext = open(log_file, 'r', encoding="utf-8-sig")
        return logtext
    else:
        guioutput = "Couldn't find the logfile.\nPlease use /log in Rift to create a logfile." \
                    "\nThen restart the Event Tracker."
        show_text(guioutput)
        time.sleep(5)
        logfilecheck()


def lofile_output(serverlocation, data_output, eventlist, zonenames, language, running_log, old_events):
    events = []
    if not running_log:
        events.append("Use /log in Rift to search for lfm.\n"
                      "In the lfm.txt you can specify what you want to search for\n\n")
    data_output = data_output + eventlist
    data_output.sort(reverse=True)
    for item in data_output:
        if serverlocation == "us" or serverlocation == "eu":
            if language == "eng":
                if item[2] == "Brutwacht":
                    for name in zonenames:
                        if name[0] == item[3]:
                            if name[3] != "unknown":
                                element = name[3]
                                item[3] = name[1] + " (" + element + ")"
                            else:
                                item[3] = name[1]
                            break
                elif item[2] == "Brisesol":
                    for name in zonenames:
                        if name[2] == item[3]:
                            if name[3] != "unknown":
                                element = name[3]
                                item[3] = name[1] + " (" + element + ")"
                            else:
                                item[3] = name[1]
                            break
                else:
                    for name in zonenames:
                        if name[1] == item[3]:
                            if name[3] != "unknown":
                                element = name[3]
                                item[3] = name[1] + " (" + element + ")"
                            else:
                                item[3] = name[1]
                            break
            elif language == "ger":
                for name in zonenames:
                    if item[2] == "Brisesol":
                        if name[2] == item[3]:
                            if name[3] != "unknown":
                                element = name[3]
                                item[3] = name[0] + " (" + element + ")"
                            else:
                                item[3] = name[0]
                            break
                    else:
                        if name[1] == item[3]:
                            if name[3] != "unknown":
                                element = name[3]
                                item[3] = name[0] + " (" + element + ")"
                            else:
                                item[3] = name[0]
                            break
            elif language == "fr":
                for name in zonenames:
                    if item[2] == "Brutwacht":
                        if name[0] == item[3]:
                            if name[3] != "unknown":
                                element = name[3]
                                item[3] = name[2] + " (" + element + ")"
                            else:
                                item[3] = name[2]
                            break
                    else:
                        if name[1] == item[3]:
                            if name[3] != "unknown":
                                element = name[3]
                                item[3] = name[2] + " (" + element + ")"
                            else:
                                item[3] = name[2]
                            break
        elif serverlocation == "log":
            if len(item) > 3:
                for name in zonenames:
                    if item[3] in name:
                        if name[3] != "unknown":
                            element = name[3]
                            item[3] += " (" + element + ")"
                            break
        m = int(math.floor((time.time() - item[0]) / 60))
        if m < 0:
            m = 0
        if m < 100:
            m = '{:02}'.format(m)
            if len(item) == 4:
                events.append(" " + m + " m  " + item[1] + " | " + item[2] + " | " + item[3] + '\n')
            else:
                events.append(" " + m + " m  " + item[1] + " | " + item[2] + "\n")
    timestamp = int(math.floor(time.time()))
    if timestamp - old_events[0] >= 1 and old_events[1] != events:
        old_events = timestamp, events
        show_text_with_colour(events)
    return old_events


def lfmtrigger():
    lfm_trigger = []
    if os.path.isfile("lfm.txt"):
        line = codecs.open("lfm.txt", 'r', "utf-8")
        for item in line:
            if "#" not in item and ";" not in item:
                lfm_trigger += [[item.split("=")[0].strip(), item.split("=")[1].strip().lower()]]
    return lfm_trigger


def update():
    if config_var['Settings']['auto_update'] == "yes":
        txt.delete(1.0, END)
        show_text("checking for updates ...\n")
        try:
            if os.path.isfile("_update.exe"):
                if os.path.isfile("update.exe"):
                    os.remove("update.exe")
                os.rename('_update.exe', 'update.exe')
            url = "https://raw.githubusercontent.com/Bamux/RiftEventTracker/master/README.md"
            path = "update.exe"
            latest_version = requests.get(url).text  # => str, not bytes
            latest_version = latest_version.split("## Rift Event Tracker ")[1]
            latest_version = latest_version.split("![Overlay]")[0]
            latest_version = latest_version.strip()
            if version < latest_version:
                print("Old Version: " + version + " New Version: " + latest_version)
                print("Starting update process")
                subprocess.Popen(path, shell=True)
                time.sleep(5)
                os._exit(1)
        except Exception as e:
            print(e)


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
        790513416: 'Ashora, Ashora, Ashora',
        1213399942: "Eastern Holdings, Östliche Besitztümer, Fiefs de l'Orient",
        1770829751: 'Cape Jule, Kap Jul, Cap Yule',
        1967477725: 'City Core, Stadtkern, Cœur de la Cité',
        479431687: 'Kingdom of Pelladane, Königreich Pelladane, Royaume de Pelladane',
        1300766935: 'Kingsward, Königszirkel, Protectorat du Roi',
        956914599: 'Morban, Morban, Morban',
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
        1801: 'Vigil',
    },
}
configfile = "config.ini"
config_var = read_config(configfile)
if config_var['Settings']['serverlocation'] not in ("eu", "prime", "log"):
    config_var['Settings']['serverlocation'] = 'us'
zone_names = eventnames()
try:
    speak = win32com.client.Dispatch('Sapi.SpVoice')
    speak.Volume = int(config_var['Settings']['volume'])
except:
    pass
if config_var['Settings']['serverlocation'] == 'prime':
    webapi = "http://web-api-us" + ".riftgame.com:8080/chatservice/zoneevent/list?shardId="
else:
    webapi = "http://web-api-" + config_var['Settings']['serverlocation'] \
             + ".riftgame.com:8080/chatservice/zoneevent/list?shardId="
zoneid = zones_to_track(config_var)
borderless = config_var["GUI"]['borderless']

# GUI
root = Tk()
root.title("Rift Event Tracker " + version)
root.geometry(config_var['GUI']['width'] + "x" + config_var['GUI']['height'])
root.geometry("+" + config_var['GUI']['x'] + "+" + config_var['GUI']['y'])
root.bind("<Button-1>", leftclick)
# test = root.bind("<Button-3>", rightclick)
txt = Text(root, borderwidth=0, highlightthickness=0, padx=5, font=(None, config_var['GUI']['font_size']),
           width=config_var['GUI']['width'], height=config_var['GUI']['height'], bg=config_var['GUI']['background'],
           fg=config_var['GUI']['foreground'])
txt.pack()
txt.configure(selectbackground=txt.cget('bg'), inactiveselectbackground=txt.cget('bg'))
txt.tag_config('fire', foreground=config_var['GUI']['fire'])
txt.tag_config('air', foreground=config_var['GUI']['air'])
txt.tag_config('water', foreground=config_var['GUI']['water'])
txt.tag_config('earth', foreground=config_var['GUI']['earth'])
txt.tag_config('life', foreground=config_var['GUI']['life'])
txt.tag_config('death', foreground=config_var['GUI']['death'])
txt.tag_config('unstable', foreground=config_var['GUI']['unstable'])
txt.tag_config('lfm', foreground=config_var['GUI']['lfm'])

show_text("loading data ...\n")

root.protocol("WM_DELETE_WINDOW", close)
root.attributes('-alpha', config_var['GUI']['alpha'])
if config_var['GUI']['always_on_top'] == "yes":
    root.wm_attributes("-topmost", 1)
if config_var["GUI"]['borderless'] == "yes":
    root.overrideredirect(1)

Thread(target=outputloop, args=(zoneid, webapi, config_var['Settings']['unstable_events'], config_var['Settings'][
    'voice'], config_var['Settings']['language'], zone_names, config_var['Settings']['lfm'])).start()
mainloop()
