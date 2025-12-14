import discord
from discord import app_commands
from discord.ext import commands
from storage import Admins, Users, Challenges
import random
import os
from dotenv import load_dotenv
import logging

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

if TOKEN is None:
    raise ValueError("DISCORD_TOKEN environment variable is not set")

LOG_FILE = 'bot.log'

logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

log = logging.getLogger("bot")

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

Owner = os.getenv('OWNER_ID')

if Owner is None:
    raise ValueError("OWNER_ID environment variable is not set")
OWNER_ID = int(Owner)


"""
Get permissions.
"""
def is_owner(user_id: int) -> bool:
    return user_id == OWNER_ID

def is_admin(user_id: int) -> bool:
    return Admins.get(user_id) is not None

"""
Ping Command.
"""

@bot.tree.command(name="ping", description="Tests the bot's response time")
async def ping_command(interaction: discord.Interaction):
    await interaction.response.send_message("Bot is online and synced!")

"""
User Commands.
"""

@bot.tree.command(name="me", description="Shows your user information")
async def me(interaction: discord.Interaction):
    user = Users.get(interaction.user.id)
    if user is None:
        await interaction.response.send_message("You are not registered yet!")
        log.info(f"{interaction.user} is not registered yet!")
    else:
        await interaction.response.send_message(f"Username: {user['username']}, Skill Level: {user['skill_level']}")
        log.info(f"{interaction.user} requested their user information")

@bot.tree.command(name="sign", description="Sign up for the minecraft week")
@app_commands.describe(skill_level = "Skill level 1-5")
async def sign(interaction: discord.Interaction, skill_level : int):
    user = Users.get(interaction.user.id)
    if user is None:
        success, message = Users.add(interaction.user.id, interaction.user.name, skill_level)
        if success:
            await interaction.response.send_message(f"Welcome to the Minecraft Week, {interaction.user.name}!")
            log.info(f"{interaction.user} signed up for the Minecraft Week")
        else:
            await interaction.response.send_message(f"Failed to sign up for the Minecraft Week: {message}")
            log.error(f"Failed to sign up for the Minecraft Week: {message}")
    else:
        await interaction.response.send_message("You are already registered! Use /me for more information.")
        log.info(f"{interaction.user} used /sign when already registered")

@bot.tree.command(name="changeskill", description="Change your skill level")
@app_commands.describe(skill_level = "Skill level 1-5")
async def changeskill(interaction: discord.Interaction, skill_level : int):
    user = Users.get(interaction.user.id)
    if user is None:
        await interaction.response.send_message("You are not registered!")
        log.info(f"{interaction.user} tried to change skill level but is not registered")
    else:
        success, message = Users.update(interaction.user.id, None, skill_level)
        if success:
            await interaction.response.send_message(f"Skill level updated to {skill_level}")
            log.info(f"{interaction.user} changed skill level to {skill_level}")
        else:
            await interaction.response.send_message(f"Failed to update skill level: {message}")
            log.error(f"{interaction.user} failed to update their skill level: {message}")

"""
Admin Commands
"""

@bot.tree.command(name="adduser", description="(Admins only) Add user.")
@app_commands.describe(mention = "Discord user to add", skill_level = "Skill level 1-5")
async def adduser(interaction: discord.Interaction, mention: discord.Member, skill_level : int):
    if not (is_admin(interaction.user.id) or is_owner(interaction.user.id)):
        await interaction.response.send_message("You are not an admin/owner!")
        log.info(f"{interaction.user} tried to add a user but is not an admin/owner")
        return
    success, message = Users.add(mention.id, mention.name, skill_level)
    if success:
        await interaction.response.send_message(f"User {mention.name} with skill level {skill_level} added successfully!")
        log.info(f"{interaction.user} added user {mention.name} with skill level {skill_level}")
    else:
        await interaction.response.send_message(f"Failed to add user: {message}")
        log.info(f"{interaction.user} failed to add user {mention.name}: {message}")

@bot.tree.command(name="deleteuser", description="(Admins only) Delete user.")
@app_commands.describe(mention = "Discord user to delete")
async def deleteuser(interaction: discord.Interaction, mention: discord.Member):
    if not (is_admin(interaction.user.id) or is_owner(interaction.user.id)):
        await interaction.response.send_message("You are not an admin/owner!")
        log.info(f"{interaction.user} tried to delete a user but is not an admin/owner")
        return
    user = Users.get_from_username(mention.name)
    if user is None:
        await interaction.response.send_message(f"User {mention.name} not found!")
        log.info(f"{interaction.user} tried to delete user {mention.name} but it was not found")
        return
    success, message = Users.delete(user["id"])
    if success:
        await interaction.response.send_message(f"User {mention.name} deleted successfully!")
        log.info(f"{interaction.user} deleted user {mention.name} ({mention.id})")
    else:
        await interaction.response.send_message(f"Failed to delete user: {message}")
        log.info(f"{interaction.user} failed to delete user {mention.name}: {message}")

