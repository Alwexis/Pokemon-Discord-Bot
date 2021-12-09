# Imports
from asyncio.windows_events import NULL
import requests
import json

def getPokemon(pokemon, species = False):
    # Pokémon & Pokedex
    if species == False:
        r = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon}")
        if r.status_code != 200:
            return None
        else:
            request_a_json = json.dumps(r.json())
            pokemon_json = json.loads(request_a_json)
            return pokemon_json
    else:
        r = requests.get(f"https://pokeapi.co/api/v2/pokemon-species/{pokemon}")
        if r.status_code != 200:
            return None
        else:
            request_a_json = json.dumps(r.json())
            pokemon_json = json.loads(request_a_json)
            return pokemon_json

def getStats(pokemon):
    # Pokémon & Pokedex
    pokemon_json = getPokemon(pokemon)
    # Saco sus Habilidades
    return f"""`HP`: {pokemon_json["stats"][0]["base_stat"]}
        `Ataque`: {pokemon_json["stats"][1]["base_stat"]}
        `Defensa`: {pokemon_json["stats"][2]["base_stat"]}
        `Ataque Especial`: {pokemon_json["stats"][3]["base_stat"]}
        `Defensa Especial`: {pokemon_json["stats"][4]["base_stat"]}
        `Velocidad`: {pokemon_json["stats"][5]["base_stat"]}"""

def getHabilidades(pokemon):
    # Pokémon & Pokedex
    pkmn_info_json = getPokemon(pokemon)
    # Saco sus Habilidades
    habilidad = ""
    for x in (pkmn_info_json["abilities"]):
        hab_req = json.dumps(requests.get(x["ability"]["url"]).json())
        hab_json = json.loads(hab_req)
        for y in (hab_json["names"]):
            if y["language"]["name"] == "es":
                habilidad += f"{y['name']}, "
                break
    if habilidad.endswith(", "):
        habilidad = habilidad[:-2]
    return habilidad

def getTipos(pokemon):
    # Pokémon & Pokedex
    pkmn_info_json = getPokemon(pokemon)
    # Saco sus tipos
    tipos = ""
    for x in (pkmn_info_json["types"]):
        tipo_req = json.dumps(requests.get(x["type"]["url"]).json())
        tipo_json = json.loads(tipo_req)
        for y in (tipo_json["names"]):
            if y["language"]["name"] == "es":
                tipos += f"{y['name']}, "
                break
    if tipos.endswith(", "):
        tipos = tipos[:-2]
    return tipos

def getInfo(pokemon):
    # Pokémon & Pokedex
    pokemon_json = getPokemon(pokemon)
    # Saco sus Habilidades
    return f"""`Habilidades`: {getHabilidades(pokemon)}
    `Tipo(s)`: {getTipos(pokemon)}
    `Nro Pokedex`: {pokemon_json["id"]}
    `EXP Base`: {pokemon_json["base_experience"]}
    `Tamaño`: {pokemon_json["height"] / 10} m
    `Peso`: {pokemon_json["weight"] / 10} kg
    {getInfoExtra(pokemon_json["id"])}
    """

def getDesc(id):
    # Pokémon & Pokedex
    pokemon_json = getPokemon(id, True)
    # Saco su info varia
    # Español
    for x in (pokemon_json["flavor_text_entries"]):
        if (x["language"]["name"] == "es"):
            return x["flavor_text"].replace("\n", " ")
    # Inglés
    for x in (pokemon_json["flavor_text_entries"]):
        if (x["language"]["name"] == "en"):
            return x["flavor_text"].replace("\n", " ")
    return "No se ha podido encontrar una descripción de este pokémon en Español ni tampoco en Inglés."

