import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
USER_ID = os.getenv("USER_ID")

# Verificação básica para garantir que USER_ID não está nulo
if USER_ID is None:
    raise ValueError("USER_ID não está definido no .env ou nos Secrets!")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot conectado como {bot.user}")
    
    try:
        user = await bot.fetch_user(int(USER_ID))
    except discord.NotFound:
        print(f"Usuário com ID {USER_ID} não encontrado.")
        await bot.close()
        return
    except Exception as e:
        print(f"Erro ao buscar usuário: {e}")
        await bot.close()
        return

    try:
        await user.send("Olá! Aqui está o gráfico atualizado da F1 🏎️")
        with open("web-scraping-f1-python-csv\\data\\pontuacoes_pilotos.png", "rb") as f:
            await user.send(file=discord.File(f))
    except Exception as e:
        print(f"Erro ao enviar mensagem: {e}")

    await bot.close()

bot.run(TOKEN)
