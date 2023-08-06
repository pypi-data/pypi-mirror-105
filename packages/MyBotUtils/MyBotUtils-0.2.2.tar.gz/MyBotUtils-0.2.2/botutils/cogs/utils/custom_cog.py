from discord.ext import commands
import logging
from .redis import RedisChannel
from .custom_bot import CustomBot

class CustomCog(commands.Cog):
    def __init__(self, bot:CustomBot, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bot = bot
        bot_logger = bot.logger
        self.logger = bot_logger.getChild('.'.join(['cog', self.__cog_name__.replace(' ', '')]))

        # Add cog item to all redis channels in our cog
        #self.logger.debug("Adding cog item to all redis channels")
        for attr in dir(self):
            try:
                item = getattr(self, attr)
            except AttributeError:
                continue
            if isinstance(item, RedisChannel):
                item.cog = self