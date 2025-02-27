from discord.ext import commands
import discord
import gspread
from discord import app_commands
import asyncio
import datetime

class TestLog(commands.Cog):
    def __init__(self, bot):
        self.bot: discord.Client = bot
        self.Database: gspread.client.Client = bot.Database_Points
        self.Config = bot.config

    @app_commands.command(name="log-test", description="Grants points to an existing user.")
    async def testlog(self, interaction: discord.Interaction, SCP: str, Clipboard: discord.Attachment):
        allowed_extensions = ['jpg', 'jpeg', 'png', 'gif', 'bmp']
        
        if len(Clipboard) > 5:
            await interaction.response.send_message("You can only attach up to 5 images.", ephemeral=True)
            return

        invalid_files = []
        valid_files = []

        for file in Clipboard:
            if file.filename.split('.')[-1].lower() in allowed_extensions:
                valid_files.append(file)
            else:
                invalid_files.append(file.filename)

        if invalid_files:
            await interaction.response.send_message(f"The following files are not valid image types: {', '.join(invalid_files)}", ephemeral=True)
            return

        Embed = discord.Embed()
        Embed.title = SCP + " Test Log"
        Embed.description = f"User: {interaction.user.name}#{interaction.user.discriminator}\nDate: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

        Guild: discord.Guild = self.bot.get_guild(self.Config["Guild"])
        Channel: discord.TextChannel = Guild.get_channel(self.Config["Test-Log-Channel"])

        await Channel.send(embed=Embed, files=[discord.File(file.fp, filename=file.filename) for file in valid_files])
        await interaction.response.send_message("Successfully logged the test.")

async def setup(bot):
    await bot.add_cog(TestLog(bot))
