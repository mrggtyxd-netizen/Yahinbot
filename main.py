import os
import json
import random
import asyncio
from datetime import timedelta
from threading import Thread

import discord
from discord.ext import commands
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot online"

def run_flask():
    app.run(host="0.0.0.0", port=8080)

Thread(target=run_flask, daemon=True).start()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True

bot = commands.Bot(command_prefix="Yahin ", intents=intents, help_command=None)

ROLE_ID_STAFF = 1521606098791043092
WARNS_FILE = "warns.json"

preguntas = [
    {"pregunta": "¿Cuál es el planeta más grande?", "respuesta": "jupiter"},
    {"pregunta": "¿Cuántos huesos tiene un adulto?", "respuesta": "206"},
    {"pregunta": "¿Quién pintó la Mona Lisa?", "respuesta": "leonardo da vinci"},
    {"pregunta": "¿Cuál es la capital de Canadá?", "respuesta": "ottawa"},
    {"pregunta": "¿Qué gas necesitan las plantas para hacer la fotosíntesis?", "respuesta": "dioxido de carbono"},
    {"pregunta": "¿Cuánto es 12×12?", "respuesta": "144"},
    {"pregunta": "¿Cuál es el río más largo del mundo?", "respuesta": "nilo"},
    {"pregunta": "¿En qué continente está Egipto?", "respuesta": "africa"},
    {"pregunta": "¿Quién escribió Don Quijote?", "respuesta": "miguel de cervantes"},
    {"pregunta": "¿Cuál es el océano más pequeño?", "respuesta": "artico"},
    {"pregunta": "¿Qué planeta tiene anillos?", "respuesta": "saturno"},
    {"pregunta": "¿Cuánto es 15²?", "respuesta": "225"},
    {"pregunta": "¿Cuál es el metal más ligero?", "respuesta": "litio"},
    {"pregunta": "¿Qué país tiene más habitantes?", "respuesta": "india"},
    {"pregunta": "¿Qué instrumento mide los terremotos?", "respuesta": "sismografo"},
    {"pregunta": "¿Cuál es el animal terrestre más rápido?", "respuesta": "guepardo"},
    {"pregunta": "¿Cuántos lados tiene un octágono?", "respuesta": "8"},
    {"pregunta": "¿Quién descubrió América en 1492?", "respuesta": "cristobal colon"},
    {"pregunta": "¿Cuál es el idioma más hablado del mundo?", "respuesta": "mandarin"},
    {"pregunta": "¿Qué país inventó el sushi?", "respuesta": "japon"},
    {"pregunta": "¿Qué órgano bombea la sangre?", "respuesta": "corazon"},
    {"pregunta": "¿Qué número romano representa el 50?", "respuesta": "l"},
    {"pregunta": "¿Qué montaña es la más alta del mundo?", "respuesta": "everest"},
    {"pregunta": "¿Qué planeta es conocido como el gigante gaseoso?", "respuesta": "jupiter"},
    {"pregunta": "¿Cuánto es 18×7?", "respuesta": "126"},
    {"pregunta": "¿Cuál es la capital de Australia?", "respuesta": "canberra"},
    {"pregunta": "¿Qué elemento tiene el símbolo Fe?", "respuesta": "hierro"},
    {"pregunta": "¿Qué país tiene forma de bota?", "respuesta": "italia"},
    {"pregunta": "¿Cuál es el animal más grande del mundo?", "respuesta": "ballena azul"},
    {"pregunta": "¿Qué océano baña la costa este de América?", "respuesta": "atlantico"},
    {"pregunta": "¿Qué inventor creó la bombilla?", "respuesta": "thomas edison"},
    {"pregunta": "¿Cuántos continentes hay?", "respuesta": "7"},
    {"pregunta": "¿Cuál es el desierto más grande del mundo?", "respuesta": "antartida"},
    {"pregunta": "¿Qué país tiene la Torre de Pisa?", "respuesta": "italia"},
    {"pregunta": "¿Qué vitamina produce el Sol en nuestro cuerpo?", "respuesta": "vitamina d"},
    {"pregunta": "¿Cuánto es 144÷12?", "respuesta": "12"},
    {"pregunta": "¿Qué planeta tarda más en dar la vuelta al Sol?", "respuesta": "neptuno"},
    {"pregunta": "¿Cuál es la moneda de Japón?", "respuesta": "yen"},
    {"pregunta": "¿Qué país tiene la Gran Muralla?", "respuesta": "china"},
    {"pregunta": "¿Quién pintó La última cena?", "respuesta": "leonardo da vinci"},
    {"pregunta": "¿Cuál es el satélite natural de la Tierra?", "respuesta": "luna"},
    {"pregunta": "¿Qué animal puede cambiar de color?", "respuesta": "camaleon"},
    {"pregunta": "¿Cuál es la capital de Brasil?", "respuesta": "brasilia"},
    {"pregunta": "¿Qué país tiene más islas?", "respuesta": "suecia"},
    {"pregunta": "¿Qué instrumento sirve para ver estrellas?", "respuesta": "telescopio"},
    {"pregunta": "¿Cuál es el hueso más largo del cuerpo?", "respuesta": "femur"},
    {"pregunta": "¿Qué país ganó el Mundial 2010?", "respuesta": "españa"},
    {"pregunta": "¿Qué océano está entre América y Europa?", "respuesta": "atlantico"},
    {"pregunta": "¿Qué animal pone el huevo más grande?", "respuesta": "avestruz"},
    {"pregunta": "¿Cuánto es 25×8?", "respuesta": "200"},
    {"pregunta": "¿Qué país tiene forma de hexágono?", "respuesta": "francia"},
    {"pregunta": "¿Cuál es el idioma oficial de Brasil?", "respuesta": "portugues"},
    {"pregunta": "¿Qué gas respiramos principalmente?", "respuesta": "oxigeno"},
    {"pregunta": "¿Qué rey construyó Versalles?", "respuesta": "luis xiv"},
    {"pregunta": "¿Cuál es el volcán más alto del mundo?", "respuesta": "ojos del salado"},
    {"pregunta": "¿Qué país tiene más volcanes activos?", "respuesta": "indonesia"},
    {"pregunta": "¿Cuál es la capital de Argentina?", "respuesta": "buenos aires"},
    {"pregunta": "¿Quién formuló la ley de la gravedad?", "respuesta": "isaac newton"},
    {"pregunta": "¿Qué país inventó la pizza?", "respuesta": "italia"},
    {"pregunta": "¿Qué planeta tiene el día más largo?", "respuesta": "venus"},
    {"pregunta": "¿Cuál es la capital de Noruega?", "respuesta": "oslo"},
    {"pregunta": "¿Qué mamífero vuela?", "respuesta": "murcielago"},
    {"pregunta": "¿Qué país tiene la Estatua de la Libertad?", "respuesta": "estados unidos"},
    {"pregunta": "¿Qué instrumento mide la temperatura?", "respuesta": "termometro"},
    {"pregunta": "¿Cuál es el país más grande del mundo?", "respuesta": "rusia"},
    {"pregunta": "¿Qué animal tiene tres corazones?", "respuesta": "pulpo"},
    {"pregunta": "¿Cuál es la capital de Turquía?", "respuesta": "ankara"},
    {"pregunta": "¿Quién escribió Harry Potter?", "respuesta": "j k rowling"},
    {"pregunta": "¿Qué océano rodea la Antártida?", "respuesta": "antartico"},
    {"pregunta": "¿Cuál es el ave más grande?", "respuesta": "avestruz"},
    {"pregunta": "¿Qué país tiene las pirámides de Giza?", "respuesta": "egipto"},
    {"pregunta": "¿Qué inventó Alexander Graham Bell?", "respuesta": "telefono"},
    {"pregunta": "¿Cuál es la capital de Marruecos?", "respuesta": "rabat"},
    {"pregunta": "¿Qué planeta tiene más lunas?", "respuesta": "saturno"},
    {"pregunta": "¿Qué país tiene el Coliseo?", "respuesta": "italia"},
    {"pregunta": "¿Cuál es el animal nacional de Australia?", "respuesta": "canguro"},
    {"pregunta": "¿Qué órgano produce la insulina?", "respuesta": "pancreas"},
    {"pregunta": "¿Cuál es el número primo más pequeño?", "respuesta": "2"},
    {"pregunta": "¿Qué científico desarrolló la teoría de la relatividad?", "respuesta": "albert einstein"},
    {"pregunta": "¿Cuál es el país más pequeño del mundo?", "respuesta": "vaticano"},
    {"pregunta": "¿Qué elemento tiene el símbolo Au?", "respuesta": "oro"},
    {"pregunta": "¿Cuál es la capital de Suiza?", "respuesta": "berna"},
    {"pregunta": "¿Qué continente tiene más países?", "respuesta": "africa"},
    {"pregunta": "¿Qué país tiene el Cristo Redentor?", "respuesta": "brasil"},
    {"pregunta": "¿Cuál es el mamífero más grande?", "respuesta": "ballena azul"},
    {"pregunta": "¿Qué planeta está más lejos del Sol?", "respuesta": "neptuno"},
    {"pregunta": "¿Quién escribió Romeo y Julieta?", "respuesta": "shakespeare"},
    {"pregunta": "¿Qué país tiene la Sagrada Familia?", "respuesta": "españa"},
    {"pregunta": "¿Qué animal duerme de pie?", "respuesta": "caballo"},
    {"pregunta": "¿Qué país inventó el papel?", "respuesta": "china"},
    {"pregunta": "¿Cuál es el mar más grande?", "respuesta": "mar de filipinas"},
    {"pregunta": "¿Qué instrumento mide la presión atmosférica?", "respuesta": "barometro"},
    {"pregunta": "¿Cuál es la capital de Corea del Sur?", "respuesta": "seul"},
    {"pregunta": "¿Qué país tiene el Big Ben?", "respuesta": "reino unido"},
    {"pregunta": "¿Qué animal es conocido como el rey de la selva?", "respuesta": "leon"},
    {"pregunta": "¿Qué país tiene el Machu Picchu?", "respuesta": "peru"},
    {"pregunta": "¿Qué órgano filtra la sangre?", "respuesta": "riñon"},
    {"pregunta": "¿Cuál es el planeta más caliente?", "respuesta": "venus"},
    {"pregunta": "¿Qué país tiene el Taj Mahal?", "respuesta": "india"},
    {"pregunta": "¿Cuál es el elemento químico más abundante del universo?", "respuesta": "hidrogeno"},
]

