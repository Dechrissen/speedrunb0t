# speedrunb0t
An IRC bot for Twitch.tv for speedrunners, with Speedrun.com API integration.

## Index
1. [Currently supported games](#currently-supported-games)
2. [What can speedrunb0t do?](#what-can-speedrunb0t-do)
3. [Bot commands](#bot-commands)
4. [How to invite speedrunb0t to your channel](#how-to-invite-speedrunb0t-to-your-channel)
5. [Guidelines for use](#guidelines-for-use)

## Currently supported games
*If you'd like me to add support for another game, just message me on Discord (Dechrissen#7708)*
- Banjo-Kazooie
- Banjo-Tooie
- Banjo-Kazooie: Grunty's Revenge
- Donkey Kong 64
- Super Mario 64
- Diddy Kong Racing
- Donkey Kong Country
- Donkey Kong Country 2: Diddy's Kong Quest
- Donkey Kong Country 3: Dixie Kong's Double Trouble!

## What can speedrunb0t do?
- Retrieve the world record for the current game & category
- Retrieve your personal best time for the current game & category
- Retrieve the personal best time of a Speedrun.com user for the current game & category
- Retrieve the leaderboard standing of a user for the current game & category
- Retrieve a list of a user's PBs for the current game
- Retrieve the rules for the current category from Speedrun.com
- Generate a Speedrun.com link to the leaderboard for the current category
- Generate a Kadgar.net race link with you and other speedrunners' Twitch channels

## Bot commands
*Square brackets around variables indicate optionality. Angle brackets indicate required variables.*  
*For commands with an optional [user] variable, the user defaults to the channel owner.*  
*For commands with an optional [category] variable, the category defaults to the category in stream title.*
- `!wr [category]`
    - Returns the world record (time and runner) for the current game & category.
- `!nth [category]`
    - Returns the nth place time and runner for the current game & category, where n = place number.
- `!pb [user] [category]`
    - Returns the personal best of a user for the current game & category.
- `!lastpb [user] [category]`
    - Returns the date that a user last PBed in the current category.
- `!place [user] [category]`
    - Returns the leaderboard standing of a user for the current category.
- `!runs [user]`
    - Returns a list of a user's PBs for the current game (all categories).
- `!leaderboard`
    - Generates a [Speedrun.com](https://www.speedrun.com/) link to the leaderboard for the current game & category.
- `!wrvid [category]`
    - Returns the link to the video for the world record run for the current game & category.
- `!rules`
    - Displays the rules for the current category (taken from Speedrun.com).
- `!race`
    - Generates a [Kadgar.net](http://kadgar.net) link with you and your opponents' streams (if you are currently racing).
- `!games`
    - Returns a list of speedrunb0t's currently supported games.
- `!guides`
    - Generates a [Speedrun.com](https://www.speedrun.com/) link to the 'Guides' page for the current game.
- `!srdiscord`
    - Returns the link to the speedrunning Discord server for the current game, if one exists.
- `!help`
    - Provides a link to speedrunb0t's GitHub site/documentation.
- `!commands`
    - Returns a list of speedrunb0t's commands.
- `!setsrcname <src_username>` (channel owner only)
    - Changes the Speedrun.com username associated with the channel. The associated username defaults to your Twitch username.

## How to invite speedrunb0t to your channel
In order to have speedrunb0t join your channel, go to its Twitch channel [here](https://www.twitch.tv/speedrunb0t) and type `$invite` in the chat. The bot will automatically join your channel. If your Speedrun.com username is *different* from your Twitch username, please use the `!setsrcname` command in *your own* chat to change the associated username to your Speedrun.com username.

## Guidelines for use
*Follow these guidelines for speedrunb0t to function properly in your channel.*
- Make sure the game you're running is set via Twitch's 'Game' feature in your Live Dashboard.
- Make sure the name of the category you're running is in your stream title exactly as it's listed on Speedrun.com.
- If the platform on which you're playing the game is *different* from the default platform on the Speedrun.com leaderboard, you must put "[*platform name*]" in your title where *platform name* is the name of the platform you're using.
    - *e.g.* If Nintendo 64 is the default platform and you run on Xbox 360, put "[Xbox 360]" somewhere in your stream title
- If you're running on emulator, make sure "emulator" is somewhere in your stream title.
- For the `!race` command to work properly, make sure "race with" is somewhere in your stream title, directly followed by the Twitch usernames of your opponents, separated by commas.
    - *e.g.* "Banjo-Tooie Any% race with streamerdude11, twitchboy101, awesomeguy55"
- It is recommended that you make speedrunb0t a Moderator in your channel so that it doesn't get accidentally timed out/banned.
