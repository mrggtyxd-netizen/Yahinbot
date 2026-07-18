import os
import random
import unicodedata
import discord
from discord.ext import commands
from flask import Flask
from threading import Thread
from datetime import timedelta

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True

bot = commands.Bot(command_prefix="Yahin ", intents=intents)

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot online"

def run_flask():
    app.run(host="0.0.0.0", port=10000)

def keep_alive():
    Thread(target=run_flask, daemon=True).start()

warnings_db = {}
pregunta_activa = {}

preguntas = [
    ("¿Cuál es el planeta más grande?", "Júpiter"),
    ("¿Cuántos huesos tiene un adulto?", "206"),
    ("¿Quién pintó la Mona Lisa?", "Leonardo da Vinci"),
    ("¿Cuál es la capital de Canadá?", "Ottawa"),
    ("¿Qué gas necesitan las plantas para hacer la fotosíntesis?", "Dióxido de carbono"),
    ("¿Cuánto es 12×12?", "144"),
    ("¿Cuál es el río más largo del mundo?", "Nilo"),
    ("¿En qué continente está Egipto?", "África"),
    ("¿Quién escribió Don Quijote?", "Miguel de Cervantes"),
    ("¿Cuál es el océano más pequeño?", "Ártico"),
    ("¿Qué planeta tiene anillos?", "Saturno"),
    ("¿Cuánto es 15²?", "225"),
    ("¿Cuál es el metal más ligero?", "Litio"),
    ("¿Qué país tiene más habitantes?", "India"),
    ("¿Qué instrumento mide los terremotos?", "Sismógrafo"),
    ("¿Cuál es el animal terrestre más rápido?", "Guepardo"),
    ("¿Cuántos lados tiene un octágono?", "8"),
    ("¿Quién descubrió América en 1492?", "Cristóbal Colón"),
    ("¿Cuál es el idioma más hablado del mundo?", "Mandarín"),
    ("¿Qué país inventó el sushi?", "Japón"),
    ("¿Qué órgano bombea la sangre?", "Corazón"),
    ("¿Qué número romano representa el 50?", "L"),
    ("¿Qué montaña es la más alta del mundo?", "Everest"),
    ("¿Qué planeta es conocido como el gigante gaseoso?", "Júpiter"),
    ("¿Cuánto es 18×7?", "126"),
    ("¿Cuál es la capital de Australia?", "Canberra"),
    ("¿Qué elemento tiene el símbolo Fe?", "Hierro"),
    ("¿Qué país tiene forma de bota?", "Italia"),
    ("¿Cuál es el animal más grande del mundo?", "Ballena azul"),
    ("¿Qué océano baña la costa este de América?", "Atlántico"),
    ("¿Qué inventor creó la bombilla?", "Thomas Edison"),
    ("¿Cuántos continentes hay?", "7"),
    ("¿Cuál es el desierto más grande del mundo?", "Sahara"),
    ("¿Qué país tiene la Torre de Pisa?", "Italia"),
    ("¿Qué vitamina produce el Sol en nuestro cuerpo?", "Vitamina D"),
    ("¿Cuánto es 144÷12?", "12"),
    ("¿Qué planeta tarda más en dar la vuelta al Sol?", "Neptuno"),
    ("¿Cuál es la moneda de Japón?", "Yen"),
    ("¿Qué país tiene la Gran Muralla?", "China"),
    ("¿Quién pintó La última cena?", "Leonardo da Vinci"),
    ("¿Cuál es el satélite natural de la Tierra?", "La Luna"),
    ("¿Qué animal puede cambiar de color?", "Camaleón"),
    ("¿Cuál es la capital de Brasil?", "Brasilia"),
    ("¿Qué país tiene más islas?", "Suecia"),
    ("¿Qué instrumento sirve para ver estrellas?", "Telescopio"),
    ("¿Cuál es el hueso más largo del cuerpo?", "Fémur"),
    ("¿Qué país ganó el Mundial 2010?", "España"),
    ("¿Qué océano está entre América y Europa?", "Atlántico"),
    ("¿Qué animal pone el huevo más grande?", "Avestruz"),
    ("¿Cuánto es 25×8?", "200"),
    ("¿Qué país tiene forma de hexágono?", "Francia"),
    ("¿Cuál es el idioma oficial de Brasil?", "Portugués"),
    ("¿Qué gas respiramos principalmente?", "Oxígeno"),
    ("¿Qué rey construyó Versalles?", "Luis XIV"),
    ("¿Cuál es el volcán más alto del mundo?", "Ojos del Salado"),
    ("¿Qué país tiene más volcanes activos?", "Indonesia"),
    ("¿Cuál es la capital de Argentina?", "Buenos Aires"),
    ("¿Quién formuló la ley de la gravedad?", "Isaac Newton"),
    ("¿Qué país inventó la pizza?", "Italia"),
    ("¿Qué planeta tiene el día más largo?", "Venus"),
    ("¿Cuál es la capital de Noruega?", "Oslo"),
    ("¿Qué mamífero vuela?", "Murciélago"),
    ("¿Qué país tiene la Estatua de la Libertad?", "Estados Unidos"),
    ("¿Qué instrumento mide la temperatura?", "Termómetro"),
    ("¿Cuál es el país más grande del mundo?", "Rusia"),
    ("¿Qué animal tiene tres corazones?", "Pulpo"),
    ("¿Cuál es la capital de Turquía?", "Ankara"),
    ("¿Quién escribió Harry Potter?", "J. K. Rowling"),
    ("¿Qué océano rodea la Antártida?", "Océano Antártico"),
    ("¿Cuál es el ave más grande?", "Avestruz"),
    ("¿Qué país tiene las pirámides de Giza?", "Egipto"),
    ("¿Qué inventó Alexander Graham Bell?", "Teléfono"),
    ("¿Cuál es la capital de Marruecos?", "Rabat"),
    ("¿Qué planeta tiene más lunas?", "Saturno"),
    ("¿Qué país tiene el Coliseo?", "Italia"),
    ("¿Cuál es el animal nacional de Australia?", "Canguro"),
    ("¿Qué órgano produce la insulina?", "Páncreas"),
    ("¿Cuál es el número primo más pequeño?", "2"),
    ("¿Qué científico desarrolló la teoría de la relatividad?", "Albert Einstein"),
    ("¿Cuál es el país más pequeño del mundo?", "Vaticano"),
    ("¿Qué elemento tiene el símbolo Au?", "Oro"),
    ("¿Cuál es la capital de Suiza?", "Berna"),
    ("¿Qué continente tiene más países?", "África"),
    ("¿Qué país tiene el Cristo Redentor?", "Brasil"),
    ("¿Cuál es el mamífero más grande?", "Ballena azul"),
    ("¿Qué planeta está más lejos del Sol?", "Neptuno"),
    ("¿Quién escribió Romeo y Julieta?", "William Shakespeare"),
    ("¿Qué país tiene la Sagrada Familia?", "España"),
    ("¿Qué animal duerme de pie?", "Caballo"),
    ("¿Qué país inventó el papel?", "China"),
    ("¿Cuál es el mar más grande?", "Mar Caribe"),
    ("¿Qué instrumento mide la presión atmosférica?", "Barómetro"),
    ("¿Cuál es la capital de Corea del Sur?", "Seúl"),
    ("¿Qué país tiene el Big Ben?", "Reino Unido"),
    ("¿Qué animal es conocido como el rey de la selva?", "León"),
    ("¿Qué país tiene el Machu Picchu?", "Perú"),
    ("¿Qué órgano filtra la sangre?", "Riñón"),
    ("¿Cuál es el planeta más caliente?", "Venus"),
    ("¿Qué país tiene el Taj Mahal?", "India"),
    ("¿Cuál es el elemento químico más abundante del universo?", "Hidrógeno"),
]

