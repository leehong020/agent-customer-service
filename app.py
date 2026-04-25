import streamlit as st

from agent.react_agent import ReactAgent


st.set_page_config(page_title="智能客服 Agent", page_icon="🤖")
st.title("智能客服 Agent")


@st.cache_resource
def get_agent() -> ReactAgent:
    return ReactAgent()


if "messages" not in st.session_state:
    st.session_state.messages = []


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


query = st.chat_input("请输入你的问题")

if query:
    st.session_state.messages.append({"role": "user", "content": query})

    with st.chat_message("user"):
        st.markdown(query)

    with st.chat_message("assistant"):
        output_placeholder = st.empty()
        answer = ""

        try:
            for chunk in get_agent().execute_stream(query):
                answer += chunk
                output_placeholder.markdown(answer)
        except Exception as e:
            answer = f"调用 Agent 出错：{e}"
            output_placeholder.error(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})
