import requests
import json
from datetime import datetime

url = "https://pokeapi.co/api/v2/pokemon"

def buscar_pokemon(pokemon: str, timeout: int = 10) -> dict | None:
    pokemon_tratado = pokemon.strip().lower()

    if not pokemon_tratado:
        print("Digite um nome ou ID.")
        return None
    
    try:
        resp = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon_tratado}", timeout=timeout)
        resp.raise_for_status()
        return resp.json()
    
    except requests.exceptions.Timeout:
        print("O servidor demorou a responder. Tente de novo.")

    except requests.exceptions.ConnectionError:
        print("Sem conexão com a internet.")

    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            print(f"Pokémon '{pokemon_tratado}' não encontrado. Verifique a grafia.")
        else:
            print(f"Erro HTTP {e.response.status_code}.")

    except requests.exceptions.RequestException as e:
        print(f"Erro inesperado: {e}")

    return None



def extrair_campos(dados: dict) -> dict:
    tipos = []
    hp = None
    for item in dados["types"]:
        tipos.append(item["type"]["name"])

    habilidades = []
    for item in dados["abilities"]:
        ability = item["ability"]["name"]
        habilidades.append(ability)

    for item in dados["stats"]:
        if item["stat"]["name"] == "hp":
            hp = item["base_stat"]
            break

   

    return {
        "id": dados["id"],
        "nome": dados["name"],
        "altura_m": dados["height"] / 10,    
        "peso_kg": dados["weight"] / 10,
        "tipos": tipos,
        "habilidades": habilidades,
        "hp": hp,
    }

def salvar_json(pokemons: list[dict], nome_arquivo: str = "pokedex.json") -> bool:
    dic_json = {
        "gerado_em": datetime.now().isoformat(timespec="seconds"),
        "total": len(pokemons),
        "pokemons": pokemons
    }

    try:
        with open(nome_arquivo, "w", encoding="utf-8") as arquivo:
            json.dump(dic_json, arquivo, indent=2, ensure_ascii=False)
        return True

    except OSError as e:
        print(f"Falha ao gerar o arquivo: {e}")
        return False
    

