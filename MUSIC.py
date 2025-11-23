# فایل: app.py
import streamlit as st
from PIL import Image
import numpy as np
from pydub import AudioSegment
from pydub.generators import Sine
import io
import time

st.set_page_config(page_title="Image to Music", layout="centered")
st.title("تبدیل تصویر به موسیقی 🎵")

# -------------------------------
# مرحله 1: آپلود تصویر
# -------------------------------
uploaded_file = st.file_uploader("یک تصویر انتخاب کنید", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    progress_text = st.empty()
    progress_bar = st.progress(0)

    # ---------- مرحله 1: باز کردن تصویر ----------
    progress_text.text("مرحله 1: باز کردن تصویر...")
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="تصویر آپلود شده", use_column_width=True)
    progress_bar.progress(10)
    time.sleep(0.2)

    # ---------- مرحله 2: تبدیل پیکسل‌ها به اعداد ----------
    progress_text.text("مرحله 2: تبدیل پیکسل‌ها به روشنایی...")
    img_array = np.array(image)
    brightness = img_array.mean(axis=2)
    small_brightness = brightness[::10, ::10].flatten()
    progress_bar.progress(30)
    time.sleep(0.2)

    # ---------- مرحله 3: نگاشت اعداد به نت موسیقی ----------
    progress_text.text("مرحله 3: نگاشت روشنایی به فرکانس‌ها...")
    min_freq = 220
    max_freq = 880
    freqs = np.interp(small_brightness, (small_brightness.min(), small_brightness.max()), (min_freq, max_freq))
    progress_bar.progress(50)
    time.sleep(0.2)

    # ---------- مرحله 4: ساخت موسیقی ----------
    progress_text.text("مرحله 4: ساخت موسیقی...")
    duration_ms = 200
    song = AudioSegment.silent(duration=0)

    total_notes = len(freqs)
    for i, f in enumerate(freqs):
        tone = Sine(f).to_audio_segment(duration=duration_ms)
        song += tone
        # بروزرسانی پیشرفت بر اساس تعداد نت‌ها
        if i % max(1, total_notes // 20) == 0:  # 20 مرحله در نوار پیشرفت
            progress_bar.progress(50 + int(40 * i / total_notes))

    progress_bar.progress(90)
    time.sleep(0.2)

    # ---------- مرحله 5: آماده‌سازی فایل و پخش ----------
    progress_text.text("مرحله 5: آماده‌سازی فایل و پخش موسیقی...")
    audio_buffer = io.BytesIO()
    song.export(audio_buffer, format="wav")
    audio_buffer.seek(0)
    progress_bar.progress(100)
    time.sleep(0.2)

    st.audio(audio_buffer, format="audio/wav")
    progress_text.text("")
    st.success("موسیقی تصویر شما آماده شد!")
