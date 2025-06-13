import streamlit as st
from openai import OpenAI
from openai.error import (
    AuthenticationError,
    PermissionDeniedError,
    NotFoundError,
    BadRequestError,
)

st.set_page_config(page_title="GPTモデル使用可否チェッカー", layout="centered")
st.title("🤖 GPTモデル使用可否チェッカー")

# OpenAI APIキーの取得
if "OPENAI_API_KEY" not in st.secrets:
    st.error("❌ OPENAI_API_KEY が設定されていません。Streamlit CloudのSecretsに登録してください。")
    st.stop()

# OpenAIクライアントを初期化
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# モデル名の入力欄
model_name = st.text_input("確認したいモデル名を入力してください（例: gpt-4o, gpt-4o-2024-11-20）")

# チェックボタン
if st.button("このモデルが使えるかチェック"):
    if not model_name:
        st.warning("モデル名を入力してください。")
    else:
        with st.spinner(f"{model_name} をテスト中..."):
            try:
                # 最小トークンでリクエストを送信して可否チェック
                response = client.chat.completions.create(
                    model=model_name,
                    messages=[{"role": "user", "content": "Hello"}],
                    max_tokens=1
                )
                st.success(f"✅ モデル `{model_name}` はこのAPIキーで使用可能です！")

            except PermissionDeniedError as e:
                st.error(f"🚫 使用できません（Permission Denied）: {e}")
            except AuthenticationError as e:
                st.error(f"🔑 APIキーが無効です: {e}")
            except NotFoundError as e:
                st.error(f"❓ モデルが見つかりません（スペルミスの可能性）: {e}")
            except BadRequestError as e:
                st.warning(f"⚠ モデルは存在しますが、構文やパラメータが不正な可能性があります: {e}")
            except Exception as e:
                st.error(f"❗️ その他のエラーが発生しました: {e}")
