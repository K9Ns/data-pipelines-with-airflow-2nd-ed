import weaviate

import streamlit as st
from langchain_openai.chat_models import AzureChatOpenAI  
import os
from langchain_openai import AzureOpenAIEmbeddings
from langchain_weaviate.vectorstores import WeaviateVectorStore
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from pages.utils import PROMPT
from vectorvault.utils import get_weaviate_client

import json

os.environ["AZURE_OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="Recipe Chat", page_icon="💬", layout="wide")

COLLECTION_NAME = "recipes"


st.title("Recipe Chat")

col1,col2 = st.columns([5,3])

weaviate_client = get_weaviate_client()

openai_client = AzureChatOpenAI(
    model_name="gpt-4", 
    deployment_name = "gpt-4",
    api_version="2024-02-01",
)

embeddings = AzureOpenAIEmbeddings(model="text-embedding-3-large")

weaviate_db = WeaviateVectorStore(
    client=weaviate_client, 
    index_name=COLLECTION_NAME, 
    text_key="chunk", 
    embedding=embeddings
)

combine_docs_chain = create_stuff_documents_chain(openai_client, PROMPT)
rag_chain = create_retrieval_chain(weaviate_db.as_retriever(), combine_docs_chain)

# 채팅 이력 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.context_documents = []

# 앱 재실행 시 이력의 채팅 메시지 표시
for message in st.session_state.messages:
    with col1.chat_message(message["role"]):
        st.markdown(message["content"])

# 사용자 입력 받기
if question := st.chat_input("What is up?"):

    col2.empty()
    # 사용자 메시지를 채팅 이력에 추가
    st.session_state.messages.append({"role": "user", "content": question})
    # 사용자 메시지를 채팅 메시지 컨테이너에 표시
    with col1.chat_message("user"):
        st.markdown(question)

    # 어시스턴트 응답을 채팅 메시지 컨테이너에 표시
    with col1.chat_message("assistant"):
        
        output = rag_chain.invoke({
                "input": question,
                "chat_history": [
                    (message["role"], message["content"]) 
                    for message 
                    in st.session_state.messages
                ]
            }
        )

        print(output["answer"])

        response = json.loads(output["answer"])

        st.session_state.context_documents = output["context"]
        
        weaviate_client.close()
    
        st.markdown(response["answer"])

    # if response["provided_recipe"]:

    #     for document in st.session_state.context_documents:
    #         col2.html(f"<sup>{document.metadata['filename']}</sub>")
    #         col2.html(f"<sup><sup>{document.metadata['chunk_uuid']}</sup></sup>")
    #         col2.html(f"<sub><sup>{document.page_content}</sup></sub>")

    st.session_state.messages.append({"role": "assistant", "content": response["answer"]})

