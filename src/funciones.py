# Imports
import requests
import json

def pokemonStats(pokemon):
    # Pokémon & Pokedex
    r = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon}")
    if r.status_code != 200:
        return f"No existe un Pokémon llamado {pokemon}"
    else:
        request_a_json = json.dumps(r.json())
        pokemon_json = json.loads(request_a_json)
        # Saco sus Habilidades
        return f"""`HP`: {pokemon_json["stats"][0]["base_stat"]}
        `Ataque`: {pokemon_json["stats"][1]["base_stat"]}
        `Defensa`: {pokemon_json["stats"][2]["base_stat"]}
        `Ataque Especial`: {pokemon_json["stats"][3]["base_stat"]}
        `Defensa Especial`: {pokemon_json["stats"][4]["base_stat"]}
        `Velocidad`: {pokemon_json["stats"][5]["base_stat"]}"""

def pokemonHabilidades(pokemon):
    # Pokémon & Pokedex
    r = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon}")
    if r.status_code != 200:
        return f"No existe un Pokémon llamado {pokemon}"
    else:
        request_a_json = json.dumps(r.json())
        pokemon_json = json.loads(request_a_json)
        # Saco sus Habilidades
        if len(pokemon_json["abilities"]) == 1:
            habilidad = pokemon_json["abilities"][0]["ability"]["name"]
        else:
            habilidad = ""
            for x in pokemon_json["abilities"]:
                if habilidad != "":
                    habilidad = habilidad + ", " + x["ability"]["name"]
                else:
                    habilidad = x["ability"]["name"]
        return habilidad

def pokemonTipo(pokemon):
    # Pokémon & Pokedex
    r = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon}")
    if r.status_code != 200:
        return f"No existe un Pokémon llamado {pokemon}"
    else:
        request_a_json = json.dumps(r.json())
        pokemon_json = json.loads(request_a_json)
        # Saco sus Tipos
        if len(pokemon_json["types"]) == 1:
            tipo = pokemon_json["types"][0]["type"]["name"]
        else:
            tipo = ""
            for x in pokemon_json["types"]:
                if tipo != "":
                    tipo = tipo + ", " + x["type"]["name"]
                else:
                    tipo = x["type"]["name"]
        return tipo

def pokemonInfo(pokemon):
    # Pokémon & Pokedex
    r = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon}")
    if r.status_code != 200:
        return f"No existe un Pokémon llamado {pokemon}"
    else:
        request_a_json = json.dumps(r.json())
        pokemon_json = json.loads(request_a_json)
        # Saco sus Habilidades
        return f"""`Habilidades`: {pokemonHabilidades(pokemon)}
        `Tipo(s)`: {pokemonTipo(pokemon)}
        `Nro Pokedex`: {pokemon_json["id"]}
        `EXP Base`: {pokemon_json["base_experience"]}
        `Tamaño`: {pokemon_json["height"] / 10} m
        `Peso`: {pokemon_json["weight"] / 10} kg
        {pokemonInfo2(pokemon_json["id"])}
        """

def pokemonDesc(id):
    # Pokémon & Pokedex
    r = requests.get(f"https://pokeapi.co/api/v2/pokemon-species/{id}")
    if r.status_code != 200:
        return f"No existe un Pokémon con la ID {id}"
    else:
        request_a_json = json.dumps(r.json())
        pokemon_json = json.loads(request_a_json)
        # Saco su info varia
        limit = len(pokemon_json["flavor_text_entries"])
        # Español
        for x in range(limit - 1):
            if len(pokemon_json["flavor_text_entries"]) - 1 >= x:
                if pokemon_json["flavor_text_entries"][x]["language"]["name"] == "es":
                    desc = pokemon_json["flavor_text_entries"][x]["flavor_text"].replace("\n", " ")
                    info = f"""Descripción del Juego Pokémon: __`{pokemon_json["flavor_text_entries"][x]["version"]["name"]}`__
                    Idioma: __`Español`__

                    _{desc}_

                    """
                    return info
                    break
                    exit()
            else:
                break
        # Inglés
        for x in range(limit - 1):
            if len(pokemon_json["flavor_text_entries"]) - 1 >= x:
                if pokemon_json["flavor_text_entries"][x]["language"]["name"] == "en":
                    desc = pokemon_json["flavor_text_entries"][x]["flavor_text"].replace("\n", " ")
                    info = f"""Descripción del Juego Pokémon: __`{pokemon_json["flavor_text_entries"][x]["version"]["name"]}`__
                    Idioma: __`Inglés`__

                    _{desc}_

                    """
                    return info
                    break
                    exit()
            else:
                return "No se ha podido encontrar una descripción de este pokémon en Español ni tampoco en Inglés."
                break
                exit()

def pokemonCriar(id):
    # Pokémon & Pokedex
    r = requests.get(f"https://pokeapi.co/api/v2/pokemon-species/{id}")
    if r.status_code != 200:
        return f"No existe un Pokémon con la ID {id}"
    else:
        request_a_json = json.dumps(r.json())
        pokemon_json = json.loads(request_a_json)
        # Saco su Info
        #egg_groups
        #gender_rate
        #growth_rate
        #hatch_counter
    # Saco sus egg_groups
        if len(pokemon_json["egg_groups"]) == 1:
            egg_group = pokemon_json["egg_groups"][0]["name"]
        else:
            egg_group = ""
            for x in pokemon_json["egg_groups"]:
                if egg_group != "":
                    egg_group = egg_group + ", " + x["name"]
                else:
                    egg_group = x["name"]
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
        growth_rate = pokemon_json["growth_rate"]["name"]
    # Saco el hatch_counter
        hatch_counter = pokemon_json["hatch_counter"]
        return f"""`Grupos de Huevo`: {egg_group}
        `Pasos para Eclosionar`: {hatch_counter * 250}
        `Ratio Crecimiento`: {growth_rate}
        `Ratio Macho`: {rate_macho}
        `Ratio Hembra`: {rate_hembra}"""

def pokemonInfo2(id):
    # Pokémon & Pokedex
    r = requests.get(f"https://pokeapi.co/api/v2/pokemon-species/{id}")
    if r.status_code != 200:
        return f"No existe un Pokémon con la ID {id}"
    else:
        request_a_json = json.dumps(r.json())
        pokemon_json = json.loads(request_a_json)
    # Saco la info
        base_happiness = pokemon_json["base_happiness"]
        capture_rate = pokemon_json["capture_rate"]
        # Tipo Español
        for x in pokemon_json["genera"]:
            if x["language"]["name"] == "es":
                tipo = x["genus"]
                break
        # Tipo Inglés
        for x in pokemon_json["genera"]:
            if x["language"]["name"] == "en":
                tipo = x["genus"]
                break
        # Generacion
        generation = pokemon_json["generation"]["name"].upper().replace("GENERATION-", "")
        if pokemon_json["habitat"] == None:
            habitat = "Ninguno"
        else:
            habitat = pokemon_json["habitat"]["name"]
        forma = pokemon_json["shape"]["name"]
        return f"""`Felicidad Base`: {base_happiness}
        `Ratio Captura`: {capture_rate}
        `Tipo`: {tipo}
        `Generación`: {generation}
        `Habitat`: {habitat}
        `Forma`: {forma}"""
