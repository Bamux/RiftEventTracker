## Rift Event Tracker 0.4
![Overlay](https://cdn.discordapp.com/attachments/374932500910309379/422081814950313984/unknown.png)

Download latest Version: https://github.com/Bamux/RiftEventTracker/archive/master.zip

Features:
- Text to Speach announcement of events (zone and server)
- Overlay display of running events

## Instructions:
- start RiftEventTracker.exe
- with left mouse click on the Rift Event Tracker window you can start/end the borderless modus
- with right mouse click you close the the Rift Event Tracker window
- if you want to use the overlay display in Rift you have to run Rift in the Fullscreen Windowed Mode
![Rift Settings](https://cdn.discordapp.com/attachments/374932500910309379/422085099841126400/unknown.png)

## Configuration:
- the configuration of the program is done via the config. ini here you can deactivate/activate the zones to be tracked and change the interface layout
- to deactivate a zone, simply place a # sign at the beginning of the line or delete the line.

config.ini:<br>
  [Settings]<br>
  serverlocation = eu (eu or na)<br>
  voice = yes (yes or no)<br>
  volume = 100 (0-100)<br>
  unstable_events = yes (yes or no)<br>

  [Zone]<br># ZonID = Zonename ;(this line is a example how you deaktivate a zone)
