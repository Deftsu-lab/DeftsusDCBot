from typing import Optional
from datetime import datetime

from discord.ext.commands import Cog, Greedy
from discord.ext.commands import CheckFailure
from discord.ext.commands import command, has_permissions, bot_has_permissions
from discord import Member, Embed

class Mod(Cog):
    def __init__(self, bot):
        self.bot = bot


    @command(name="kick")
    @bot_has_permissions(kick_members=True)
    @has_permissions(kick_members=True)
    async def kick_members(self, ctx, targets: Greedy[Member], *, reason: Optional[str] = "Wahrscheinlich warst n Arsch"):
        if not len(targets):
            await ctx.send("Ein oder mehr benötigte Argumente fehlen")

        else:
            for target in targets:
                await target.kick(reason=reason)

                embed = Embed(title="Member kicked",
                              colour=0xdd2222,
                              timestamp=datetime.utcnow())

                embed.set_thumbnail(url=target.avatar_url)

                fields = [("Member", f"{target.name} a.k.a. {target.display_name}", False),
                          ("Gekickt von", ctx.author.display_name, False),
                          ("Grund", reason, False)]

                for name, value, inline in fields:
                    embed.add_field(name=name, value=value, inline=inline)

                await self.log_channel.send(embed=embed)

    @kick_members.error
    async def kick_members_error(self, ctx, exc):
        if isinstance(exc, CheckFailure):
            await ctx.send("Keine Berechtigung das zu tun")

    @command(name="ban")
    async def ban_members(self, ctx, targets: Greedy[Member]):
        pass


    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("mod")
            self.log_channel = self.bot.get_channel(804376598156673045)

def setup(bot):
    bot.add_cog(Mod(bot))
