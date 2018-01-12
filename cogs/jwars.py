import json

import discord
import discord.ext.commands as commands
import fuzzywuzzy.fuzz
import fuzzywuzzy.process

import paths

def setup(bot):
    bot.add_cog(JWars(bot))

class JWars:
    """Juggernaut Wars commands"""
    def __init__(self, bot):
        with open(paths.CHAR_INFO_DATA, encoding='utf-8') as fp:
            self.char_info = json.load(fp)
        self.emojis = {e.name.lower(): e for e in bot.emojis}

    @commands.command()
    async def info(self, ctx, *, name):
        """Shows info about a character."""
        try:
            best_match = next(fuzzywuzzy.process.extractWithoutOrder(name, self.char_info.keys(), scorer=fuzzywuzzy.fuzz.token_sort_ratio, score_cutoff=50))
        except StopIteration:
            return await ctx.send(f'Could not find character "{name}".')

        char_info = self.char_info.get(best_match[0])
        stats = '\n'.join(f'**{stat["name"]}: {stat["value"]}**' if stat["highlight"] else f'{stat["name"]}: {stat["value"]}' for stat in char_info['stats'])
        wins = ''.join(str(self.emojis[char]) for char in char_info['matchups']['wins'])
        loss = ''.join(str(self.emojis[char]) for char in char_info['matchups']['loss'])

        embed = discord.Embed(colour=discord.Colour.blurple(), title=char_info['name'], description=char_info['description'])
        embed.set_thumbnail(url=self.emojis[best_match[0]].url)
        embed.add_field(name='Stats', value=stats, inline=False)
        embed.add_field(name='Bien contre', value=wins)
        embed.add_field(name='Faible contre', value=loss)
        await ctx.send(embed=embed)