def load_warns():
    if not os.path.exists(WARNS_FILE):
        return {}
    with open(WARNS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_warns(data):
    with open(WARNS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

warns = load_warns()

@bot.event
async def on_ready():
    print(f"Conectado como {bot.user}")

@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason="Sin razón"):
    await member.kick(reason=reason)
    await ctx.send(f"✅ {member.mention} expulsado. Motivo: {reason}")

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason="Sin razón"):
    await member.ban(reason=reason)
    await ctx.send(f"✅ {member.mention} baneado. Motivo: {reason}")

@bot.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, user_id: int):
    user = await bot.fetch_user(user_id)
    await ctx.guild.unban(user)
    await ctx.send(f"✅ {user.name} desbaneado.")

@bot.command()
@commands.has_permissions(manage_messages=True)
async def warn(ctx, member: discord.Member, *, reason="Sin razón"):
    guild_id = str(ctx.guild.id)
    user_id = str(member.id)
    warns.setdefault(guild_id, {})
    warns[guild_id].setdefault(user_id, [])
    warns[guild_id][user_id].append(reason)
    save_warns(warns)
    await ctx.send(f"⚠️ {member.mention} advertido. Motivo: {reason}")

@bot.command()
@commands.has_permissions(manage_messages=True)
async def unwarn(ctx, member: discord.Member):
    guild_id = str(ctx.guild.id)
    user_id = str(member.id)
    if guild_id not in warns or user_id not in warns[guild_id] or not warns[guild_id][user_id]:
        await ctx.send("❌ Ese usuario no tiene warns.")
        return
    warns[guild_id][user_id].pop()
    if not warns[guild_id][user_id]:
        del warns[guild_id][user_id]
    if not warns[guild_id]:
        del warns[guild_id]
    save_warns(warns)
    await ctx.send(f"✅ Se ha quitado un warn a {member.mention}")

