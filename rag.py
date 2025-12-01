import chromadb
from docx import Document
import requests
import streamlit as st

# ベクトルDBセットアップ
DB_DIR = "./chroma_db"
chroma_client = chromadb.PersistentClient(path=DB_DIR)

try:
    chroma_client.delete_collection(name="local_docs")
except ValueError:
    pass 

st.session_state.collection = chroma_client.get_or_create_collection(
  name = "local_docs"
)

# Wordファイルを読み込む関数
def load_word_document(file):
  return "\n".join(para.text for para in Document(file).paragraphs)

# テキスト分割関数
def split_text(text):
    chunk_size = 500
    overlap = 50
    chunks = []
    start = 0
    
    # ここで separators を宣言する
    separators = ["\n\n", "\n", "。", "、", " ", ""]
    
    while start < len(text):
        # 基本の終了位置
        target_end = start + chunk_size
        
        # テキストの最後ならそのまま終了
        if target_end >= len(text):
            chunks.append(text[start:])
            break
            
        # 区切り文字を探して、chunk_size以内で最も後ろにある場所を見つける
        end = target_end
        found_separator = False
        
        # target_endからoverlap分くらい戻った範囲内で区切り文字を探す
        search_start = max(start, target_end - overlap)
        
        for sep in separators:
            if sep == "": # 区切り文字が見つからない場合は強制分割
                break
                
            # 区切り文字を検索（後ろから探す）
            sep_pos = text.rfind(sep, search_start, target_end)
            if sep_pos != -1:
                end = sep_pos + len(sep) # 区切り文字を含める
                found_separator = True
                break
        
        chunks.append(text[start:end])
        
        # 次の開始位置（オーバーラップを考慮、ただし区切り文字で切れた場合はそこから）
        if found_separator:
            start = end
        else:
            start += chunk_size - overlap
            
    return chunks

# テキストをベクトル化する関数
def ollama_embed(text):
  r = requests.post(
    "http://localhost:12000/api/embeddings",
    json = {"model": "nomic-embed-text:v1.5", "prompt": text}
  )
  data = r.json()
  return data["embedding"]
