## Motivadores

Após criar e desenvolver alguns pacotes, como [cloudgeass](https://pypi.org/project/cloudgeass/), [gluesnake](https://pypi.org/project/gluesnake/) e [xplotter](https://pypi.org/project/xplotter/), pude perceber o quão rico seria se toda organização básica do repositório de cada novo pacote Python já estivesse disponível e pronta para uso a mercê apenas de algumas adaptações.

Assim nasce projeto *pandora*: para cada novo pacote [Python](https://packaging.python.org/en/latest/tutorials/packaging-projects/) a ser criado, independente do proposito ou aplicação, uma série de insumos, arquivos de configuração, diretórios e *templates* podem ser utilizados para abstrair todo um *overhead* básico de configuração da nova biblioteca.

Foque mais no desenvolvimento e menos na parte burocrática!

## De que forma isso é possível?

Na prática, o projeto *pandora* nada mais é do que um repositório *template* criado no GitHub e pré configurado para criar outros repositórios. Com isso, o usuário poderá idealizar suas bibliotecas Python e já ter em mãos toda uma configuração prévia que vai desde uma proposta de organização do projeto até arquivos de CI com esteiras do GitHub Actions para gerenciamento de ações.

??? tip "O que há nesse repositório template?"
    Essa é a grande questão que define o projeto *pandora* da forma mais técnica possível. Acesse o [link que explica sobre o conteúdo do repositório](./repo.md) e entenda mais a respeito.