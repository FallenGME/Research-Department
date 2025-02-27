from discord.ext import commands
import discord
import gspread
from discord import app_commands
import asyncio

class GrantPoints(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.Database: gspread.client.Client = bot.Database_Points
        self.Config = bot.config

    async def get_data_from_spreadsheet(self, worksheet):
        user_ids = worksheet.col_values(1)  
        usernames = [name.lower() for name in worksheet.col_values(2)] 
        points = worksheet.col_values(3)  
        ranks = worksheet.col_values(4) 
        return user_ids, usernames, points, ranks

    @app_commands.command(name="grant-points", description="Grants points to an existing user.")
    async def grant_points(self, interaction: discord.Interaction, username: str, amount: int):
        await interaction.response.defer(ephemeral=True, thinking=True)

        if not any(interaction.user.roles) in self.Config["CommandPermissions"]["add-points"]:
            embed = discord.Embed(color=discord.Color.red(), title="Error", description=f'You do not have permission to use this command.')
            await interaction.followup.send(embed=embed, ephemeral=True)
            return
        
        try:
            spreadsheet = self.Database.open_by_url("https://docs.google.com/spreadsheets/d/1Z8oKqdCDWt_Fz-RnQSDhAJ6cN9O_WOuSc-cM0yxEPQQ/edit?gid=134285913#gid=134285913")
            worksheet = spreadsheet.worksheet("Database")

            user_ids, usernames, points, ranks = await self.get_data_from_spreadsheet(worksheet)

            user_name_lower = username.lower()

            if user_name_lower in usernames:
                row_number = usernames.index(user_name_lower) + 1

                if not len(points) >= row_number:
                    embed = discord.Embed(color=discord.Color.red(), title="Error", description=f'Points data is missing for {username}.')
                    await interaction.followup.send(embed=embed, ephemeral=True)
                    return
                
                current_points = int(points[row_number - 1])  
                new_points = current_points + amount

                worksheet.update_cell(row_number, 3, new_points)  
                
                embed = discord.Embed(color=discord.Color.green(), title="Success", description=f'{amount} points have been granted to {username}. New total: {new_points} points.')
                await interaction.followup.send(embed=embed, ephemeral=True)

            else:
                embed = discord.Embed(color=discord.Color.red(), title="Error", description=f'User {username} not found in the database. Please add them first.')
                await interaction.followup.send(embed=embed, ephemeral=True)
        
        except Exception as e:
            embed = discord.Embed(color=discord.Color.red(), title="Error", description=f'An error occurred: {e}')
            await interaction.followup.send(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(GrantPoints(bot))
