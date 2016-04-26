from discord.ext import commands

class Misc:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def oink(self, numoinks=15):
        NUM_OINKS = numoinks
        if numoinks > 100:
            return await self.bot.say("Nice try.")
        output = "OINK " * NUM_OINKS
        return await self.bot.say(output, tts=True)


    @commands.command(pass_context=True)
    async def echo(self, context):
        """
        !echo [message]
        """
        return await self.bot.say(str(context.message.content)[6:])

    @commands.command()
    async def lenny(self):
        return await self.bot.say("( ͡° ͜ʖ ͡°)")

    @commands.command(pass_context=True)
    async def hi(self, context):
        #phrases = ["Hi", "Hey", "What's up", "Hey hey hey", "Salutations", "Ahoy-hoy", "Sup"]
        return await self.bot.say("Hey, " + str(context.message.author) + "!")


def setup(bot):
    bot.add_cog(Misc(bot))