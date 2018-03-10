## Rift Event Tracker 0.4
![Overlay](https://cdn.discordapp.com/attachments/374932500910309379/422081814950313984/unknown.png)

Download latest Version: https://github.com/Bamux/RiftEventTracker/archive/master.zip

Features:
- Text to Speach announcement of events (zone and server)
- Overlay display of running events

## Instructions:
- If you want to use the overlay display you have to run Rift in the Fullscreen Windowed Mode
![Rift Settings](https://cdn.discordapp.com/attachments/374932500910309379/422085099841126400/unknown.png)
I programmed an event tracker that uses the web api of Trion, which has the advantage that you don't need a logfile and you don't have to be in the game to use it.<br><br>
It is still a prototype, so there is no user interface yet. The configuration of the program is done via the config. ini here you can also deactivate/activate the zones to be tracked. To deactivate a zone, simply place a # sign at the beginning of the line or delete the line.<br><br>The event announcements are currently made via Text to Speach (zone and server), but in the future I want to insert an overlay window with all necessary information via the DirectX interface.<br><br>
config.ini:<br><br>
[Settings]<br>
serverlocation = eu (eu or na)<br>
volume = 50 (0-100)<br>
unstable_events = yes (yes or no)<br>

[Zone]<br># ZonID = Zonename (this line is a example how you deaktivate a zone)
