# O Diretório .github/

Em linha com os objetivos do projeto *pandora* em fornecer o máximo de insumos possíveis para facilitar a organização de um repositório de pacote Python, o diretório `.github/` representa a centralização de tópicos relacionados à automação de processos no próprio GitHub. Neste seção serão fornecidos detalhes sobre o conteúdo disponibilizado neste diretório e os impactos positivos na jornada do usuário.

## Templates de Issues e Pull Requests

Sempre que criamos um novo repositório no GitHub, pensamos em formas de facilitar interações com os usuários consumidores. As [issues](https://docs.github.com/en/issues/tracking-your-work-with-issues/about-issues) são elementos capazes de providenciar, entre outras milhares de vantagens, uma forma efetiva de realizar o *tracking* de necessidades de um repositório. Já os [pull requests](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests) permitem indicar alterações já realizadas em uma determinada *branch* de um repositório e que precisam navegar até outra *branch* específica.

Dado o presente cenário, o projeto *pandora* traz consigo *templates* de *issues* e *pull requests* disponíveis com um padrão amigável de uso. Dessa forma, usuários consumidores (ou até mesmo o *owner* do repositório) podem se servir de um canal eficiente de comunicação entre si. Ao criar um novo repositório a partir do *pandora*, o usuário poderá acessar tais modelos em:

- `.github/pull_request_template.md` contendo um modelo padrão de abertura de PR
- `.github/ISSUE_TEMPLATE/` contendo diferentes modelos de *issues* para cada tipo de tarefa a ser realizada (*bugs*, requisição de features, documentação, entre outros)

??? tip "Saiba mais sobre modelos de issues e pull requests"
    Para mais detalhes a respeito dos dois elementos acima citados, a [documentação oficial do GitHub](https://docs.github.com/en) pode ser consumida. Além disso, a documentação do GitHub também proporciona exemplos de padronização de modelos de *issues* e *PRs*:

    - [Sobre modelos de issues](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/configuring-issue-templates-for-your-repository)
    - [Sobre modelos de pull requests](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/creating-a-pull-request-template-for-your-repository)

## Workflows e Esteiras CI

Um outro aspecto extremamente relevante dentro da proposta de organização de um repositório é a forma como o *owner* realiza a entrega contínua do conteúdo codificado. Na proposta do *pandora*, esteiras básicas de *Continuous Integration* são disponibilizadas ao usuário para uso em contextos relacionados ao desenvolvimento de projetos Python.

### CI Feature

Presente em [.github/workflows/ci-feature.yml](https://github.com/ThiagoPanini/pandora/blob/main/.github/workflows/ci-feature.yml), esta esteira é executada sempre que um *push* é realizado para uma *branch feature*. Os passos consolidados podem ser adaptados pelo usuário e, a princípio, o bloco principal oferecido contempla:

-  Instalação do Python no *runner* do GitHub Actions
-  Instalação de dependências em arquivos de *requirements*
-  Análise de lintagem do código via `flake8`
-  Análise de docstrings do código via `pydocstyle`
-  Realização de testes unitários com `pytest`
-  Avaliação de cobertura de testes com [Codecov](http://codecov.io/)
-  Abertura automática de PR para a branch *main*

??? example "Clique para visualizar uma versão simplificada da esteira ci-feature.yml"

    ```yaml
    name: "⚙️ CI feature branch"

    on:
    push:
        branches:
        - feature**

    permissions:
    id-token: write
    contents: read
    pull-requests: write

    jobs:
    ci-python:
        ...
        steps:
        - name: Checkout
            ...
        - name: Instalação do Python
            ...
        - name: Instalação das Dependências
            ...
        - name: Análise de Linter - flake8
            ...
        - name: Análise de Docstrings - pydocstyle
            ...
        - name: Testes Unitários com pytest
            ...
        - name: Cobertura dos Testes - codecov
            ...

    open-pr-to-main:
        ...
        steps:
        - name: Checkout
            ...
        - name: Cria PR para main
            ...
    ```

### CI Main

Presente em [.github/workflows/ci-main.yml](https://github.com/ThiagoPanini/pandora/blob/main/.github/workflows/ci-feature.yml), esta esteira tem, como gatilho de execução, a abertura de pull requests para a branch principal do repositório (main). Os passos executados são essencialmente os mesmos da `ci-feature.yml`, com exceção da etapa de abertura automática de PR.

??? example "Clique para visualizar uma versão simplificada da esteira ci-main.yml"

    ```yaml
    name: "⚙️ CI main"

    on:
    pull_request:
        branches:
        - main

    permissions:
    id-token: write
    contents: read

    jobs:
    ci-python:
        ...
        steps:
        - name: Checkout
            ...
        - name: Instalação do Python
            ...
        - name: Instalação das Dependências
            ...
        - name: Análise de Linter - flake8
            ...
        - name: Análise de Docstrings - pydocstyle
            ...
        - name: Testes Unitários com pytest
            ...
        - name: Cobertura dos Testes - codecov
            ...
    ```

### CI Package Publish

Por mim, o terceiro arquivo de esteira na ordem cronológica de execução pode ser encontrado em [.github/workflows/ci-pkg-publish.yml](https://github.com/ThiagoPanini/pandora/blob/main/.github/workflows/ci-pkg-publish.yml). Sua principal função é proporcionar uma forma automatizada de realizar dois principais processos:

1. Criação automática de um *draft* de *release* no repositório
2. Publicação automática de versão da biblioteca no PyPI

???+ warning "Configuração de tokens no repositório para permitir ações na esteira"
    Em alguns casos, será preciso considerar a inclusão de alguns *tokens* no repositório criado a partir do template *pandora*. Caso o usuário queira utilizar a esteira de publicação automática no PyPI, por exemplo, é preciso fornecer um [PYPI_API_TOKEN](https://pypi.org/help/#apitoken).

    Para mais detalhes, analise as documentações oficiais de cada uma das *actions* utilizadas nas esteiras via GitHub Marketplace.

