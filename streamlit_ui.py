import streamlit as st
from rag import load_word_document, split_text, ollama_embed


def setup_page():
  # streamlitの設定
  st.set_page_config(page_title="Local LLM Chat")

  st.sidebar.title("設定")
  model = st.sidebar.text_input("モデル名", value="llama3.1:8b")
  temperature = st.sidebar.slider("temperature", 0.0, 2.0, 0.3, 0.1)
  system_prompt = st.sidebar.text_area(
    "System Prompt",
    "あなたは有能なアシスタントです。日本語で回答してください",
  )

  ## ファイルアップロード
  upload_files = st.sidebar.file_uploader(
    "Wordファイルをアップロード(.docx)",
    type = ["docx"],
    accept_multiple_files = True
  )

  ## インデックス作成
  if st.sidebar.button("インデックス作成"):
    for file in upload_files:
      text = load_word_document(file)
      chunks = split_text(text)
      for i, chunk in enumerate(chunks):
        embed = ollama_embed(chunk)
        st.session_state.collection.add(
          documents = [chunk],
          embeddings = [embed],
          ids = [f"{file.name}_{i}"]
        )
    st.sidebar.success("インデックス作成完了")


  # state管理（会話履歴の保持）
  if "messages" not in st.session_state:
    st.session_state.messages = []

  if st.sidebar.button("会話をリセット"):
    st.session_state.messages = []

  for m in st.session_state.messages:
    with st.chat_message(m["role"]):
      st.write(m["content"])

  prompt = st.chat_input("メッセージを入力")

  return model, temperature, system_prompt, prompt
