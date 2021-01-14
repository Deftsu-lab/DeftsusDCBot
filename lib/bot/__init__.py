from asyncio import sleep
from datetime import datetime
from glob import glob

from discord import Intents
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from discord import Embed, File
from discord.ext.commands import Bot as BotBase
from discord.ext.commands import CommandNotFound

from ..db import db

PREFIX = ">"
OWNER_IDS = [316985703152091146]
COGS = [path.split("\\")[-1][:-3] for path in glob("./lib/Cogs/*.py")]


class Ready(object):
    def __init__(self):
        for cog in COGS:
            setattr(self, cog, False)

    def ready_up(self, cog):
        setattr(self, cog, True)
        print(f"{cog} cog geladen")

    def all_ready(property):
        return all([getattr(property, cog)for cog in COGS])


class Whisper(BotBase):
    def __init__(self):
        self.PREFIX = PREFIX
        self.ready = False
        self.cogs_ready = Ready()
        self.guild = None
        self.scheduler = AsyncIOScheduler()

        db.autosave(self.scheduler)
        super().__init__(command_prefix=PREFIX,
                         owner_ids=OWNER_IDS,
                         intents=Intents.all())

    def setup(self):
        for cog in COGS:
            self.load_extension(f"lib.Cogs.{cog}")
            print(f"{cog} cog ist geladen")

        print("Setup complete")

    def run(self, version):
        self.VERSION = version

        print("running setup...")
        self.setup()

        with open("./lib/bot/token.0", "r", encoding="utf-8") as tf:
            self.TOKEN = tf.read()

        print("Whisper lädt nach...")
        super().run(self.TOKEN, reconnect = True)

    async def print_message(self):
        await self.stdout.send("HIER KANNST DU DEIN ANNOUNCEMENT JEDE STUNDE REIN TUN")

    async def on_connect(self):
        print("Bot verbunden")

    async def on_disconnect(self):
        print("Verbindung unterbrochen")

    async def on_error(self, err, *args, **kwargs):
        if err == "on_command_error":
            await args[0].send("Das ist ja gestern nicht so gut gelaufen.")

        await self.stdout.send("Da passiert doch was! Nämlich ein Fehler.")
        raise

    async def on_command_error(self, ctx, exc):
        if isinstance(exc, CommandNotFound):
            await ctx.send("Command nicht gefunden")

        elif hasattr(exc, "original"):
            raise exc.original
        else:
            raise exc

    async def on_ready(self):
        if not self.ready:
            self.guild = self.get_guild(794869585224007680)
            self.stdout = self.get_channel(797248019245563924)
            self.scheduler.add_job(self.print_message, CronTrigger(minute=0, second=0))
            self.scheduler.start()

#            await self.stdout.send("Bot online")

#            embed = Embed(title="Whisper geladen(Lmao Wortwitz)", description="Der Bot ist online und bereit",
#                          colour=0xFF0000, timestamp=datetime.utcnow())
#            fields = [("Name", "Value", True),
#                      ("Noch ein Feld", "Dieses Feld ist neben dem Anderem!", True),
#                      ("Ein Feld, dass selbstsüchtig ist", "Dieses Feld hat seine eigene Reihe", False)]
#            for name, value, inline in fields:
#                embed.add_field(name=name, value=value, inline=inline)
#            embed.set_author(name="Nicht Eric sondern Ben", icon_url=self.guild.icon_url)
#            embed.set_footer(text="Das ist eine Fußzeile!")
#            embed.set_thumbnail(url=self.guild.icon_url)
#            embed.set_image(url=self.guild.icon_url)
#            await channel.send(embed=embed)

            while not self.cogs_ready.all_ready():
                await sleep(0.5)

            self.ready = True
            print("Whisper geladen! Lmao wasn Wortwitz")

        else:
            print("Bot verbunden")

    async def on_message(self, message):
        pass


bot = Whisper()



