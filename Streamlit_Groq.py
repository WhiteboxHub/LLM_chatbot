import streamlit as st
from llm_2_opensource import LLM_model_Groq  # Import the function from the file
from FinetuningLLm import FineTuned_LLM_model_Groq
with st.sidebar:
    st.header("About")
    st.markdown(
        """
        This chatbot interfaces with data that has been synthetically generated.
        """
    )

    st.header("Example Questions")
    st.markdown("- Tell me more about <advisor name>?")
    st.markdown("- Do they have any disclosure? If so how recent and what was the dollar amount?")

st.title("System Chatbot")
st.info(
    """Ask me questions about CRD!"""
)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if "output" in message.keys():
            st.markdown(message["output"])

        

if prompt := st.chat_input("What do you want to know?"):
    st.chat_message("user").markdown(prompt)

    st.session_state.messages.append({"role": "user", "output": prompt})

    data = {"text": prompt}

    with st.spinner("Searching for an answer..."):
        # Call the external function with the input prompt
        try:
            result = LLM_model_Groq(prompt)
            # result = FineTuned_LLM_model_Groq(prompt)
            
            # st.write(result['output'])
            st.chat_message("assistant").markdown(result['output'] )
            st.session_state.messages.append({
                            "role": "assistant",
                            "output": result['output'] })
        except Exception as e:
            print(e)
            st.write("Error: Try a different question")
