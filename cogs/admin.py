import logging
from collections import Counter

import discord
import discord.ext.commands as commands


log = logging.getLogger(__name__)


def setup(bot):
    bot.add_cog(Admin(bot))


class Admin:
    """Bot management commands and events."""
    def __init__(self, bot):
        self.commands_used = Counter()
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def restart(self, ctx):
        """Restarts the bot."""
        ctx.bot.restart()

    @commands.command()
    @commands.is_owner()
    async def shutdown(self, ctx):
        """Shuts the bot down."""
        ctx.bot.shutdown()

    @commands.command()
    @commands.is_owner()
    async def status(self, ctx, *, status=None):
        """Changes the bot's status."""
        await ctx.bot.change_status(status)

    async def on_command(self, ctx):
        self.commands_used[ctx.command.qualified_name] += 1
        if ctx.guild is None:
            log.info(f'DM:{ctx.author.name}:{ctx.author.id}:{ctx.message.content}')
        else:
            log.info(f'{ctx.guild.name}:{ctx.guild.id}:{ctx.channel.name}:{ctx.channel.id}:{ctx.author.name}:{ctx.author.id}:{ctx.message.content}')

    async def on_guild_join(self, guild):
        # Log that the bot has been added somewhere
        log.info(f'GUILD_JOIN:{guild.name}:{guild.id}:{guild.owner.name}:{guild.owner.id}:')

    async def on_guild_remove(self, guild):
        # Log that the bot has been removed from somewhere
        log.info(f'GUILD_REMOVE:{guild.name}:{guild.id}:{guild.owner.name}:{guild.owner.id}:')
