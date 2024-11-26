import streamlit as st
from Groq_llm import Groq_LLM
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
            result = Groq_LLM(prompt)
            # st.write(result['output'])
            if result.content:
                st.chat_message("assistant").markdown(result.content )
                st.session_state.messages.append({
                                "role": "assistant",
                                "output": result.content })
            else:
                st.chat_message("assistant").markdown(result.error.message )
                st.session_state.messages.append({
                                "role": "assistant",
                                "output": result.error.message })
        except Exception as e:
            print(e)
            st.write("Error: Try a different question")
