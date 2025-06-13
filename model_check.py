import streamlit as st
from openai import OpenAI

st.title("GPTモデル使用可否チェック")

if "OPENAI_API_KEY" not in st.secrets:
    st.error("APIキーがありません")
    st.stop()

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

model_name = st.text_input("モデル名（例: gpt-4o）")

if st.button("チェック"):
    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": "Hello"}],
            max_tokens=1
        )
        st.success(f"{model_name} は使用可能です！")
    except Exception as e:
        st.error(f"使用できません: {e}")
