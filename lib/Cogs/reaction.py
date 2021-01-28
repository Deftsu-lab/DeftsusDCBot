from discord.ext.commands import Cog
import discord


class Reaction(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.reaction_message = await self.bot.get_channel(798873634553856021).fetch_message(804277860175970336)
            self.bot.cogs_ready.ready_up("reaction")

    @Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if self.bot.ready and payload.message_id == self.reaction_message.id:
            role = discord.utils.get(self.bot.guild.roles, name= payload.emoji.name)
            await payload.member.add_roles(role)

    @Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        if self.bot.ready and payload.message_id == self.reaction_message.id:
            member = self.bot.guild.get_member(payload.user_id)
            role = discord.utils.get(self.bot.guild.roles, name= payload.emoji.name)
            await member.remove_roles(role)




def setup(bot):
    bot.add_cog(Reaction(bot))
