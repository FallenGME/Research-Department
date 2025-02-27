import os
import discord
from discord.ext import commands
from discord import app_commands
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google.oauth2 import service_account

SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

class DocumentHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.Config = bot.config
        self.creds = service_account.Credentials.from_service_account_file("./credentials.json", scopes=SCOPES)
        self.service = build('drive', 'v3', credentials=self.creds)

    @app_commands.command(name="document", description="Download a Google Doc as PDF, convert to PNG, and send via DM.")
    async def get_document(self, interaction: discord.Interaction, name: str):
        await interaction.response.defer(ephemeral=True, thinking=True)
        user = interaction.user

        try:
            doc_url = await self.fetch_document_url_by_name(name)
            if not doc_url:
                await interaction.followup.send(f"Document '{name}' not found.", ephemeral=True)
                return

            doc_id = self.extract_doc_id_from_url(doc_url)
            if not doc_id:
                await interaction.followup.send(f"Invalid document URL for '{name}'.", ephemeral=True)
                return

            pdf_path = f"{name}.pdf"

            request = self.service.files().export_media(fileId=doc_id, mimeType='application/pdf')
            with open(pdf_path, "wb") as fh:
                downloader = MediaIoBaseDownload(fh, request)
                done = False
                while not done:
                    status, done = downloader.next_chunk()

            dm_channel = await user.create_dm()

            with open(pdf_path, 'rb') as pdf_file:
                discord_file = discord.File(pdf_file, filename=f"{name}.pdf")  
                await dm_channel.send(file=discord_file)
            
            os.remove(pdf_path)

            await interaction.followup.send("Document has been sent to your DMs.", ephemeral=True)

        except Exception as e:
            print(f"An error occurred: {e}")
            await interaction.followup.send(f"An error occurred: {e}", ephemeral=True)

    async def fetch_document_url_by_name(self, doc_name: str):
        document_urls = self.Config["Documents"]
        return document_urls.get(doc_name)

    def extract_doc_id_from_url(self, url: str):
        parts = url.split('/')
        return parts[5] if len(parts) > 5 else None

async def setup(bot):
    await bot.add_cog(DocumentHandler(bot))
