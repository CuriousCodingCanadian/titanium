import discord
from discord import app_commands, Color
import discord.ext
from discord.ext import commands
from discord.ui import View
from datetime import datetime

class user_utils(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    context = discord.app_commands.AppCommandContext(guild=True, dm_channel=True, private_channel=True)
    installs = discord.app_commands.AppInstallationType(guild=True, user=True)
    userGroup = app_commands.Group(name="user", description="User related commands.", allowed_contexts=context, allowed_installs=installs)

    # Server Info command
    @userGroup.command(name = "info", description = "Get info about a user.")
    async def server_info(self, interaction: discord.Interaction, user: discord.User):
        await interaction.response.defer()
        
        try:
            member = interaction.guild.get_member(user.id)

            if member == None:
                member = user
                inGuild = False
            else:
                inGuild = True
        except AttributeError:
            member = user
            inGuild = False
        
        embed = discord.Embed(title = f"User Info", color = Color.random())
        embed.set_author(name=f"{member.display_name} (@{member.name})", icon_url=member.display_avatar.url)

        creationDate = int(member.created_at.timestamp())
        joinDate = (int(member.joined_at.timestamp()) if inGuild else None)
        
        embed.add_field(name = "ID", value = member.id)
        
        # Other info
        embed.add_field(name = "Joined Discord", value = f"<t:{creationDate}:R> (<t:{creationDate}:f>)")
        (embed.add_field(name = "Joined Server", value = f"<t:{joinDate}:R> (<t:{joinDate}:f>)") if inGuild else None)

        if inGuild:
            roles = []
            
            for role in member.roles:
                roles.append(role.mention)
            
            embed.add_field(name = "Roles", value = ", ".join(roles))
        
        embed.set_thumbnail(url = member.display_avatar.url)
        embed.set_footer(text = f"Requested by {interaction.user.name}", icon_url = interaction.user.display_avatar.url)
        
        view = View()
        view.add_item(discord.ui.Button(label="User URL", style=discord.ButtonStyle.url, url=f"https://discord.com/users/{user.id}", row = 0))
        view.add_item(discord.ui.Button(label="Download PFP", style=discord.ButtonStyle.url, url=user.display_avatar.url, row = 0))
        
        # Send Embed
        await interaction.edit_original_response(embed = embed, view = view)

    # PFP command
    @userGroup.command(name = "pfp", description = "Show a user's PFP.")
    @app_commands.allowed_installs(guilds=True, users=True)
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def pfp(self, interaction: discord.Interaction, user: discord.User):
        await interaction.response.defer()
        
        embed = discord.Embed(title = f"PFP - {user.name}", color = (user.accent_color if user.accent_color != None else Color.random()))
        embed.set_image(url = user.display_avatar.url)
        embed.set_footer(text = f"Requested by {interaction.user.name} - right click or long press to save image", icon_url = interaction.user.display_avatar.url)
        
        # Send Embed
        await interaction.followup.send(embed = embed)

async def setup(bot):
    await bot.add_cog(user_utils(bot))