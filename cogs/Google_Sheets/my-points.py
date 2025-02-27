from discord.ext import commands
import discord
import gspread
from discord import app_commands
import asyncio

class MyPoints(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.Database: gspread.client.Client = bot.Database_Points
    async def get_data_from_spreadsheet(self, worksheet):
        user_ids = worksheet.col_values(1)  
        usernames = [name.lower() for name in worksheet.col_values(2)] 
        points = worksheet.col_values(3)  
        ranks = worksheet.col_values(4) 
        return user_ids, usernames, points, ranks

    @app_commands.command(name="view-points", description="Displays the points and rank of a user.")
    async def view_points(self, interaction: discord.Interaction, username: str):
        await interaction.response.defer(thinking=True, ephemeral=True)
        try:
            username1 = str.lower(username)
            spreadsheet = self.Database.open_by_url("https://docs.google.com/spreadsheets/d/1Z8oKqdCDWt_Fz-RnQSDhAJ6cN9O_WOuSc-cM0yxEPQQ/edit?gid=134285913#gid=134285913")
            worksheet = spreadsheet.worksheet("Database")

            user_ids, usernames, points, ranks = await self.get_data_from_spreadsheet(worksheet)

            if username1 in usernames:
                row_number = usernames.index(username1) + 1

                if not len(points) >= row_number:
                    embed = discord.Embed(color=discord.Color.red(), title="Error", description=f'Points data is missing for {username}.')
                    await interaction.followup.send(embed=embed, ephemeral=True)
                    return
                if not len(ranks) >= row_number:
                    embed = discord.Embed(color=discord.Color.red(), title="Error", description=f'Rank data is missing for {username}.')
                    await interaction.followup.send(embed=embed, ephemeral=True)
                    return
                
                embed = discord.Embed(color=discord.Color.from_str("#18d1db"))
                embed.title = f"{username}´s Information"
                embed.add_field(name="Points", value=points[row_number - 1], inline=False)
                embed.add_field(name="Rank", value=ranks[row_number - 1], inline=False)
                await interaction.followup.send(embed=embed, ephemeral=True)
            else:
                embed = discord.Embed(color=discord.Color.red(), title="Error", description=f'Username {username} not found.')
                await interaction.followup.send(embed=embed, ephemeral=True)
        except Exception as e:
            embed = discord.Embed(color=discord.Color.red(), title="Error", description=f'An error occurred: {e}')
            await interaction.followup.send(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(MyPoints(bot))
