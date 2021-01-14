#Tutorial für Discord Bot Basics

https://realpython.com/how-to-make-a-discord-bot-python/

https://github.com/Rapptz/discord.py

https://discordpy.readthedocs.io/en/latest/api.html#event-reference

#Für Ben, virtual enviroment doku
https://docs.python.org/3/library/venv.html#module-venv

#Reaction Role 
https://www.youtube.com/watch?v=MgCJG8kkq50

@Whisper.event
async def on_raw_reaction_add(payload):
    message_id = payload.message_id
    if message_id == 798873790875435019:
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g: g.id == guild_id, Whisper.guilds)

        role = discord.utils.get(guild.roles, name=payload.emoji.name)

        if role is not None:
            member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)
            if member is not None:
                await member.add_role(role)
                print("Done")
            else:
                print("Person nicht gefunden.")
        else:
            print("Rolle nicht gefunden")


@Whisper.event
async def on_raw_reaction_remove(payload):
    message_id = payload.message_id
    if message_id == 798873790875435019:
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g: g.id == guild_id, Whisper.guilds)

        role = discord.utils.get(guild.roles, name=payload.emoji.name)

        if role is not None:
            member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)
            if member is not None:
                await member.remove_role(role)
                print("Done")
            else:
                print("Person nicht gefunden.")
        else:
            print("Rolle nicht gefunden")
