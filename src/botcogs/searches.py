import discord
from discord.ext import commands
import urllib.request
import urllib.parse
import re
import wikipedia


class Search:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def yts(self, query, num=1):
        """
        !yts QUERY -- Youtube Search.  If you want more than one word, you need
        to do !yts "your query here" with the quotations
        """
        if (num > 5):
            return await self.bot.say("Hey. 5 videos or less")
        if query.startswith('"') and query.endswith('"'):
            query = query[1:-1]
        elif query.startswith("'") and query.endswith("'"):
            query = query[1:-1]
        query_string = urllib.parse.urlencode({'search_query':query})
        html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)
        search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())
        search_results = search_results[1:]
        print(search_results)
        output = ""
        for i in range(0, num * 2, 2):
            output += "http://www.youtube.com/watch?v=" + \
                      search_results[i] + "\n"
        return await self.bot.say(output)

    @commands.command()
    async def wiki(self, query):
        """
        !wiki QUERY -- Wikipedia search and summary.  If you want mroe than
        one word, you need to do !wiki "your query here" with the quotes
        """
        SENTENCE_NUM = 7
        if query == "" or query is None:
            return

        results = wikipedia.search(query)
        if results:
            try:
                summary = str(wikipedia.page(results[0]).url) + "\n"
            except wikipedia.exceptions.DisambiguationError as e:
                summary = str(wikipedia.page(e.options[0]).url) + "\n"
            # Discord takes care of this already.
            #summary += wikipedia.summary(results[0], sentences=SENTENCE_NUM)
        else:
            summary = "Couldn't find any page with that!"
        return await self.bot.say(summary)


def setup(bot):
    bot.add_cog(Search(bot))