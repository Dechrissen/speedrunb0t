import string
import re
import time
import math
import urllib.request
from urllib.request import urlopen
from json import loads
from Socket import openSocket, sendMessage
from Initialize import joinRoom
from Read import getUser, getMessage, getChannel
from Settings import COOLDOWN, IDENT, ADMIN, CLIENT_ID
from Games import GAMES, CATEGORIES, PLATFORMS


def getUserID(username):
    try:
        url = "https://api.twitch.tv/kraken/users?login={}".format(username)
        hdr = {'Client-ID': CLIENT_ID, 'Accept': 'application/vnd.twitchtv.v5+json'}
        req = urllib.request.Request(url, headers=hdr)
        response = urllib.request.urlopen(req)
    except urllib.error.HTTPError as err:
        raise LookupError('User not found')
        return

    readable = response.read().decode('utf-8')
    lst = loads(readable)
    USER_ID = lst['users'][0]['_id']
    return USER_ID

def getStreamTitle(USER_ID):
    try:
        url = "https://api.twitch.tv/kraken/channels/{}".format(USER_ID)
        hdr = {'Client-ID': CLIENT_ID, 'Accept': 'application/vnd.twitchtv.v5+json'}
        req = urllib.request.Request(url, headers=hdr)
        response = urllib.request.urlopen(req)
    except urllib.error.HTTPError as err:
        raise LookupError('User not found')
        return

    readable = response.read().decode('utf-8')
    lst = loads(readable)
    title = lst['status'].lower()
    return title

def getGame(USER_ID):
    try:
        url = "https://api.twitch.tv/kraken/channels/{}".format(USER_ID)
        hdr = {'Client-ID': CLIENT_ID, 'Accept': 'application/vnd.twitchtv.v5+json'}
        req = urllib.request.Request(url, headers=hdr)
        response = urllib.request.urlopen(req)
    except urllib.error.HTTPError as err:
        raise LookupError('User not found')
        return

    readable = response.read().decode('utf-8')
    lst = loads(readable)
    current_game = lst['game']
    if isinstance(current_game, str) == True:
        pass
    else:
        return None, None, None

    for i in range(len(GAMES)):
        if GAMES[i][0].lower() == current_game.lower():
            game = GAMES[i][1]
            platform = GAMES[i][3]
            platform_title = GAMES[i][2]
            return game, platform, platform_title
    return None, None, None


def isEmulator(title):
    if 'emulator' in title:
        return True
    else:
        return False


def joinChannel(input):
    if input == message.lower().strip() and CHANNEL == ADMIN:
        global channel_list
        is_joined = False
        for chan in channel_list:
            chan = chan.split(':')[0]
            if chan == user:
                is_joined = True
                break
        if is_joined == False:
            with open('channels.txt', 'a') as f:
                f.write(user + ":" + user + "\n")
            channel_list.append(user + ":" + user)
            s.send(("JOIN #" + user + "\r\n").encode())
            sendMessage(s, user, "/me has joined.")
            sendMessage(s, CHANNEL, "@" + user + " speedrunb0t has successfully joined your channel.")
            cooldown()
        else:
            sendMessage(s, CHANNEL, "@" + user + " speedrunb0t is already in your channel.")
            cooldown()

def addChannel(input):
    if input == message.lower().split()[0] and user == ADMIN:
        try:
            newChannel = message.lower().split()[1]
        except IndexError as err:
            sendMessage(s, CHANNEL, "Error: Invalid syntax for the !addchannel command. Correct syntax is !addchannel <channel>")
            return

        try:
            message.split()[2]
        except IndexError as err:
            pass
        else:
            sendMessage(s, CHANNEL, "Error: Invalid syntax for the !addchannel command. Correct syntax is !addchannel <channel>")
            return
        global channel_list
        is_joined = False
        for chan in channel_list:
            chan = chan.split(':')[0]
            if chan == newChannel:
                is_joined = True
                break
        if is_joined == False:
            with open('channels.txt', 'a') as f:
                f.write(newChannel + ":" + newChannel + "\n")
            channel_list.append(newChannel + ":" + newChannel)
            s.send(("JOIN #" + newChannel + "\r\n").encode())
            sendMessage(s, newChannel, "/me has joined.")
            sendMessage(s, CHANNEL, "speedrunb0t has successfully joined " + newChannel + "'s channel.")
            cooldown()
            return
        else:
            sendMessage(s, CHANNEL, "speedrunb0t is already in " + newChannel + "'s channel.")
            cooldown()
            return

    elif input == message.lower().split()[0] and user != ADMIN:
        sendMessage(s, CHANNEL, "@" + user + " Only the Administrator may use the !addchannel command.")
        cooldown()
        return


def channels(input):
    if input == message.lower().strip() and user == ADMIN:
        global channel_list
        channels = []
        for chan in channel_list:
            chan = chan.split(':')[0]
            channels.append(chan)
        channels_message = "speedrunb0t is currently being used in the following " + str(len(channels)) + " channels: " + str(channels)
        if len(channels_message) < 500:
            sendMessage(s, CHANNEL, channels_message)
        elif len(channels_message) < 1000:
            sendMessage(s, CHANNEL, channels_message[0:500])
            sendMessage(s, CHANNEL, channels_message[500:])
        else:
            sendMessage(s, CHANNEL, "The list of channels is too long.")
    elif input == message.lower().strip() and user != ADMIN:
        sendMessage(s, CHANNEL, "@" + user + " Only the Administrator may use the !channels command.")
        cooldown()
        return


