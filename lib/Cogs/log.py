from datetime import datetime

from discord.ext.commands import Cog
from discord.ext.commands import command
from discord import Embed


class Log(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.log_channel =self.bot.get_channel(799390051599122502)
            self.bot.cogs_ready.ready_up("log")

    @Cog.listener()
    async def on_user_update(self, before, after):

        if before.name != after.name:

            embed = Embed(title="Member update",
                          description="neuer Username",
                          colour=after.colour,
                          timestamp=datetime.utcnow())

            fields = [("Vorher", before.name, False),
                      ("After", after.name, False)]

            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)

            await self.log_channel.send(embed=embed)

        if before.discriminator != after.discriminator:

            embed = Embed(title="Member update",
                          description="neuer Discriminator",
                          colour=after.colour,
                          timestamp=datetime.utcnow())

            fields = [("Vorher", before.discriminator, False),
                      ("After", after.discriminator, False)]

            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)

            await self.log_channel.send(embed=embed)

        if before.avatar_url != after.avatar_url:
            embed = Embed(title="Member update",
                          description="neuer Avatar(das Untere ist neu)",
                          colour=self.log_channel.guild.get_member(after.id).colour,
                          timestamp=datetime.utcnow())

            embed.set_thumbnail(url=before.avatar_url)
            embed.set_image(url=after.avatar_url)

            await self.log_channel.send(embed=embed)



    @Cog.listener()
    async def on_member_update(self, before, after):
        if before.display_name is not after.display_name:
            embed = Embed(title="Member update",
                          description="neuer Nickname",
                          colour=after.colour,
                          timestamp= datetime.utcnow())

            fields = [("Vorher", before.display_name, False),
                      ("After", after.display_name, False)]

            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)

            await self.log_channel.send(embed=embed)

        elif before.roles != after.roles:
            embed = Embed(title="Member update",
                          description="neue Rollenvergabe",
                          colour=after.colour,
                          timestamp= datetime.utcnow())

            fields = [("Vorher", ",".join([r.mention for r in before.roles[1:]]), False),
                      ("After", ",".join([r.mention for r in after.roles[1:]]), False)]

            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)

            await self.log_channel.send(embed=embed)




    @Cog.listener()
    async def on_message_edit(self, before, after):
        if not after.author.bot:
            pass


    @Cog.listener()
    async def on_message_delete(self, before, after):
        if not after.author.bot:
            pass


def setup(bot):
    bot.add_cog(Log(bot))
