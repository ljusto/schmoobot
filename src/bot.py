__author__ = 'Lambert Justo'

import glob         # for getting botcogs

import discord
from discord.ext import commands
import credentials
from botcogs.utils import check

bot_prefix = "!"
formatter = commands.HelpFormatter(show_check_failure=False)
bot = commands.Bot(command_prefix=bot_prefix, formatter=formatter,
                   description="Schmoo Bot!", pm_help=None)
prev = None

def list_cogs():
    """
    Gets all modules from [cwd]/botcogs/ and puts them in a list to return in the
    form of ["botcogs.module1", "botcogs.module2", "botcogs.module3", ...]
    :return: list of strings where each module J.py is of form "botcogs.J"
    """
    cogs = glob.glob("botcogs/*.py")
    cog_list = []
    for c in cogs:
        cog_list.append("botcogs." +
                        c.replace("/","\\").split("\\")[1].replace(".py", ""))
    return cog_list

# cogs_list = list_cogs()
cogs_list = ["botcogs.rng", "botcogs.searches"] # FOR NOW, KEEP A HARDCODED LIST


def load_cog(cog_name : str):
    cog_name = cog_name.strip()
    if cog_name not in cogs_list:
        print("Couldn't find module", cog_name)
        return
    try:
        bot.load_extension(cog_name)
    except (ImportError, discord.ClientException, AttributeError) as e:
        print("Failed to load cog", cog_name, " due to", str(e))
        return


@bot.event
async def on_ready():
    print("Logged in as:")
    print("name:", bot.user.name)
    print("id:", bot.user.id)
    print("--------------------------------------------")


@check.is_owner()
@bot.command()
async def load(extension_name : str):
    print("got to load function")
    """
    attempt to load a cog - a cog is a module that has commands
    """
    # strip any whitespace
    extension_name = extension_name.strip()

    # check if the extension is in the list of loaded botcogs
    if extension_name not in cogs_list:
        output = "Couldn't find module " + extension_name
        await bot.say(output)
        return

    # attempt to load the extension
    try:
        bot.load_extension(extension_name)
    except (ImportError, discord.ClientException, AttributeError) as e:
        output = "Failed to load cog " + extension_name + " due to ", str(e)
        await bot.say(output)
        return
    output = "Loaded " + extension_name + " successfully!"
    await bot.say(output)


@bot.command()
@check.is_owner()
async def load_all():
    for elem in cogs_list:
        load_cog(elem)

    await bot.say("Loaded " + str(cogs_list) + " successfully!")
    await bot.say("Active commands (syntax: '![command] [extra_argument]'): "
                  + str(list(bot.commands.keys())))


@bot.command()
@check.is_owner()
async def unload(extension_name : str):
    """attempt to load an extension (plugin"""
    # extension_name = botcogs.<module_name>
    extension_name = extension_name.strip()
    try:
        bot.unload_extension(extension_name)
    except Exception as e:
        await bot.say("Failed to unload cog " + extension_name + " due to " + str(e))
    await bot.say("Unloaded " + extension_name + " successfully!")


@bot.command()
@check.is_owner()
async def reload(extension_name : str):
    if extension_name not in cogs_list:
        await bot.say("Failed to find cog " + str(extension_name))
        return
    try:
        bot.unload_extension(extension_name)
        load_cog(extension_name)
    except Exception as e:
        await bot.say("Failed to reload cog " + extension_name + " due to " + str(e))
        return
    await bot.say("Reloaded " + extension_name + " successfully!")


#@bot.command(pass_context=True)
#async def r(context):
#    """work in progress: remember last command?"""
#    pass


@bot.event
async def on_message(message):
    # TODO: keep track of whitelisted/blacklisted users
    await bot.process_commands(message)

@bot.event
async def on_command(command, context):
    # not even sure why this is here???
    pass

"""
TODO:
join
leave
load cogs
modules!
"""
bot.run(credentials.email, credentials.password)
