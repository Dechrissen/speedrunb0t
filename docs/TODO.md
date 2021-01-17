# To-Do List

- [x] `!1st`, `!2nd`, `!3rd` --> `!nth`
- [ ] Add a cache system for certain heavily-used commands (like `!wr`) for faster retrieval
- [ ] Update error messages to be more consistent in wording
- [x] Clean up code and add comments and docstrings where necessary
- [ ] `!part` command: Makes the bot leave a channel at runtime
- [ ] `!stats` command: Display some kind of statistics based on bot usage in each channel
- [x] `!srdiscord` command: Returns the speedrun Discord server link for the current game, if one exists
- [x] `!guides` command: Returns a link to the Speedrun.com guides for the current game
- [x] `!wrvid` command: Returns a link to the video for the world record run
- [ ] `!disable` and `!enable` commands that temporarily disable and re-renable speedrunb0t in a user's channel
- [ ] 'Title converter' function (within getStreamTitle) that converts stream titles to allow for category aliases ('hundo', 'trotless')
- [ ] Create an API system to return usage statistics
- [ ] Fix `!race` command to have a more user-friendly format
- [ ] If an API call takes too long (because Speedrun.com is unstable), make it so the bot tells the user that instead of acting slow
- [ ] Fix `!srdiscord` (if current game is not in game list, it will cause bot to crash)
- [ ] Add BK Category Extensions from SRC (Glitchless, etc.)
- [ ] Fix `!11th` not working (but `!11st` does)

## Possible To-Do

- [ ] Alert in chat when the WR for current game is beaten
- [ ] Channel-specific command on/off switches
- [ ] Set up automatic emails with crash reports
- [ ] `!pbprogression` command: Does some sort of calculation with a user's PBs in a given category over time
- [ ] `!wrdiff` command: Calculates the difference between a user's PB and the WR
- [ ] Challonge.com integration for tournaments (`!bracket`, `!standings`, etc.)
- [ ] Command to tell you the WR at a specific point in time in the past
- [ ] Append run video links to `!wr`, `!pb`, etc.

### Cosmetic To-Do
- [ ] Change speedrunb0t Twitch account username color with Turbo/Prime
- [ ] Create logo
- [ ] Get the Twitch-wide FFZ bot icon for speedrunb0t
