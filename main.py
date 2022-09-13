import discord, os
from discord.ext import commands

token = open("token","r").read()

def main():
    intents = discord.Intents.default()
    intents.message_content = True

    bot = commands.Bot(command_prefix='r!', intents=intents, help_command=None)

    bot.run(token)

    return 0

main()