# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['quotesaggregator', 'quotesaggregator.tests']

package_data = \
{'': ['*']}

install_requires = \
['aiologger>=0.6.1,<0.7.0',
 'aiomysql>=0.0.21,<0.0.22',
 'asyncio>=3.4.3,<4.0.0',
 'cryptography>=3.4.7,<4.0.0',
 'prodict>=0.8.16,<0.9.0',
 'pytz>=2021.1,<2022.0',
 'websockets>=9.0.1,<10.0.0']

entry_points = \
{'console_scripts': ['aggregator-run = '
                     'quotesaggregator.__main__:run_forever_async',
                     'aggregator-run-tests = '
                     'quotesaggregator.tests.test_aggregator:run']}

setup_kwargs = {
    'name': 'quotesaggregator',
    'version': '0.1.0',
    'description': 'QuotesAggregator is a quote aggregator program that stores the instant values of various currencies to create and save 1, 5 and 10 minute candles in a database through the Poloniex API.',
    'long_description': '# QuotesAggregator\n\nQuotesAggregator é um programa agregador de cotações que armazena os valores instantâneos de várias moedas para criar e\nsalvar candles de 1, 5 e 10 minutos num banco de dados através da API da Poloniex.\n\n- Gráficos gerados a partir do banco de dados:\n\n![Gráfico de 1 minuto](.github/chart1.png)\n![Gráfico de 5 minutos](.github/chart5.png)\n![Gráfico de 10 minutos](.github/chart10.png)\n\n## Como Utilizar\n\n### Pré-requisitos\n\n- Docker\n\n### Utilizando\n\n```shell\ndocker-compose up\n```\n\n#### Executando testes unitários\n\n```shell\n# Na pasta raiz do projeto\n# Lembre-se de criar um virtual env\npip install --no-cache-dir -r requirements.txt\npytest\n```\n\n### Criando graficos\n\n[Clique aqui](createcharts/README.md)\n\n## Decisões de arquitetura\n\n- Uso de websokets ao invés da HTTP API\n    - Para manter a consistência dos dados seria necessário fazer varias requisições a HTTP API e por conta disso,\n      poderia ser bloqueado ou ter requisições recusadas, além de receber dados desnecessários. Por conta disso,\n      utilizei websockets API, dessa forma basta inscrever-se no canal para receber a atualização das moedas.\n- Uso de bibliotecas asyncio\n    - O programa demanda muito IO (receber os dados da API, salva-los), por isso, optei por utilizar bibliotecas\n      assíncronas para isso, dessa forma o programa não é bloqueado enquanto a recebimento ou envio de dados.\n- Utilização do prodict\n    - Para facilitar a leitura do código, utilizei uma classe que se comporta como um dicionário, porém deixa os\n      atributos mais legíveis e funcionalidade de autocomplete.\n- Objeto candle não contem a currency_id\n    - Uma estratégia possível, seria utilizar outra chave do candle contendo o ‘id’ da moeda, porém ao utiliza-lo seria\n      necessário iterar, no pior caso, sobre toda a lista, ou seja, O(n). Utilizando um dicionário que se comporta como\n      um HashMap a complexidade de tempo cai para [O(1) no caso médio](https://wiki.python.org/moin/TimeComplexity#dict)\n      , ou seja, a complexidade de tempo para encontrar os candles é O(1).\n- Não Utilização de ORM\n    - Também seria possível utilizar um ORM para facilitar a interação com o banco de dados, porém optei por utilizar\n      consultas SQL para demonstrar os meus conhecimentos em SQL (Mesmo que, nessa prova, apenas consultas simples são\n      necessárias).\n\n### Funcionamento\n\nApos se inscrever no canal Ticker Data é recebido a atualização do valor das moedas, este valor é processado e a partir\ndele é criado um objeto chave-valor que contem uma lista de 3 candles de 1 5, 10 minutos respetivamente, então estes\ncandles recebem atualização constantemente, até que o período do candle se encerre e ele seja salvo e os seus atributos\nsobrescritos.\n\n### Resultados\n\nOs candles gerados podem ser encontrados através do banco de dados disponível na porta `34807` da sua maquina. Além\ndisso, o programa gera logs visíveis no stdout do docker.\n\n### Dificuldades (Resolvidas)\n\n- Como nunca havia testado métodos assíncronos ainda, foi difícil entender como faze-lo.\n- Ao criar a tabela, utilizei float para os campos, e não comportava o tamanho de alguns valores recebidos, mudei para\n  DECIMAL, que inclusive é mais adequado para valores monetários por problemas de arredondamento em outros tipos de\n  dados.\n- Por desconhecer o modulo aiomysql, cometi o erro de não fazer o commit na transação do banco de dados, e por isso, os\n  dados não eram salvos. Para corrigir habilitei o autocommit na chamada.\n- Tentei algumas abordagens para saber quando salvar o candle, uma delas deixava os valores de abertura-fechamento\n  errado, pois ele considerava o valor pertencente ao período como valor inicial, sendo que o valor do final de um deve\n  ser igual ao inicial do outro, além disso, o candle de 1 minuto estava sendo atualizado a cada 2 minutos, pois eu\n  utilizei o modulo de 2 ao invés do de 1, porque todo numero dividido por um tem resto 0, então ele salvaria o candle\n  antes de o minuto ser finalizado. A solução foi junto ao modulo, verificar se o tempo do candle atual era diferente do\n  novo valor recebido.',
    'author': 'Lucas',
    'author_email': 'lmr2199@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mrlucasrib/QuotesAggregator',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