def setSRCName(input):
    if input == message.lower().split()[0]:
        if user == CHANNEL:
            global channel_list
            try:
                new_srcname = message.lower().split(' ', 1)[1].strip()
            except IndexError as err:
                sendMessage(s, CHANNEL, "Error: Invalid syntax for the !setsrcname command. Correct syntax is !setsrcname <src_username>")
                cooldown()
                return
            if ' ' in new_srcname:
                sendMessage(s, CHANNEL, "Error: New Speedrun.com username must not contain whitespace")
                cooldown()
                return
            new_line = user.lower() + ":" + new_srcname.lower()
            with open("channels.txt", "r+") as f:
                for chan in channel_list:
                    if chan.split(':')[0] == user:
                        channel_list.remove(chan)
                        channel_list.append(new_line)
                        f.truncate(0)
                        f.writelines(channel_list)
                        break
            sendMessage(s, CHANNEL, "The Speedrun.com username associated with this channel has been set to \'" + new_srcname + "\'.")
            cooldown()

        elif user != CHANNEL:
            sendMessage(s, CHANNEL, "@" + user + " Only the channel owner may use the !setsrcname command.")
            cooldown()


#Returns the world record for the category that's written in the stream title
def worldRecord(input):
    if input == message.lower().split()[0].strip():
        #Check to see if an argument is specified first
        argument = False
        try:
            message.lower().split()[1]
        except IndexError as err:
            pass
        else:
            argument = True

        #get user ID of current channel
        try:
            USER_ID = getUserID(CHANNEL)
        except LookupError as err:
            sendMessage(s, CHANNEL, "User not found")
            cooldown()
            return

        #get title of current channel
        title = getStreamTitle(USER_ID)
        if isEmulator(title):
            emulators = 'true'
        else:
            emulators = 'false'
        game, platform, platform_title = getGame(USER_ID)
        if '[' in title and ']' in title:
            for i in range(len(PLATFORMS)):
                if PLATFORMS[i][0].lower() == title.split('[')[1].split(']')[0]:
                    platform = PLATFORMS[i][1]
                    platform_title = PLATFORMS[i][0]
                    break
        category = None
        category_title = None

        #Check again to see if an argument was specified
        if argument == False:
            for i in range(len(CATEGORIES)):
                if CATEGORIES[i][0].lower() in title:
                    category = CATEGORIES[i][1]
                    category_title = CATEGORIES[i][0]
                    break
        elif argument == True:
            specified_category = message.lower().split(input, 1)[-1].strip()
            for i in range(len(CATEGORIES)):
                if specified_category == CATEGORIES[i][0].lower():
                    category_title = CATEGORIES[i][0]
                    category = CATEGORIES[i][1]
                    break
            if category == None:
                sendMessage(s, CHANNEL, "Error: Invalid category specified")
                cooldown()
                return


        if game == None:
            sendMessage(s, CHANNEL, "Error: No game/category info found in stream title")
            cooldown()
            return

        if category != None:
            try:
                response = urlopen('https://www.speedrun.com/api/v1/leaderboards/{}/category/{}?top=1&embed=players&platform={}&emulators={}'.format(game, category, platform, emulators))
            except urllib.error.HTTPError as err:
                sendMessage(s, CHANNEL, "Error: No category \"" + category_title + "\" for the current game")
                cooldown()
                return
            readable = response.read().decode('utf-8')
            lst = loads(readable)
            runner = lst['data']['players']['data'][0]['names']['international']
            time_in_sec = int(lst['data']['runs'][0]['run']['times']['realtime_t'])
            hours = divmod(time_in_sec, 3600)
            minutes = divmod(hours[1], 60)
            seconds = minutes[1]
            wr = ''
            if hours[0] > 0:
                wr = str(hours[0]) + ":" + str(minutes[0]).zfill(2)  + ":" + str(seconds).zfill(2) + " "
            elif minutes[0] > 0:
                wr = str(minutes[0]) + ":" + str(seconds).zfill(2) + " "
            else:
                wr = str(seconds) + " sec "

            sendMessage(s, CHANNEL, "The world record for " + category_title + " is " + wr + "by " + runner + ".")
            cooldown()
            return

        elif category == None:
            sendMessage(s, CHANNEL, "Error: No game/category info found in stream title")
            cooldown()
            return


