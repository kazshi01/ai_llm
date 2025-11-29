import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="Local LLM Chat")

st.sidebar.title("設定")
model = st.sidebar.text_input("モデル名", value="llama3.1:8b")
temperature = st.sidebar.slider("temperature", 0.0, 2.0, 0.3, 0.1)
system_prompt = st.sidebar.text_area(
  "System Prompt",
  "あなたは有能なアシスタントです。日本語で回答してください",
)

if "messages" not in st.session_state:
  st.session_state.messages = []

if st.sidebar.button("会話をリセット"):
  st.session_state.messages = []

for m in st.session_state.messages:
  with st.chat_message(m["role"]):
    st.write(m["content"])

prompt = st.chat_input("メッセージを入力")

if prompt:
  client = OpenAI(
    api_key="ollama",
    base_url="http://localhost:12000/v1"
  )

  st.session_state.messages.append({"role": "user", "content": prompt})

  with st.chat_message("user"):
    st.write(prompt)

  if system_prompt.strip():
    messages = [{"role": "system_prompt", "content": system_prompt}] + st.session_state.messages
  else:
    messages = st.session_state.messages

  with st.chat_message("assistant"):
    placeholder = st.empty()
    stream_response = ""
    stream = client.chat.completions.create(
      model=model,
      messages=messages,
      temperature=temperature,
      stream=True
    )

    for chunk in stream:
      stream_response += chunk.choices[0].delta.content
      placeholder.write(stream_response)

  st.session_state.messages.append({"role": "assistant", "content": stream_response})
