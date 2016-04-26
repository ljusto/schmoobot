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
    async def choose(self, context):
        "Makes a choice. Separate choices by commas!"
        # separated by commas!
        choices = [x.strip() for x in str(context.message.content)[7:].split(',')]
        return await self.bot.say(str(context.message.author) + " got: " +
                                  choices[random.randint(0, len(choices) - 1)])

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

    @commands.command(pass_context=True)
    async def hug(self, context):
        gets_hug = random.randint(0,25)
        hug_messages = ["I'll be your teddy bear, buddy", "come here, let me give you a hug", "here's a hug for you",
                        "here's a free hug", "it's alright man, it's alright", "a hug today keeps the sad away", "leeeroyyy huggins"]
        if (not gets_hug):
            return await self.bot.say(str(context.message.author) + ", you don't deserve a hug.")
        else:
            return await self.bot.say(str(context.message.author) + ", " + random.choice(hug_messages))


def setup(bot):
    bot.add_cog(RNG(bot))