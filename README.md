# 💬 Chatbot (Gemini)

Streamlit で動く Gemini チャットボット。API キーは `st.secrets` から読むので毎回入力しなくてよい。

### API キーの保管場所

キーの読み込み順: `secrets.toml` → 環境変数 `GEMINI_API_KEY` → サイドバーの手入力。

**ローカル / Codespaces**

```
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
# secrets.toml を開いて GEMINI_API_KEY にキーを貼る
```

`.streamlit/secrets.toml` は `.gitignore` 済みなので commit されない。**このリポジトリは公開なので、キーは絶対に commit しないこと。**

**Streamlit Community Cloud**

アプリの「Settings」→「Secrets」に以下を貼って保存する。

```
GEMINI_API_KEY = "ここにキー"
```

### ローカルで動かす

```
pip install -r requirements.txt
streamlit run streamlit_app.py
```
