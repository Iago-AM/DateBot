'''
DATE

Author: Iago Monte
'''

import discord
from discord.ext import commands, tasks
from discord.utils import get
import asyncio
from itertools import cycle
import pandas as pd

bot = commands.Bot(command_prefix = '!', intents = discord.Intents.all())
status = cycle(['Qualquer dúvida, fale com um dos nossos administradores', '!login para se cadastrar'])
df = pd.read_excel('Banco de Dados.xlsx')

@bot.event
async def on_ready():
    change_status.start()
    print("Estou pronto!")


@tasks.loop(seconds=10)
async def change_status():
    await bot.change_presence(activity=discord.Game(next(status)))


# @bot.command(aliases=['login', 'matricula', 'registrar', 'registro'])
@bot.command()
async def login(ctx):
    await ctx.channel.purge(limit=20)
    await ctx.author.send("Digite seu nome completo (incluindo acentos): ")
    
    try:
        message = await bot.wait_for("message", check=lambda m: m.author == ctx.author, timeout=60.0)

    except asyncio.TimeoutError:
        await ctx.author.send("Tempo limite expirado! Tente novamente")

    else:
        if message.content.isnumeric() == True:
            await ctx.author.send("Seu nome não está correto!")

        if message.content.isnumeric() == False:
            nomecompleto = message.content
            nomecompleto = nomecompleto.upper()
            await ctx.author.send("Estamos verificando sua matrícula, não digite nada até que a operação seja concluída...")
            try:
                index = df.loc[df["NOME COMPLETO"] == nomecompleto].index.item()
                nome = df.loc[index, "NOME COMPLETO"]
                curso = df.loc[index, "CURSO"]
                matricula = df.loc[index, "MATRICULA"]
                
                try:
                    await ctx.author.send(f'Você confirma que é: {nome}, aluno(a) de: {curso}, sob a matrícula: {matricula}? (Sim/Não)')

                    try:
                        message = await bot.wait_for("message", check=lambda m: m.author == ctx.author, timeout=60.0)
                        message.content = message.content.lower()

                        if message.content == "sim" or message.content == "s":
                            if df.loc[index, "DISCORD"] == 0:
                                await ctx.author.send('Cadastro realizado, agora você pode usar o DateDiscord normalmente!')
                                df.loc[index, "DISCORD"] = message.author.id
                                channel = bot.get_channel(1024815448820297798)
                                role = discord.utils.get(ctx.author.guild.roles, name='Estudante')
                                await ctx.author.add_roles(role)
                                role = discord.utils.get(ctx.author.guild.roles, name='Não Registrado')
                                await ctx.author.remove_roles(role)
                                iddiscord = ctx.author.id
                                #await channel.send(f'{nome} < ADICIONADO A > <@{iddiscord}>')
                                embed = discord.Embed(
                                    description= f'{nome} < ADICIONADO A > <@{iddiscord}>',
                                    colour=0x00FF00,
                                )
                                embed.set_footer(text='Adicionado a ' + ctx.author.name, icon_url=ctx.author.avatar.url)

                                await channel.send(embed=embed)
                                df.to_excel('Banco de Dados.xlsx', index=False)

                            else:
                                await ctx.author.send('Opa! Parece que alguém já está usando esse usuário. Caso você pense que houve algum engano, contate um de nossos administradores.')
                    
                        else:
                            await ctx.author.send('Não? Sugiro que tente novamente ou contate um de nossos administradores!')        

                    except asyncio.TimeoutError:
                        await ctx.author.send("Tempo limite expirado! Tente novamente")       
                
                except asyncio.TimeoutError:
                    await ctx.author.send("Tempo limite expirado! Tente novamente")
            
            except:
                await ctx.author.send('Parece que não encontramos seu nome no banco de dados. Tente adicionar/remover acentos, ou contate um de nossos administradores')



