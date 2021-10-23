<div align="center">
    <br><img src="https://i.imgur.com/C4tK4by.png" alt="nbaflow logo">
</div>

<div align="center">  
  
  ![Release](https://img.shields.io/badge/release-ok-brightgreen)
  [![PyPI](https://img.shields.io/pypi/v/nbaflow?color=orange)](https://pypi.org/project/nbaflow/)
  ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/nbaflow?color=blue)
  ![PyPI - Status](https://img.shields.io/pypi/status/nbaflow)

</div>


<div align="center">
  <strong>:basketball: Solução integrada para extração e análise de dados estatísticos da NBA :basketball:</strong>
</div>
<br/>


## Table of contents

- [Sobre o Projeto](#sobre-o-nbaflow)
- [Funcionalidades Disponíveis](#funcionalidades-disponíveis)
- [Pacote Python NBAFlow](#pacote-python-nbaflow)
  - [Instalação](#instalação)
  - [Features](#features)
  - [Exemplo de Uso](#exemplo-de-uso)
- [Painel Tableau NBAFlow](#painel-tableau-nbaflow)

## Sobre o NBAFlow

O projeto NBAFlow tem como propósito encapsular e abstrair o consumo de APIs relacionadas à NBA, facilitando a extração e a análise de dados e proporcionando aos por usuários um _pool_ de funcionalidades ligadas à NBA. Tendo como principal fonte a biblioteca Python [`nba_api`](https://github.com/swar/nba_api) que, por sua vez, funciona como um facilitador para acesso aos _endpoints_ do [site oficial de estatísticas da NBA](https://www.nba.com/stats/), este projeto une ferramentas já existentes para propor funcionalidades específicas de acordo com as principais necessidades de análise dos amantes do esporte.

<div align="center">
    <br><img src="https://i.imgur.com/IN9oZjn.jpg" alt="nbaflow diagram">
</div>

## Funcionalidades Disponíveis

Uma vez conhecida a arquitetura de desenvolvimento do NBAFlow, é importante ter conhecimento sobre as _features_ contempladas pelo projeto (até o momento!). Neste cenário, o projeto como um todo pode ser dividido em duas principais frentes de consumo para os usuários:

- 🐍 **_Pacote Python nbaflow:_** neste modo de consumo, o usuário poderá instalar o pacote Python já disponível no [PyPI](https://pypi.org/project/nbaflow/) e utilizar as funções, classes e métodos disponíveis dentro de seu próprio fluxo de extração de dados.
- 📊 **_Painel NBAFlow no Tableau Public:_** visando propor um consumo dinâmico, foi desenvolvido um painel no Tableau com algumas visões extremamente interessantes considerando as extrações realizadas pelas próprias funcionalidades presentes no código nbaflow. Com isso, os usuários poderão acessar este maravilhoso dashboard diretamente do [Tableau Public](https://public.tableau.com/app/profile/thiago.henrique.gomes.panini/viz/NBAFlow-InsightsdeDadosdaNBA/PaineldeEstatsticasdeJogadores) para ter insights interessantes sobre jogadores da NBA.

> O post de divulgação do painel NBAFlow foi visto por mais de 12 mil pessoas no [LinkedIn](https://www.linkedin.com/posts/thiago-panini_python-tableau-nba-activity-6822851884097773568-UD_p), sendo compartilhado por um dos [gerentes nacionais](https://www.linkedin.com/posts/jaimem2_python-tableau-nba-activity-6822904915346628608-_wZN) da Tableau Software e por diretores de grandes empresas, como [Salesforce](https://www.linkedin.com/posts/marilouvain_python-tableau-nba-activity-6822911222367752195-GY05).

___

## Pacote Python NBAFlow

### Instalação

Com o [ambiente virtual python](https://realpython.com/python-virtual-environments-a-primer/) ativo, para a instalação do pacote _nbaflow_ via pip, basta executar o comando abaixo:

```bash
pip install nbaflow
```

Com isso, todo o ferramental disponível na última versão do pacote poderá ser usufruído. Vale citar que o pacote possui algumas dependências associadas que são gerenciadas automaticamente no ato de sua instalação, sendo elas:
* `nba_api`: API de abstração com rotas de consumo do site oficial de estatísticas da NBA
* `pandas`: poderosa ferramenta para a manipulação de dados em python

Output esperado após a execução do comando de instalação:
```bash
[...]
Installing collected packages: urllib3, six, idna, charset-normalizer, certifi, requests, pytz, python-dateutil, numpy, pandas, nba-api, nbaflow
Successfully installed certifi-2021.10.8 charset-normalizer-2.0.7 idna-3.3 nba-api-1.1.9 nbaflow-0.0.3 numpy-1.21.3 pandas-1.3.4 python-dateutil-2.8.2 pytz-2021.3 requests-2.26.0 six-1.16.0 urllib3-1.26.7
```

___

### Features

Até o presente momento, o pacote _nbaflow_ conta com o módulo `players.py` responsável por consolidar as principais operações relacionadas à extração de dados de jogadores da NBA, sejam informações básicas de atividade na liga ou então histórico de cada uma das partidas disputadas em uma determinada temporada (regular ou playoffs). Em sua versão mais recente, o referido módulo está estruturado em um formato de funções e entrega, a princípio, as seguintes funcionalidades:

| Função                      | Descrição                                                                                              |
| :-------------------------: | :---------------------------------------------------------------------------------------------------:  |         
| `get_player_info()`         | Coleta informações gerais de jogadores a partir do endpoint `commonallplayers` da biblitoeca `nba_api` |
| `get_player_image()`        | Requisita a imagem oficial de um jogador (identificado por um `player_id`) direto do site da NBA       |
| `get_player_gamelog()`      | Coleta o histórico de partidas de um jogador em uma temporada de tipo específico (regular, playoffs)   |

Cada uma das funções acima listadas possuem uma documentação completa e que pode ser acessada diretamente no respectivo módulo.

Adicionalmente, foi construída a classe `PlayerFeatures`, também presente no módulo `players.py`, com o objetivo de gerenciar possíveis problemas de timeout eventualmente obtidos em scripts que utilizam as funções acima citadas. Propondo uma forma simples de garantir a execução da função e a obtenção do dado solicitado, a classe possui regras de identificação e reprocessamento de requisição em casos de erros de _timeout_, trazendo assim uma abordagem que permite o usuário configurar um laço infinito de repetição ou então definir um número máximo de tentativas a ser considerada na obtenção dos dados.

___

### Exemplo de Uso

O repositório possui [scripts](https://github.com/ThiagoPanini/nbaflow/tree/main/scripts) prontos capazes de fornecer excelentes exemplos de utilização das funcionalidades do pacote _nbaflow_. Em resumo, o trecho resumido de código abaixo é responsável por obter dados de partidas do jogador Damian Lillard (`player_id=203081`) nos playoffs 2020-21 (o jogo contra o Denver de duas prorrograções ainda me assombra):

```python
# Importando bibliotecas
from nbaflow.players import get_player_gamelog

# Retornando gamelog de jogador
player_gamelog = get_player_gamelog(
    player_id=203081,
    season='2020-21',
    season_type='Playoffs'
)
```

O retorno da função é dado em um formato DataFrame do pandas e suas primeiras linhas esperadas são:

|row  |   season_id  |player_id     |game_id  |game_date      |matchup |wl  |min  |fgm  |...  |blk  |tov  |pf  |pts  |plus_minus  |video_available   |season  |season_type|
|:-----:|   :-----: |:-----:     |:-----:  |:-----:      |:-----: |:-----:  |:-----:  |:-----:  |:-----:  |:-----:  |:-----:  |:-----:  |:-----:  |:-----:  |:-----:   |:-----:  |:-----:|
| 0|     42020|     203081|  0042000166| 2021-06-03|  POR vs. DEN  |L   |43    |8  |...    |0    |5   |1   |28         |-11                |1  |2020-21     |Playoffs|       
| 1|     42020|     203081|  0042000165| 2021-06-01|    POR @ DEN  |L   |52   |17  |...    |3    |1   |0   |55         |  2                |1  |2020-21     |Playoffs|       
| 2|     42020|     203081|  0042000164| 2021-05-29|  POR vs. DEN  |W   |31    |1  |...    |0    |1   |2   |10         | 33                |1  |2020-21     |Playoffs|       
| 3|     42020|     203081|  0042000163| 2021-05-27|  POR vs. DEN  |L   |40   |15  |...    |0    |1   |3   |37         | -6                |1  |2020-21     |Playoffs|       
| 4|     42020|     203081|  0042000162| 2021-05-24|    POR @ DEN  |L   |42   |11  |...    |1    |3   |1   |42         |-16                |1  |2020-21     |Playoffs|       
| 5|     42020|     203081|  0042000161| 2021-05-22|    POR @ DEN  |W   |40   |10  |...    |0    |2   |2   |34         | 25                |1  |2020-21     |Playoffs| 

Para descobrir o id de um jogador, é possível utilizar a função `get_players_info()` e filtrar o jogador por uma das colunas que achar mais simples (nome, sobrenome, entre outras).

## Painel Tableau NBAFlow

Como mencionado na descrição inicial de funcionalidades do projeto, ao longo do processo de desenvolvimento, achou-se interessante a ideia de disponibilizar um dashboard altamente interativo e atrativo aos usuários para que estes possam acessar diretamente os resultados dos módulos nbaflow pelo Tableau. Assim, surgiu o [Painel NBAFlow](https://public.tableau.com/app/profile/thiago.henrique.gomes.panini/viz/NBAFlow-InsightsdeDadosdaNBA/PaineldeEstatsticasdeJogadores?publish=yes) contando, até o momento, com um painel inicial de navegação e um panel analítico de jogadores com uma série de visões relevantes para que os melhores insights e análises possam ser realizados com um esforço mínimo do usuário.

* _Capa / Painel Principal_

<div align="center">
    <br><img src="https://i.imgur.com/VwZP0Aq.png" alt="nbaflow-tableau-01">
</div>
<br/>

* _Painel de Estatísticas de Jogadores_

<div align="center">
    <br><img src="https://i.imgur.com/VWn2Pt2.png" alt="nbaflow-tableau-02>
</div>
<br/>
___
        
        ## Contatos

* LinkedIn: https://www.linkedin.com/in/thiago-panini/
* Outros pacotes desenvolvidos: https://github.com/ThiagoPanini

