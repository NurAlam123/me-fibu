import discord
import sqlite3
from discord.ext import commands

con_qna = sqlite3.connect("./data/qna.db")
c_qna = con_qna.cursor()


class QNA(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def ans(self, ctx, *, question):
        questions = c_qna.execute(
            "select * from data where question like ?", (question+"%",)).fetchall()
        if len(questions) > 1:
            await ctx.send(f"Hey {message.author}! Kindly type full question. 🙂")
        elif questions == []:
            c_qna.execute("insert into not_answered values (?)", (question,))
            con_qna.commit()
            await ctx.send("I am extremely sorry that I haven't any answer of your question. 😢\n[**Please check your question. Is there any type mistake or anything?**]\nAlso I have noted your question and will soon answer your question.\n*Thank you!* 🙂")
        elif len(questions) <= 1:
            ans = c_qna.execute("select * from data where id=?",
                                (questions[0][0],)).fetchone()
            await ctx.send(ans[2])


def setup(bot):
    bot.add_cog(QNA(bot))
