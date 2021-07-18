#!/usr/bin/python3
#
# A discord bot to read all (with MEE6) played songs since a specific date time
#
import os
import discord
import re
import pytz
from datetime import datetime, timezone
from discord_slash import SlashCommand
from discord_slash.utils.manage_commands import create_option
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()
slash = SlashCommand(client, sync_commands=True)

guild_ids = []

@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break
    guild_ids.append(guild.id)
    print("Ready! "+str(guild.id))

@slash.slash(name="listSongs", description="Prints a list of the played songs in the current channel since the given date time", guild_ids=guild_ids, options=[
    create_option(
        name="date_time",
        description="The date and time when to start with searching through the messages. Format: \"hh:mm dd-MM-yyy\"",
        option_type=3,
        required=True
    )])


async def listSongs(ctx, date_time: str):
    datetimeForBegin = datetime.strptime(date_time, "%H:%M %d-%m-%Y")
    datetimeForBegin.astimezone()
    datetimeForBegin=datetimeForBegin.replace(tzinfo=datetime.utcnow().astimezone(pytz.timezone('Europe/Berlin')).tzinfo)
    datetimeForBegin = datetimeForBegin.astimezone(timezone.utc)
    datetimeForBegin = datetimeForBegin.replace(tzinfo=None)
    songs = await readSongsFromHistory(ctx, datetimeForBegin)
    songs_text = ""
    for song in songs:
        songs_text = songs_text + song + "\n"

    await ctx.send(f'Hey {ctx.author.mention} here you go:\n{songs_text}\n\nYou can create a spotify playlist for them here: https://epsil.github.io/spotgen/')

def checkIsMee6Author(message):
    return message.author.name == "MEE6"

def checkIsSongMessage(message):
    return message.content.startswith( '<:CHECK6:403540120181145611> **' )

def messageToSongName(message):
    # The regex matches all between the first ** and * or an ( without including them
    regexMatch = re.search(r'(?<=\*\*)(.*?)-(.*?)(?=[-*(\[])', message.content)
    if regexMatch:
        return regexMatch.group().strip()
    else:
        return ""

def checkIfNotEmpty(text: str):
    return text

async def readSongsFromHistory(ctx, date_time: datetime):
    return await ctx.channel.history(after=date_time).filter(checkIsMee6Author).filter(checkIsSongMessage).map(messageToSongName).filter(checkIfNotEmpty).flatten()

client.run(TOKEN)