import os
import discord
import datetime
from discord import Intents
from dotenv import load_dotenv

class Bot(discord.Client):

    def __init__(self, *args, **kwargs):
        super().__init__(*args,
                         **kwargs,
                         intents=Intents.all())

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


    async def on_raw_reaction_add(self, payload):
        #Stellt sicher dass die Nachricht auf die Reagiert wurde die Nachricht ist, auf die der Bot achten soll
        if payload.message_id != self.role_message_id:
            return

        try:
            role_id = self.emoji_to_role[payload.emoji]
        except KeyError:
            #Wenn der Emoji nicht der ist, auf den wir achten wollen, verlasse die Funktion
            return

        #Nimmt sich die Id des Servers auf dem der Bot im Moment ist
        guild = self.get_guild(payload.guild_id)

        if guild is None:
            #Überprüft ob der Bot auf einem Server ist
            return

        role = guild.get_role(role_id)
        if role is None:
            #Überprüft ob die Rolle noch gültig ist
            return

        try:
            #Gibt Nutzer die Rolle
            await payload.member.add_roles(role)
        except discord.HTTPException:
            #Hier einfügen was im Falle eines Fehlers passieren soll
            pass

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
            WilkommensNachricht = f'Willkommen {member.name} auf dem Turnier Server!'
            Log = open(self.LogPath, "a")
            now = datetime.datetime.now()
            LogEntry = now.strftime("%Y-%m-%d %H:%M:%S") + ' ' + member.name + f'({str(member.id)}' + 'hat den Ping Command genutzt'
            Log.write('\n' + LogEntry)
            Log.close()
            await guild.system_channel.send(WilkommensNachricht)
        return

    async def on_message(self, message):
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

        if message.content == '!members':
            Log = open(self.LogPath, "a")
            now = datetime.datetime.now()
            LogEntry = now.strftime("%Y-%m-%d %H:%M:%S") + ' ' + message.author.name + f'({str(message.author.id)}) ' + 'hat den Member Command genutzt'
            Log.write('\n' + LogEntry)
            Log.close()
            for member in self.guild.members:
                print(member.name)

        if message.content == '!channel':
            Log = open(self.LogPath, "a")
            now = datetime.datetime.now()
            LogEntry = now.strftime("%Y-%m-%d %H:%M:%S") + ' ' + message.author.name + f'({str(message.author.id)}) ' + 'hat den Channel Command genutzt'
            Log.write('\n' + LogEntry)
            Log.close()
            for channel in self.guild.channels:
                print(channel)

        #Funktioniert noch nicht
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