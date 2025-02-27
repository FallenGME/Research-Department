from discord.ext import commands
import discord
import gspread
from discord import app_commands
import datetime

class TestLog(commands.Cog):
    def __init__(self, bot):
        self.bot: discord.Client = bot
        self.Database: gspread.client.Client = bot.Database_Points
        self.Config = bot.config

    @app_commands.command(name="log_test", description="Grants points to an existing user.")
    async def testlog(self, interaction: discord.Interaction, scp_name: str, clipboard_1: discord.Attachment = None, clipboard_2: discord.Attachment = None, clipboard_3: discord.Attachment = None, clipboard_4: discord.Attachment = None, clipboard_5: discord.Attachment = None):
        allowed_extensions = ['jpg', 'jpeg', 'png', 'gif', 'bmp']
        
        clipboards = [clipboard_1, clipboard_2, clipboard_3, clipboard_4, clipboard_5]
        valid_files = []
        invalid_files = []

        for file in clipboards:
            if file and file.filename.split('.')[-1].lower() in allowed_extensions:
                valid_files.append(file)
            elif file:
                invalid_files.append(file.filename)

        if invalid_files:
            await interaction.response.send_message(f"The following files are not valid image types: {', '.join(invalid_files)}", ephemeral=True)
            return

        Embed = discord.Embed()
        Embed.title = scp_name + " Test Log"
        Embed.description = f"User: {interaction.user.name}#{interaction.user.discriminator}\nDate: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

        Guild: discord.Guild = self.bot.get_guild(self.Config["Guild"])
        Channel: discord.TextChannel = Guild.get_channel(self.Config["Test-Log-Channel"])

        await Channel.send(embed=Embed, files=[discord.File(file.fp, filename=file.filename) for file in valid_files])
        await interaction.response.send_message("Successfully logged the test.")

async def setup(bot):
    await bot.add_cog(TestLog(bot))