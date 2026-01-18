import logging
import os

import discord
from discord.ext import commands
import dotenv

dotenv.load_dotenv()

bot: commands.Bot = commands.Bot(command_prefix='/', intents=discord.Intents.all())
log_handler = logging.FileHandler(filename='latest.log', encoding='utf-8', mode='w')

@bot.event
async def on_ready():
    logging.info('Ready!')
    logging.info(f'Login as {bot.user.name}')
    logging.info('Timings Reset')

@bot.event
async def on_voice_state_update(
        member: discord.Member,
        before: discord.VoiceState,
        after: discord.VoiceState
):
    logging.info(f'''Voice state changed:
    member: "{member.name}",
    before: {before},
    after: {after}''')


discord.utils.setup_logging()
bot.run(
    os.getenv("BOT_TOKEN"),
    log_handler=log_handler,
    log_level=logging.INFO,
    root_logger=True
)