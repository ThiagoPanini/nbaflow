# O Diretório requirements/

Possuindo também uma construção extremamente mais simples que os demais diretórios do *template pandora*, o `requirements/` traz consigo uma proposta de simplificar a separação de dependências com base em cenários específicos de uso da biblioteca a ser criada.

O isolamento proposto envolve a existência de três arquivos distintos:

- `requirements/dev.txt` para dependências de desenvolvimento do projeto
- `requirements/docs.txt` para dependências relacionadas à documentação do projeto
- `requirements/all.txt` todas as dependências do projeto obtidas via `pip freeze`

## requirements/dev.txt

No arquivo [requirements/dev.txt](https://github.com/ThiagoPanini/pandora/blob/main/requirements/dev.txt), o usuário poderá incluir dependências relacionadas ao desenvolvimento propriamente dito de seu pacote Python.

??? example "Exemplo de dependêncais que poderiam ser colocadas em dev.txt"

    ```text
    build
    flake8
    pydocstyle
    pytest
    pytest-cov
    notebook
    pandas
    boto3
    ```

## requirements/docs.txt

Como o *pandora* proporciona uma rota inicial para documentação de projetos via MkDocs, o isolamento de dependências para esta finalidade se mostra algo interessante quando imaginamos, por exemplo, o *deploy* automático da página de documentação por plataforma externas como o [readthedocs](https://readthedocs.org/). Além disso, os usuários podem ter uma visão clara sobre as dependências necessárias para desenvolver funcionalidades da biblioteca e dependências utilizadas para fins de documentação.

??? example "Exemplo de dependêncais que poderiam ser colocadas em docs.txt"

    ```text
    mkdocs
    pymdown-extensions
    mkdocs-material
    mkdocstrings[python]
    ```

## requirements/all.txt

Por fim, o arquivo [requirements/all.txt](https://github.com/ThiagoPanini/pandora/blob/main/requirements/all.txt) pode consolidar todas as dependências do projeto obtidas através do comando `pip freeze`. Aqui, além das referências nominais das principais bibliotecas necessárias para o desenvolvimento da solução, são também consideradas as dependências dessas dependências, permitindo assim uma visão bem específica sobre o ambiente virtual utilizado na construção.

??? example "Exemplo de dependêncais que poderiam ser colocadas em all.txt"

    ```text
    anyio==3.6.2
    argon2-cffi==21.3.0
    argon2-cffi-bindings==21.2.0
    arrow==1.2.3
    asttokens==2.2.1
    attrs==22.2.0
    backcall==0.2.0
    beautifulsoup4==4.11.2
    bleach==6.0.0
    build==0.10.0
    certifi==2022.12.7
    cffi==1.15.1
    charset-normalizer==3.0.1
    click==8.1.3
    colorama==0.4.6
    comm==0.1.2
    coverage==7.2.1
    debugpy==1.6.6
    decorator==5.1.1
    defusedxml==0.7.1
    exceptiongroup==1.1.0
    executing==1.2.0
    fastjsonschema==2.16.3
    flake8==6.0.0
    ...
    ```

## Considerações

:material-alert-decagram:{ .mdx-pulse .warning } Aqui, mais uma vez, é importante reforçar que todos os insumos disponibilizados neste e nos demais diretórios do *template pandora* são de uso **opcional**. Os usuários podem decidir adotar as estratégias oferecidas por sua livre e espontânea vontade. A grande ideia é tentar facilitar, ao máximo, trabalhos burocráticos de organização e configuração de repositórios. Se alguma proposta se mostra inviável na prática, sua inutilização é algo totalmente esperado.