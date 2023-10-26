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

import cohere

api_key = "c6pobgap7gKlXOuU29e97W3Q0A2mJhg01hfbWwlJ"
co = cohere.Client(api_key) 
# Create a Streamlit app
st.title("STC Chatbot")


## Loading Text data from csv with pandas
def extract_text_from_csv(csv_path):
    df = pd.read_csv(csv_path)
    docs = []
    for row, item in df.iterrows():
        content = str(item.to_dict())
        metaDic = item.to_dict()
        metaDic['row'] = row
        metaDic['source'] = csv_path
        doc = Document(page_content = content, metadata = metaDic)
        docs.append(doc)
    return docs

#loading balancesheet only
balancesheetFile =r"https://github.com/aditya3194/app-starter-kit/raw/f102b905a51df9824713f97588b32e9b5ef297ac/Files/table1_2019_balance_sheet.csv"
balanceSheetItems = extract_text_from_csv(balancesheetFile)

#loading income statement only
statementFile =r"https://github.com/aditya3194/app-starter-kit/raw/f102b905a51df9824713f97588b32e9b5ef297ac/Files/table2_2019_income_statement.csv"
statementItems = extract_text_from_csv(statementFile)

## Loading Text data from PDF
def extract_text_from_pdf(pdf_path):
    raw_pdf_elements = partition_pdf(filename=pdf_path,
                                 # Unstructured first finds embedded image blocks
                                 extract_images_in_pdf=False,
                                 # Use layout model (YOLOX) to get bounding boxes (for tables) and find titles
                                 # Titles are any sub-section of the document 
                                 infer_table_structure=False, 
                                 # Post processing to aggregate text once we have the title 
                                 chunking_strategy="by_title",
                                 # Chunking params to aggregate text blocks
                                 # Attempt to create a new chunk 800 chars
                                 # Attempt to keep chunks > 500 chars 
                                 max_characters=1000, 
                                 new_after_n_chars=800, 
                                 combine_text_under_n_chars=500)
    docs = []
    for element in raw_pdf_elements:
        doc = Document(page_content = element.text, metadata = element.metadata.to_dict())
        docs.append(doc)
    
    return docs

pdf_path = r"https://github.com/aditya3194/app-starter-kit/raw/f102b905a51df9824713f97588b32e9b5ef297ac/Files/*.pdf"
pdfItems = []

for file in glob.glob(pdf_path):
    item = extract_text_from_pdf(file)
    pdfItems.extend(item)

st.text("This is some text.")

# #databases
# balanceSheetDB = FAISS.from_documents(balanceSheetItems, CohereEmbeddings())
# finStatementDB = FAISS.from_documents(statementItems, CohereEmbeddings())
# pdfDB = FAISS.from_documents(pdfItems, CohereEmbeddings())

# #base retrieval
# balanceSheetRetriever = balanceSheetDB.as_retriever(
#    search_kwargs={"k": 50} # Change 50 docs
# )
# finStatementRetriever = finStatementDB.as_retriever(
#    search_kwargs={"k": 50} # Change 50 docs
# )
# pdf_retriever = pdfDB.as_retriever(
#    search_kwargs={"k": 50} # Change 50 docs
# )

# # adding reranker
# compressor = CohereRerank(top_n = 10)
# balance_sheet_compression_retriever = ContextualCompressionRetriever(
#     base_compressor=compressor, base_retriever=balanceSheetRetriever
# )
# fin_statement_compression_retriever = ContextualCompressionRetriever(
#     base_compressor=compressor, base_retriever=finStatementRetriever
# )
# pdf_compression_retriever = ContextualCompressionRetriever(
#     base_compressor=compressor, base_retriever=pdf_retriever
# )
# retriever_infos = [
#     {
#         "name": "Balance Sheet",
#         "description": "Good for answering questions about Assets, Liabilities, Equity and other similar items which STC has on balance sheet for years 2018 and 2019",
#         "retriever": balance_sheet_compression_retriever
#     },
#     {
#         "name": "Financial Statement",
#         "description": "Good for answering questions about financial performance of STC for years 2018 and 2019, such as Revenues, Profits, Costs of sales, amortizations etc",
#         "retriever": fin_statement_compression_retriever
#     },
#     {
#         "name": "PDF Files",
#         "description": "Good for answering questions about STC strategy, its chairman and key activities, as well as other non-finance related questions for STC",
#         "retriever": pdf_compression_retriever
#     }
# ]

# chain = MultiRetrievalQAChain.from_retrievers(ChatCohere(), retriever_infos, verbose=True,default_retriever=pdf_compression_retriever)

# print(chain.run("Who is the Chief Executive officer of STC in year 2022?"))



# Store LLM generated responses
if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "नमस्ते! कैसे मदद कर सकता हूँ?"}]

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])


# User-provided prompt
if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)





if st.session_state.messages[-1]["role"] != "assistant":
    with st.spinner("Thinking..."):
        time.sleep(2)
        user_input = prompt.lower()
        message = []
        if user_input in responses:
            st.chat_message("assistant:")
            st.write(responses[user_input])
            message = {"role": "assistant", "content": responses[user_input]}
        else:
            st.chat_message("assistant:")
            st.write("I'm sorry, I don't have the information you requested. Please try asking something else.")
            message = {"role": "assistant", "content": "No Information about it"}
    st.session_state.messages.append(message)


# Handle user input and display responses
# if st.button("Send"):
#     user_input = user_input.lower()
#     if user_input in responses:
#         st.text("Chatbot:")
#         st.write(responses[user_input])
#     else:
#         st.text("Chatbot:")
#         st.write("I'm sorry, I don't have the information you requested. Please try asking something else.")

# Instructions for the user
st.sidebar.header("Instructions")
# st.sidebar.markdown("1. Type your question in the text input.")
# st.sidebar.markdown("2. Click the 'Send' button to get a response.")

