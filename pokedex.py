import requests

url = "https://pokeapi.co/api/v2/pokemon"
resp = requests.get(url, timeout=10)

def buscar_pokemon(pokemon: str, timeout: int=10) -> dict | None:
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
    