def getCrianza(id):
    # Pokémon & Pokedex
    pokemon_json = getPokemon(id, True)
    # Saco sus egg_groups
    egg_groups = ""
    for x in (pokemon_json["egg_groups"]):
        egg_req = json.dumps(requests.get(x["url"]).json())
        egg_json = json.loads(egg_req)
        for y in (egg_json["names"]):
            if y["language"]["name"] == "es":
                egg_groups += f"{y['name']}, "
                break
    if egg_groups.endswith(", "):
        egg_groups = egg_groups[:-2]
    # Saco su gender_rate
    if pokemon_json["gender_rate"] == 0 or pokemon_json["gender_rate"] == 1:
        rate_macho = "100%"
        rate_hembra = "0%"
    elif pokemon_json["gender_rate"] == 2 or pokemon_json["gender_rate"] == 3:
        rate_macho = "87.5%"
        rate_hembra = "12.5%"
    elif pokemon_json["gender_rate"] >= 4 and pokemon_json["gender_rate"] <= 7:
        rate_macho = "75%"
        rate_hembra = "25%"
    elif pokemon_json["gender_rate"] >= 8 and pokemon_json["gender_rate"] <= 11:
        rate_macho = "50%"
        rate_hembra = "50%"
    elif pokemon_json["gender_rate"] >= 12 and pokemon_json["gender_rate"] <= 15:
        rate_macho = "25%"
        rate_hembra = "75%"
    else:
        rate_macho = "NaN"
        rate_hembra = "NaN"
    # Saco el growth_rate
    growth_rate = traducir("growthrate", pokemon_json["growth_rate"]["name"])
    # Saco el hatch_counter
    hatch_counter = pokemon_json["hatch_counter"]
    return f"""`Grupos de Huevo`: {egg_groups}
    `Pasos para Eclosionar`: {hatch_counter * 250}
    `Ratio Crecimiento`: {growth_rate}
    `Ratio Macho`: {rate_macho}
    `Ratio Hembra`: {rate_hembra}"""

def getInfoExtra(id):
    # Pokémon & Pokedex
    pokemon_json = getPokemon(id, True)
    # Saco la info
    base_happiness = pokemon_json["base_happiness"]
    capture_rate = pokemon_json["capture_rate"]
    # Tipo Español
    tipo = ""
    for x in pokemon_json["genera"]:
        if x["language"]["name"] == "es":
            tipo = x["genus"]
            break
    # Tipo Inglés
    if tipo == "":
        for x in pokemon_json["genera"]:
            if x["language"]["name"] == "en":
                tipo = x["genus"]
                break
    # Generacion
    generation = pokemon_json["generation"]["name"].upper().replace("GENERATION-", "")
    # Habitat
    if pokemon_json["habitat"] == None:
        habitat = "Ninguno"
    else:
        habitat = ""
        hab_req = json.dumps(requests.get(pokemon_json["habitat"]["url"]).json())
        hab_json = json.loads(hab_req)
        for x in hab_json["names"]:
            if x["language"]["name"] == "es":
                habitat = x["name"]
                break
        if habitat == "":
            habitat = pokemon_json["habitat"]["name"]
    # Forma
    forma = ""
    form_req = json.dumps(requests.get(pokemon_json["shape"]["url"]).json())
    form_json = json.loads(form_req)
    for x in form_json["names"]:
        if x["language"]["name"] == "es":
            forma = x["name"]
            break
    if forma == "":
        forma = pokemon_json["shape"]["name"]
    # Return
    return f"""`Felicidad Base`: {base_happiness}
    `Ratio Captura`: {capture_rate}
    `Tipo`: {tipo}
    `Generación`: {generation}
    `Habitat`: {habitat}
    `Forma`: {forma}"""

