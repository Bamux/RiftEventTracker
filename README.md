## Rift Event Tracker 0.7.5
![Overlay](https://cdn.discordapp.com/attachments/374932500910309379/422081814950313984/unknown.png)

Download latest Version: https://github.com/Bamux/RiftEventTracker/archive/master.zip

Features:
- text to speach announcement of events (zone and server) and lfm raids/experts
- overlay display of running events and lfm raids/experts
- with strg + v you can quickly answer a player who is looking for other players with lfm

## Instructions:
- start RiftEventTracker.exe
- with left mouse click on the Rift Event Tracker window you can start/end the borderless modus
- with right mouse click you can close the window
- if you want to use the overlay display in Rift you have to use Rift in the Fullscreen Windowed Mode

![Rift Settings](https://cdn.discordapp.com/attachments/374932500910309379/422085099841126400/unknown.png)

## Configuration:
- after the first start a configuration file is created in the same folder
- the configuration of the program is done via the config. ini here you can deactivate/activate the zones to be tracked and change the interface layout
- to deactivate a zone, simply place ; at the beginning of the line or delete the line

  [Settings]<br>
  serverlocation = eu, us or prime<br>
  language = eng , ger or fr<br>
  voice = yes or no<br>
  volume = 0-100<br>
  unstable_events = yes, no or only<br>
  lfm = yes, no or only (shows if someone is looking for a group, see also lfm.txt)<br>
  auto_update = yes or no (if you want the program to keep itself up to date use yes)
  
## Add Raids, Experts or other activities to be displayed
- change in the config.ini following setting: lfm = yes
- add new raids, experts or other activities to lfm.txt
- Raidname = Keyword most searched for e.g. Bastion of Steal = BoS
- to deactivate a raid, simply place ; or # at the beginning of the line

  
## Change your Text to Speech voice
- Open the Windows Text to Speech Engine. Default folder is C:\Windows\SysWOW64\Speech\SpeechUX\sapi.cpl
- Choose a voice that you like

![Voice Settings](https://raw.githubusercontent.com/Bamux/Rift-Raid-Alert/images/Text%20to%20Speach.png)

- Under http://www.mwsreader.com/en/voices/ you can download other voices (different languages).
