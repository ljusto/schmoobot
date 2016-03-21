import discord
from discord.ext import commands
import random


class RNG:
    def __init__(self, bot):
        self.bot = bot
        self.magic8ball = ["Christian, shut up", "Very much so", "Absolutely!", "Pretty good chance", "No way man"]
        self.fortunes = open('fortunes.txt', encoding='utf-8',
                             errors='ignore').readlines()

    @commands.command(pass_context=True)
    async def diceroll(self, context, sides=6):
        """
        !diceroll NUMBER-OF-FACES -- e.g., !diceroll 3 gives 1, 2 or 3.
        """
        # this is because SOMEONE will definitely try to put in a decimal.
        """ don't even need this...
        try:
            sides = int(sides)
        except Exception:
            return await self.bot.say("Something went wrong reading your number. Try again.")
        """

        if sides <= 0:
            ret = await self.bot.say(str(context.message.author) + " rolled a 69 :^)")
        else:
            ret = await self.bot.say(str(context.message.author) + " rolled a " + str(random.randint(1, sides)))
        return ret

    @commands.command(pass_context=True)
    async def coin(self, context):
        """
        !coin -- gives heads or tails
        """
        result = "heads" if random.randint(1,2) == 1 else "tails"
        return await self.bot.say(str(context.message.author) + " got a " +
                                  result)

    @commands.command(pass_context=True)
    async def fortune(self, context):
        """
        !fortune -- gives back your fortune!
        """
        fortune = random.choice(self.fortunes)
        return await self.bot.say(str(context.message.author) + "'s fortune: " +
                                  fortune.rstrip("\n"))


def setup(bot):
    bot.add_cog(RNG(bot))