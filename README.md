# API 01 - API REST com POSTGRES

## Integrantes:
````shell
- Ana Julia
- Anna Clara 
- Natali
```` 


## Dependencias do projeto 
```shell
 poetry add fastapi
 poetry add sqlmodel
 poetry add uvicorn
 poetry add psycopg2-binaty
```

## Iniciando o servidor http
```shell
 uvicorn src.server:app --reload
```

## Descrição do Projeto
Este projeto visa construir uma API de Resultado de avaliações calculados eletronicamente. A API é projetada para lidar com avaliações que consistem em dez questões de múltipla escolha, representadas pelas alternativas 'a', 'b', 'c' e 'd'.

## Rotas e Funcionalidades
### POST /provas
Endpoint para cadastrar uma nova prova na tabela "provas".

##### Requisição:
````shell
- Descrição da avaliação
- Data de realização
- Alternativas corretas para as questões Q1 a Q10
````
##### Validações:
Verifica se já existe uma prova com a mesma descrição e data.
Se existir, retorna status code 400 com a mensagem "Prova já cadastrada."
Se não existir, cadastra a prova e retorna os dados da prova inserida, com status code 201.

### POST /resultados_provas
Endpoint para inserir o resultado de um aluno.

##### Requisição:
````shell
- Nome do aluno
- ID da prova (relacionamento com a tabela "provas")
- Alternativas respondidas para as questões Q1 a Q10
````
##### Validações:
Verifica se a prova com o ID especificado existe no banco de dados.
Se não existir, retorna status code 404 com a mensagem "Prova não cadastrada."
Se existir, realiza a correção automática das respostas, atualiza a nota final e insere na tabela "resultados_provas".
Retorna os dados do resultado com status code 201.

### GET /resultados_provas/:prova_id
Endpoint para obter os resultados de todos os alunos de uma prova.

##### Requisição:
````shell
- ID da prova (parâmetro de rota)
````
##### Resposta:
````shell
- Descrição da prova
- Data de aplicação
- Array contendo os dados por aluno: nome, nota e resultado final ("aprovado", "recuperação" ou "reprovado").
````

### PATCH /provas_aplicadas/:id
Endpoint para alterar as respostas de um aluno em uma prova.

##### Requisição:
````shell
- ID do resultado na tabela "resultados_provas" (parâmetro de rota)
- Novas alternativas respondidas para as questões Q1 a Q10
````
##### Ação:
Recalcula a nota final usando a mesma lógica da inclusão do resultado da prova.

### DELETE /provas/:id
Endpoint para excluir uma prova, caso não existam resultados de provas cadastrados para a mesma.

##### Requisição:
````shell
- ID da prova (parâmetro de rota)
````
##### Validação:
Permite a exclusão apenas se não existirem resultados de provas cadastrados na tabela "resultados_provas" com o ID da prova.
Executando a API
Para executar a API, siga as instruções no arquivo README.md fornecido com o código-fonte. Certifique-se de configurar corretamente o ambiente e as dependências antes de iniciar a aplicação.