def second(input):
    if input == message.lower().split()[0].strip():
        #Check to see if an argument is specified first
        argument = False
        try:
            message.lower().split()[1]
        except IndexError as err:
            pass
        else:
            argument = True

        #get user ID of current channel
        try:
            USER_ID = getUserID(CHANNEL)
        except LookupError as err:
            sendMessage(s, CHANNEL, "User not found")
            cooldown()
            return

        #get title of current channel
        title = getStreamTitle(USER_ID)
        if isEmulator(title):
            emulators = 'true'
        else:
            emulators = 'false'
        game, platform, platform_title = getGame(USER_ID)
        if '[' in title and ']' in title:
            for i in range(len(PLATFORMS)):
                if PLATFORMS[i][0].lower() == title.split('[')[1].split(']')[0]:
                    platform = PLATFORMS[i][1]
                    platform_title = PLATFORMS[i][0]
                    break
        category = None
        category_title = None

        #Check again to see if an argument was specified
        if argument == False:
            for i in range(len(CATEGORIES)):
                if CATEGORIES[i][0].lower() in title:
                    category = CATEGORIES[i][1]
                    category_title = CATEGORIES[i][0]
                    break
        elif argument == True:
            specified_category = message.lower().split(input, 1)[-1].strip()
            for i in range(len(CATEGORIES)):
                if specified_category == CATEGORIES[i][0].lower():
                    category_title = CATEGORIES[i][0]
                    category = CATEGORIES[i][1]
                    break
            if category == None:
                sendMessage(s, CHANNEL, "Error: Invalid category specified")
                cooldown()
                return

        if game == None:
            sendMessage(s, CHANNEL, "Error: No game/category info found in stream title")
            cooldown()
            return

        if category != None:
            try:
                response = urlopen('https://www.speedrun.com/api/v1/leaderboards/{}/category/{}?top=2&embed=players&platform={}&emulators={}'.format(game, category, platform, emulators))
            except urllib.error.HTTPError as err:
                sendMessage(s, CHANNEL, "Error: No category \"" + category_title + "\" for the current game")
                cooldown()
                return
            readable = response.read().decode('utf-8')
            lst = loads(readable)
            runner = lst['data']['players']['data'][1]['names']['international']
            time_in_sec = int(lst['data']['runs'][1]['run']['times']['realtime_t'])
            hours = divmod(time_in_sec, 3600)
            minutes = divmod(hours[1], 60)
            seconds = minutes[1]
            place2nd = ''
            if hours[0] > 0:
                place2nd = str(hours[0]) + ":" + str(minutes[0]).zfill(2)  + ":" + str(seconds).zfill(2) + " "
            elif minutes[0] > 0:
                place2nd = str(minutes[0]) + ":" + str(seconds).zfill(2) + " "
            else:
                place2nd = str(seconds) + " sec "

            sendMessage(s, CHANNEL, "The 2nd place time for " + category_title + " is " + place2nd + "by " + runner + ".")
            cooldown()
            return

        elif category == None:
            sendMessage(s, CHANNEL, "Error: No game/category info found in stream title")
            cooldown()
            return


def third(input):
    if input == message.lower().split()[0].strip():
        #Check to see if an argument is specified first
        argument = False
        try:
            message.lower().split()[1]
        except IndexError as err:
            pass
        else:
            argument = True

        #get user ID of current channel
        try:
            USER_ID = getUserID(CHANNEL)
        except LookupError as err:
            sendMessage(s, CHANNEL, "User not found")
            cooldown()
            return

        #get title of current channel
        title = getStreamTitle(USER_ID)
        if isEmulator(title):
            emulators = 'true'
        else:
            emulators = 'false'
        game, platform, platform_title = getGame(USER_ID)
        if '[' in title and ']' in title:
            for i in range(len(PLATFORMS)):
                if PLATFORMS[i][0].lower() == title.split('[')[1].split(']')[0]:
                    platform = PLATFORMS[i][1]
                    platform_title = PLATFORMS[i][0]
                    break
        category = None
        category_title = None

        #Check again to see if an argument was specified
        if argument == False:
            for i in range(len(CATEGORIES)):
                if CATEGORIES[i][0].lower() in title:
                    category = CATEGORIES[i][1]
                    category_title = CATEGORIES[i][0]
                    break
        elif argument == True:
            specified_category = message.lower().split(input, 1)[-1].strip()
            for i in range(len(CATEGORIES)):
                if specified_category == CATEGORIES[i][0].lower():
                    category_title = CATEGORIES[i][0]
                    category = CATEGORIES[i][1]
                    break
            if category == None:
                sendMessage(s, CHANNEL, "Error: Invalid category specified")
                cooldown()
                return

        if game == None:
            sendMessage(s, CHANNEL, "Error: No game/category info found in stream title")
            cooldown()
            return

        if category != None:
            try:
                response = urlopen('https://www.speedrun.com/api/v1/leaderboards/{}/category/{}?top=3&embed=players&platform={}&emulators={}'.format(game, category, platform, emulators))
            except urllib.error.HTTPError as err:
                sendMessage(s, CHANNEL, "Error: No category \"" + category_title + "\" for the current game")
                cooldown()
                return
            readable = response.read().decode('utf-8')
            lst = loads(readable)
            runner = lst['data']['players']['data'][2]['names']['international']
            time_in_sec = int(lst['data']['runs'][2]['run']['times']['realtime_t'])
            hours = divmod(time_in_sec, 3600)
            minutes = divmod(hours[1], 60)
            seconds = minutes[1]
            place3rd = ''
            if hours[0] > 0:
                place3rd = str(hours[0]) + ":" + str(minutes[0]).zfill(2)  + ":" + str(seconds).zfill(2) + " "
            elif minutes[0] > 0:
                place3rd = str(minutes[0]) + ":" + str(seconds).zfill(2) + " "
            else:
                place3rd = str(seconds) + " sec "

            sendMessage(s, CHANNEL, "The 3rd place time for " + category_title + " is " + place3rd + "by " + runner + ".")
            cooldown()
            return

        elif category == None:
            sendMessage(s, CHANNEL, "Error: No game/category info found in stream title")
            cooldown()
            return


