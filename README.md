# Web scrapper para posts políticos

Web scrapper para extração de posts relacionados a eleição de 2024 nos EUA. Este projeto tem como objetivo identificar como os posts em rede social refletem o clima político de eleições.

## Instruções

Para executar o scrapper basta criar um virtual enviroment e instalar as dependências.

python3 -m venv env

pip install -r requirements.txt


## Datasets
results.json 
    - Todos os posts obtidos

results_1.json e results_2.json
    - Submissões segregadas por keywords
    - Usadas para etapa de análise

clean_1.json e clean_2.json
    - Dados limpos

sentiment_results.json
    - Resultados de análise gerados pelo Vader