def normalizar(texto: str) -> str:
    texto = texto.lower().strip()
    texto = ''.join(
        c for c in unicodedata.normalize('NFD', texto)
        if unicodedata.category(c) != 'Mn'
    )
    return texto

@bot.event
async def on_ready():
    print(f"Conectado como {bot.user}")
    try:
        await bot.tree.sync()
    except Exception as e:
        print(e)

@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")

@bot.command()
@commands.has_permissions(moderate_members=True)
async def warn(ctx, member: discord.Member, *, reason):
    warnings_db.setdefault(str(member.id), []).append(reason)
    total = len(warnings_db[str(member.id)])
    await ctx.send(f"{member.mention} has sido advertido y ahora tienes {total} advertencias.\nRazón: {reason}")

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason="Sin razón"):
    await member.ban(reason=reason)
    await ctx.send(f"{member.mention} baneado. Razón: {reason}")

@bot.command()
@commands.has_permissions(moderate_members=True)
async def mute(ctx, member: discord.Member, tiempo: str, *, reason="Sin razón"):
    units = {"s": 1, "m": 60, "h": 3600, "d": 86400}
    try:
        num = int(tiempo[:-1])
        unit = tiempo[-1].lower()
        seconds = num * units[unit]
    except:
        return await ctx.send("Formato inválido. Usa 30s, 30m, 30h o 30d.")

    await member.timeout(timedelta(seconds=seconds), reason=reason)
    await ctx.send(f"{member.mention} silenciado por {tiempo}. Razón: {reason}")

