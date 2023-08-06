import argparse
import asyncio

from run_bot import main as run_bot
from create_config import main as create_config

def get_args():
    parser = argparse.ArgumentParser()
    runner_subparser = parser.add_subparsers(dest="subcommand")
    bot_parser = runner_subparser.add_parser("run")
    config_parser = runner_subparser.add_parser("create-config")

    bot_parser.add_argument("config_file", type=str, default="config/config.toml", help="Config file for the bot")
    bot_parser.add_argument("--loglevel", type=str, default="debug", help="Global log level.")
    bot_parser.add_argument("--shardcount", type=int,default=None, help="The number of shards to run the bot with.")
    bot_parser.add_argument("--min", type=int, default=None, help="The minimum shard ID that the bot will run with.")
    bot_parser.add_argument("--max", type=int, default=None, help="The maximum shard ID that the bot will run with.")
    return parser.parse_args()

def main():
    args = get_args()
    if args.subcommand == "run":
        asyncio.get_event_loop().run_until_complete(run_bot(args))

    if args.subcommand == "create-config":
        create_config(args)

if __name__ == '__main__':
    main()
