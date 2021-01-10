
from discord.ext import commands
import main

bot = commands.Bot(command_prefix='.')

@bot.event()
async def on_ready():
    print('Commands geladen!')

@bot.command():
async def ping(ctx):
    await ctx.send(f'Pong! {round(bot.latency *1000)}ms')

@bot.command()
async def zähle(ctx, *args):
    await ctx.send('{} Argumente: {}'.format(len(args), ', '.join(args)))



client.run(main.TOKEN)