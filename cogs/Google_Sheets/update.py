from discord.ext import commands
import discord
import gspread
from discord import app_commands
import asyncio

class Update(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.Database: gspread.client.Client = bot.Database_Points
        self.rank_roles = {
            "Director": [1343641756574416980]  
        }

    async def get_data_from_spreadsheet(self, worksheet):
        user_ids = worksheet.col_values(9)  
        usernames = [name.lower() for name in worksheet.col_values(2)] 
        points = worksheet.col_values(3)  
        ranks = worksheet.col_values(4) 
        return user_ids, usernames, points, ranks

    @app_commands.command(name="update", description="Updates a user's roles based on their rank in the database.")
    async def update(self, interaction: discord.Interaction, member: discord.Member = None):
        await interaction.response.defer(thinking=True, ephemeral=True)
        if not member:
            member = interaction.user

        if member.id == interaction.guild.owner_id:
            embed = discord.Embed(color=discord.Color.red(), title="Uh oh! An error occurred.", description=f'I can\'t update the owner of this guild')
            await interaction.followup.send(embed=embed, ephemeral=True)
            return
        
        
        try:
            spreadsheet = self.Database.open_by_url("https://docs.google.com/spreadsheets/d/1Z8oKqdCDWt_Fz-RnQSDhAJ6cN9O_WOuSc-cM0yxEPQQ/edit?gid=134285913#gid=134285913")
            worksheet = spreadsheet.worksheet("Database")
            
            user_ids, usernames, points, ranks = await self.get_data_from_spreadsheet(worksheet)
            user_id_str = str(member.id)

            if user_id_str in user_ids:
                row_number = user_ids.index(user_id_str) + 1
                if len(ranks) < row_number:
                    embed = discord.Embed(color=discord.Color.red(), title="Error", description=f'Rank data is missing for {member.display_name}.')
                    await interaction.followup.send(embed=embed, ephemeral=True)
                    return

                rank = ranks[row_number - 1]
                role_ids = self.rank_roles.get(rank, [])
                
                if role_ids:
                    roles_to_add = [interaction.guild.get_role(role_id) for role_id in role_ids if interaction.guild.get_role(role_id)]
                    added_roles = []
                    removed_roles = []
                    
                    current_roles = set(member.roles)
                    expected_roles = set(roles_to_add)
                    all_rank_roles = {interaction.guild.get_role(r_id) for ids in self.rank_roles.values() for r_id in ids if interaction.guild.get_role(r_id)}
                    
                    for role in roles_to_add:
                        if role not in member.roles:
                            await member.add_roles(role)
                            added_roles.append(role.name)
                    
                    for role in current_roles & all_rank_roles:
                        if role not in expected_roles:
                            await member.remove_roles(role)
                            removed_roles.append(role.name)
                    
                    embed = discord.Embed(color=discord.Color.green(), title=member.name + " has been updated!")
                    embed.add_field(name="Added Roles", value=", ".join(added_roles) if added_roles else "None", inline=False)
                    embed.add_field(name="Removed Roles", value=", ".join(removed_roles) if removed_roles else "None", inline=False)
                    await interaction.followup.send(embed=embed, ephemeral=True)
                    return
                
                embed = discord.Embed(color=discord.Color.red(), title="Error", description=f'No roles mapped for rank {rank}.')
                await interaction.followup.send(embed=embed, ephemeral=True)
            else:
                embed = discord.Embed(color=discord.Color.red(), title="Error", description=f'UserID {member.id} not found in the database.')
                await interaction.followup.send(embed=embed, ephemeral=True)
                current_roles = set(member.roles)
                all_rank_roles = {interaction.guild.get_role(r_id) for ids in self.rank_roles.values() for r_id in ids if interaction.guild.get_role(r_id)}

                for role in current_roles & all_rank_roles:
                    await member.remove_roles(role)
        except Exception as e:
            embed = discord.Embed(color=discord.Color.red(), title="Error", description=f'An error occurred: {e}')
            await interaction.followup.send(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(Update(bot))
