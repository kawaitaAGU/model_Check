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

# APIキーの取得
if "OPENAI_API_KEY" not in st.secrets:
    st.error("❌ OPENAI_API_KEY が設定されていません。Streamlit CloudのSecretsに登録してください。")
    st.stop()

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
                # ダミーリクエスト（実質的に0トークンしか使わない）
                response = client.chat.completions.create(
                    model=model_name,
                    messages=[{"role": "user", "content": "Hello"}],
                    max_tokens=1
                )
                st.success(f"✅ モデル `{model_name}` はこのAPIキーで使用可能です！")

            except PermissionDeniedError as e:
                st.error(f"🚫 PermissionDeniedError: `{model_name}` は使えません。\n\n{e}")
            except AuthenticationError as e:
                st.error(f"🔑 APIキーが無効です: {e}")
            except NotFoundError as e:
                st.error(f"❓ モデルが存在しない、あるいは入力ミスの可能性があります。\n\n{e}")
            except BadRequestError as e:
                st.warning(f"⚠ モデルは存在しますが、別の設定エラーがある可能性があります。\n\n{e}")
            except Exception as e:
                st.error(f"❗️ その他のエラー:\n\n{e}")