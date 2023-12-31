import os
import discord
import compiler_operations
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
viable_languages = "Python, C++(17), Java, Bash"
options_flag = False


async def send_message(message, user_message, is_private, options_flag):
    try:
        if options_flag:
            response = "**Language Options for Compiling:**\n" + viable_languages
            await message.author.send(response) if is_private else await message.channel.send(response)
        else:
            language = user_message.split()[1][3:]
            response = compiler_operations.compileInfo(language, user_message)
            await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)


def run_discord_bot():
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():  # console process/log
        print(f'{client.user} is now running!')

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return

        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)

        print(f"{username} said: '{user_message}' ({channel})\n")

        if user_message[0:9] == '.!compile':
            await send_message(message, user_message, is_private=True, options_flag=False)
        elif user_message[0:8] == '!compile':
            await send_message(message, user_message, is_private=False, options_flag=False)
        elif user_message == '?compile':
            await send_message(message, user_message, is_private=False, options_flag=True)
        elif user_message == '.?compile':
            await send_message(message, user_message, is_private=True, options_flag=True)
        else:
            return  # only runs with these commands above

    client.run(TOKEN)
