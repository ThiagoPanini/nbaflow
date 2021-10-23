<div align="center">
    <br><img src="https://i.imgur.com/C4tK4by.png" alt="nbaflow logo">
</div>

<div align="center">
  <strong>:basketball: Solução integrada para extração e análise de dados estatísticos da NBA :basketball:</strong>
</div>
<br/>


## Table of contents

- [Sobre o Projeto](#sobre-o-nbaflow)
- [Funcionalidades Presentes](#funcionalidades-presentes)
  - [NBA Stats](#nba-stats)
  - [NBA API](#nba-api)
  - [Visualização de Dados](#visualização-de-dados)
- [NBAFlow - Solução Integrada](#nbaflow---solução-integrada)
    - [Consumo da Solução](#consumo-da-solução)
    - [Painel Analítico - Tableau](#painel-analítico---tableau)
- [Contatos](#contatos)


## Sobre o NBAFlow

O projeto NBAFlow tem como propósito encapsular e abstrair o consumo de APIs relacionadas à NBA visando propor uma maior facilidade na extração e análise de dados relacionados por usuários que desejam ter em mãos todo esse _pool_ de usabilidade. Tendo como principal fonte a biblioteca Python [`nba_api`](https://github.com/swar/nba_api) que, por sua vez, funciona como um facilitador para acesso aos _endpoints_ do [site oficial de estatísticas da NBA](https://www.nba.com/stats/), este projeto une ferramentas já existentes para propor funcionalidades específicas de acordo com as principais necessidades de análise dos amantes do esporte.

<div align="center">
    <br><img src="https://i.imgur.com/IN9oZjn.jpg" alt="nbaflow diagram">
</div>

## Funcionalidades Presentes

Uma vez conhecida a arquitetura de desenvolvimento do NBAFlow, é importante ter conhecimento sobre as _features_ contempladas pelo projeto (até o momento!). Neste cenário, o projeto como um todo pode ser dividido em duas principais frentes de consumo para os usuários:

- **_Pacote Python nbaflow:_** neste modo de consumo, o usuário poderá instalar o pacote Python já disponível no [PyPI](https://pypi.org/project/nbaflow/) e utilizar as funções, classes e métodos disponíveis dentro de seu próprio fluxo de extração de dados.
- **_Painel NBAFlow no Tableau Public:_** visando propor um consumo dinâmico, foi desenvolvido um painel no Tableau com algumas visões extremamente interessantes considerando as extrações realizadas pelas próprias funcionalidades presentes no código nbaflow. Com isso, os usuários poderão acessar este maravilhoso dashboard diretamente do [Tableau Public](https://public.tableau.com/app/profile/thiago.henrique.gomes.panini/viz/NBAFlow-InsightsdeDadosdaNBA/PaineldeEstatsticasdeJogadores) para ter insights interessantes sobre jogadores da NBA.

> 📌 O post de divulgação do painel NBAFlow foi visto por mais de 12 mil pessoas no [LinkedIn](https://www.linkedin.com/posts/thiago-panini_python-tableau-nba-activity-6822851884097773568-UD_p), sendo compartilhado por um dos [gerentes nacionais](https://www.linkedin.com/posts/jaimem2_python-tableau-nba-activity-6822904915346628608-_wZN) da Tableau Software e por diretores de grandes empresas, como [Salesforce](https://www.linkedin.com/posts/marilouvain_python-tableau-nba-activity-6822911222367752195-GY05).

### Pacote Python nbaflow

## Contatos

* LinkedIn: https://www.linkedin.com/in/thiago-panini/
* Outras soluções desenvolvidas: https://github.com/ThiagoPanini
