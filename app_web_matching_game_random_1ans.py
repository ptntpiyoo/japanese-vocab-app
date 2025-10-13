import streamlit as st
import pandas as pd
import random

# --- Cấu hình ---
CSV_FILE = r"C:\Thuy-Data\日本語N1\Python-Nihongo\Python_vocab_game_Web\vocab.csv"

# --- Load dữ liệu ---
def load_vocab(csv_file):
    df = pd.read_csv(csv_file)
    df = df[df["Status"].str.strip() == "Test"]
    return df.to_dict("records")

# --- Cập nhật trạng thái ---
def update_status(word, status):
    df = pd.read_csv(CSV_FILE)
    mask = (
        (df["Kanji"] == word["Kanji"]) &
        (df["Hiragana"] == word["Hiragana"]) &
        (df["Viet"] == word["Viet"])
    )
    df.loc[mask, "Status"] = status
    df.to_csv(CSV_FILE, index=False, encoding="utf-8-sig")

# --- Khởi tạo session_state ---
if "vocab" not in st.session_state:
    st.session_state.vocab = load_vocab(CSV_FILE)
    st.session_state.current_word = None
    st.session_state.show_answer = False
    st.session_state.result = ""
    st.session_state.no_pass = False

st.title("📘 Japanese Matching Game")
st.session_state.no_pass = st.checkbox("No Pass (set status = NG)", value=False)

# --- Hiển thị tiến độ ---
total_words = len(pd.read_csv(CSV_FILE))
learned_words = total_words - len(st.session_state.vocab)
st.write(f"Đã học {learned_words} / {total_words} từ")

# --- Khi hết từ ---
if not st.session_state.vocab:
    st.success("🎉 Hoàn tất tất cả các từ có Status = Test!")
    st.stop()

# --- Nếu chưa có từ hiện tại, chọn từ mới ---
if st.session_state.current_word is None:
    st.session_state.current_word = random.choice(st.session_state.vocab)
    st.session_state.show_answer = False
    st.session_state.result = ""

# --- Button tiếng Việt ---
viet_text = st.session_state.current_word["Viet"]
viet_key = "viet_btn"
viet_html = f"""
<style>
div.stButton > button#{viet_key} {{
    background-color: #a0e7e5;
    color: black;
    height: 80px;
    width: 600px;
    font-size: 22px;
    font-weight: bold;
    white-space: normal;
}}
</style>
"""
st.markdown(viet_html, unsafe_allow_html=True)

if st.button(viet_text, key=viet_key):
    st.session_state.show_answer = True

# --- Nếu đã click tiếng Việt, hiển thị đáp án đúng ---
if st.session_state.show_answer:
    correct_jp = f"{st.session_state.current_word['Kanji']}\n（{st.session_state.current_word['Hiragana']}）"
    btn_key = "answer_btn"

    jp_html = f"""
    <style>
    div.stButton > button#{btn_key} {{
        white-space: pre-line;
        background-color: #90ee90;
        height: 80px;
        width: 300px;
        font-size: 20px;
        font-weight: bold;
    }}
    </style>
    """
    st.markdown(jp_html, unsafe_allow_html=True)

    if st.button(correct_jp, key=btn_key):
        status = "OK" if not st.session_state.no_pass else "NG"
        update_status(st.session_state.current_word, status)

        # Loại từ vừa chơi khỏi danh sách
        st.session_state.vocab = [
            w for w in st.session_state.vocab
            if w["Kanji"] != st.session_state.current_word["Kanji"]
        ]

        # Reset để chọn từ mới
        st.session_state.current_word = None
        st.session_state.show_answer = False
        st.session_state.result = ""
        st.rerun()  # cập nhật UI ngay lập tức

# --- Hiển thị kết quả ---
if st.session_state.result:
    st.markdown(f"**{st.session_state.result}**")