@bot.command(aliases=['remover', 'delete', 'del'])
@commands.has_role("Date")
async def remove(ctx, member: discord.Member, *, message):
    nomecompleto = message.upper()

    try:
        index = df.loc[df["NOME COMPLETO"] == nomecompleto].index.item()

    except:
        await ctx.reply('Nome incorreto, tente adicionar/remover os acentos ou busque no banco de dados!')

    else:
        nome = df.loc[index, "NOME COMPLETO"]
        curso = df.loc[index, "CURSO"]
        matricula = df.loc[index, "MATRICULA"]
        await ctx.send(f'Você deseja remover o link de: {nome} ({matricula} - {curso}) com o perfil {member.mention}? Essa operação é irreversível (Sim/Não)')

        try:
            message = await bot.wait_for("message", check=lambda m: m.author == ctx.author, timeout=60.0)
            message.content = message.content.lower()

            if message.content == "sim" or message.content == "s":
                if df.loc[index, "DISCORD"] != 0:
                    df.loc[index, "DISCORD"] = 0
                    await member.edit(roles=[])
                    role = discord.utils.get(member.guild.roles, name='Não Registrado')
                    await member.add_roles(role)
                    await ctx.send(f'Operação realizada com sucesso! {nome} perdeu seu acesso ao servidor')
                    iddiscord = member.id
                    channel = bot.get_channel(1024815448820297798)
                    #await channel.send(f'{nome} < REMOVIDO DE > <@{iddiscord}>')

                    embed = discord.Embed(
                        description= f'{nome} < REMOVIDO DE > <@{iddiscord}>',
                        colour=0xFF0000,
                    )
                    embed.set_footer(text='Removido por ' + ctx.author.name, icon_url=ctx.author.avatar.url)

                    await channel.send(embed=embed)
                    df.to_excel('Banco de Dados.xlsx', index=False)

                else:
                    await ctx.send(f'Parece que {nome} não tem nenhuma Discord ID associada a ele.')
                    
            else:
                await ctx.send('Operação cancelada!')

        except asyncio.TimeoutError:
            await ctx.send('Tempo expirado!')


@bot.command(aliases=['cadastrar', 'add', 'register', 'registro', 'cadastro'])
@commands.has_role("Date")
async def registrar(ctx, member: discord.Member, *, message):
    nomecompleto = message.upper()
    
    try:
        index = df.loc[df["NOME COMPLETO"] == nomecompleto].index.item()

    except:
        await ctx.reply('Nome incorreto, tente adicionar/remover os acentos ou busque no banco de dados!')

    else:
        nome = df.loc[index, "NOME COMPLETO"]
        curso = df.loc[index, "CURSO"]
        matricula = df.loc[index, "MATRICULA"]
        await ctx.send(f'Você deseja registrar: {nome} ({matricula} - {curso}) a {member.mention}? (Sim/Não)')

        try:
            message = await bot.wait_for("message", check=lambda m: m.author == ctx.author, timeout=60.0)
            message.content = message.content.lower()

            if message.content == "sim" or message.content == "s":
                if df.loc[index, "DISCORD"] == 0:
                    df.loc[index, "DISCORD"] = member.id
                    await ctx.send(f'Operação realizada com sucesso! {nome} cadastrado(a) ao servidor')
                    channel = bot.get_channel(1024815448820297798)
                    role = discord.utils.get(member.guild.roles, name='Estudante')
                    await member.add_roles(role)
                    role = discord.utils.get(member.guild.roles, name='Não Registrado')
                    await member.remove_roles(role)
                    iddiscord = member.id
                    #await channel.send(f'{nome} < ADICIONADO A > <@{iddiscord}>')

                    embed = discord.Embed(
                        description= f'{nome} < ADICIONADO A > <@{iddiscord}>',
                        colour=0x00FF00,
                    )
                    embed.set_footer(text='Adicionado por ' + ctx.author.name, icon_url=ctx.author.avatar.url)

                    await channel.send(embed=embed)
                    df.to_excel('Banco de Dados.xlsx', index=False)


                else:
                    await ctx.send(f'Parece que {nome} já está cadastrado no servidor.')

            else:
                await ctx.send('Operação Cancelada!')

        except asyncio.TimeoutError:
            await ctx.send('Tempo expirado!')



@bot.command(aliases=['apagar', 'clear'])
@commands.has_role("Date")
async def purge(ctx, amount):
    quantidade = int(amount)
    await ctx.channel.purge(limit=quantidade)


#-------------------------------------------------------------------------------------------------#


bot.run('TOKEN')
