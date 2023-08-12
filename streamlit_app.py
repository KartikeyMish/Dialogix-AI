import openai
import streamlit as st

st.set_page_config(
    page_title="Dialogbox-AI",
    page_icon="🧠"
    # layout="wide",
    # initial_sidebar_state="expanded",
    # menu_items={
    #     'Code': 'https://github.com/kartikeymishra/Dialogbox-AI',
    #     'Connect': "https://www.linkedin.com/in/kartikeymish/",
    #     'About': "# This is a header. This is an *extremely* cool app!"
    # }
)

with st.sidebar:
    st.title('🧠 Dialogbox-AI 🗣️')
    if 'OPENAI_API_KEY' in st.secrets:
        st.success('API key already provided!', icon='✅')
        openai.api_key = st.secrets['OPENAI_API_KEY']
    else:
        openai.api_key = st.text_input('Enter OpenAI API key:', type='password')
        if not (openai.api_key.startswith('sk-') and len(openai.api_key)==51):
            st.warning('Please enter your credentials!', icon='⚠️')           
            st.info('You can find your API key at https://beta.openai.com/account/api-keys', icon='🔑')
        else:
            st.success('Proceed to entering your prompt message & interact!', icon='👉')

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is in your mind?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        for response in openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": m["role"], "content": m["content"]}
                      for m in st.session_state.messages], stream=True):
            full_response += response.choices[0].delta.get("content", "")
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})