def fourth(input):
    if input == message.lower().split()[0].strip():
        #Check to see if an argument is specified first
        argument = False
        try:
            message.lower().split()[1]
        except IndexError as err:
            pass
        else:
            argument = True

        #get user ID of current channel
        try:
            USER_ID = getUserID(CHANNEL)
        except LookupError as err:
            sendMessage(s, CHANNEL, "User not found")
            cooldown()
            return

        #get title of current channel
        title = getStreamTitle(USER_ID)
        if isEmulator(title):
            emulators = 'true'
        else:
            emulators = 'false'
        game, platform, platform_title = getGame(USER_ID)
        if '[' in title and ']' in title:
            for i in range(len(PLATFORMS)):
                if PLATFORMS[i][0].lower() == title.split('[')[1].split(']')[0]:
                    platform = PLATFORMS[i][1]
                    platform_title = PLATFORMS[i][0]
                    break
        category = None
        category_title = None

        #Check again to see if an argument was specified
        if argument == False:
            for i in range(len(CATEGORIES)):
                if CATEGORIES[i][0].lower() in title:
                    category = CATEGORIES[i][1]
                    category_title = CATEGORIES[i][0]
                    break
        elif argument == True:
            specified_category = message.lower().split(input, 1)[-1].strip()
            for i in range(len(CATEGORIES)):
                if specified_category == CATEGORIES[i][0].lower():
                    category_title = CATEGORIES[i][0]
                    category = CATEGORIES[i][1]
                    break
            if category == None:
                sendMessage(s, CHANNEL, "Error: Invalid category specified")
                cooldown()
                return

        if game == None:
            sendMessage(s, CHANNEL, "Error: No game/category info found in stream title")
            cooldown()
            return

        if category != None:
            try:
                response = urlopen('https://www.speedrun.com/api/v1/leaderboards/{}/category/{}?top=4&embed=players&platform={}&emulators={}'.format(game, category, platform, emulators))
            except urllib.error.HTTPError as err:
                sendMessage(s, CHANNEL, "Error: No category \"" + category_title + "\" for the current game")
                cooldown()
                return
            readable = response.read().decode('utf-8')
            lst = loads(readable)
            runner = lst['data']['players']['data'][3]['names']['international']
            time_in_sec = int(lst['data']['runs'][3]['run']['times']['realtime_t'])
            hours = divmod(time_in_sec, 3600)
            minutes = divmod(hours[1], 60)
            seconds = minutes[1]
            place4th = ''
            if hours[0] > 0:
                place4th = str(hours[0]) + ":" + str(minutes[0]).zfill(2)  + ":" + str(seconds).zfill(2) + " "
            elif minutes[0] > 0:
                place4th = str(minutes[0]) + ":" + str(seconds).zfill(2) + " "
            else:
                place4th = str(seconds) + " sec "

            sendMessage(s, CHANNEL, "The 4th place time for " + category_title + " is " + place4th + "by " + runner + ".")
            cooldown()
            return

        elif category == None:
            sendMessage(s, CHANNEL, "Error: No game/category info found in stream title")
            cooldown()
            return


def fifth(input):
    if input == message.lower().split()[0].strip():
        #Check to see if an argument is specified first
        argument = False
        try:
            message.lower().split()[1]
        except IndexError as err:
            pass
        else:
            argument = True

        #get user ID of current channel
        try:
            USER_ID = getUserID(CHANNEL)
        except LookupError as err:
            sendMessage(s, CHANNEL, "User not found")
            cooldown()
            return

        #get title of current channel
        title = getStreamTitle(USER_ID)
        if isEmulator(title):
            emulators = 'true'
        else:
            emulators = 'false'
        game, platform, platform_title = getGame(USER_ID)
        if '[' in title and ']' in title:
            for i in range(len(PLATFORMS)):
                if PLATFORMS[i][0].lower() == title.split('[')[1].split(']')[0]:
                    platform = PLATFORMS[i][1]
                    platform_title = PLATFORMS[i][0]
                    break
        category = None
        category_title = None

        #Check again to see if an argument was specified
        if argument == False:
            for i in range(len(CATEGORIES)):
                if CATEGORIES[i][0].lower() in title:
                    category = CATEGORIES[i][1]
                    category_title = CATEGORIES[i][0]
                    break
        elif argument == True:
            specified_category = message.lower().split(input, 1)[-1].strip()
            for i in range(len(CATEGORIES)):
                if specified_category == CATEGORIES[i][0].lower():
                    category_title = CATEGORIES[i][0]
                    category = CATEGORIES[i][1]
                    break
            if category == None:
                sendMessage(s, CHANNEL, "Error: Invalid category specified")
                cooldown()
                return

        if game == None:
            sendMessage(s, CHANNEL, "Error: No game/category info found in stream title")
            cooldown()
            return

        if category != None:
            try:
                response = urlopen('https://www.speedrun.com/api/v1/leaderboards/{}/category/{}?top=5&embed=players&platform={}&emulators={}'.format(game, category, platform, emulators))
            except urllib.error.HTTPError as err:
                sendMessage(s, CHANNEL, "Error: No category \"" + category_title + "\" for the current game")
                cooldown()
                return
            readable = response.read().decode('utf-8')
            lst = loads(readable)
            runner = lst['data']['players']['data'][4]['names']['international']
            time_in_sec = int(lst['data']['runs'][4]['run']['times']['realtime_t'])
            hours = divmod(time_in_sec, 3600)
            minutes = divmod(hours[1], 60)
            seconds = minutes[1]
            place5th = ''
            if hours[0] > 0:
                place5th = str(hours[0]) + ":" + str(minutes[0]).zfill(2)  + ":" + str(seconds).zfill(2) + " "
            elif minutes[0] > 0:
                place5th = str(minutes[0]) + ":" + str(seconds).zfill(2) + " "
            else:
                place5th = str(seconds) + " sec "

            sendMessage(s, CHANNEL, "The 5th place time for " + category_title + " is " + place5th + "by " + runner + ".")
            cooldown()
            return

        elif category == None:
            sendMessage(s, CHANNEL, "Error: No game/category info found in stream title")
            cooldown()
            return

