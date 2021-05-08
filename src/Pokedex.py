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
        # Request
        pkmn_info = json.dumps(r.json())
        pkmn_info_json = json.loads(pkmn_info)
        # Saco sus Habilidades
        if len(pkmn_info_json["abilities"]) == 1:
            habilidad = ""
            hab_req = requests.get(pkmn_info_json["abilities"][0]["ability"]["url"])
            hab_info = json.dumps(hab_req.json())
            hab_json = json.loads(hab_info)
            for x in hab_json["names"]:
                if x["language"]["name"] == "es":
                    habilidad = x["name"]
                    break
            if habilidad == "":
                habilidad = pkmn_info_json["abilities"][0]["ability"]["name"]
        else:
            habilidad = ""
            for x in pkmn_info_json["abilities"]:
                hab_req = requests.get(x["ability"]["url"])
                hab_info = json.dumps(hab_req.json())
                hab_json = json.loads(hab_info)
                habilidad_f = ""
                for x in hab_json["names"]:
                    if x["language"]["name"] == "es":
                        habilidad_f = x["name"]
                        break
                if habilidad_f == "":
                    habilidad_f = pkmn_info_json["abilities"][0]["ability"]["name"]
                if habilidad == "":
                    habilidad = habilidad_f
                else:
                    habilidad = habilidad + ", " + habilidad_f
        return habilidad

def pokemonTipo(pokemon):
    # Pokémon & Pokedex
    r = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon}")
    if r.status_code != 200:
        return f"No existe un Pokémon llamado {pokemon}"
    else:
        pkmn_info = json.dumps(r.json())
        pkmn_info_json = json.loads(pkmn_info)
        # Saco sus Tipos
        if len(pkmn_info_json["types"]) == 1:
            tipo = ""
            tipo_req = requests.get(pkmn_info_json["types"][0]["type"]["url"])
            tipo_info = json.dumps(tipo_req.json())
            tipo_json = json.loads(tipo_info)
            for x in tipo_json["names"]:
                if x["language"]["name"] == "es":
                    tipo = x["name"]
                    break
            if tipo == "":
                tipo = pkmn_info_json["types"][0]["type"]["name"]
        else:
            tipo = ""
            for x in pkmn_info_json["types"]:
                tipo_req = requests.get(x["type"]["url"])
                tipo_info = json.dumps(tipo_req.json())
                tipo_json = json.loads(tipo_info)
                tipo_f = ""
                for x in tipo_json["names"]:
                    if x["language"]["name"] == "es":
                        tipo_f = x["name"]
                        break
                if tipo_f == "":
                    tipo_f = tipo_json["types"][x]["type"]["name"]
                if tipo == "":
                    tipo = tipo_f
                else:
                    tipo = tipo + ", " + tipo_f
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
    # Saco sus egg_groups
        if len(pokemon_json["egg_groups"]) == 1:
            egg_group = ""
            eg_req = requests.get(pokemon_json["egg_groups"][0]["url"])
            eg_info = json.dumps(eg_req.json())
            eg_json = json.loads(eg_info)
            for x in eg_json["names"]:
                if x["language"]["name"] == "es":
                    egg_group = x["name"]
                    break
            if egg_group == "":
                egg_group = pokemon_json["egg_groups"][0]["name"]
        else:
            egg_group = ""
            for x in pokemon_json["egg_groups"]:
                eg_req = requests.get(x["url"])
                eg_info = json.dumps(eg_req.json())
                eg_json = json.loads(eg_info)
                for y in eg_json["names"]:
                    if y["language"]["name"] == "es":
                        egg_group_f = y["name"]
                        break
                if egg_group_f == "":
                    egg_group_f = pokemon_json["egg_groups"][0]["name"]
                if egg_group != "":
                    egg_group = egg_group + ", " + egg_group_f
                else:
                    egg_group = egg_group_f
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
            r_hab = requests.get(pokemon_json["habitat"]["url"])
            hab_req = json.dumps(r_hab.json())
            hab_json = json.loads(hab_req)
            for x in hab_json["names"]:
                if x["language"]["name"] == "es":
                    habitat = x["name"]
                    break
            if habitat == "":
                habitat = pokemon_json["habitat"]["name"]
    # Forma
        forma = ""
        r_form = requests.get(pokemon_json["shape"]["url"])
        form_req = json.dumps(r_form.json())
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

def color_por_tipo(tipo):
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

