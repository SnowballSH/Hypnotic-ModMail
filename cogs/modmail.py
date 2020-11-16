from replit import db
import discord
import os
from discord.ext import commands

from config import STAFF_ID


def is_staff(): return commands.check(
    lambda ctx: ctx.message.author.id in STAFF_ID)


class ModMailCommands(commands.Cog, name='ModMail Commands'):
    '''These are the modmail commands'''

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener("on_message")
    async def on_message(self, message):
        if not isinstance(message.channel, discord.DMChannel) or message.author.id == self.bot.user.id:
            return

        channel = self.bot.get_channel(int(os.environ.get("MAIL_CHANNEL")))

        if not channel:
            print("Mail channel not found! Reconfigure bot!")

        content = message.clean_content

        embed = discord.Embed(title="New modmail!")
        embed.add_field(name="Author", value=f"{message.author.mention} ({message.author.name}) ({message.author.id})",
                        inline=False)

        embed.add_field(name="Message", value=content[:1000] or "blank")
        if message.attachments:
            embed.add_field(name="Attachments", value=", ".join(
                [i.url for i in message.attachments]))

        if len(content[1000:]) > 0:
            embed.add_field(name="Message (continued):", value=content[1000:])

        await channel.send(embed=embed)

        try:
            await message.add_reaction('📬')
        except discord.ext.commands.errors.CommandInvokeError:
            await message.channel.send('📬')

        db["last"] = message.author.id

    @commands.command(name="resolve", aliases=['res', 'end'])
    @is_staff
    async def resolve(self, ctx):
        if db["last"] is None:
            await ctx.send("No current sessions!")
            return

        user = self.bot.get_user(db["last"])
        db["last"] = None

        await user.send(f'Your session has been marked as resolved by {ctx.author.mention}. Thank you for using the modmail!')
        await ctx.send(f'Session marked as resolved by {ctx.author.mention}.')

    @commands.command(name="start", aliases=['st', 'ss'])
    @is_staff
    async def start(self, ctx, user: discord.User):
        db["last"] = user.id

        await user.send(f'A modmail session started by {ctx.author.mention}. Have fun!')
        await ctx.send(f'Session started with **{user.display_name}** by {ctx.author.mention}.')

    @commands.command(name="dm")
    @is_staff
    async def dm(self, ctx, user: discord.User, *, msg):
        if ctx.channel.id != int(os.environ.get("MAIL_CHANNEL")):
            return
        if 1:
            await user.send(f"From {ctx.author.mention}: {msg}")
        else:
            await user.send(msg)
        await ctx.message.add_reaction('📬')

    @commands.command(name="reply", aliases=['r'])
    @is_staff
    async def reply(self, ctx, *, msg):
        if db["last"] is None:
            await ctx.send("No user to reply to!")
            return

        user = self.bot.get_user(db["last"])
        await self.dm.callback(self, ctx, user=user, msg=msg)


def setup(bot):
    bot.add_cog(ModMailCommands(bot))