#Returns the channel owner's personal best time for the category that's written in the stream title
def personalBest(input):
    if input == message.lower().split()[0]:
        SRC_USERNAME = ''
        for i in channel_list:
            if CHANNEL in i:
                SRC_USERNAME = i.split(":")[1].strip('\n')
                break
            else:
                SRC_USERNAME = ADMIN

        category_specified = False
        try:
            message.split()[2]
        except IndexError as err:
            pass
        else:
            category_specified = True

        #get user ID of current channel
        try:
            USER_ID = getUserID(CHANNEL)
        except LookupError as err:
            sendMessage(s, CHANNEL, "User not found")
            cooldown()
            return

        #get title of current channel
        title = getStreamTitle(USER_ID)
        game, platform, platform_title = getGame(USER_ID)
        if '[' in title and ']' in title:
            for i in range(len(PLATFORMS)):
                if PLATFORMS[i][0].lower() == title.split('[')[1].split(']')[0]:
                    platform_title = PLATFORMS[i][0]
                    break

        category_title = None
        if category_specified == True:
            category_title = message.lower().strip('!pb ')
            first_word = category_title.lower().split()[0]
            category_title = category_title.split(first_word, 1)[-1].strip()
            check = False
            for i in range(len(CATEGORIES)):
                if CATEGORIES[i][0].lower() == category_title:
                    check = True
                    category_title = CATEGORIES[i][0]
                    break
            if check == False:
                sendMessage(s, CHANNEL, "Error: Invalid category specified")
                cooldown()
                return

        elif category_specified == False:
            for i in range(len(CATEGORIES)):
                if CATEGORIES[i][0].lower() in title:
                    category_title = CATEGORIES[i][0]
                    break

        if game == None:
            sendMessage(s, CHANNEL, "Error: No game/category info found in stream title")
            cooldown()
            return

        username = None
        try:
            message.split()[1]
        except IndexError as err:
            username = SRC_USERNAME
        else:
            username = message.split()[1]


        if category_title != None:
            try:
                response = urlopen('https://www.speedrun.com/api/v1/users/{}/personal-bests?embed=category,game,platform,players'.format(username))
            except urllib.error.HTTPError as err:
                sendMessage(s, CHANNEL, "Error: Speedrun.com user not found")
                cooldown()
                return

            readable = response.read().decode('utf-8')
            lst = loads(readable)

            try:
                username = lst['data'][0]['players']['data'][0]['names']['international']
            except IndexError as err:
                sendMessage(s, CHANNEL, "Error: User " + username + " has no submitted runs")
                cooldown()
                return

            place = None
            time_in_sec = None
            for cat in lst['data']:
                if cat['category']['data']['name'].lower() == category_title.lower() and cat['game']['data']['abbreviation'].lower() == game and cat['platform']['data']['name'].lower() == platform_title.lower():
                    time_in_sec = int(cat['run']['times']['realtime_t'])
                    place = cat['place']
                    break

            if place == None:
                sendMessage(s, CHANNEL, username + " currently does not have a PB for " + category_title + " on the leaderboard.")
                cooldown()
                return

            ordinal = lambda n: "%d%s" % (n,"tsnrhtdd"[(math.floor(n/10)%10!=1)*(n%10<4)*n%10::4])

            hours = divmod(time_in_sec, 3600)
            minutes = divmod(hours[1], 60)
            seconds = minutes[1]
            pb = ''
            if hours[0] > 0:
                pb = str(hours[0]) + ":" + str(minutes[0]).zfill(2)  + ":" + str(seconds).zfill(2) + " "
            elif minutes[0] > 0:
                pb = str(minutes[0]) + ":" + str(seconds).zfill(2) + " "
            else:
                pb = str(seconds) + " sec "

            sendMessage(s, CHANNEL, username + "\'s " + category_title + " PB is " + pb + " (" + ordinal(place) + " place).")
            cooldown()

        elif category_title == None:
            sendMessage(s, CHANNEL, "Error: No game/category info found in stream title")
            cooldown()
            return