def getCadenaEvolucion(id):
    # Pokémon & Pokedex
    pkmn_json = getPokemon(id, True)
    request_a_json = json.dumps(requests.get(pkmn_json["evolution_chain"]["url"]).json())
    pokemon_json = json.loads(request_a_json)
    evoluciones = [pokemon_json["chain"]["species"]["name"]]
    if len(pokemon_json["chain"]["evolves_to"]) > 0:
        evoluciones.append(pokemon_json["chain"]["evolves_to"][0]["species"]["name"])
        for x in pokemon_json["chain"]["evolves_to"][0]["evolution_details"][0]:
            e = pokemon_json["chain"]["evolves_to"][0]["evolution_details"][0][x]
            if e != False and e != None and e != "" and x != "trigger":
                evolucion_detalle = f"{traducir('evtrigger', x)}: {e}"
                evoluciones.append(evolucion_detalle)
        if (len(pokemon_json["chain"]["evolves_to"][0]["evolves_to"])):
            evoluciones.append(pokemon_json["chain"]["evolves_to"][0]["evolves_to"][0]["species"]["name"])
            for y in pokemon_json["chain"]["evolves_to"][0]["evolves_to"][0]["evolution_details"][0]:
                i = pokemon_json["chain"]["evolves_to"][0]["evolves_to"][0]["evolution_details"][0][y]
                if i != False and i != None and i != "" and y != "trigger":
                    evolucion_detalle2 = f"{traducir('evtrigger', y)}: {i}"
                    evoluciones.append(evolucion_detalle2)
        return evoluciones
    else:
        return "No posee una cadena evolutiva"

def traducir(tipo, texto):
    if tipo == "growthrate":
        if texto == "slow":
            return "Lento"
        elif texto == "medium":
            return "Medio"
        elif texto == "fast":
            return "Rápido"
        elif texto == "medium-slow":
            return "Medio lento"
        elif texto == "slow then very fast":
            return "Lento, luego rápido"
        elif texto == "fast then very slow":
            return "Rápido, luego lento"
        else:
            return "No se ha podido traducir"
    elif tipo == "evtrigger":
        textoNuevo = texto
        textoNuevo = textoNuevo.replace("gender", "Género")
        textoNuevo = textoNuevo.replace("held_item", "Objeto Equipado")
        textoNuevo = textoNuevo.replace("item", "Objeto")
        textoNuevo = textoNuevo.replace("known_move", "Movimiento")
        textoNuevo = textoNuevo.replace("known_move_type", "Tipo de Movimiento")
        textoNuevo = textoNuevo.replace("location", "Ubicación")
        textoNuevo = textoNuevo.replace("min_affection", "Amistad")
        textoNuevo = textoNuevo.replace("min_beauty", "Belleza")
        textoNuevo = textoNuevo.replace("min_happiness", "Felicidad")
        textoNuevo = textoNuevo.replace("min_level", "Nivel")
        textoNuevo = textoNuevo.replace("level-up", "Nivel")
        textoNuevo = textoNuevo.replace("needs_overworld_rain", "Necesita lluvia")
        textoNuevo = textoNuevo.replace("party_species", "Pokémon en Equipo")
        textoNuevo = textoNuevo.replace("party_type", "Tipo en Equipo")
        textoNuevo = textoNuevo.replace("relative_physical_stats", "Stats relativas")
        textoNuevo = textoNuevo.replace("time_of_day", "Hora")
        textoNuevo = textoNuevo.replace("trade_species", "Intercambio")
        return textoNuevo

def getColor(tipo):
    if tipo.startswith("steel"):
        return 0xAFACBB
    if tipo.startswith("water"):
        return 0x3A97EC
    if tipo.startswith("bug"):
        return 0xAAB73C
    if tipo.startswith("dragon"):
        return 0x7B67D2
    if tipo.startswith("electric"):
        return 0xFFDF80
    if tipo.startswith("ghost"):
        return 0x6B6899
    if tipo.startswith("fire"):
        return 0xF74926
    if tipo.startswith("fairy"):
        return 0xFEACFF
    if tipo.startswith("ice"):
        return 0x85D7F0
    if tipo.startswith("fighting"):
        return 0xB9594E
    if tipo.startswith("normal"):
        return 0xC1BBB7
    if tipo.startswith("grass"):
        return 0x7FC862
    if tipo.startswith("psychic"):
        return 0xDE6590
    if tipo.startswith("rock"):
        return 0xBBAA69
    if tipo.startswith("dark"):
        return 0x69574B
    if tipo.startswith("ground"):
        return 0xD9BC58
    if tipo.startswith("poison"):
        return 0xAA5E9C
    if tipo.startswith("flying"):
        return 0x7298E0
