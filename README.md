# pokedex-cli

CLI (Interface de Linha de Comando) em Python que busca pokémons na PokeAPI por nome ou número e salva os resultados em um arquivo JSON. Os principais erros da requisição (nome inexistente, timeout, falta de conexão e erros do servidor) são tratados com mensagens claras para o usuário.

## Demonstração

```text
Digite o nome ou número do Pokémon (ou 'sair'): pikachu
pikachu | tipos: electric | habilidades: static, lightning-rod
Digite o nome ou número do Pokémon (ou 'sair'): xyzw
Pokémon 'xyzw' não encontrado. Verifique a grafia.
Digite o nome ou número do Pokémon (ou 'sair'):       
Digite um nome ou ID.
Digite o nome ou número do Pokémon (ou 'sair'): charizard
charizard | tipos: fire, flying | habilidades: blaze, solar-power
Digite o nome ou número do Pokémon (ou 'sair'): charmeleon
charmeleon | tipos: fire | habilidades: blaze, solar-power
Digite o nome ou número do Pokémon (ou 'sair'): sair
3 pokémons salvos em pokedex.json
```

## O que ele faz

- Busca um Pokémon pelo nome ou pelo número na PokeAPI
- Extrai id, nome, altura, peso, tipos, habilidades e hp
- Trata erros de nome inexistente, timeout, falta de conexão e outros erros HTTP
- Evita Pokémon repetidos na mesma sessão
- Ao digitar `sair`, salva tudo em `pokedex.json`

## Pré-requisitos

- Python (versão que você usou, confira com `python --version`)
- Conexão com a internet

## Instalação e execução

```bash
git clone https://github.com/SEU_USUARIO/pokedex-cli.git
cd pokedex-cli
python -m venv .venv
.venv\Scripts\activate        # Linux/Mac: source .venv/bin/activate
pip install -r requirements.txt
python pokedex.py
```

## Como usar

- Digite o nome (`pikachu`) ou o número (`25`) de um Pokémon e tecle Enter
- Nomes compostos funcionam com espaço ou hífen (`mr mime` ou `mr-mime`)
- Digite `sair` para encerrar e gerar o arquivo

## Formato de saída

O arquivo `pokedex.json` é criado na pasta em que você rodou o programa. Veja um exemplo completo em `exemplo_saida.json`.

```json
{
  "gerado_em": "2026-11-07T12:41:09",
  "total": 1,
  "pokemons": [
    {
      "id": 25,
      "nome": "pikachu",
      "altura_m": 0.4,
      "peso_kg": 6.0,
      "tipos": ["electric"],
      "habilidades": ["static", "lightning-rod"],
      "hp": 35
    }
  ]
}
```

| Campo | Descrição |
|---|---|
| `altura_m` | altura em metros (a API devolve em decímetros) |
| `peso_kg` | peso em quilos (a API devolve em hectogramas) |
| (os demais) | (descreva em poucas palavras) |

## Tratamento de erros

| Situação | O que acontece |
|---|---|
| Pokémon inexistente (404) | avisa para verificar a grafia e continua |
| Servidor demorou (timeout) | avisa e continua |
| Sem internet | avisa e continua |
| Outro erro HTTP | mostra o código do erro e continua |
| Entrada vazia | pede de novo, sem chamar a API |
| Falha ao salvar o arquivo | avisa que nada foi salvo e permite tentar `sair` de novo |

## Limitações conhecidas

- (Ex.: alguns nomes têm grafia própria na API, como `mime-jr` e `farfetchd`)
- (Ex.: o arquivo é sobrescrito a cada execução)

## API utilizada

[PokeAPI](https://pokeapi.co/):