@bot.command()
async def avatar(ctx, member: discord.Member = None):
    member = member or ctx.author
    embed = discord.Embed(title=f"Avatar de {member}", color=discord.Color.blue())
    embed.set_image(url=member.display_avatar.url)
    await ctx.send(embed=embed)

@bot.command()
async def warnings(ctx, member: discord.Member):
    warns = warnings_db.get(str(member.id), [])
    if not warns:
        return await ctx.send(f"{member.mention} no tiene warns.")
    msg = "\n".join([f"{i+1}. {r}" for i, r in enumerate(warns)])
    await ctx.send(f"Warns de {member.mention}:\n{msg}")

@bot.command()
async def pregunta(ctx):
    if not preguntas:
        return await ctx.send("No hay preguntas cargadas.")

    key = ctx.guild.id if ctx.guild else ctx.author.id
    if key in pregunta_activa:
        return await ctx.send("Ya hay una pregunta activa.")

    pregunta, respuesta = random.choice(preguntas)

    pregunta_activa[key] = {
        "answer": normalizar(respuesta),
        "channel_id": ctx.channel.id,
        "user_id": ctx.author.id
    }

    embed = discord.Embed(
        title="Yahin Pregunta",
        description=f"**{pregunta}**\n\nTienes **1 minuto** para responder.",
        color=discord.Color.blurple()
    )
    await ctx.send(embed=embed)

    def check(m):
        return (
            m.channel.id == ctx.channel.id and
            m.author.id == ctx.author.id and
            normalizar(m.content) == pregunta_activa[key]["answer"]
        )

    try:
        await bot.wait_for("message", timeout=60, check=check)
        pregunta_activa.pop(key, None)
        await ctx.send(f"✅ {ctx.author.mention} ¡La adivinaste!")
    except discord.TimeoutError:
        pregunta_activa.pop(key, None)
        await ctx.send(f"⏰ {ctx.author.mention}, se acabó el tiempo. La respuesta era: **{respuesta}**")

@bot.command(name="addrol")
@commands.has_permissions(manage_roles=True)
async def addrol(ctx, rol: discord.Role, member: discord.Member):
    await member.add_roles(rol)
    await ctx.send(f"Rol {rol.mention} dado a {member.mention}")

@bot.command()
async def staff(ctx):
    role_id = 1521606098791043092
    role = ctx.guild.get_role(role_id)

    if role is None:
        return await ctx.send("No encontré ese rol.")

    conectados = [
        m for m in role.members
        if m.status != discord.Status.offline and not m.bot
    ]

    if not conectados:
        return await ctx.send("No hay miembros del staff conectados.")

    mentions = " ".join(m.mention for m in conectados)

    embed = discord.Embed(
        title="Staff conectado",
        description=f"Hay **{len(conectados)}** miembros conectados:\n\n{mentions}",
        color=discord.Color.green()
    )
    await ctx.send(embed=embed)


keep_alive()
bot.run(TOKEN)
