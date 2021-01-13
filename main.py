# Importiert die Library für die Standard OS Funktionen
import os
# Importiert die Library für den Discord Client
import discord
# Importiert die die commands Funktionen aus discord.ext
from discord.ext import commands
# Importiert die load_dotenv() Funktion aus dem dotenv Package
from dotenv import load_dotenv
import Client

# lädt Umgebungsvariablen aus der .env
load_dotenv()
# Der Bot Token der den Bot für die Discord Server verifiziert
TOKEN = os.getenv('DISCORD_TOKEN')
# Der Server Token der die App für unseren Discord verifiziert
GUILD = os.getenv('DISCORD_GUILD')

def main():
    try:
        # lädt Umgebungsvariablen aus der .env
        load_dotenv()
        # Der Bot Token der den Bot für die Discord Server verifiziert
        TOKEN = os.getenv('DISCORD_TOKEN')
        # Der Server Token der die App für unseren Discord verifiziert
        GUILD = os.getenv('DISCORD_GUILD')

    finally:
        print("Laden der Umgebungsvariablen erfolgreich")
        client = Client.Whisper()
        client.run(TOKEN)

if __name__ == "__main__":
    main()



