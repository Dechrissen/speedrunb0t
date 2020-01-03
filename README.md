# speedrunb0t
An always-online bot for Twitch.tv with speedrunner-specific functionality and Speedrun.com API integration.

## Games Currently Supported
*If you'd like me to add support for another game, just message me on Discord [Dechrissen#7708] :-)*
- Banjo-Kazooie
- Banjo-Tooie
- Donkey Kong 64
- Super Mario 64
- Diddy Kong Racing

## Index
1. [What Can speedrunb0t Do?](#what-can-speedrunb0t-do)
2. [Bot Commands](#bot-commands)
3. [How to Invite speedrunb0t to Your Channel](#how-to-invite-speedrunb0t-to-your-channel)
4. [Guidelines for Use](#guidelines-for-use)

## What Can speedrunb0t Do?
- Tell a user the world record for the current game & category, or a specified category
- Tell a user the second, third, or fourth place time for the current game & category, or a specified category
- Tell a user your personal best time for the current game & category
- Tell a user the personal best time of a specified Speedrun.com user for the current game & category, or a specified category
- Tell a user the leaderboard standing of the channel owner for the current game & category
- Tell a user the leaderboard standing of a specified user for the current game & category, or a specified category
- List all of your PBs for the current game, or the PBs of a specified user
- Generate a Speedrun.com link to the leaderboard for the current category
- Generate a kadgar.net race link with you and other speedrunners' Twitch channels 

## Bot Commands
*Square brackets around variables indicate optionality. Angled brackets indicate required variables.*
- `!wr [category]` (everyone)
    - Returns the world record (time and runner) for the current game & category (or, the specified category).
- `!2nd [category]` (everyone)
    - Returns the 2nd place time and runner for the current game & category (or, the specified category).
- `!3rd [category]` (everyone)
    - Returns the third place time and runner for the current game & category (or, the specified category).
- `!4th [category]` (everyone)
    - Returns the fourth place time and runner for the current game & category (or, the specified category).
- `!pb [user] [category]` (everyone)
    - Returns your personal best (or, the personal best of a specified user) for the current game & category (or, the specified category).
- `!place [user] [category]` (everyone)
    - Returns the leaderboard standing of the channel owner for the current category, or the leaderboard standing of the specified user. A different category can also be specified as a third argument.
- `!runs [user]` (everyone)
    - Returns a list of your PBs for the current game (or, the PBs of a specified user).
- `!leaderboard` (everyone)
    - Generates a [Speedrun.com](https://www.speedrun.com/) link to the leaderboard for the game & category specified in your stream title.
- `!race` (everyone)
    - Generates a [Kadgar.net](http://kadgar.net) link with you and your opponents' streams (if you are currently racing).
- `!commands` (everyone)
    - Returns a list of speedrunb0t's commands.
- `!setsrcname <src_username>` (channel owner only)
    - Changes the Speedrun.com username associated with the channel. The associated username defaults to your Twitch username.
- `!help` (everyone)
    - Provides a link to speedrunb0t's GitHub site/documentation.

## How to Invite speedrunb0t to Your Channel
In order to have speedrunb0t join your channel, go to my Twitch channel [here](https://www.twitch.tv/dechrissen) and type `$invite` in the chat. The bot will automatically join your channel, and you won't have to do anything else.

## Guidelines for Use
*Follow these guidelines for speedrunb0t to function properly in your channel.*
- It is recommended that you Mod (or VIP) speedrunb0t in your channel so that it can send the same message multiple times in a row if necessary, and it doesn't accidentally get banned/timed out.
- If your Twitch username is different from your Speedrun.com username, use `!setsrcname <src_username>` to update it in speedrunb0t's registry.
- Make sure the game you're running is set via Twitch's 'game' feature in your Live Dashboard.
- Make sure the name of the category you're running is in your stream title exactly as it's listed on Speedrun.com.
- [Optional] If the platform on which you're playing the game is *different* from the default platform on the Speedrun.com leaderboard, you must put "[*platform name*]" in your title where *platform name* is the name of the platform you're using.
    - *e.g.* If Nintendo 64 is the default platform and you run on Xbox 360, add "[Xbox 360]" somewhere in your stream title
- [Optional] If you're running on emulator, make sure "emulator" is somewhere in your stream title.
- For the `!race` command to work properly, make sure "race with" is somewhere in your stream title, directly followed by the Twitch usernames of your opponents, separated by commas.
    - *e.g.* "Banjo-Tooie Any% race with streamerdude11, twitchboy101, awesomeguy55"
