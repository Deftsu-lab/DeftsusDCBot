import os
import discord
import datetime
from discord import Intents
from dotenv import load_dotenv
from discord.ext import commands
import time


class Bot(commands.Bot):

    def __init__(self, *args, **kwargs):
        super().__init__(*args,
                         **kwargs,
                         intents=Intents.all(),
                         command_prefix='%')
#Reaction Role
        @Bot.event
        async def on_raw_reaction_add(payload):
            message_id = payload.message_id
            if message_id == 798873790875435019:
                guild_id = payload.guild_id
                guild = discord.utils.find(lambda g : g.id == guild_id, Bot.guilds)

                role = discord.utils.get(guild.roles, name = payload.emoji.name)

                if role is not None:
                    member = discord.utils.find(lambda  m : m.id == payload.user_id, guild.members)
                    if member is not None:
                        await member.add_role(role)
                        print("Done")
                    else:
                        print("Person nicht gefunden.")
                else:
                    print("Rolle nicht gefunden")

        @Bot.event
        async def on_raw_reaction_remove(payload):
            pass

#Hier starten die Commands für den Bot
        @Bot.command(self)
        async def ping(ctx):
            before = time.monotonic()
            ping = (time.monotonic() - before) * 1000
            await ctx.send(f'Pong {int(ping)}ms')


        @Bot.command(self)
        async def channel(ctx):
            for channel in self.guild.channels:
               await ctx.send(channel)

        @Bot.command(self)
        async def members(ctx):
            for member in self.guild.members:
                await ctx.send(member.name)


        @Bot.command(self)
        async def zähle(ctx, *args):
            await ctx.send('{} arguments: {}'.format(len(args), ', '.join(args)))

        @Bot.command(self)
        async def announce(ctx, str):
            ctx.channel = Bot.get_channel(self, id=794908890147717131)
            await ctx.channel.send("@everyone\n Die nächste Runde startet um " + str +" Uhr. Good Luck, Have Fun!")


        #Die Rolle der Nachricht auf die reagiert werden soll
        try:
            # lädt Umgebungsvariablen aus der .env
            load_dotenv()
            self.GUILD = os.getenv('DISCORD_GUILD')
            self.INTERESTED = os.getenv('USER_INTER_ROLE')
            # Pfad für die Logs
            self.LogPath = 'Logs.txt'
            #Pfad für die Rollen Datei
            self.RolePath = 'Roles.txt'
            #Pfad für die Emoji Datei
            self.EmojiPath= 'Emojis.txt'
            #Die ID der Message die beobachtet werden soll
            self.role_message_id = 0
            self.emoji_to_role = {
                #das Emoji "partial_emoji_1" wird mit der Rolle mit der Id 0 verknüpft
                partial_emoji_1: 0,
                # das Emoji "partial_emoji_2" wird mit der Rolle mit der Id 1 verknüpft
                partial_emoji_2: 1,
            }
        except NameError:
            #Öffnet die Datei am angegebenen Pfad
            Log = open(self.LogPath, "a")
            #Nimmt die aktuelle Uhrzeit
            now = datetime.datetime.now()
            #Erstellt den Logeintrag(Uhrzeit + Nutzer + Das Ereignis
            LogEntry = now.strftime('%Y-%m-%d %H:%M:%S') + ' SYSTEM' + ' NameError bei der Initialisierung.'
            #Schreibt den Logeintrag in die Datei und setzt immer einen Zeilenumbruch davor
            Log.write('\n' + LogEntry)
            #Schließt den Log, das Geschriebene wird damit gespeichert
            Log.close()
            return



    async def on_ready(self):
        self.guild = self.get_guild(int(self.GUILD))

        print('Logged on as', self.user)
        print('ID:', str(self.user.id))
        print('Server: ', self.guild.name)
        print('Erstelle Datei mit allen Rollen')
        try:
            Roles = open(self.RolePath, 'w')
            for role in self.guild.roles:
                Roles.write('\n' + role.name + ' ' + str(role.id))
        finally:
            Roles.close()
            print("Erstellung der Datei erfolgreich")
        print('Erstelle Datei mit allen Emojis')
        try:
            Emojis = open(self.EmojiPath, 'w')
            for emoji in self.guild.emojis:
                Emojis.write('\n' + emoji.name + ' ' + str(emoji.id))
        finally:
            Emojis.close()
            print("Erstellung der Datei erfolgreich")


    async def on_member_join(self, member):
        guild = member.guild
        if guild.system_channel is not None:
            WilkommensNachricht = f'Willkommen {member.name} auf dem Turnier Server! Bitte gehe in den Channel Rollenvergabe um deine Rollen zu wählen!'
            Log = open(self.LogPath, "a")
            now = datetime.datetime.now()
            LogEntry = now.strftime("%Y-%m-%d %H:%M:%S") + ' ' + member.name + f'({str(member.id)}' + 'hat den Ping Command genutzt'
            Log.write('\n' + LogEntry)
            Log.close()
            await guild.system_channel.send(WilkommensNachricht)
        return



    async def on_message(self, message):
        # Hier startet die Routine, die Nachrichten Tracken soll
        guild = message.guild

        if guild:
            path = "chatlogs/{}.txt".format(guild.id)
            with open(path, 'a+') as f:
                now = datetime.datetime.now()
                print(now.strftime("%Y-%m-%d %H:%M:%S") + " : {0.author.name} : {0.content}".format(message), file=f)

        #Nicht sich selber antworten, da rekursiv
        if message.author == self.user:
            return

        if message.content == '!ping':
            Log = open(self.LogPath, "a")
            now = datetime.datetime.now()
            LogEntry = now.strftime("%Y-%m-%d %H:%M:%S") + ' ' + message.author.name + f'({str(message.author.id)}) ' + 'hat den Ping Command genutzt'
            Log.write('\n' + LogEntry)
            Log.close()
            await message.channel.send('pong')
            return

        if message.content == '!channel':
            Log = open(self.LogPath, "a")
            now = datetime.datetime.now()
            LogEntry = now.strftime("%Y-%m-%d %H:%M:%S") + ' ' + message.author.name + f'({str(message.author.id)}) ' + 'hat den Channel Command genutzt'
            Log.write('\n' + LogEntry)
            Log.close()
            for channel in self.guild.channels:
                print(channel)

        if message.content == '!interessiert':
            Log = open(self.LogPath, "a")
            now = datetime.datetime.now()
            LogEntry = now.strftime("%Y-%m-%d %H:%M:%S") + ' ' + message.author.name + f'({str(message.author.id)}) ' + 'hat den Interessiert Command genutzt'
            Log.write('\n' + LogEntry)
            Log.close()
            try:
                member = message.author
                await member.add_roles(self.guild.get_role(int(self.INTERESTED)))
            finally:
                print('Hinzufügen des Users erfolgreich')

        await Bot.process_commands(self, message)


