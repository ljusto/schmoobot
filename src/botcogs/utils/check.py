from discord.ext import commands
import credentials


def owner_clearance(message):
    """
    This is meant for functions that can only be executed by the bot's owner
    :param message: Message to check
    :return: Whether the message was sent by the owner or not.
    """
    return message.author.id == credentials.owner

def is_owner():
    return commands.check(lambda context: owner_clearance(context.message))