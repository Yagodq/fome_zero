# Marketplace Fome Zero
Este repositório contem arquivos e script para construção de um dashboard de estratégia empresarial.
## Problema de negócio

Você acaba de ser contratado como Cientista de Dados da empresa
Fome Zero, e a sua principal tarefa nesse momento é ajudar o CEO Kleiton Guerra
a identificar pontos chaves da empresa, respondendo às perguntas que ele fizer
utilizando dados!

A empresa Fome Zero é uma marketplace de restaurantes. Ou seja, seu core
business é facilitar o encontro e negociações de clientes e restaurantes. Os
restaurantes fazem o cadastro dentro da plataforma da Fome Zero, que disponibiliza
informações como endereço, tipo de culinária servida,  e também uma nota de avaliação dos serviços e produtos do restaurante,
dentre outras informações.

O CEO Guerra também foi recém contratado e precisa entender melhor o negócio
para conseguir tomar as melhores decisões estratégicas e alavancar ainda mais a
Fome Zero, e para isso, ele precisa que seja feita uma análise nos dados da
empresa e que sejam gerados dashboards, a partir dessas análises

Seu trabalho é utilizar os dados que a empresa Fome Zero possui e responder as
perguntas feitas do CEO e criar o dashboard solicitado.

## Premissas assumidas para a análise

1. Marketplace foi o modelo de negócio assumido.
2. As 4 principais visões foram: Visão Geral, Visão Países, Visão Cidades, Visão Tipos de cozinhas.
3. Quantidade de votos seguido pela nota média de avaliação como critério para escolher os melhores restaurantes.

## Estratégia da solução

O painel estratégico foi desenvolvido utilizando as métricas que refletem as principais visões do modelo de negócio da empresa, Cada visão é representada pelo seguinte conjunto de métricas:

### Visão de crescimento geral

1. Quantos restaurantes únicos estão registrados
2. Quantos países únicos estão registrados
3. Quantas cidades únicas estão registradas
4. Qual o total de avaliações feitas
5. Qual o total de tipos de culinária registrados
6. Quantos tipos de moeda como forma de pagamento
7. Mapa com localização de todos os restaurantes

### Visão de crescimento por país

1. Qual o país que possui mais cidades registradas
2. Qual o país que possui mais restaurantes registrados
3. Qual o país que possui a maior quantidade de tipos de culinária distintos
4. Qual o país que possui, na média, a maior nota registrada
5. Qual  do país que possui, na média , a menor nota  registrada

### Visão de crescimento por cidade

1. Qual a cidade que possui mais restaurantes registrados
2. Qual a cidade que possui mais restaurantes com nota média acima de 4
3. Qual a cidade que possui mais restaurantes com nota média abaixo de 2.5
4. Qual a cidade que possui a maior quantidade de tipos de culinária distintas

### Visão de crescimento por tipo culinário

1. **Qual o nome do restaurante com a maior nota média**
2. **Qual o tipo de culinária que possui a maior nota média**
3. **Qual o tipo culinário com mais restaurantes**

## Top 3 insights de dados

1. A Índia é o principal mercado deste Marketplace, pois concentra o maior número de cidades, restaurantes e tipos culinários por nação. Seguido pelos EUA.
2. O Brasil apresenta 3 cidades com alta taxa de restaurantes com notas inferiores a 2.5, Sendo: São Paulo, Brasília e Rio de Janeiro.
3. Os dois tipos culinários com mais restaurantes, são típicos dos respectivos países com maior parcela de mercado. Sendo North Indian e American.

## O produto final do projeto

Painel online interativo, hospedado em um Cloud e disponível para acesso em qualquer dispositivo conectado á internet.

O painel pode ser acessado através desse link: https://yagodq-fome-zero-main.streamlit.app/

## Conclusão

O objetivo desse projeto é criar um conjunto de gráficos e/ou tabelas que exibam essas métricas da melhor forma possível para o CEO.

Da visão da empresa podemos definir quais o maiores mercados, distribuição geográfica dos restaurantes e oferta de tipos culinários para melhor tomada de decisão e alocação de recursos por parte da empresa.

## Próximos passos

1. Criar novos filtros
2. Explorar outros tipos de gráficos
3. Explorar nossas visões relacionadas a entrega a domicilio e faixa de preço
