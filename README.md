LangChain e FastAPI - Parte 2: Questão 2 (Tradução EN-FR com OpenAI)

Serviço de tradução de inglês para francês utilizando o framework LangChain (com LCEL e templates de prompt) integrado à API de modelos da OpenAI.
Tecnologias Utilizadas

    Python

    FastAPI / Pydantic

    LangChain (ChatOpenAI, ChatPromptTemplate, StrOutputParser)

Configuração e Execução

    Ative o ambiente virtual executando no PowerShell:
    .\venv\Scripts\Activate

    Instale as dependências executando:
    pip install fastapi uvicorn langchain langchain-openai langchain-core pydantic

    Defina a variável de ambiente com a chave da OpenAI (ou utilize o modo de simulação embutido caso esteja sem chave):
    $env:OPENAI_API_KEY="sua-chave-de-api-aqui"

    Inicie o servidor executando:
    uvicorn tradutor_openai_api:app --reload

    Acesse o Swagger UI em:
    http://127.0.0.1:8000/docs
