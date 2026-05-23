import discord
from discord.ext import commands
from deep_translator import GoogleTranslator
import asyncio
import os

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot("/", intents=intents)

@bot.event 
async def on_ready():
    print("Bot inciado")

@bot.command()
async def tradutor(ctx):
    await ctx.reply("em desenvolvimento")

# Nome do cargo : idioma destino
ROLE_LANGUAGES = {
    "inglês": "en",
    "espanhol": "es",
    "francês": "fr",
    "japonês": "ja",
    "brasileiro": "pt",


    "arábia": "ar",
    "chinês": "zh-CN",
    "italiano": "it",
    
}

async def traslate_text(text: str, target: str) -> str:
    return await asyncio.to_thread(
        GoogleTranslator(source="auto", target=target).translate,text
        )

class TranslateButton(discord.ui.View):
    def __init__(self, original_text):
        super().__init__(timeout=None)
        self.original_text = original_text

    @discord.ui.button(
        label="🌐",
        style=discord.ButtonStyle.secondary
    )
    async def translate_button(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):
        for role_name, lang_code in ROLE_LANGUAGES.items():
            role = discord.utils.get(interaction.guild.roles, name=role_name)

            if role in interaction.user.roles:
                translated = await traslate_text(self.original_text, lang_code)

                await interaction.response.send_message(
                    f"Tradução para você:\n> {translated}",
                    ephemeral=True
                )
                return

        await interaction.response.send_message(
            "Você não tem cargo de idioma.",
            ephemeral=True
        )

@bot.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return 
    
    if not message.guild:
        return
    
    content = message.content.strip()
    
    if not content:
        return
    
    await message.reply(
           view=TranslateButton(content),
           mention_author=False
            
        )
        
    await bot.process_commands(message)
    

bot.run(TOKEN)