@bot.tree.command(name="listusers", description="(Admins only) List all users.")
async def listusers(interaction: discord.Interaction):
    if not (is_admin(interaction.user.id) or is_owner(interaction.user.id)):
        await interaction.response.send_message("You are not an admin/owner!")
        log.info(f"{interaction.user} tried to list users but is not an admin/owner")
        return
    users = Users.list()
    if not users:
        await interaction.response.send_message("No users found!")
        log.info(f"{interaction.user} listed no users")
    else:
        await interaction.response.send_message(f"Users:\n{', '.join([f'{user['username']} ({user['skill_level']})' for user in users])}")
        log.info(f"{interaction.user} listed users")

"""
Owner Commands
"""

@bot.tree.command(name="addadmin", description="(Owner only) Add admin.")
@app_commands.describe(mention = "Discord username of the admin to add")
async def addadmin(interaction: discord.Interaction, mention : discord.Member):
    if not is_owner(interaction.user.id):
        await interaction.response.send_message("You are not an owner!")
        log.info(f"{interaction.user} tried to add a user but is not an owner")
        return
    success, message = Admins.add(mention.id, mention.name)
    if success:
        await interaction.response.send_message(f"Admin {mention.name} added successfully to the admin list!")
        log.info(f"{interaction.user} added admin {mention.name} to the admin list")
    else:
        await interaction.response.send_message(f"Failed to add admin: {message} to the admin list!")
        log.info(f"{interaction.user} failed to add admin {mention.name} to the admin list! {message}")

@bot.tree.command(name="deleteadmin", description="(Owner only) Delete admin.")
@app_commands.describe(mention = "Discord username of the admin to delete")
async def deleteadmin(interaction: discord.Interaction, mention: discord.Member):
    if not is_owner(interaction.user.id):
        await interaction.response.send_message("You are not the owner!")
        log.info(f"{interaction.user} tried to delete a user but is not the owner")
        return
    admin = Admins.get_from_username(mention.id)
    if admin is None:
        await interaction.response.send_message(f"User {mention.name} not found in the admin list!")
        log.info(f"{interaction.user} tried to delete user {mention.name} from the admin list but it was not found")
        return
    success, message = Admins.delete(admin["id"])
    if success:
        await interaction.response.send_message(f"User {mention.name} deleted successfully from the admin list!")
        log.info(f"{interaction.user} deleted user {mention.name} from the admin list")
    else:
        await interaction.response.send_message(f"Failed to delete user from admin list: {message}")
        log.info(f"{interaction.user} failed to delete user from the admin list: {mention.name}: {message}")

@bot.tree.command(name="listadmins", description="(Owner only) List all admins.")
async def listadmins(interaction: discord.Interaction):
    if not is_owner(interaction.user.id):
        await interaction.response.send_message("You are not the owner!")
        log.info(f"{interaction.user} tried to list admins but is not the owner")
        return
    admins = Admins.list()
    if not admins:
        await interaction.response.send_message("No admins found!")
        log.info(f"{interaction.user} listed no admins")
    else:
        await interaction.response.send_message(f"Users:\n{', '.join([f'{admin['username']} ({admin['skill_level']})' for admin in admins])}")
        log.info(f"{interaction.user} listed users")

@bot.tree.command(name="wipeusers", description="(Owner only) Wipe all user data.")
async def wipeusers(interaction: discord.Interaction):
    if not is_owner(interaction.user.id):
        await interaction.response.send_message("You are not the owner!")
        log.info(f"{interaction.user} tried to wipe users but is not the owner")
        return
    Users.delete_data()
    await interaction.response.send_message("All user data has been wiped!")
    log.info(f"{interaction.user} wiped all user data")

@bot.tree.command(name="wipeadmins", description="(Owner only) Wipe all admin data.")
async def wipeadmins(interaction: discord.Interaction):
    if not is_owner(interaction.user.id):
        await interaction.response.send_message("You are not the owner!")
        log.info(f"{interaction.user} tried to wipe admins but is not the owner")
        return
    Admins.delete_data()
    await interaction.response.send_message("All admin data has been wiped!")
    log.info(f"{interaction.user} wiped all admin data")

@bot.event
async def on_ready():
    synced = await bot.tree.sync()
    print(f"Syncronized {len(synced)} commands globally.")
    log.info(f"Bot is ready. Logged in as {bot.user}")
    print(f"Logged in as {bot.user}")

bot.run(TOKEN)
