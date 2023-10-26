pip install faiss-cpu
import streamlit as st
import time
import random
from langchain.document_loaders import CSVLoader, PyPDFLoader
import glob
import IPython
import pandas as pd
from langchain.vectorstores import FAISS 
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.cohere import CohereEmbeddings
from langchain.chat_models import ChatCohere
# from unstructured.partition.pdf import partition_pdf
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import CohereRerank
from langchain.chains.router import MultiRetrievalQAChain

import os
import cohere
import sys
sys.path.append('../..')


api_key = "qULTg702krwwoZyfvyKHkwPQkVpBAl2v2liNhlCh"
os.environ['COHERE_API_KEY'] = "qULTg702krwwoZyfvyKHkwPQkVpBAl2v2liNhlCh"
co = cohere.Client(api_key) 
  
st.title("STC Chatbot")


# load databases locally
db_location = "./db/"
balanceSheetDB = FAISS.load_local(db_location+"balance_sheet_db", CohereEmbeddings())
finStatementDB = FAISS.load_local(db_location+"fin_statement_db", CohereEmbeddings())
pdfDB = FAISS.load_local(db_location+"pdf_db", CohereEmbeddings())

#base retrieval
balanceSheetRetriever = balanceSheetDB.as_retriever(
   search_kwargs={"k": 50} # Change 50 docs
)
finStatementRetriever = finStatementDB.as_retriever(
   search_kwargs={"k": 50} # Change 50 docs
)
pdf_retriever = pdfDB.as_retriever(
   search_kwargs={"k": 50} # Change 50 docs
)
 
# adding reranker
compressor = CohereRerank(top_n = 10)
balance_sheet_compression_retriever = ContextualCompressionRetriever(
    base_compressor=compressor, base_retriever=balanceSheetRetriever
)
fin_statement_compression_retriever = ContextualCompressionRetriever(
    base_compressor=compressor, base_retriever=finStatementRetriever
)
pdf_compression_retriever = ContextualCompressionRetriever(
    base_compressor=compressor, base_retriever=pdf_retriever
)
retriever_infos = [
    {
        "name": "Balance Sheet",
        "description": "Good for answering questions about Assets, Liabilities, Equity and other similar items which STC has on balance sheet for years 2018 and 2019",
        "retriever": balance_sheet_compression_retriever
    },
    {
        "name": "Financial Statement",
        "description": "Good for answering questions about financial performance of STC for years 2018 and 2019, such as Revenues, Profits, Costs of sales, amortizations etc",
        "retriever": fin_statement_compression_retriever
    },
    {
        "name": "PDF Files",
        "description": "Good for answering questions about STC strategy, its chairman and key activities, as well as other non-finance related questions for STC",
        "retriever": pdf_compression_retriever
    }
]

chain = MultiRetrievalQAChain.from_retrievers(ChatCohere(), retriever_infos, verbose=True,default_retriever=pdf_compression_retriever)

st.write(chain.run("Who is the Chief Executive officer of STC in year 2022?"))



# # Store LLM generated responses
# if "messages" not in st.session_state.keys():
#     st.session_state.messages = [{"role": "assistant", "content": "नमस्ते! कैसे मदद कर सकता हूँ?"}]

# # Display chat messages
# for message in st.session_state.messages:
#     with st.chat_message(message["role"]):
#         st.write(message["content"])


# # User-provided prompt
# if prompt := st.chat_input():
#     st.session_state.messages.append({"role": "user", "content": prompt})
#     with st.chat_message("user"):
#         st.write(prompt)





# if st.session_state.messages[-1]["role"] != "assistant":
#     with st.spinner("Thinking..."):
#         time.sleep(2)
#         user_input = prompt.lower()
#         message = []
#         if user_input in responses:
#             st.chat_message("assistant:")
#             st.write(responses[user_input])
#             message = {"role": "assistant", "content": responses[user_input]}
#         else:
#             st.chat_message("assistant:")
#             st.write("I'm sorry, I don't have the information you requested. Please try asking something else.")
#             message = {"role": "assistant", "content": "No Information about it"}
#     st.session_state.messages.append(message)


# # Handle user input and display responses
# # if st.button("Send"):
# #     user_input = user_input.lower()
# #     if user_input in responses:
# #         st.text("Chatbot:")
# #         st.write(responses[user_input])
# #     else:
# #         st.text("Chatbot:")
# #         st.write("I'm sorry, I don't have the information you requested. Please try asking something else.")

# Instructions for the user
st.sidebar.header("Instructions")
# st.sidebar.markdown("1. Type your question in the text input.")
# st.sidebar.markdown("2. Click the 'Send' button to get a response.")