def lastPB(input):
    if input == message.lower().split()[0]:
        SRC_USERNAME = ''
        for i in channel_list:
            if CHANNEL in i:
                SRC_USERNAME = i.split(":")[1].strip('\n')
                break
            else:
                SRC_USERNAME = ADMIN

        category_specified = False
        try:
            message.split()[2]
        except IndexError as err:
            pass
        else:
            category_specified = True

        #get user ID of current channel
        try:
            USER_ID = getUserID(CHANNEL)
        except LookupError as err:
            sendMessage(s, CHANNEL, "User not found")
            cooldown()
            return

        #get title of current channel
        title = getStreamTitle(USER_ID)
        game, platform, platform_title = getGame(USER_ID)
        if '[' in title and ']' in title:
            for i in range(len(PLATFORMS)):
                if PLATFORMS[i][0].lower() == title.split('[')[1].split(']')[0]:
                    platform_title = PLATFORMS[i][0]
                    break

        category_title = None
        if category_specified == True:
            category_title = message.lower().strip('!lastpb ')
            first_word = category_title.lower().split()[0]
            category_title = category_title.split(first_word, 1)[-1].strip()
            check = False
            for i in range(len(CATEGORIES)):
                if CATEGORIES[i][0].lower() == category_title:
                    check = True
                    category_title = CATEGORIES[i][0]
                    break
            if check == False:
                sendMessage(s, CHANNEL, "Error: Invalid category specified")
                cooldown()
                return

        elif category_specified == False:
            for i in range(len(CATEGORIES)):
                if CATEGORIES[i][0].lower() in title:
                    category_title = CATEGORIES[i][0]
                    break

        if game == None:
            sendMessage(s, CHANNEL, "Error: No game/category info found in stream title")
            cooldown()
            return

        username = None
        try:
            message.split()[1]
        except IndexError as err:
            username = SRC_USERNAME
        else:
            username = message.split()[1]


        if category_title != None:
            try:
                response = urlopen('https://www.speedrun.com/api/v1/users/{}/personal-bests?embed=category,game,platform,players'.format(username))
            except urllib.error.HTTPError as err:
                sendMessage(s, CHANNEL, "Error: Speedrun.com user not found")
                cooldown()
                return

            readable = response.read().decode('utf-8')
            lst = loads(readable)

            try:
                username = lst['data'][0]['players']['data'][0]['names']['international']
            except IndexError as err:
                sendMessage(s, CHANNEL, "Error: User " + username + " has no submitted runs")
                cooldown()
                return

            place = None
            time_in_sec = None
            for cat in lst['data']:
                if cat['category']['data']['name'].lower() == category_title.lower() and cat['game']['data']['abbreviation'].lower() == game and cat['platform']['data']['name'].lower() == platform_title.lower():
                    place = cat['place']
                    date = cat['run']['date']
                    break

            if place == None:
                sendMessage(s, CHANNEL, username + " currently does not have a PB for " + category_title + " on the leaderboard.")
                cooldown()
                return

            sendMessage(s, CHANNEL, username + " last PBed in " + category_title + " on " + date + ".")
            cooldown()

        elif category_title == None:
            sendMessage(s, CHANNEL, "Error: No game/category info found in stream title")
            cooldown()
            return

def runs(input):
    if input == message.lower().split()[0]:
        SRC_USERNAME = ''
        for i in channel_list:
            if CHANNEL in i:
                SRC_USERNAME = i.split(":")[1].strip('\n')
                break
            else:
                SRC_USERNAME = ADMIN


        #get user ID of current channel
        try:
            USER_ID = getUserID(CHANNEL)
        except LookupError as err:
            sendMessage(s, CHANNEL, "User not found")
            cooldown()
            return

        #get title of current channel
        title = getStreamTitle(USER_ID)
        game, platform, platform_title = getGame(USER_ID)
        if '[' in title and ']' in title:
            for i in range(len(PLATFORMS)):
                if PLATFORMS[i][0].lower() == title.split('[')[1].split(']')[0]:
                    platform_title = PLATFORMS[i][0]
                    break

        if game == None:
            sendMessage(s, CHANNEL, "Error: No game info found")
            cooldown()
            return

        username = None
        try:
            message.split()[1]
        except IndexError as err:
            username = SRC_USERNAME
        else:
            username = message.split()[1]


        try:
            response = urlopen('https://www.speedrun.com/api/v1/users/{}/personal-bests?embed=game,platform,category,players&game={}'.format(username, game))
        except urllib.error.HTTPError as err:
            sendMessage(s, CHANNEL, "Error: Speedrun.com user not found")
            cooldown()
            return

        readable = response.read().decode('utf-8')
        lst = loads(readable)

        try:
            username = lst['data'][0]['players']['data'][0]['names']['international']
        except IndexError as err:
            pass

        ordinal = lambda n: "%d%s" % (n,"tsnrhtdd"[(math.floor(n/10)%10!=1)*(n%10<4)*n%10::4])
        place = None
        time_in_sec = None
        list_of_runs = []
        if lst['data'] != []:
            pass
        else:
            sendMessage(s, CHANNEL, "User " + username + " has no submitted runs for the current game.")
            cooldown()
            return
        for run in lst['data']:
            #if run['platform']['data']['name'].lower() == platform_title.lower():
            time_in_sec = int(run['run']['times']['realtime_t'])
            place = run['place']
            category_title = run['category']['data']['name']
            hours = divmod(time_in_sec, 3600)
            minutes = divmod(hours[1], 60)
            seconds = minutes[1]
            pb = ''
            if hours[0] > 0:
                pb = str(hours[0]) + ":" + str(minutes[0]).zfill(2)  + ":" + str(seconds).zfill(2)
            elif minutes[0] > 0:
                pb = str(minutes[0]) + ":" + str(seconds).zfill(2)
            else:
                pb = str(seconds) + " sec"
            #add run to the list to be printed
            list_of_runs.append(category_title + " in " + pb + " (" + ordinal(place) + ")")

        game_title = lst['data'][0]['game']['data']['names']['international']
        run_message = username + "\'s " + game_title + " PBs: " + ", ".join(list_of_runs) + "."
        if len(run_message) < 500:
            sendMessage(s, CHANNEL, run_message)
        elif len(run_message) < 1000:
            run_message1 = run_message[0:500]
            run_message2 = run_message[500:]
            sendMessage(s, CHANNEL, run_message1)
            sendMessage(s, CHANNEL, run_message2)
            cooldown()
        else:
            sendMessage(s, CHANNEL, "This user's list of PBs is too long.")
            cooldown()



