import discord

class Bot(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)

        #Die Rolle der Nachricht auf die reagiert werden soll
        self.role_message_id = 0
        self.emoji_to_role = {
            #das Emoji "partial_emoji_1" wird mit der Rolle mit der Id 0 verknüpft
            partial_emoji_1: 0,
            # das Emoji "partial_emoji_2" wird mit der Rolle mit der Id 1 verknüpft
            partial_emoji_2: 1,
        }

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
        print('Logged on as', self.user)

    async def on_message(self, message):
        #Nicht sich selber antworten, da rekursiv
        if message.author == self.user:
            return

        if message.content == 'ping':
            await message.channel.send('pong')