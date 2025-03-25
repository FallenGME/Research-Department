import discord
import os
from discord.ext import commands
import gspread
from config import Return

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

bot.config = Return
bot.Config = bot.config
bot.Database_Points = gspread.service_account(filename="./credentials.json")

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    await load_cogs()
    await bot.change_presence(activity=discord.Game('Managing Site-64.'))

@bot.command(name="sync-tree")
async def sync_tree(ctx):
    await bot.tree.sync()
    await ctx.send("Tree has been synced.")

async def load_cogs():
    for root, _, files in os.walk("./cogs"):
        for filename in files:
            if filename.endswith(".py"):
                relative_path = os.path.relpath(os.path.join(root, filename), ".")
                module_name = relative_path.replace(os.sep, ".")[:-3] 
                try:
                    await bot.load_extension(module_name)
                    print(f"Loaded {module_name}")
                except Exception as e:
                    print(f"Failed to load {module_name}: {e}")

bot.run("PASTE YOUR TOKEN HERE")
