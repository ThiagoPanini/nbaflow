# O Diretório docs/

Ah, as documentações...

É sempre muito complexo pensar em documentar algum código ou solução. Em grande parte das situações, a falta de clareza de ferramentas que possam facilitar este trabalho criam uma imensa lacuna entre iniciativas extremamente ricas, mas documentações muito aquém do mínimo esperado. Neste seção, serão detalhados os insumos do *template pandora* presentes no diretório `docs/` e que certamente podem facilitar o trabalho do usuário para criar uma **excelente documentação** para seu pacote Python.

## Estrutura de Subpastas

Menos complexo que o conteúdo presente no [diretório .github/](./github.md), os insumos presentes em `docs/` basicamente comportam locais para armazenar imagens, gifs, ícones e, principalmente, arquivos markdown utilizados para construir páginas de documentação.

A proposta do *pandora* no que tange aspectos de documentação é proporcionar uma forma rápida de utilizar o [MkDocs](https://www.mkdocs.org/) como forma de documentar soluções através do tema [material](https://squidfunk.github.io/mkdocs-material/).

## MkDocs

No diretório `docs/mkdocs/`, o usuário poderá encontrar exatamente os arquivos markdown utilizados para geração desta própria documentação. A ideia é disponibilizar um exemplo prático de como seu futuro pacote Python pode ser documentado.

???+ warning "O pandora cria a documentação automaticamente para o usuário?"
    Não. O projeto *pandora* não tem a pretensão de gerar nenhum tipo de documentação automática para aquilo que o usuário irá desenvolver em sua biblitoeca (até pelo fato de não ser possível saber de antemão a utilidade deste pacote a ser criado, certo?). Dessa forma, o usuário tem em mãos apenas um formato organização de diretórios e arquivos que foram utilizados para formar uma documentação de exemplo (esta documentação).

    Cabe ao usuário observar o cenário entregue e aplicar suas próprias adaptações futuramente, se assim preferir.

    Existem documentações altamente detalhadas sobre o uso do MkDocs e do tema material disponíveis, incluindo tópicos relacionados à extensões e customizações específicas.