import discord
from discord.ext import commands, tasks
from discord import app_commands
import asyncio
import pandas as pd
import os
from itertools import cycle

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

DATA_FILE = 'Banco de Dados.xlsx'

status = cycle([
    'Qualquer dúvida, fale com um dos nossos administradores',
    '/login para se cadastrar'
])

# ---------------- UTILS ---------------- #

def load_data():
    if not os.path.exists(DATA_FILE):
        return pd.DataFrame()
    return pd.read_excel(DATA_FILE)

def save_data(df):
    df.to_excel(DATA_FILE, index=False)

def is_yes(msg):
    return msg.lower() in ['sim', 's', 'yes', 'y']

# ---------------- EVENTS ---------------- #

@bot.event
async def on_ready():
    await bot.tree.sync()
    change_status.start()
    print(f'Logado como {bot.user}')

@tasks.loop(seconds=15)
async def change_status():
    await bot.change_presence(activity=discord.Game(next(status)))

# ---------------- LOGIN ---------------- #

@bot.tree.command(name="login", description="Cadastrar no sistema acadêmico")
async def login(interaction: discord.Interaction):

    await interaction.response.send_message(
        "📩 Vou te chamar no privado para continuar!",
        ephemeral=True
    )

    user = interaction.user

    # tenta abrir DM
    try:
        await user.send("Digite seu nome completo (com acentos):")
    except discord.Forbidden:
        return await interaction.followup.send(
            "❌ Não consegui te mandar DM. Ative mensagens privadas.",
            ephemeral=True
        )

    def check(m):
        return m.author == user and isinstance(m.channel, discord.DMChannel)

    # recebe nome
    try:
        msg = await bot.wait_for("message", check=check, timeout=60)
    except asyncio.TimeoutError:
        return await user.send("⏰ Tempo expirado.")

    nome = msg.content.upper()

    if nome.isnumeric():
        return await user.send("❌ Nome inválido.")

    df = load_data()

    try:
        index = df.loc[df["NOME COMPLETO"] == nome].index.item()
    except ValueError:
        return await user.send("❌ Nome não encontrado no banco de dados.")

    aluno = df.loc[index]

    # confirmação
    await user.send(
        f"Você confirma?\n\n"
        f"**{aluno['NOME COMPLETO']}**\n"
        f"{aluno['CURSO']}\n"
        f"Matrícula: {aluno['MATRICULA']}\n\n"
        f"(Sim/Não)"
    )

    try:
        confirm = await bot.wait_for("message", check=check, timeout=60)
    except asyncio.TimeoutError:
        return await user.send("⏰ Tempo expirado.")

    if not is_yes(confirm.content):
        return await user.send("❌ Cadastro cancelado.")

    if aluno["DISCORD"] != 0:
        return await user.send("⚠️ Esse aluno já está cadastrado.")

    # salva ID
    df.loc[index, "DISCORD"] = user.id
    save_data(df)

    # roles (no servidor)
    guild = interaction.guild
    member = guild.get_member(user.id)

    role_ok = discord.utils.get(guild.roles, name='Estudante')
    role_not = discord.utils.get(guild.roles, name='Não Registrado')

    if member:
        await member.add_roles(role_ok)
        await member.remove_roles(role_not)

    # log
    log_channel = guild.get_channel('ID_DO_CANAL_DE_LOGS - sem as aspas')

    embed = discord.Embed(
        title='Novo Aluno Adicionado',
        description=f"{aluno['NOME COMPLETO']} <=> {member.mention}",
        color=0x00FF00
    )

    await log_channel.send(embed=embed)

    await user.send("✅ Cadastro realizado com sucesso!")

# ---------------- REGISTRAR (ADMIN) ---------------- #

@bot.tree.command(name="registrar", description="Registrar aluno manualmente")
@app_commands.describe(
    membro="Usuário do Discord",
    nome="Nome completo do aluno"
)
async def registrar(interaction: discord.Interaction, membro: discord.Member, nome: str):

    if not any(role.name == "NOME_DO_CARGO" for role in interaction.user.roles):
        return await interaction.response.send_message(
            "❌ Você não tem permissão.",
            ephemeral=True
        )

    df = load_data()
    nome = nome.upper()

    try:
        index = df.loc[df["NOME COMPLETO"] == nome].index.item()
    except ValueError:
        return await interaction.response.send_message(
            "❌ Nome não encontrado.",
            ephemeral=True
        )

    aluno = df.loc[index]

    await interaction.response.send_message(
        f"Confirmar registro?\n\n{aluno['NOME COMPLETO']} → {membro.mention}",
        ephemeral=True
    )

    df.loc[index, "DISCORD"] = membro.id
    save_data(df)

    role_ok = discord.utils.get(interaction.guild.roles, name='NOME_REGISTRADO')
    role_not = discord.utils.get(interaction.guild.roles, name='NOME_NAO_REGISTRADO')

    await membro.add_roles(role_ok)
    await membro.remove_roles(role_not)

# ---------------- PURGE ---------------- #

@bot.tree.command(name="limpar", description="Apagar mensagens")
@app_commands.describe(quantidade="Quantidade de mensagens")
async def limpar(interaction: discord.Interaction, quantidade: int):

    if not any(role.name == "Date" for role in interaction.user.roles):
        return await interaction.response.send_message(
            "❌ Sem permissão.",
            ephemeral=True
        )

    await interaction.channel.purge(limit=quantidade)

    await interaction.response.send_message(
        f"🧹 {quantidade} mensagens apagadas.",
        ephemeral=True
    )

# ---------------- RUN ---------------- #

with open("token.txt", "r") as f:
    TOKEN = f.read().strip()

bot.run(TOKEN)