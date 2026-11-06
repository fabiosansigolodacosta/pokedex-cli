# pokedex-cli

CLI (Interface de Linha de Comando) em Python que busca pokémons na PokeAPI por nome ou número e salva os resultados em um arquivo JSON. Os principais erros da requisição (nome inexistente, timeout, falta de conexão e erros do servidor) são tratados com mensagens claras para o usuário.

Este é o primeiro projeto do meu plano de estudos de IA e automações. O objetivo foi praticar a base de tudo o que vem depois: requisições HTTP, JSON, tratamento de erros, ambiente virtual e Git. Os próximos projetos usam bancos de dados (Supabase), automações (n8n) e agentes de IA.

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

- Desenvolvido com Python 3.14.3; a sintaxe usada exige 3.10 ou superior
- Conexão com a internet

## Instalação e execução

```bash
git clone https://github.com/fabiosansigolodacosta/pokedex-cli.git
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
| `id` | código numérico que representa o pokémon |
| `nome` | nome do pokémon |
| `altura_m` | altura em metros (a API devolve em decímetros) |
| `peso_kg` | peso em quilos (a API devolve em hectogramas) |
| `tipos` | todos os tipos do pokémon |
| `habilidades` | todas as habilidades do pokémon |
| `hp` | quantidade de vida |

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

- Alguns nomes têm grafia própria na API (ex.: `mime-jr`, `farfetchd`). Se o nome não for exatamente o da API, o resultado é "não encontrado"; nesse caso, use o número do Pokémon.
- O arquivo `pokedex.json` é sobrescrito a cada execução, então os dados de sessões anteriores não são mantidos.
- Os dados só são gravados quando você digita `sair`. Se o programa for interrompido antes, a sessão se perde.
- Em caso de timeout ou falha de conexão, o programa avisa mas não tenta de novo sozinho.
- Não há testes automatizados: os cenários foram verificados manualmente.

## API utilizada

[PokeAPI](https://pokeapi.co/): gratuita e sem necessidade de chave.

## Estrutura do projeto

```text
pokedex-cli/
  pokedex.py           # código principal do programa
  requirements.txt     # dependências (requests)
  exemplo_saida.json   # exemplo do arquivo que o programa gera
  README.md            # esta documentação
  LICENSE              # licença MIT
  .gitignore           # arquivos ignorados pelo Git
```

O arquivo `pokedex.json` é criado quando você roda o programa e não é versionado.

### Funções do `pokedex.py`

| Função | O que faz |
|---|---|
| `buscar_pokemon` | consulta a PokeAPI e trata os erros da requisição |
| `extrair_campos` | filtra o JSON da API e converte as unidades (altura e peso) |
| `salvar_json` | grava os pokémons da sessão no arquivo |
| `main` | controla o loop de entrada e junta as funções acima |

## O que aprendi

Este projeto me fez entender na prática o que acontece quando um programa conversa com uma API: montar a requisição, ler o status da resposta e transformar o JSON enorme que volta da API apenas nas informações de que eu preciso.

O que mais me ensinou foi o tratamento de erros. Usei blocos `try/except` para tratar cada problema separadamente (`Timeout`, `ConnectionError`, `HTTPError` e `OSError` ao salvar o arquivo). Para isso, precisei pesquisar o nome de cada exceção da biblioteca `requests` e entender em que situação cada uma acontece. Depois testei vários cenários (nome errado, entrada vazia, internet desligada, falha ao gravar o arquivo) para encontrar a maioria dos erros possíveis e deixar uma mensagem clara para quem usa o programa.

Os testes também me mostraram coisas que eu não esperava. Buscar `mr mime` devolveu erro 403 em vez de 404, e resolvi trocando os espaços por hífen antes da requisição. Na primeira versão eu também fazia a mesma requisição duas vezes a cada busca, e corrigi depois de revisar o código.

Aprendi ainda a dividir o programa em funções com uma responsabilidade só e a usar ambiente virtual, `requirements.txt`, `.gitignore` e Git/GitHub como parte do fluxo de um projeto.

## Próximos passos

- Exportar também em CSV
- Manter os dados entre execuções, em vez de sobrescrever o `pokedex.json`
- Tentar a requisição de novo automaticamente em caso de timeout ou queda de conexão
- Gravar o arquivo mesmo que o programa seja interrompido com `Ctrl+C`
- Criar testes automatizados com `pytest`

## Licença

MIT. Veja o arquivo `LICENSE`.