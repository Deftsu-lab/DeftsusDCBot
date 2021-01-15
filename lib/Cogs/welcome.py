from discord.ext.commands import Cog
from discord import Forbidden

from ..db import db


class Welcome(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("welcome")

    @Cog.listener()
    async def on_member_join(self, member):
        db.execute("INSERT INTO exp (UserID) VALUES (?)", member.id)
        await self.bot.get_channel(798550966168191006).send(
            f"Willkommen auf unserem Turnierserver {member.mention}! Bitten begib in <#798873634553856021> um deine Rolle zu bekommen!")

        try:
            await member.send(f"Willkommen auf **{member.guild.name}**! Genieße den Aufenthalt")

        except Forbidden:
            pass

        await member.add_roles(member.guild.get_role(799381512201044018))

    @Cog.listener()
    async def on_member_leave(self, member):
        db.execute("DELETE FROM exp WHERE UserID = ?", member.id)


def setup(bot):
    bot.add_cog(Welcome(bot))