#Tells user the leaderboard standing of the channel owner, or a specified user
def place(input):
    if input == message.lower().split()[0]:
        SRC_USERNAME = ''
        for i in channel_list:
            if CHANNEL in i:
                SRC_USERNAME = i.split(":")[1].strip('\n')
                break
            else:
                SRC_USERNAME = ADMIN

        category_specified = False
        try:
            message.split()[2]
        except IndexError as err:
            pass
        else:
            category_specified = True

        username = None
        try:
            message.split()[1]
        except IndexError as err:
            username = SRC_USERNAME
        else:
            username = message.split()[1]

        #get user ID of current channel
        try:
            USER_ID = getUserID(CHANNEL)
        except LookupError as err:
            sendMessage(s, CHANNEL, "User not found")
            cooldown()
            return

        #get title of current channel
        title = getStreamTitle(USER_ID)
        game, platform, platform_title = getGame(USER_ID)
        if '[' in title and ']' in title:
            for i in range(len(PLATFORMS)):
                if PLATFORMS[i][0].lower() == title.split('[')[1].split(']')[0]:
                    platform_title = PLATFORMS[i][0]
                    break

        category_title = None
        if category_specified == True:
            category_title = message.lower().strip('!place ')
            first_word = category_title.lower().split()[0]
            category_title = category_title.split(first_word, 1)[-1].strip()
            check = False
            for i in range(len(CATEGORIES)):
                if CATEGORIES[i][0].lower() == category_title:
                    check = True
                    category_title = CATEGORIES[i][0]
                    break
            if check == False:
                sendMessage(s, CHANNEL, "Error: Invalid category specified")
                cooldown()
                return

        elif category_specified == False:
            for i in range(len(CATEGORIES)):
                if CATEGORIES[i][0].lower() in title:
                    category_title = CATEGORIES[i][0]
                    break

        if game == None:
            sendMessage(s, CHANNEL, "Error: No game/category info found in stream title")
            cooldown()
            return


        if category_title != None:
            try:
                response = urlopen('https://www.speedrun.com/api/v1/users/{}/personal-bests?embed=category,game,platform,players'.format(username))
            except urllib.error.HTTPError as err:
                sendMessage(s, CHANNEL, "Error: Speedrun.com user not found")
                cooldown()
                return

            readable = response.read().decode('utf-8')
            lst = loads(readable)

            try:
                username = lst['data'][0]['players']['data'][0]['names']['international']
            except IndexError as err:
                sendMessage(s, CHANNEL, "Error: User " + username + " has no submitted runs")
                cooldown()
                return

            place = None
            time_in_sec = None
            for cat in lst['data']:
                if cat['category']['data']['name'].lower() == category_title.lower() and cat['game']['data']['abbreviation'].lower() == game and cat['platform']['data']['name'].lower() == platform_title.lower():
                    time_in_sec = int(cat['run']['times']['realtime_t'])
                    place = cat['place']
                    break

            if place == None:
                sendMessage(s, CHANNEL, username + " currently does not have a PB for " + category_title + " on the leaderboard.")
                cooldown()
                return

            ordinal = lambda n: "%d%s" % (n,"tsnrhtdd"[(math.floor(n/10)%10!=1)*(n%10<4)*n%10::4])

            sendMessage(s, CHANNEL, username + " is in " + ordinal(place) + " place for " + category_title + ".")

        elif category_title == None:
            sendMessage(s, CHANNEL, "Error: No game/category info found in stream title")
            cooldown()
            return



def leaderboard(input):
    if input == message.lower().strip():
        #get user ID of current channel
        try:
            USER_ID = getUserID(CHANNEL)
        except LookupError as err:
            sendMessage(s, CHANNEL, "User not found")
            cooldown()
            return

        #get title of current channel
        title = getStreamTitle(USER_ID)
        game, platform, platform_title = getGame(USER_ID)
        game_title = None

        for i in range(len(GAMES)):
            if GAMES[i][1] == game:
                game_title = GAMES[i][0]
                break

        category = None
        category_title = None
        for i in range(len(CATEGORIES)):
            if CATEGORIES[i][0].lower() in title:
                category = CATEGORIES[i][1]
                category_title = CATEGORIES[i][0]
                break

        if game == None:
            sendMessage(s, CHANNEL, "Error: No game/category info found in stream title")
            cooldown()
            return

        if category != None:
            sendMessage(s, CHANNEL, game_title + " " + category_title + " Leaderboard: https://www.speedrun.com/{}#{}".format(game, category))
            cooldown()
            return

        elif category == None:
            sendMessage(s, CHANNEL, "Error: No game/category info found in stream title")
            cooldown()
            return

