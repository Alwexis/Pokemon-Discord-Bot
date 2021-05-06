# Imports
import discord
import requests
import json
import random
from funciones import pokemonStats
from funciones import pokemonInfo
from funciones import pokemonDesc
from funciones import pokemonCriar

# Discord & Intents
client = discord.Client()
intents = discord.Intents.default()
intents.members = True
intents.messages = True
intents.integrations = True

# Evento on_ready
@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith(';pokedex'):
        # Pokémon & Pokedex
        if len(message.content.split(" ")) <= 1:
            await message.reply("""Por favor menciona un Pokémon válido. Puedes utilizar el parámetro `-r` para que este sea uno random.
__`Parámetros`__:
    `-r` = Pokémon Random
    `-i` = Información Extendida del Pokémon
    `-c` = Información de Crianza.""")
        else:
            pokemon = message.content.lower().replace(";pokedex ", "")
            if "-r" in pokemon:
                random_pokemon = True
            else:
                random_pokemon = False
            if "-c" in pokemon:
                pokemon = pokemon.replace(" -c", "")
                display_crianza = True
            else:
                display_crianza = False
            if "-i" in pokemon:
                pokemon = pokemon.replace(" -i", "")
                display_info = True
            else:
                display_info = False
            if " " in pokemon:
                pokemon = pokemon.replace(" ", "-")
            if "'" in pokemon:
                pokemon = pokemon.replace("'", "")
            if random_pokemon == False:
                r = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon}")
            else:
                r2 = requests.get(f"https://pokeapi.co/api/v2/pokemon?offset=1&limit=1116")
                request2_a_json = json.dumps(r2.json())
                pokemon2_json = json.loads(request2_a_json)
                pokemon = pokemon2_json["results"][random.randint(0, 1115)]["name"]
                r = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon}")
            if r.status_code != 200:
                await message.reply(f"No existe un pokémon llamado {pokemon}", mention_author=False)
            else:
                request_a_json = json.dumps(r.json())
                pokemon_json = json.loads(request_a_json)
                stats = pokemonStats(pokemon)
                info = pokemonInfo(pokemon)
                pokedex = pokemon_json["id"]
                desc = pokemonDesc(pokedex)
                crianza = pokemonCriar(pokedex)
                if random_pokemon == False:
                    titulo = f"Pokémon {pokemon} ({pokedex})"
                else:
                    titulo = f"(RANDOM) Pokémon {pokemon} ({pokedex})"
            # Embeds
                embed = discord.Embed(title=titulo, url=f"https://www.pokemon.com/el/pokedex/{pokemon}", description=desc, color=0xeb4034)
                embed.set_author(name=message.author.display_name, url="", icon_url=message.author.avatar_url)
                embed.set_thumbnail(url=pokemon_json["sprites"]["other"]["official-artwork"]["front_default"])
                embed.add_field(name="Estadísticas", value=stats, inline=False)
                if display_info == True:
                    embed.add_field(name="Información", value=info, inline=False)
                if display_crianza == True:
                    embed.add_field(name="Crianza", value=crianza, inline=False)
                embed.set_footer(text="Pokédex by Alexis", icon_url="https://images.wikidexcdn.net/mwuploads/wikidex/2/2e/latest/20171012163310/RotomDex_USUL.png")
                await message.reply(embed=embed, mention_author=False)

client.run('TOKEN')
