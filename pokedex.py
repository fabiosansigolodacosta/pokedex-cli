import requests
import json
from datetime import datetime

def buscar_pokemon(pokemon: str, timeout: int = 10) -> dict | None:
    pokemon_tratado = pokemon.strip().lower().replace(" ", "-")

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
    
def main():
    pokedex = []
    ids_pokemons = []
    while True:
        pokemon = input("Digite o nome ou número do Pokémon (ou 'sair'): ")
        pokemon = pokemon.lower().strip()
        if pokemon == "sair":
            if len(ids_pokemons) == 0:
                print("Saindo. Nenhum pokemon salvo")
                break

            if salvar_json(pokedex):
                print(f"{len(ids_pokemons)} pokémons salvos em pokedex.json")
                break

            else:
                print("Os dados não foram salvos, tente sair novamente.")
                continue

        dados_pokemon = buscar_pokemon(pokemon)
        if dados_pokemon:
            campos = extrair_campos(dados_pokemon)
            if campos["id"] not in ids_pokemons:
                ids_pokemons.append(campos["id"])
                pokedex.append(campos)
                print(f"{campos['nome']} | tipos: {', '.join(campos['tipos'])} | habilidades: {', '.join(campos['habilidades'])}")


if __name__ == "__main__":
    main()
