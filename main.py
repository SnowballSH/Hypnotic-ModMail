import config

import os
from keep_alive import keep_alive
from discord.ext import commands

bot = commands.Bot(
    command_prefix="m!",
    case_insensitive=True
)


@bot.event
async def on_ready():  # When the bot is ready
    print("I'm in")
    print(bot.user)  # Prints the bot's username and identifier


@bot.event
async def on_command_error(ctx, exception):
    if int(os.environ.get('DEBUG')):
        await ctx.send(exception)
    elif isinstance(exception, commands.errors.MissingRequiredArgument):
        await ctx.send(exception)


extensions = [
    'cogs.modmail',
    'jishaku'
]

if __name__ == '__main__':
    for extension in extensions:
        bot.load_extension(extension)

keep_alive()
token = os.environ.get("TOKEN")
bot.run(token)
