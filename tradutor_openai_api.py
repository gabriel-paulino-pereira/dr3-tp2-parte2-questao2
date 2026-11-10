"""
Módulo de API FastAPI para tradução automática de Inglês para Francês 
utilizando LangChain integrado à API da OpenAI (com tratamento para ambiente sem chave).
"""

import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Verifico se a chave da OpenAI está definida; caso contrário, utilizo um LLM simulado para fins de teste acadêmico
if not os.environ.get("OPENAI_API_KEY"):
    from langchain_core.language_models.fake import FakeListLLM
    llm = FakeListLLM(responses=["[Modo Simulação OpenAI] La traduction de votre texte en français est simulée avec succès."])
else:
    from langchain_openai import ChatOpenAI
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)

# Inicializo a aplicação FastAPI definindo metadados descritivos
app = FastAPI(
    title="API de Tradução com OpenAI e LangChain",
    description="Serviço de tradução de inglês para francês utilizando LangChain e modelos da OpenAI.",
    version="1.0.1"
)

# Construo o template de prompt estruturado para orientar a tarefa de tradução
prompt_template = ChatPromptTemplate.from_messages([
    ("system", "Você é um tradutor profissional altamente preciso. Traduza o texto fornecido do inglês para o francês de forma natural e correta, retornando apenas o texto traduzido."),
    ("user", "{texto_ingles}")
])

# Encadeio os componentes utilizando o operador pipe (|) do LangChain (LCEL)
cadeia_traducao = prompt_template | llm | StrOutputParser()

# Defino o esquema de dados de entrada via Pydantic para validação do JSON
class RequisicaoTraducaoOpenAI(BaseModel):
    texto: str

@app.post("/traduzir-openai", summary="Traduz texto do inglês para o francês via LangChain e OpenAI")
def traduzir_com_openai(dados: RequisicaoTraducaoOpenAI):
    """
    Recebo um texto em inglês via JSON, executo a cadeia de tradução do LangChain 
    conectada à OpenAI (ou simulador) e retorno o texto traduzido estruturado em JSON.
    """
    try:
        # Valido se o texto de entrada não está vazio
        if not dados.texto.strip():
            raise HTTPException(status_code=400, detail="O texto de entrada não pode estar vazio.")
        
        # Executo a cadeia do LangChain passando o input validado
        resultado_traducao = cadeia_traducao.invoke({"texto_ingles": dados.texto})
        
        # Retorno o resultado estruturado para o cliente HTTP
        return {
            "texto_original_en": dados.texto,
            "texto_traduzido_fr": resultado_traducao
        }
        
    except Exception as erro:
        raise HTTPException(status_code=500, detail=f"Erro interno no processamento: {str(erro)}")

