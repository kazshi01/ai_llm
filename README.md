## python 仮想環境

#### myenv　有効化

```bash
source myenv/bin/activate
```

#### myenv 無効化

```bash
deactivate
```

## ollama サーバー起動（※別ターミナルで起動する）

```bash
OLLAMA_HOST=127.0.0.1:12000 ollama serve
```
補足) デフォルトのollamaサーバーは`127.0.0.1:11434`だが、既に使用されているため`12000`に変更する。

## streamlit 起動

```bash
streamlit run local_llm.py
```
