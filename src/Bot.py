# Imports
import discord
import requests
import json
import random

from Pokedex import *

# Discord & Intents
client = discord.Client()
intents = discord.Intents.default()
intents.members = True
intents.messages = True
intents.integrations = True

# Evento on_ready
@client.event
async def on_ready():
    print('Inicié sesión con el nombre {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    # Pokedex Command
    if message.content.startswith(';pokedex'):
        # Pokémon & Pokedex
        if len(message.content.split(" ")) <= 1:
            await message.reply("Por favor menciona un Pokémon válido.\n__`Parámetros`__:\n    `-i` = Información Extendida del Pokémon\n    `-c` = Información de Crianza.",
            mention_author=False)
        else:
            pokemon = message.content.lower().replace(";pokedex ", "")
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
            r = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon}")
            if r.status_code != 200:
                await message.reply(f"No existe un pokémon llamado {pokemon}", mention_author=False)
            else:
                request_a_json = json.dumps(r.json())
                pokemon_json = json.loads(request_a_json)
                stats = pokemonStats(pokemon)
                info = pokemonInfo(pokemon)
                pokedex = pokemon_json["id"]
                color = color_por_tipo(pokemon_json["types"][0]["type"]["name"])
                desc = pokemonDesc(pokedex)
                crianza = pokemonCriar(pokedex)
            # Embeds
                embed = discord.Embed(title=f"Pokémon {pokemon} ({pokedex})", url=f"https://www.pokemon.com/el/pokedex/{pokemon}", description=desc, color=color)
                embed.set_author(name=message.author.display_name, url="", icon_url=message.author.avatar_url)
                embed.set_thumbnail(url=pokemon_json["sprites"]["other"]["official-artwork"]["front_default"])
                embed.add_field(name="Estadísticas", value=stats, inline=False)
                if display_info == True:
                    embed.add_field(name="Información", value=info, inline=False)
                if display_crianza == True:
                    embed.add_field(name="Crianza", value=crianza, inline=False)
                evoluciones = cadenaDeEvoluciones(pokedex)
                if evoluciones != "No posee una cadena evolutiva":
                    embed.add_field(name="Cadena Evolutiva:", value=f"Cadena evolutiva del Pokémon `{pokemon}`", inline=False)
                    embed.add_field(name=evoluciones[0], value=f"No hay información sobre una pre-evolución.\n\n[Wiki](https://www.pokemon.com/el/pokedex/{evoluciones[0]})", inline=True)
                    if len(evoluciones) > 2:
                        embed.add_field(name=evoluciones[1], value=f"{evoluciones[2]}\n\n[Wiki](https://www.pokemon.com/el/pokedex/{evoluciones[1]})")
                        if len(evoluciones) > 4:
                            embed.add_field(name=evoluciones[3], value=f"{evoluciones[4]}\n\n[Wiki](https://www.pokemon.com/el/pokedex/{evoluciones[3]})")
                embed.set_footer(text="Pokédex by Alexis", icon_url="https://images.wikidexcdn.net/mwuploads/wikidex/2/2e/latest/20171012163310/RotomDex_USUL.png")
                await message.reply(embed=embed, mention_author=False)
    # Items Command
    
    # Berries Command

    # TMs and MOs Command

    # Breeding Info command

    # Type Chart

    # Who's that Pokémon game

client.run('TOKEN')
