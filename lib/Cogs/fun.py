from random import choice, randint
from typing import Optional

from discord import Member
from discord.ext.commands import BadArgument
from discord.ext.commands import Cog
from discord.ext.commands import command

class Fun(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name="hallo", aliases=["hi"])
    async def say_hello(self, ctx):
        await ctx.send(f"{choice(('Hallo', 'Grüße', 'Hey', 'Hi', 'Guten Tag', 'Was geht aaaaaaaaab'))} {ctx.author.mention}!")

    @command(name="dice", aliases=["roll"])
    async def roll_the_dice(self, ctx, die_string: str):
        dice, value = (int(term) for term in die_string.split("d"))

        if dice <= 25:
            rolls = [randint(1, value) for i in range(dice)]

            await ctx.send(" + ".join([str(r) for r in rolls]) + f" = {sum(rolls)}")

        else:
            await ctx.send("Wer soll das denn alles werfen? Ein paar weniger würde ich machen!")


    @command(name="slap")
    async def slap_member(self, ctx, member: Member, *, reason:Optional[str] = "einfach so"):
        await ctx.send(f"{ctx.author.mention} hat {member.mention} {reason} geschlagen")

    @slap_member.error
    async def slap_member_error(self, ctx, exc):
        if isinstance(exc, BadArgument):
            await ctx.send("Den kann ich nicht finden. ¯\_(ツ)_/¯")

    @command(name="echo", aliases=["say"])
    async def echo_message(self, ctx, *, message):
        await ctx.message.delete()
        await ctx.send(message)

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("fun")


def setup(bot):
    bot.add_cog(Fun(bot))