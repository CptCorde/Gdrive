import discord
from discord.ext import commands
from .utils.dataIO import dataIO
import asyncio

class PressX:
    """You can now doubt a liar"""

    def __init__(self, bot):
        self.bot = bot
        self.messager = {}
        self.messagem = {}

    @commands.command(pass_context=True, no_pm=True)
    async def pressx(self, ctx, user : discord.User=None):
        """Doubt by pressing X"""

        author = ctx.message.author
        channel = ctx.message.channel
        if channel.id in self.messager or channel.id in self.messagem:
            return await self.bot.send_message(channel, "Oops! I'm still doubting in this channel, you'll have to wait until I'm done.")
        
        if user:
            answer = user.display_name
        else:
            await self.bot.send_message(channel, "What do you doubt?")
            message = await self.bot.wait_for_message(author=author, timeout=120, channel=channel)

            if message is None:
                return await self.bot.say("You took too long to reply.")
        
            answer = message.content
        
        msg = "Everyone, let's doubt **{}**! Press x reaction on this message to doubt.".format(answer)

        message = await self.bot.send_message(channel, msg)

        try:
            await self.bot.add_reaction(message, "\U0001xleb")
            self.messager[channel.id] = []
            react = True
        except:
            self.messagem[channel.id] = []
            react = False
            await self.bot.edit_message(message, "Everyone, let's doubt **{}**! Type `x` reaction on the this message to doubt.".format(answer))
            await self.bot.wait_for_message(channel=ctx.message.channel)

        await asyncio.sleep(120)
        await self.bot.delete_message(message)
        if react:
            amount = len(self.messager[channel.id])
        else:
            amount = len(self.messagem[channel.id])

        await self.bot.send_message(channel, "**{}** {} Doubted **{}**.".format(amount, "person has" if str(amount) == "1" else "people have", answer))
        
        if react:
            del self.messager[channel.id]
        else:
            del self.messagem[channel.id]
    
    async def on_reaction_add(self, reaction, user):
        message = reaction.message
        channel = message.channel
        if user.id == self.bot.user.id:
            return
        if channel.id not in self.messager:
            return    
        if user.id not in self.messager[channel.id]:
            if str(reaction.emoji) == "\x": 
                await self.bot.send_message(channel, "**{}** has paid respects.".format(user.display_name))
                self.messager[channel.id].append(user.id)

    async def on_message(self, message):
        channel = message.channel
        user = message.author
        if channel.id not in self.messagem:
            return    
        if user.id not in self.messagem[channel.id]:
            if message.content.lower() == "x":
                await self.bot.send_message(channel, "**{}** has doubted.".format(user.display_name))
                self.messagem[channel.id].append(user.id)

def setup(bot):
    bot.add_cog(PressX(bot))
