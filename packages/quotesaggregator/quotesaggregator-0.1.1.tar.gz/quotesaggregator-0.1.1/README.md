# QuotesAggregator

QuotesAggregator é um programa agregador de cotações que armazena os valores instantâneos de várias moedas para criar e
salvar candles de 1, 5 e 10 minutos num banco de dados através da API da Poloniex.

- Gráficos gerados a partir do banco de dados:

![Gráfico de 1 minuto](.github/chart1.png)
![Gráfico de 5 minutos](.github/chart5.png)
![Gráfico de 10 minutos](.github/chart10.png)

## Como Utilizar

### Pré-requisitos

- Docker

### Utilizando

```shell
docker-compose up
```

#### Executando testes unitários

```shell
# Na pasta raiz do projeto
# Lembre-se de criar um virtual env
pip install --no-cache-dir -r requirements.txt
pytest
```

### Criando graficos

[Clique aqui](createcharts/README.md)

## Decisões de arquitetura

- Uso de websokets ao invés da HTTP API
    - Para manter a consistência dos dados seria necessário fazer varias requisições a HTTP API e por conta disso,
      poderia ser bloqueado ou ter requisições recusadas, além de receber dados desnecessários. Por conta disso,
      utilizei websockets API, dessa forma basta inscrever-se no canal para receber a atualização das moedas.
- Uso de bibliotecas asyncio
    - O programa demanda muito IO (receber os dados da API, salva-los), por isso, optei por utilizar bibliotecas
      assíncronas para isso, dessa forma o programa não é bloqueado enquanto a recebimento ou envio de dados.
- Utilização do prodict
    - Para facilitar a leitura do código, utilizei uma classe que se comporta como um dicionário, porém deixa os
      atributos mais legíveis e funcionalidade de autocomplete.
- Objeto candle não contem a currency_id
    - Uma estratégia possível, seria utilizar outra chave do candle contendo o ‘id’ da moeda, porém ao utiliza-lo seria
      necessário iterar, no pior caso, sobre toda a lista, ou seja, O(n). Utilizando um dicionário que se comporta como
      um HashMap a complexidade de tempo cai para [O(1) no caso médio](https://wiki.python.org/moin/TimeComplexity#dict)
      , ou seja, a complexidade de tempo para encontrar os candles é O(1).
- Não Utilização de ORM
    - Também seria possível utilizar um ORM para facilitar a interação com o banco de dados, porém optei por utilizar
      consultas SQL para demonstrar os meus conhecimentos em SQL (Mesmo que, nessa prova, apenas consultas simples são
      necessárias).

### Funcionamento

Apos se inscrever no canal Ticker Data é recebido a atualização do valor das moedas, este valor é processado e a partir
dele é criado um objeto chave-valor que contem uma lista de 3 candles de 1 5, 10 minutos respetivamente, então estes
candles recebem atualização constantemente, até que o período do candle se encerre e ele seja salvo e os seus atributos
sobrescritos.

### Resultados

Os candles gerados podem ser encontrados através do banco de dados disponível na porta `34807` da sua maquina. Além
disso, o programa gera logs visíveis no stdout do docker.

### Dificuldades (Resolvidas)

- Como nunca havia testado métodos assíncronos ainda, foi difícil entender como faze-lo.
- Ao criar a tabela, utilizei float para os campos, e não comportava o tamanho de alguns valores recebidos, mudei para
  DECIMAL, que inclusive é mais adequado para valores monetários por problemas de arredondamento em outros tipos de
  dados.
- Por desconhecer o modulo aiomysql, cometi o erro de não fazer o commit na transação do banco de dados, e por isso, os
  dados não eram salvos. Para corrigir habilitei o autocommit na chamada.
- Tentei algumas abordagens para saber quando salvar o candle, uma delas deixava os valores de abertura-fechamento
  errado, pois ele considerava o valor pertencente ao período como valor inicial, sendo que o valor do final de um deve
  ser igual ao inicial do outro, além disso, o candle de 1 minuto estava sendo atualizado a cada 2 minutos, pois eu
  utilizei o modulo de 2 ao invés do de 1, porque todo numero dividido por um tem resto 0, então ele salvaria o candle
  antes de o minuto ser finalizado. A solução foi junto ao modulo, verificar se o tempo do candle atual era diferente do
  novo valor recebido.

# Observação importante

Um dos criterios da avaliação é o formato de distribuição, e tendo em vista que o programa é uma biblioteca que ao
chamar é sempre executada (Não dando espaço para que outro script consuma qualquer parte do mesmo), o programa é
distribuido através de um "executavel" hospedado no The Python Package Index (PyPi)
. [Link aqui](https://pypi.org/project/quotesaggregator/)

Para executa-lo faça (fora do projeto):

```shell
pipenv install quotesaggregator
pipenv shell
export QUOTESAGGREGATOR_DB_HOST=localhost 
export QUOTESAGGREGATOR_DB_PORT=3306 
export QUOTESAGGREGATOR_DB_USER=admin
export QUOTESAGGREGATOR_DB_PASSWORD=admin
export QUOTESAGGREGATOR_DB_NAME=quotes

agregator-run
```

Lembre-se que o container do MySQL deve estar rodando ou também é possível usar outro banco MySQL desde que ele possua a
tabela (comando de criação em [db-init/init.sql](db-init/init.sql)).