def listRules(input):
    if input == message.lower().strip():
        #get user ID of current channel
        try:
            USER_ID = getUserID(CHANNEL)
        except LookupError as err:
            sendMessage(s, CHANNEL, "User not found")
            cooldown()
            return

        #get title of current channel
        title = getStreamTitle(USER_ID)
        game, platform, platform_title = getGame(USER_ID)
        game_title = None

        for i in range(len(GAMES)):
            if GAMES[i][1] == game:
                game_title = GAMES[i][0]
                break

        category = None
        category_title = None
        for i in range(len(CATEGORIES)):
            if CATEGORIES[i][0].lower() in title:
                category = CATEGORIES[i][1]
                category_title = CATEGORIES[i][0]
                break

        if game == None:
            sendMessage(s, CHANNEL, "Error: No game/category info found in stream title")
            cooldown()
            return

        if category != None:
            try:
                response = urlopen('https://www.speedrun.com/api/v1/games/{}/categories'.format(game))
            except urllib.error.HTTPError as err:
                sendMessage(s, CHANNEL, "HTTP Error")
                cooldown()
                return

            readable = response.read().decode('utf-8')
            lst = loads(readable)

            list_of_rules = "Not found"
            rules = ' '

            for cat in lst['data']:
                if cat['name'].lower() == category_title.lower():
                    rules = cat['rules'].split('\r\n')
                    for rule in rules:
                        rule = rule.strip('-')
                    list_of_rules = ' '.join(rules)

            if len(list_of_rules) < 475:
                sendMessage(s, CHANNEL, game_title + " " + category_title + " rules: " + list_of_rules)
            elif len(list_of_rules) < 1000:
                list_of_rules1 = list_of_rules[0:475]
                list_of_rules2 = list_of_rules[475:]
                sendMessage(s, CHANNEL, game_title + " " + category_title + " rules: " + list_of_rules1)
                sendMessage(s, CHANNEL, list_of_rules2)
            else:
                sendMessage(s, CHANNEL, "Whoops! This games's list of rules is too long.")

            cooldown()
            return

        elif category == None:
            sendMessage(s, CHANNEL, "Error: No game/category info found in stream title")
            cooldown()
            return


def listGames(input):
    if input == message.lower().strip():
        sendMessage(s, CHANNEL, "Games currently supported: " + ", ".join([game[0] for game in GAMES]))
        cooldown()
        return


#Returns a kadgar.net link with the channel owner and the other racers if a race is happening
def raceCommand(input):
    if input == message.lower().strip():
        #get user ID of current channel
        try:
            USER_ID = getUserID(CHANNEL)
        except LookupError as err:
            sendMessage(s, CHANNEL, "User not found")
            cooldown()
            return

        #get title of current channel
        title = getStreamTitle(USER_ID)

        if 'race with' in title:
            pass
        elif 'race with' not in title:
            sendMessage(s, CHANNEL, CHANNEL + " is not currently racing or no racers found in stream title.")
            cooldown()
            return

        title_list = title.split()
        r = title_list.index('with') + 1
        contenders = []
        length = len(title_list)
        diff = length - r
        while True:
            contenders.append(title_list[r].strip(','))
            diff = diff - 1
            r = r + 1
            if diff == 0:
                break
        sendMessage(s, CHANNEL, "Race link: http://kadgar.net/live/" + CHANNEL + "/" + "/".join(contenders))
        cooldown()



#Displays commands
def getCommands(input):
    if input == message.strip().lower():
        sendMessage(s, CHANNEL, '/me commands: !wr • !2nd • !3rd • !4th • !5th • !pb • !lastpb • !runs • !place • !leaderboard • !rules • !race • !games • !help')
        cooldown()

#Documentation
def docs(input):
    if input == message.lower().strip():
        sendMessage(s, CHANNEL, "speedrunb0t's documentation can be found here: https://dechrissen.github.io/speedrunb0t")
        cooldown()


#Global cooldown
def cooldown():
    if user == ADMIN or user == CHANNEL:
        pass
    elif user:
        abort_after = COOLDOWN
        start = time.time()
        while True:
            delta = time.time() - start
            if delta >= abort_after:
                break


#Checks if a message is from Twitch or a user
def Console(line):
    if "PRIVMSG" in line:
        return False
    else:
        return True


#Quits the bot program (admin only)
def quitCommand(input):
    if input == message.strip().lower() and user == ADMIN:
        sendMessage(s, ADMIN, "/me has disconnected.")
        #for chan in channel_list:
            #chan = chan.split(":")[0]
            #if chan != ADMIN:
                #sendMessage(s, chan, "/me [Disconnected]")
        quit()
    elif input == message.strip():
        sendMessage(s, CHANNEL, "@" + user + " Only the Administrator may use the !kill command.")
        cooldown()





s = openSocket()
joinRoom(s)
readbuffer = ""

with open("channels.txt", "r") as f:
    channel_list = f.readlines()

for chan in channel_list:
    chan = chan.split(":")[0]
    if chan != ADMIN:
        s.send(("JOIN #" + chan + "\r\n").encode())
        #sendMessage(s, chan, "/me [Connected]")

while True:

    readbuffer = s.recv(1024)
    readbuffer = readbuffer.decode()
    temp = readbuffer.split("\n")
    readbuffer = readbuffer.encode()
    readbuffer = temp.pop()

    for line in temp:
        try:
            print(line)
        except OSError as err:
            print('OSError: Invalid symbol')
            continue
        if "PING" in line and Console(line):
            msgg = "PONG tmi.twitch.tv\r\n".encode()
            s.send(msgg)
            print(msgg)
            break
        if ".tmi.twitch.tv" in line and Console(line):
            break
        user = getUser(line)
        message = getMessage(line)
        CHANNEL = getChannel(line)
        if '!' not in message and '$' not in message:
            continue
        print(user + " said: " + message)

        #Chat commands
        getCommands('!commands')
        worldRecord('!wr')
        worldRecord('!1st')
        second('!2nd')
        third('!3rd')
        fourth('!4th')
        fifth('!5th')
        personalBest('!pb')
        lastPB('!lastpb')
        runs('!runs')
        place('!place')
        leaderboard('!leaderboard')
        listRules('!rules')
        listGames('!games')
        raceCommand('!race')
        setSRCName('!setsrcname')
        docs('!help')
        joinChannel('$invite')
        addChannel('!addchannel')
        channels('!channels')
        quitCommand('!kill')
        continue
