from discord.ext.commands import Cog
import discord


class Rules(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.rule_message = await self.bot.get_channel(804394925307068437).fetch_message(804394943786254346)
            self.bot.cogs_ready.ready_up("rules")

    @Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if self.bot.ready and payload.message_id == self.rule_message.id:
            role = discord.utils.get(self.bot.guild.roles, name=payload.emoji.name)
            await payload.member.add_roles(role)

    @Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        if self.bot.ready and payload.message_id == self.rule_message.id:
            member = self.bot.guild.get_member(payload.user_id)
            role = discord.utils.get(self.bot.guild.roles, name=payload.emoji.name)
            await member.remove_roles(role)


def setup(bot):
    bot.add_cog(Rules(bot))
