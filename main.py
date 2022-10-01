import discord, os
from discord.ext import commands

token = open("token","r").read()

def main():
    intents = discord.Intents.default()
    intents.message_content = True

    bot = commands.Bot(command_prefix='r!', intents=intents, help_command=None)

    bot.load_extension("bot")

    @bot.event
    async def on_command_error(ctx, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.send("Unknown command!")

    bot.run(token)

main()