def cadenaDeEvoluciones(id):
    # Pokémon & Pokedex
    r = requests.get(f"https://pokeapi.co/api/v2/pokemon-species/{id}")
    if r.status_code != 200:
        return f"No existe un Pokémon con la ID {id}"
    else:
        request_a_json = json.dumps(r.json())
        pokemon_json = json.loads(request_a_json)

        r = requests.get(pokemon_json["evolution_chain"]["url"])
        request_a_json = json.dumps(r.json())
        pokemon_json = json.loads(request_a_json)
        id_ev = pokemon_json["id"]
        evo0 = pokemon_json["chain"]["species"]["name"]
        if len(pokemon_json["chain"]["evolves_to"]) != 0:
            evo1 = pokemon_json["chain"]["evolves_to"][0]["species"]["name"]
            evo1_trigger = pokemon_json["chain"]["evolves_to"][0]["evolution_details"][0]["trigger"]["name"]
            evo1_details = ""
            for x in pokemon_json["chain"]["evolves_to"][0]["evolution_details"][0]:
                i = pokemon_json["chain"]["evolves_to"][0]["evolution_details"][0][x]
                if i != None and i != False and i != "" and x != "trigger":
                    if evo1_details == "":
                        i = pokemon_json["chain"]["evolves_to"][0]["evolution_details"][0][x]
                        if x != "held_item" and x !="item" and x != "known_move" and x != "known_move_type" and x != "party_species" and x != "party_type":
                            evo1_details = f"{x}: {i}"
                        else:
                            i = pokemon_json["chain"]["evolves_to"][0]["evolution_details"][0][x]
                            evo1_details = f"{x}: {i}"
                    else:
                        i = pokemon_json["chain"]["evolves_to"][0]["evolution_details"][0][x]
                        if x != "held_item" and x !="item" and x != "known_move" and x != "known_move_type" and x != "party_species" and x != "party_type":
                            evo1_details = f"{evo1_details}\n  {x}: {i}"
                        else:
                            i = pokemon_json["chain"]["evolves_to"][0]["evolution_details"][0][x]
                            evo1_details = f"{evo1_details}\n  {x}: {i}"
        # Traducciones
            evo1_details = evo1_details.replace("gender", "Género")
            evo1_details = evo1_details.replace("held_item", "Objeto Equipado")
            evo1_details = evo1_details.replace("item", "Objeto")
            evo1_details = evo1_details.replace("known_move", "Movimiento")
            evo1_details = evo1_details.replace("known_move_type", "Tipo de Movimiento")
            evo1_details = evo1_details.replace("location", "Ubicación")
            evo1_details = evo1_details.replace("min_affection", "Amistad")
            evo1_details = evo1_details.replace("min_beauty", "Belleza")
            evo1_details = evo1_details.replace("min_happiness", "Felicidad")
            evo1_details = evo1_details.replace("min_level", "Nivel")
            evo1_details = evo1_details.replace("needs_overworld_rain", "Necesita lluvia")
            evo1_details = evo1_details.replace("party_species", "Pokémon en Equipo")
            evo1_details = evo1_details.replace("party_type", "Tipo en Equipo")
            evo1_details = evo1_details.replace("relative_physical_stats", "Stats relativas")
            evo1_details = evo1_details.replace("time_of_day", "Hora")
            evo1_details = evo1_details.replace("trade_species", "Intercambio")
        # Check otra evo
            if len(pokemon_json["chain"]["evolves_to"][0]["evolves_to"]) != 0:
                evo2 = pokemon_json["chain"]["evolves_to"][0]["evolves_to"][0]["species"]["name"]
                evo2_trigger = pokemon_json["chain"]["evolves_to"][0]["evolves_to"][0]["evolution_details"][0]["trigger"]["name"]
                evo2_details = ""
                for x in pokemon_json["chain"]["evolves_to"][0]["evolves_to"][0]["evolution_details"][0]:
                    i = pokemon_json["chain"]["evolves_to"][0]["evolves_to"][0]["evolution_details"][0][x]
                    if i != None and i != False and i != "" and x != "trigger":
                        if evo2_details == "":
                            i = pokemon_json["chain"]["evolves_to"][0]["evolves_to"][0]["evolution_details"][0][x]
                            if x != "held_item" and x !="item" and x != "known_move" and x != "known_move_type" and x != "party_species" and x != "party_type":
                                evo2_details = f"{x}: {i}"
                            else:
                                i = pokemon_json["chain"]["evolves_to"][0]["evolves_to"][0]["evolution_details"][0][x]["name"]
                                evo2_details = f"{x}: {i}"
                        else:
                            i = pokemon_json["chain"]["evolves_to"][0]["evolves_to"][0]["evolution_details"][0][x]
                            if x != "held_item" and x !="item" and x != "known_move" and x != "known_move_type" and x != "party_species" and x != "party_type":
                                evo2_details = f"{evo2_details}\n  {x}: {i}"
                            else:
                                i = pokemon_json["chain"]["evolves_to"][0]["evolves_to"][0]["evolution_details"][0][x]["name"]
                                evo2_details = f"{evo2_details}\n  {x}: {i}"
            # Traducciones
                evo2_details = evo2_details.replace("gender", "Género")
                evo2_details = evo2_details.replace("held_item", "Objeto Equipado")
                evo2_details = evo2_details.replace("item", "Objeto")
                evo2_details = evo2_details.replace("known_move", "Movimiento")
                evo2_details = evo2_details.replace("known_move_type", "Tipo de Movimiento")
                evo2_details = evo2_details.replace("location", "Ubicación")
                evo2_details = evo2_details.replace("min_affection", "Amistad")
                evo2_details = evo2_details.replace("min_beauty", "Belleza")
                evo2_details = evo2_details.replace("min_happiness", "Felicidad")
                evo2_details = evo2_details.replace("min_level", "Nivel")
                evo2_details = evo2_details.replace("needs_overworld_rain", "Necesita lluvia")
                evo2_details = evo2_details.replace("party_species", "Pokémon en Equipo")
                evo2_details = evo2_details.replace("party_type", "Tipo en Equipo")
                evo2_details = evo2_details.replace("relative_physical_stats", "Stats relativas")
                evo2_details = evo2_details.replace("time_of_day", "Hora")
                evo2_details = evo2_details.replace("trade_species", "Intercambio")
            # returns
                evo1_details = f"{evo1_details}\nTrigger: {evo1_trigger}"
                evo2_details = f"{evo2_details}\nTrigger: {evo2_trigger}"
                return [evo0, evo1, evo1_details, evo2, evo2_details]
            else:
                return [evo0, evo1, evo1_details]
        else:
            return "No posee una cadena evolutiva"
