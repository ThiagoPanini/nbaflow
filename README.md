<div align="center">
    <br><img src="https://i.imgur.com/l07Xn2Y.png" height=400 width=400 alt="nbaflow logo">
</div>

<div align="center">
  <strong>:basketball: Solução integrada para extração e análise de dados estatísticos da NBA :basketball:</strong>
</div>
<br/>


## Table of contents

- [Sobre o Projeto](#sobre-o-projeto)
    - [Fases do Desenvolvimento](#fases-do-desenvolvimento)
    - [Arquitetura - Fase 01](#arquitetura---fase-01)
- [Contextos e Cenários](#contextos-e-cenários)
  - [NBA Stats](#nba-stats)
  - [NBA API](#nba-api)
  - [Visualização de Dados](#visualização-de-dados)
- [NBAFlow - Solução Integrada](#nbaflow---solução-integrada)
    - [Consumo da Solução](#consumo-da-solução)
    - [Painel Analítico - Tableau](#painel-analítico---tableau)
- [Contatos](#contatos)


## Sobre o Projeto

Antes de mais nada, imagine algo pessoal que você goste de acompanhar, seja um esporte, um programa de TV ou mesmo notícias sobre um determinado assunto. Agora pense sobre unir seus conhecimentos em tecnologia para aprender mais sobre esse assunto ao mesmo tempo que aprimora suas _skills_ técnicas. Assim surge o NBAFlow: uma mistura entre programação, arquitetura, desenvolvimento e esporte! Para acessar diretamente os detalhes de uso da solução, navegar até o tópico [NBAFlow - Solução Integrada](#nbaflow---solução-integrada)

### Fases do Desenvolvimento

Concebido como uma forma prática e bacana de mergulhar em universos ainda desconhecidos, o NBAFlow pode ser definido como uma frente de aprendizado próprio e compartilhamento de conhecimentos com a comunidade de tecnologia. Após uma jornada inicial de maturação do projeto, faz-se válida a divisão do desenvolvimento implementado e da produção de conteúdo em **_fases_** distintas, sendo elas:

___
* [**_Fase 01: Primeiros Passos_**](https://github.com/ThiagoPanini/nbaflow/tree/fase-01): a primeira fase do projeto consistiu em um essencial entendimento de todas as possibilidades de geração, extração e análise de dados da NBA a partir de APIs e bibliotecas compatíveis com a linguagem Python. Nela, foi possível construir componentes e módulos capazes de encapsular todo o processo de preparação de dados de jogadores em cada uma de suas respectivas partidas disputadas na liga. A materialização de todo este trabalho se deu por meio de um painel no Tableau altamente responsivo e dinâmico que rendeu e vem rendendo bons frutos aos amantes do esporte. Em resumo, os principais resultados alcançados nesta primeita etapa do projeto envolvem:
    *   Construção dos módulos [gamelog.py](https://github.com/ThiagoPanini/nbaflow/blob/fase-01/nbaflow/gamelog.py) e [images.py](https://github.com/ThiagoPanini/nbaflow/blob/fase-01/nbaflow/images.py) para extração e preparação de dados de partidas de jogadores
    *   Construção de [scripts](https://github.com/ThiagoPanini/nbaflow/tree/fase-01/dev/scripts) de processamento de dados para construção de base final a ser analisada
    *   Criação de um painel publicado no [Tableau Public](https://public.tableau.com/app/profile/thiago.henrique.gomes.panini/viz/NBAFlow-InsightsdeDadosdaNBA/PaineldeEstatsticasdeJogadores)
    
> 📌 O [post de divulgação do painel](https://www.linkedin.com/posts/thiago-panini_python-tableau-nba-activity-6822851884097773568-UD_p) da Fase 01 do projeto foi visto por mais de 12 mil pessoas no LinkedIn, sendo compartilhado por um dos [**gerentes nacionais**](https://www.linkedin.com/posts/jaimem2_python-tableau-nba-activity-6822904915346628608-_wZN) da Tableau Software e por diretores de grandes empresas como [**Salesforce**](https://www.linkedin.com/posts/marilouvain_python-tableau-nba-activity-6822911222367752195-GY05).
___

* [**_Fase 02: O Contato com a AWS_**](https://github.com/ThiagoPanini/nbaflow/tree/fase-02): após uma jornada recompensadora vivenciada na primeira fase do projeto, novos horizontes vieram à tona e uma nobre ideia de utilizar os serviços de uma provedora cloud se fizeram presentes para aprimorar ainda mais o projeto. Assim, motivado por um mergulho inicial no universo de computação em nuvem, decidiu-se realizar uma verdadeira _migração_ do fluxo existente, este formado sob um viés de processamento totalmente local, para uma arquitetura em nuvem capaz de proporcionar uma série de facilidades adicionais ao projeto. Dessa forma, utilizando a AWS como provedora cloud, a segunda fase do projeto NBAFlow permitiu:
    * Utilização do serviço [RDS](https://aws.amazon.com/pt/rds/) para armazenamento dos dados de partidas de jogadores em um banco de dados relacional
    * Utilização de instância computacional [EC2](https://aws.amazon.com/pt/ec2/) contendo lógica de consumo de dados diretamente do RDS
    * Desenho de arquitetura segura e de alta disponibilidade a partir de configurações de _Security Groups_ e _Subnets_ na AWS
___

* [**_Fase 03: Imersão na AWS com Lambda_**](https://github.com/ThiagoPanini/nbaflow/tree/fase-03): _em andamento..._

___

### Arquitetura - Fase 03

Em andamento...

___

## Contextos e Cenários

Criado como uma ideia genérica de análise e exploração de dados da NBA dentro de cenários que pudessem proporcionar uma aprendizagem de tecnologias relevantes em termos de construção de pipelines de ingestão, armazenamento, visualização e análise de dados, o projeto **NBAFlow** teve, como ponto de partida, o próprio site de [estatísticas oficiais da NBA](https://www.nba.com/stats/). Neste momento, a pergunta a ser respondida se resumiu a: _"Como obter esse tipo de dado para análises mais refinadas?"_

Já nas primeiras tentativas em busca das possíveis formas de obter os tais dados estatísticos da NBA, chegou-se a biblioteca python `nba-api` capaz de servir como um agente integrador proporcionando o acesso a dados diretamente do site. Com o avanço da obtenção e exploração dos dados, novas inspirações focadas em visualização de dados se tornaram um grande meio para materializar todos os estudos propostos. E assim, considerando os três alicerces motivacionais que giram em torno do projeto, esta breve seção tem por objetivo detalhar o conteúdo presente no site oficial de estatísticas da NBA, na biblitoeca `nba_api` implementada e em frentes de visualização de dados utilizando cenários da NBA.

### NBA Stats

A página de estatísticas da NBA é um repositório altamente rico em termos de dados de jogadores e times. Em um exemplo prático, ao acessar a rota https://www.nba.com/stats/player/203081/ referente ao jogador Damian Lillard, é possível, logo de cara, consumir um denso pacote de indicadores de performance:

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

Pensando nisso, usuários da comunidade Python desenvolveram uma poderosa API conhecida por [`nba-api`](https://pypi.org/project/nba-api/) capaz de proporcionar uma série de módulos úteis para o retorno de informações relacionadas a estatísticas da NBA. 

Maiores detalhes sobre a biblioteca `nba-api` podem ser encontrados em:
* Repositório PyPI: https://pypi.org/project/nba-api/
* Repositório Github: https://github.com/swar/nba_api

### Visualização de Dados

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

___

## NBAFlow - Solução Integrada

Após um vasto consumo da literatura e documentação disponíveis em fontes relacionadas, entende-se pelo projeto **NBAFlow** como ponto central para o desenvolvimento de fluxos e scripts de requisição e preparação de dados de modo a permitir a construção de visualizações dinâmicas envolvendo estatísticas da NBA. Como MVP, o diagrama de solução abaixo demonstra uma parcela dos entregáveis obtidos até o momento, sendo estes:

* Classes e scripts Python capazes de coletar, preparar e transformar dados estatísticos da NBA;
* Painel analítico e interativo construído no _Tableau_;

### Consumo da Solução

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
pyhon scripts\one_player_gamelog.py
```

### Painel Analítico - Tableau

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
