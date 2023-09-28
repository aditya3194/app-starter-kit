import streamlit as st


# Create a Streamlit app
st.title("Banking Chatbot")

# Define a text input for user messages
# user_input = st.text_input("")


# Define a dictionary of user inputs and corresponding responses (rule-based)
responses = {
    "balance": "Your account balance is $5,000.",
    "transaction history": "You have three recent transactions: \n1. $100 deposit on 2023-09-25 \n2. $50 withdrawal on 2023-09-24 \n3. $200 deposit on 2023-09-23",
    "interest rates": "The current interest rate for savings accounts is 2.5% per annum.",
    "contact info": "You can reach our customer support at support@bank.com or call us at +1-800-123-4567.",
    "help": "I'm here to provide information about your account and our services. How can I assist you today?",
}

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

    # with st.chat_message("assistant"):
    #     with st.spinner("Thinking..."):
    #         response = generate_response(load+prompt) 
    #         st.write(response) 
    # message = {"role": "assistant", "content": responses[user_input]}
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
st.sidebar.markdown("1. Type your question in the text input.")
st.sidebar.markdown("2. Click the 'Send' button to get a response.")

