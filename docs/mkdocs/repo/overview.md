# O Conteúdo do Repositório

## Diretórios Principais

Possuindo a essência de ser um *template* de repositório, o projeto *pandora* providencia a seguinte organização de diretórios aos usuários:

| :open_file_folder: **Diretório** | :pencil: **Descrição** |
| :-- | :-- |
| `.github/` | Contém arquivos de configuração de esteiras CI que podem ser utilizados para automatização dos processos mais comuns presentes em bibliotecas Python, como validação de linter, docstrings, testes unitários, abertura de PRs e até mesmo publicação automática de versões no PyPI. Além disso, este diretório traz *templates* de issues e pull requests pensados para aprimorar ainda mais o gerenciamento do repositório como um todo. |
| `docs/` | Contém uma estrutura básica para documentação do pacote Python a partir do MkDocs (tema [material](https://squidfunk.github.io/mkdocs-material/)). A proposta de organização do *pandora* envolve a disponibilização de diretórios para o armazenamento de imagens, gifs, arquivos markdown e até mesmo estruturas de customização em CSS (opcional). |
| `package-name/` | Referência simbólica. Aqui é onde o usuário que utilizar o *template* do *pandora* irá construir seu pacote Python. Este diretório deve ser renomeado para o nome da biblioteca a ser criada. |
| `requirements/` | Contém diferentes arquivos de requirements para diferentes contextos. A proposta é isolar algumas necessidades específicas da biblioteca, como uma lista de dependências utilizadas apenas para assuntos relacionados à documentação (`doc.txt`) e outra lista apenas para desenvolvimento de funcionalidades (`dev.txt`). |
| `tests/` | Diretório responsável por alocar todo o desenvolvimento de testes unitários do pacote criado. Não há qualquer insumo pré programado para o usuário, visto que qualquer implementação de teste depende unica e exclusivamente dos detalhes da biblioteca a ser construída após a obtenção do *template*. |

## Outros Arquivos

Além da visão geral dos repositórios disponíveis no modelo proposta de organização, alguns arquivos adicionais se fazem presente nessa jornada:

- `pytest.ini`: arquivo de configuração do `pytest` que pode opcionalmente ser utilizado para detalhar especifidades relacionadas aos testes da biblioteca
- `mkdocs.yml`: arquivo principal de configuração da documentação MkDocs do pacote
- `setup.py`: arquivo de setup de pacotes Python pré preenchido para o usuário
- `.gitignore`: arquivo ignore do git com template Python