from cogs import utils
import logging
import sys
import discord

def get_shard_ids(min, max, shardcount):
    if shardcount is None:
        return None

    if not min:
        min = 0
    if not max:
        max = shardcount - 1
        
    shard_ids = list(range(min, max + 1))
    return shard_ids

def set_log_level(logger, level):
    if isinstance(logger, str):
        logger = logging.getLogger(logger)

    try:
        level = getattr(logging, level.upper())
    except AttributeError:
        raise ValueError(f"Could not find log level {level.upper()} in the logging module.")
    
    logger.setLevel(level)

async def create_redis_pool(bot:utils.Bot):
    try:
        bot.logger.info("Running redis startup")
        await bot.redis.create_pool(bot.config['redis'])
    except ConnectionRefusedError:
        bot.logger.error("Redis connection refused - Did you set the right information in the config?")
    except Exception as e:
        raise e 

async def create_database_pool(bot:utils.Bot):
    try:
        logger.info("Running database startup")
        await bot.database.create_pool(bot.config['database'])
    except ConnectionRefusedError:
        logger.error("Database connection refused - Did you set the right information in the config?")
    except Exception as e:
        raise e 

async def main(args):
    logging.basicConfig(format='%(asctime)s:%(name)s:%(levelname)s: %(message)s', stream=sys.stdout)
    logger = logging.getLogger('bot')
    set_log_level(logger, args.loglevel)
    set_log_level("discord", "info")

    bot = utils.Bot(
        activity=discord.Game("Connecting..."),
        status=discord.Status.dnd,
        config_file=args.config_file,
        shard_count=args.shardcount,
        shard_ids=get_shard_ids(args.min, args.max, args.shardcount),
        logger=logger,
        case_insensitive=True
    )

    if bot.database_enabled:
        await create_database_pool(bot)

    if bot.redis_enabled:
        await create_redis_pool(bot)

    bot.load_all_extensions()
    try:
        logger.info("Running bot")
        await bot.start()
    except KeyboardInterrupt:
        logger.info("Closing bot")
        await bot.close()

    if bot.database_enabled:
        logger.info("Closing database pool")
        await bot.database.pool.close()

    if bot.redis_enabled:
        logger.info("Closing redis pool")
        await bot.redis.pool.close()

    logger.info("Closing asyncio loop")
    loop.close()



