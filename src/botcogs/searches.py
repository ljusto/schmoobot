import discord
from discord.ext import commands
import requests
from xml.etree import ElementTree
import urllib.request
import urllib.parse
import re
import wikipedia
import json


class Search:
    def __init__(self, bot):
        self.bot = bot
        self.cities = []

    @commands.command()
    async def yts(self, query, num=1):
        """
        !yts QUERY -- Youtube Search.  If you want more than one word, you need
        to do !yts "your query here" with the quotations
        """
        if (num > 5):
            return await self.bot.say("Hey. 5 videos or less")
        query_string = urllib.parse.urlencode({'search_query':self.trim_query(query)})
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
        results = wikipedia.search(self.trim_query(query))
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


    """
    @commands.command()
    async def google(self, query, num=1):

        !yts QUERY -- Youtube Search.  If you want more than one word, you need
        to do !yts "your query here" with the quotations

        if num > 5:
            return await self.bot.say("Hey. 5 results or less.")
        if query.startswith('"') and query.endswith('"'):
            query = query[1:-1]
        elif query.startswith("'") and query.endswith("'"):
            query = query[1:-1]

        query_string = urllib.parse.urlencode({'q':query})
        url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&%s&rsz=large' % query_string
        html_content = urllib.request.urlopen("http://www.google.com/search?" + query_string)
        search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())
        search_results = search_results[1:]
        print(search_results)
        output = ""
        for i in range(0, num * 2, 2):
            output += "http://www.youtube.com/watch?v=" + \
                      search_results[i] + "\n"
        return await self.bot.say(output)
    """


    @commands.command()
    async def weather(self, city="Toronto"):
        pass
        # work in progress!

    @commands.command()
    async def urban(self, query, num=1):
        if num > 5:
            return await self.bot.say("Hey. 5 results or less.")

        query_string = urllib.parse.urlencode({'term':self.trim_query(query)})
        url = "http://api.urbandictionary.com/v0/define?" + query_string
        html_content = urllib.request.urlopen(url)
        results = json.loads(html_content.read().decode('utf-8'))
        output = ""
        if (len(results['list']) < num):
            num = len(results['list'])
        for i in range(num):
            output += "- " + results['list'][i]['definition'] + "\n\n"
        return await self.bot.say(str(query) + ":\n\n" + output)

    """
    @commands.command()
    async def anime(self, query, num=1):

        Performs a MAL query to get the first num results with synopses and links

        if num > 5:
            return await self.bot.say("Hey. 5 results or less.")
        query_string = urllib.parse.urlencode({"q":self.trim_query(query)})
        url = "http://myanimelist.net/api/anime/search.xml?" + query_string
        xml_tree = None
        session = requests.Session()
        session.headers.update({'Authorization': MALAUTH, 'User-Agent': MALUSERAGENT})
        try:
            response = requests.get(url)
            xml_tree = ElementTree.fromstring(response.content)
    """

    def trim_query(self, query):
        if query.startswith('"') and query.endswith('"'):
            query = query[1:-1]
        elif query.startswith("'") and query.endswith("'"):
            query = query[1:-1]
        return query

def setup(bot):
    bot.add_cog(Search(bot))