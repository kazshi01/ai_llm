import streamlit as st
from openai import OpenAI

import streamlit_ui
from rag import ollama_embed


client = OpenAI(
    api_key = "ollama",
    base_url = "http://localhost:12000/v1"
  )

model, temperature, system_prompt, prompt = streamlit_ui.setup_page()

# LLMへの問い合わせ処理
if prompt:

  with st.chat_message("user"):
    st.write(prompt)

  ## RAG検索
  query_embed = ollama_embed(prompt)
  results = st.session_state.collection.query(
    query_embeddings = [query_embed],
    n_results = 15
  )

  if results["documents"]:
    context_text = "\n".join(results["documents"][0])
    rag_prompt = f"""
    以下は関連ドキュメントの抜粋です。
    {context_text}
    この情報はユーザーの情報です。この情報を参考に以下の質問に答えてください。
    {prompt}
    """
  else:
    rag_prompt = ""

  st.session_state.messages.append({"role": "user", "content": prompt})

  if system_prompt.strip():
    messages = [{"role": "system", "content": f"{system_prompt}\n\n{rag_prompt}" if rag_prompt else system_prompt}] + st.session_state.messages
  else:
    messages = [{"role": "system", "content": rag_prompt}] + st.session_state.messages

  with st.chat_message("assistant"):
    placeholder = st.empty()
    stream_response = ""
    stream = client.chat.completions.create(
      model = model,
      messages = messages,
      temperature = temperature,
      stream = True
    )

    for chunk in stream:
      stream_response += chunk.choices[0].delta.content
      placeholder.write(stream_response)

  st.session_state.messages.append({"role": "assistant", "content": stream_response})
