## Features 

Commands :
* Effortlessly handle "disruptive" members on your server using the simple `kick` and `ban` features for effective moderation control. 
* For the previously mentioned commands, you may optionally include a ***reason*** for why the user was kicked or banned from the server. 

* The bot enables smooth audio playback and queuing of various formats on Discord through the use of FFmpeg integration with `play` and `queue` commands.  
* Control your music easily with commands like `pause`, `resume`, and `stop` from the bot.
* Jump to the next song in the queue using the `skip` command.
* Stay in the know with the `song` command, effortlessly revealing the currently playing track. (one of the coolest feature)
 
* The `queue list` command efficiently presents a comprehensive list of all songs currently in the queue.
* The `queue shuffle` command allows users with the ability to rearrange their queues, adding an element of fun and spontaneity to their playlist management.
* The `queue clear` command enables users to delete all songs from the list, making room for new additions.
* The `queue remove` command enables users to remove any song in queue as long as the user provides the right index number.
	  
* Quickly find songs with minimal information, such as the ***name of the artist*** or a ***keyword*** in the song title.
	  
Events :
  * Sets a welcoming tone in your server with automatic member greetings from the bot upon arrival and departure, offering a friendly atmosphere.
  * Identifies whether there are any users in the voice channel. If no users are detected, the bot will disconnect automatically and clear out the queue.
  * Identifies any profanity in user messages and remove them. To "educate" users on our policy against swearing, a replacement message will be sent.
    
## Demo

[<img src="https://github.com/Dragos20Tech/Discord-Bot/assets/79509739/76830615-a7ad-4d73-959a-2fbb67a30912">](https://discord.com/api/oauth2/authorize?client_id=1161229265308749957&permissions=8&scope=bot)

## Packages
	* `pip install discord.py`
	* `pip install PyNaCl`
	* `pip install ffmpeg`
	* `pip install better-profanity`
  
## Ideas for improvement

  * It would be excellent to program the bot to play tunes using the *spotipy* library.
  * It would be nice if the bot could identify the user who most recently requested it to play a song and *relocate* to that user's channel in case the user switches channels.
  * It would be beneficial if the bot could detect when the song is finished, assuming the queue is empty, and immediately disconnect from the voice channel.
  * It would be great to have a command that loops the current song. `loop`
  * It would be AMAZING to have a user-friendly interface for managing music and server administration tasks.

