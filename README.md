<div align="center">
    <br><img src="https://i.imgur.com/l07Xn2Y.png" height=400 width=400 alt="nbaflow logo">
</div>

<div align="center">
  <strong>:basketball: Solução integrada para extração e análise de dados estatísticos da NBA :basketball:</strong>
</div>
<br/>


## Table of contents

- [Motivação e Contexto](#introdução-e-contexto)
- [Cenários e Benchmarks](#cenários-e-benchmarks)
  - [NBA Stats](#nba-stats)
  - [NBA API](#nba-api)
  - [Visualizações](#visualizações)
  - [Cloud](#cloud)
- [NBAFlow - Solução Integrada](#nbaflow---solução-integrada)
- [Consumo da Solução](#consumo-da-solução)
- [Painel Analítico - Tableau](#painel-analítico---tableau)
- [Contatos](#contatos)

___

## Introdução e Contexto

> 📌 Para ir direto ao desenvolvimento da solução proposta, é sugerido consumir essa documentação a partir do tópico **[NBAFlow - Solução Integrada](#nbaflow---solução-integrada)**

Em linhas gerais, o projeto **NBA Flow** tem como premissa a construção de ferramentas de consumo, visualização e pipelines de transformação de dados utilizando estatísticas de jogadores e partidas da NBA extraídas dinamicamente a partir de requisição de APIs ou fontes centralizadas disponíveis publicamente.

Em contatos iniciais com as possíveis formas de obter dados estatísticos da NBA dentro do contexto proposto, chegou-se a biblioteca python `nba-api` que, por sua vez, pode ser definida como um pacote responsável por proporcionar uma API capaz de acessar dados diretamente do site [NBA.com](https://www.nba.com/).

Assim, ainda em um cenário genérico, este repositório irá alocar códigos e documentar procedimentos relacionados aos primeiros contatos com a biblioteca `nba-api` e possivelmente outras fontes centralizadas que surgirem ao longo do desenvolvimento, mantendo, como principal objetivo, a construção de códigos capazes de fornecer dados suficientemente analisáveis dentro das motivações estatísticas propostas. Os primeiros passos pro projeto **NBA Flow** serão dados aqui!

___

## Cenários e Benchmarks

Após uma breve explicação sobre os objetivos e as propostas relacionadas a construção deste repositório, é importante ressaltar as motivações atreladas ao projeto como um todo. Basicamente, o projeto **NBA Flow** surgiu como uma ideia genérica de análise e exploração de dados da NBA dentro de cenários que pudessem proporcionar uma aprendizagem de tecnologias relevantes em termos de construção de pipelines de ingestão, armazenamento, visualização e análise de dados.

Sem possuir um _moon shoot_ estritamente definido, o **NBA Flow** surge como uma forma de aprender coisas novas, utilizando um tema de fácil acesso e relativamente amigável para os usuários que dele fazem parte.

### NBA Stats

Analisando as possibilidades existentes atualmente, sabe-se que o site [NBA.com](https://www.nba.com/) possui uma [sessão](https://www.nba.com/stats/) vasta em termos estatísticos contendo dados altamente relevantes para análises pontuais. Em um exemplo prático, ao acessar a rota https://www.nba.com/stats/player/203081/ referente ao jogador Damian Lillard, é possível, logo de cara, consumir um denso pacote de indicadores de performance:

<div align="center">
    <br><img src="https://i.imgur.com/97O3wqA.png" height=300 width=800 alt="lillard stats header">
</div>

Ao navegar pela página, ainda é possível utilizar filtros e menus específicos para gerar novas visões agrupadas e estatísticas da performance do jogador em cenários de temporada regular ou de playoffs em diferentes anos.

<div align="center">
    <br><img src="https://i.imgur.com/Exr5go3.png" height=300 width=800 alt="lillard stats table splits">
</div>

Existem, ainda, diversas outras funcionalidades presentes na rota _/stats_ do site da NBA, permitindo assim uma série de análises pontuais, históricas e comparações, sejam em uma visão individual de jogadores ou de franquias como um todo. O site da NBA fornece um mundo completo de estatísticas para os usuários e, de alguma forma, seria extremamente vantajoso poder requisitar e ter em mãos esses dados para transformações e análises próprias.

### NBA API

Imaginando um cenário onde os usuários podem ter em suas mãos dados estatísticos de jogadores da NBA e de franquias diretamente do site oficial da NBA, seria possível realizar uma série de atividades envolvendo análises descritivas ou até mesmo preditivas em contextos livres, desde dados individuais de jogadores ou até mesmo de situações envolvendo atacantes e defensores.

Pensando nisso, usuários da comunidade Python desenvolveram uma poderosa API conhecida por [`nba-api`](https://pypi.org/project/nba-api/) capaz de proporcionar uma série de módulos úteis para o retorno de informações relacionadas a estatísticas da NBA. Contendo uma vasta documentação, essa biblioteca Python pode ser explorada em maiores detalhes ao longo do desenvolvimento do projeto **NBA Flow**.

Maiores detalhes sobre a biblioteca `nba-api` podem ser encontrados em:
* Repositório PyPI: https://pypi.org/project/nba-api/
* Repositório Github: https://github.com/swar/nba_api

> 📌 **Contexto dos dados:** ao longo da exploração e desenvolvimento das extrações de dados diretamente da API, será preciso definir o contexto inicial a ser utilizado no fluxo, isto é, o layout de tabela e o direcionamento do projeto para requisitar dados de forma adequada visando a construção de bases condizentes com o objetivo definido. A princípio, uma boa proposta gira em torno de construir uma base única com estatísticas individuais de jogadores ao longo dos anos.

### Visualizações

Uma das grandes motivações relacionadas ao início deste projeto tem raízes conectadas a visualização de dados. Nomes como Kirk Goldsberry ([@kirkgoldsberry](https://www.instagram.com/kirkgoldsberry/)) são grandes inspirações dentro deste cenário de Data Viz. Em sua página no Instagram, Kirk compartilha uma série de visualizações extremamente interessantes sobre tópicos relacionados a NBA, desde os melhores arremessadores por zona, até dispersões relacionadas a tentativas de arremessos e eficiência em percentual de grandes nomes da liga.

Abaixo, seguem alguns exemplos de visualizações criadas por Kirk Goldsberry em sua página:

<div align="center">
    <br><img src="https://i.imgur.com/zc671dJ.png" height=500 width=500 alt="lillard stats game5">
</div>

<div align="center">
<i>A imagem acima traz uma visão de eficiência de arremessos do jogador Damian Lillard, do Portland Trailblazers, no fatídico jogo 5 dos playoffs de 2021 contra Denver Nuggets.</i>
</div>

<div align="center">
    <br><img src="https://i.imgur.com/7ldISzz.png" height=500 width=500 alt="lillard stats game5">
</div>

<div align="center">
<i>Já essa segunda imagem traz uma relação de tentativas e eficiência de arremessos realizados por jogadores na fase de playoffs.</i>
</div>

### Cloud

Em uma quarta e última vertente, a análise de dados da NBA pode, eventualmente, proporcionar um viés extremamente positivo em relação ao uso de recursos da nuvem para propor pipelines completos de extração, tratamento e visualização de dados, permitindo assim explorar uma série de serviços e atividades em um contexto de aprendizagem.

Considerando a idealização dos usuários em aprender novos conceitos de computação em nuvem, essa frente de trabalho pode ser um gatilho positivo para implementar soluções já considerando uma provedora cloud. Dessa forma, além de desenvolver estudos em contextos altamente interessantes para os usuários do projeto, será possível também aprender conceitos práticos sobre plataformas usualmente aplicadas em pipelines de dados.

___

## NBAFlow - Solução Integrada

Após um vasto consumo da literatura e documentação disponíveis em fontes relacionadas, entende-se pelo projeto **NBAFlow** como ponto central para o desenvolvimento de fluxos e scripts de requisição e preparação de dados de modo a permitir a construção de visualizações dinâmicas envolvendo estatísticas da NBA. Como MVP, o diagrama de solução abaixo demonstra uma parcela dos entregáveis obtidos até o momento, sendo estes:

* Classes e scripts Python capazes de coletar, preparar e transformar dados estatísticos da NBA;
* Painel analítico e interativo construído no _Tableau_;

<div align="center">
    <br><img src="https://i.imgur.com/HMfAMMV.jpg" alt="nbaflow-c4">
</div>

___

## Consumo da Solução

Como mencionado anteriormente, a construção de toda a solução proposta tem como base a linguagem Python em conjunto com algumas bibliotecas disponibilizadas para fins específicos. Dessa forma, para utilizar os scripts desenvolvidos neste projeto, recomenda-se a execução das seguintes etapas:

**_1. Criação e ativação de um ambiente virtual Python_**

```bash
# Criando e ativando venv no Linux
$ python -m venv <path_venv>/<name_venv>
$ source <path_venv>/<nome_venv>/bin/activate

# Criando e ativando venv no Windows
$ python -m venv <path_venv>/<name_venv>
$ <path_venv>/<nome_venv>/Scripts/activate
```

**_2. Clone do repositório NBAFlow_**

```bash
git clone https://github.com/ThiagoPanini/nbaflow.git
```

**_3. Instalação das dependências do projeto via requirements.txt_**
```
# Navegando até o diretório do projeto e instalando pacotes
cd nbaflow/
pip install -r requirements.txt
```

**_4. Instalação do pacote/projeto em modo de edição_**
> Isso permitirá a devida leitura de módulos internos dentro dos scripts já desenvolvidos
```bash
pip install -e .
```

**_5. [OPCIONAL] Execução de scripts já desenvolvidos para finalidades de estudo_**
```bash
pyhon scripts\player_gamelog.py
```

___

## Painel Analítico - Tableau

Como principal produto dentro desse projeto, encontra-se o [Painel Analítico de Estatística de Jogadores](https://public.tableau.com/views/NBAFlow-InsightsdeDadosdaNBA/PaineldeEstatsticasdeJogadores?:language=pt-BR&:display_count=n&:origin=viz_share_link) publicado e disponível no [Tableau Public](https://public.tableau.com/s/). Em resumo, trata-se de uma solução altamente refinada e construída sob as principais boas práticas de Data Viz, UX e UI com foco nos amantes do esporte e nos entusiastas de análise de dados.

Como principais funcionalidades, o painel disponibilizado possui:

* Menu principal e painel de estatística de jogadores com background disruptivo
* Filtro dinâmico para visualização de indicadores de cada um dos jogadores ativos da liga
* Imagem personalizada para cada jogador da liga de acordo com o filtro (isso foi trabalhoso!)
* Dados agregados de todos os jogadores da liga em todas as temporadas jogadas
* Farois dinâmicos e comparativos com as médias da liga
* Interação dinâmica de dispersão de arremessos
* Ranking de jogadores de acordo com atributos dinâmicos (rebotes, assistências, pontos, minutos, entre outros)
* Muito mais...

<div align="center">
    <br><a href="https://public.tableau.com/app/profile/thiago.henrique.gomes.panini/viz/NBAFlow-InsightsdeDadosdaNBA/PaineldeEstatsticasdeJogadores"><img src="https://i.imgur.com/aHCg0qb.png" alt="nbaflow-tableau"></a>
</div>

<div align="center">
    <br><a href="https://public.tableau.com/app/profile/thiago.henrique.gomes.panini/viz/NBAFlow-InsightsdeDadosdaNBA/PaineldeEstatsticasdeJogadores"><img src="https://i.imgur.com/sjlLqru.png" alt="nbaflow-tableau"></a>
</div>

## Contatos

* LinkedIn: https://www.linkedin.com/in/thiago-panini/
* Outras soluções desenvolvidas: https://github.com/ThiagoPanini
