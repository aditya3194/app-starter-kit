import streamlit as st

# Define a dictionary of user inputs and corresponding responses (rule-based)
responses = {
    "balance": "Your account balance is $5,000.",
    "transaction history": "You have three recent transactions: \n1. $100 deposit on 2023-09-25 \n2. $50 withdrawal on 2023-09-24 \n3. $200 deposit on 2023-09-23",
    "interest rates": "The current interest rate for savings accounts is 2.5% per annum.",
    "contact info": "You can reach our customer support at support@bank.com or call us at +1-800-123-4567.",
    "help": "I'm here to provide information about your account and our services. How can I assist you today?",
}

# Create a Streamlit app
st.title("Banking Chatbot")

# Define a text input for user messages
user_input = st.text_input("You:", "")

# Handle user input and display responses
if st.button("Send"):
    user_input = user_input.lower()
    if user_input in responses:
        st.text("Chatbot:")
        st.write(responses[user_input])
    else:
        st.text("Chatbot:")
        st.write("I'm sorry, I don't have the information you requested. Please try asking something else.")

# Instructions for the user
st.sidebar.header("Instructions")
st.sidebar.markdown("1. Type your question in the text input.")
st.sidebar.markdown("2. Click the 'Send' button to get a response.")