@bot.command()
@commands.has_permissions(manage_messages=True)
async def warnings(ctx, member: discord.Member):
    guild_id = str(ctx.guild.id)
    user_id = str(member.id)
    user_warns = warns.get(guild_id, {}).get(user_id, [])
    if not user_warns:
        await ctx.send(f"✅ {member.mention} no tiene warns.")
        return
    texto = "\n".join([f"{i+1}. {w}" for i, w in enumerate(user_warns)])
    await ctx.send(f"⚠️ Warns de {member.mention}:\n{texto}")

@bot.command()
@commands.has_permissions(moderate_members=True)
async def mute(ctx, member: discord.Member, tiempo: int):
    await member.timeout(timedelta(minutes=tiempo), reason="Muteado por moderación")
    await ctx.send(f"✅ {member.mention} muteado por {tiempo} minutos.")

@bot.command()
@commands.has_permissions(moderate_members=True)
async def unmute(ctx, member: discord.Member):
    await member.timeout(None)
    await ctx.send(f"✅ {member.mention} desmuteado.")

@bot.command()
async def pregunta(ctx):
    q = random.choice(preguntas)
    await ctx.send(f"🟡 Pregunta: **{q['pregunta']}**\nTienes 1 minuto para responder.")
    def check(m):
        return m.channel == ctx.channel and m.author == ctx.author
    try:
        msg = await bot.wait_for("message", timeout=60.0, check=check)
        if msg.content.lower().strip() == q["respuesta"].lower().strip():
            await ctx.send("✅ Respuesta correcta.")
        else:
            await ctx.send(f"❌ Respuesta incorrecta. La correcta era: **{q['respuesta']}**")
    except asyncio.TimeoutError:
        await ctx.send(f"⌛ Se acabó el tiempo. La respuesta era: **{q['respuesta']}**")

@bot.command()
@commands.has_permissions(administrator=True)
async def addrol(ctx, member: discord.Member, role: discord.Role):
    await member.add_roles(role)
    await ctx.send(f"✅ Rol {role.mention} añadido a {member.mention}")

@bot.command()
async def staff(ctx):
    role = ctx.guild.get_role(ROLE_ID_STAFF)
    if not role:
        await ctx.send("❌ No encontré el rol staff.")
        return
    online_members = [m.mention for m in role.members if m.status != discord.Status.offline]
    if not online_members:
        await ctx.send("No hay usuarios conectados con ese rol.")
        return
    await ctx.send(f"📣 {' '.join(online_members)}")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ No tienes permisos para usar ese comando.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("❌ Faltan argumentos.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("❌ Argumento inválido.")
    else:
        await ctx.send(f"❌ Error: {error}")

bot.run(os.getenv("TOKEN"))
