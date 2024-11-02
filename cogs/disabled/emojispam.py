from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
import discord
from discord import interactions
from discord.ext import commands
import asyncio
import logging
import json
from helpers import helpers

class EmojiSpam(commands.Cog, name='EmojiSpam'):
    """Experimental stuff that most likely won't work"""
    
    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger("CattoBotto.emojiSpam")
        self.last_sent = None
        self.channels = self.load_channels()
        self.users = self.load_users()
        self.emoji = self.get_emoji()
        self.scheduler = AsyncIOScheduler()
        
    def load_channels(self):
        with open('channels.txt') as f:
            channels = f.readlines()
            return [int(line.strip()) for line in channels]
        
    def load_users(self):
        with open('users.txt') as f:
            users = f.readlines()
            return [int(line.strip()) for line in users]
    
    def get_emoji(self):
        with open('emoji.json') as f:
            self.emoji = json.read(f)

    async def send_message(self):
        print("Hi")
        for channel in self.channels:
            _channel = self.bot.get_channel(channel)
            await _channel.send(self.emoji)
        for user in self.users:
            _user = await self.bot.fetch_user(user)
            await _user.send(self.emoji)

    @commands.command()
    async def test_spam(self, ctx):
        print(ctx.author.id)
        other = await self.bot.fetch_user(ctx.author.id)
        print(ctx.author.id == other.id)
        await self.send_message()

    @commands.Cog.listener()
    async def on_ready(self):
        self.logger.info('Emoji spammer is loaded')
        #self.scheduler.add_job(self.send_message, CronTrigger(hour=18, minute=0))
        #self.scheduler.start()

async def setup(bot):
    await bot.add_cog(EmojiSpam(bot))