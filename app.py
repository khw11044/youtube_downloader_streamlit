import streamlit as st
from pytubefix import YouTube
from pytubefix.cli import on_progress

# 진행률 콜백 함수
def progress_function(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage = bytes_downloaded / total_size * 100

    # Streamlit의 진행률 표시
    progress_bar.progress(int(percentage))
    progress_text.text(f"진행률: {int(percentage)}%")

# Streamlit 앱
st.title("YouTube 비디오/오디오 다운로더")
st.write("YouTube 링크를 입력하고 비디오 또는 오디오를 선택하세요.")

video_or_audio = st.radio("비디오 or 오디오?", ('비디오', '오디오'))
url = st.text_input("링크를 입력하세요:")

# 진행률 표시 위젯 생성
progress_bar = st.progress(0)
progress_text = st.empty()

# 다운로드 버튼 생성
if st.button("다운로드"):
    if url:
        try:
            # `use_po_token=True` 옵션 추가
            yt = YouTube(url, on_progress_callback=progress_function)
            st.write(f"제목: {yt.title}")

            if video_or_audio == '비디오':
                ys = yt.streams.get_highest_resolution()
                ys.download()
                st.success("비디오 다운로드 완료!")
            else:
                ys = yt.streams.get_audio_only()
                ys.download(mp3=True)
                st.success("오디오 다운로드 완료!")
        except Exception as e:
            st.error(f"에러 발생: {e}")
    else:
        st.warning("링크를 입력하세요.")