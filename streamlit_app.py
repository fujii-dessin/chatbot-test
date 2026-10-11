import streamlit as st
from google import genai

# タイトルと説明の表示
st.title("💬 Gemini Chatbot")
st.write(
    "This is a simple chatbot that uses Google's Gemini model to generate responses. "
    "To use this app, you need to provide a Gemini API key, which you can get from Google AI Studio."
)

# ユーザーにGemini APIキーの入力を促す
gemini_api_key = st.text_input("Gemini API Key", type="password")

if not gemini_api_key:
    st.info("Please add your Gemini API key to continue.", icon="🗝️")
else:
    # Geminiクライアントの初期化
    client = genai.Client(api_key=gemini_api_key)

    # セッション状態にチャット履歴（メッセージ）がない場合は初期化
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # 過去のメッセージを表示
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # ユーザーからの入力を受け取る
    if prompt := st.chat_input("What is up?"):
        # ユーザーの入力をセッションに追加して表示
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # OpenAIの形式（"assistant"）をGeminiの形式（"model"）に変換して履歴を作成
        gemini_history = [
            {
                "role": "model" if m["role"] == "assistant" else "user",
                "parts": [m["content"]]
            }
            for m in st.session_state.messages[:-1] # 今回のプロンプトを除外した履歴
        ]

        # アシスタント（Gemini）の返答をストリーミングで生成
        with st.chat_message("assistant"):
            try:
                # チャットセッションを開始（過去の履歴を引き継ぐ）
                chat = client.chats.create(
                    model="gemini-2.5-flash", 
                    history=gemini_history
                )
                
                # ストリーミングレスポンスを受け取る関数
                def generate_stream():
                    response = chat.send_message(prompt, stream=True)
                    for chunk in response:
                        if chunk.text:
                            yield chunk.text

                # st.write_streamを使ってリアルタイムに表示
                response = st.write_stream(generate_stream())
                
                # アシスタントの返答をセッションに追加
                st.session_state.messages.append({"role": "assistant", "content": response})

            except Exception as e:
                st.error(f"エラーが発生しました: {e}")
