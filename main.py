import discord, os
from datetime import datetime
from discord.ext import commands, tasks
from replit import db
from random import choice

# from PIL import Image, ImageDraw, ImageFont
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(
    commands.when_mentioned_or("s!", "S!"), intents=intents, case_insensitive=True
)


@bot.event
async def on_ready():
    print("Running.")


cursed_list = [
    "I tried to get back to the drawing board but I can't draw.",
    'My mom comes into my room with my grades, and one of them have a zero, and she asks, "Why does it say that this is incomplete?" I say, "It was optional." For me it was optional.',
    "I used to do magic in a Chinese restaurant only problem is an hour later everyone wanted to see it again!",
    'I only drink on days beginning with "T". Tuesday, Thursday, today and tomorrow.',
    "I've learnt that saying \"Oh, this old thing?\" isn't an appropriate way to introduce an elderly relative.",
    "My wife told me she'll slam my head on the keyboard if I don't get off the computer. I'm not too worried, I think she's jokinlkjhfakljn m,.nbziyoao78yv87dfaoyuofaytdf",
    "My wife left a note on the fridge that said, \"This isn't working.\" I'm not sure what she's talking about. I opened the fridge door and it's working fine!",
    "They say that breakfast is the most important meal of the day. Well, not if it's poisoned. Then the antidote becomes the most important.",
    "I just read that someone in London gets stabbed every 52 seconds. Poor guy.",
    "What's red and bad for your teeth? A brick.",
    'Why did Mozart kill all of his chickens? When he asked them who the best composer was, they all replied, "Bach, Bach, Bach."',
    "What’s the difference between a joke and two dicks? You can’t take a joke.",
    "I hope Death is a woman. That way it will never come for me.",
]


@bot.command()
@commands.cooldown(rate=1, per=10)
async def ping(ctx):
    pem = discord.Embed(
        title="Pong!",
        description=f"Your ping is {round(bot.latency * 1000)}ms.",
        color=0x39F220,
    )
    pem.set_footer(text=choice(cursed_list))
    await ctx.reply(embed=pem)


async def pingusers():
    users = []
    for user in db["users"]:
        users.append(user)
    channel = bot.get_channel(db["scrumsend"])
    await channel.send(f"It's time for your scrum - {users}.")


@tasks.loop(seconds=1)
async def checkTime():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    if current_time == db["time"]:
        await pingusers()


checkTime.start()
bot.load_extension("questions")
bot.load_extension("errorhandler")

bot.run(os.environ["vringe"])
