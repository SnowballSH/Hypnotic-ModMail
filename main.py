from discord.ext import commands
import discord
from keep_alive import keep_alive
import os

from config import run_config

run_config()


bot = commands.Bot(
    command_prefix="m!",
    case_insensitive=True,
    description="Hypnotics Music ModMail Bot"
)


@bot.event
async def on_ready():  # When the bot is ready
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='your DMs!'))
    print("READY,", bot.user)


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
