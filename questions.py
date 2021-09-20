import discord, os
from PIL import Image, ImageDraw, ImageFont
from discord.ext import commands
from replit import db
from datetime import datetime


class Scrum(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        help="Allows you to 'add' to, 'remove' from, 'clear' or 'show' the questions list."
    )
    async def questions(self, ctx, command: str = "show", *, question: str = None):
        cmd = command.lower()
        if cmd == "add":
            db["questions"].append(question + "?")
            await ctx.reply(f"Added `{question}?` to the question list.")
        elif cmd == "clear":
            db["questions"] = []
            await ctx.reply("Reset the questions list.")
        elif cmd == "remove":
            db["questions"].remove(question + "?")
            await ctx.reply("Done.")
        elif cmd == "show":
            background = Image.open(db["file"])
            write = ImageDraw.Draw(background)
            heading = ImageFont.truetype("FreeMono.ttf", 65)
            questions = ImageFont.truetype("FreeMono.ttf", 50)
            write.text((66, 79), f"Questions", font=heading, fill=(0, 255, 42))
            table = [200, 235, 340, 375, 480, 515, 620, 655]
            for question in db["questions"]:
                index = db["questions"].index(question) * 2
                coords = table[index]
                write.text((70, coords), question, font=questions, fill=(0, 255, 42))
            background.save("questions.png")
            with open("questions.png", "rb") as fh:
                f = discord.File(fh, filename="questions.png")
            await ctx.send(file=f)
            await ctx.message.delete()
            os.remove(f"questions.png")

    @commands.command(help="Allows a user to answer their daily scrum.")
    async def answer(self, ctx):
        answers = {}
        todel = []

        def check(m: discord.Message):
            return m.author.id == ctx.author.id and m.channel.id == ctx.channel.id

        for question in db["questions"]:
            q = await ctx.reply(
                embed=discord.Embed(
                    title=question,
                    description=f"You have {db['deltime']} seconds to answer.",
                    color=0x39F220,
                )
            )
            answer = await self.bot.wait_for(
                event="message", check=check, timeout=db["deltime"]
            )
            answers[question] = answer.content
            todel.append(answer)
            todel.append(q)
        aem = discord.Embed(title=f"{ctx.author.display_name}'s scrum.", color=0x39F220)

        for item in answers.keys():
            aem.add_field(name=item, value=answers[item], inline=False)
            # db[datetime.datetime.now().day] = {ctx.author.id:[]}
        channel = self.bot.get_channel(db["scrumsend"])
        await channel.send(embed=aem)
        try:
            for item in todel:
                await item.delete()
        except:
            pass

        background = Image.open(db["file"])
        write = ImageDraw.Draw(background)
        headingfont = ImageFont.truetype("FreeMono.ttf", 65)
        questionsfont = ImageFont.truetype("FreeMono.ttf", 50)
        answersfont = ImageFont.truetype("FreeMono.ttf", 45)
        write.text(
            (66, 79),
            f"{ctx.author.display_name}'s Scrum.",
            font=headingfont,
            fill=(255, 255, 255),
        )
        table = [200, 340, 480, 620, 690]
        anstable = [250, 390, 530, 670, 740]
        for question in answers.keys():
            index = db["questions"].index(question)
            coords = table[index]
            anscords = anstable[index]
            write.text((70, coords), question, font=questionsfont, fill=(255, 215, 0))
            write.text(
                (70, anscords),
                answers[question],
                font=answersfont,
                fill=(255, 255, 255),
            )
        background.save(f"{ctx.author.id}answers.png")
        with open(f"{ctx.author.id}answers.png", "rb") as fh:
            f = discord.File(fh, filename=f"{ctx.author.id}answers.png")
        await channel.send(file=f)
        os.remove(f"{ctx.author.id}answers.png")
        await ctx.message.delete()

    @commands.command(help="Sets the background image.")
    async def setbg(self, ctx, bg: str = None):
        db["file"] = bg
        await ctx.reply("Done.")

    @commands.command(help="Sets how long you have to answer the scrum.")
    async def deltimer(self, ctx, time: int = None):
        db["deltime"] = time
        await ctx.reply("Done.")

    @commands.command(help="Sets the channel to send to.")
    async def channel(self, ctx, channel: discord.TextChannel):
        try:
            db["scrumsend"] = channel.id
        except Exception as e:
            raise e
        await ctx.reply("Done.", delete_after=5)
        await ctx.message.delete()

    @commands.command(help="Begins the setup process.")
    async def setup(self, ctx):
        def check(m: discord.Message):
            return m.author.id == ctx.author.id and m.channel.id == ctx.channel.id

        await ctx.reply("Add questions using `s!questions add <question>`.")
        await ctx.reply(
            "Pick an image - \nsigma.jpg\nwhoa.png\noml.jpg\nPlease enter one of the above."
        )
        with open(f"sigma.jpg", "rb") as fh:
            f = discord.File(fh, filename=f"sigma.jpg")
        await ctx.send(file=f)
        with open(f"whoa.png", "rb") as fh:
            f = discord.File(fh, filename=f"whoa.png")
        await ctx.send(file=f)
        with open(f"oml.jpg", "rb") as fh:
            f = discord.File(fh, filename=f"oml.jpg")
        await ctx.send(file=f)
        answer = await self.bot.wait_for(event="message", check=check, timeout=30.0)
        db["file"] = answer.content
        await ctx.reply(
            "Now choose a channel to send the scrum messages in. **SEND THE ID**"
        )
        channel = await self.bot.wait_for(event="message", check=check, timeout=30.0)
        db["scrumsend"] = int(channel.content)
        await ctx.reply("Done.")

    @commands.command(help="DMs you when it's time to do your scrum.")
    async def register(self, ctx, arg=None, user: discord.Member = None):
        if arg is None:
            db["users"].append(ctx.author.mention)
            await ctx.reply("Done.")
        elif arg.lower() == "clear":
            db["users"] = []
            await ctx.reply("Done.")
        elif arg.lower() == "show":
            await ctx.reply(db["users"])
        elif arg.lower() == "remove":
            db["users"].remove(user.mention)
            await ctx.reply("Done.")

    @commands.command(help="Sets the time to get pinged.")
    async def setTime(self, ctx, *args):
        if args[0].lower() == "show":
            rn = datetime.now()
            await ctx.reply(rn.strftime("%H:%M:%S"))
        elif args[0].lower() == "set":
            db["time"] = args[1]
            await ctx.reply("Done.")


# p = Scrum(discord.ext.commands.cog)
#


def setup(bot):
    bot.add_cog(Scrum(bot))
