import streamlit as st
from pytubefix import YouTube
import os
import re

import warnings
warnings.simplefilter("ignore")

# 진행률 콜백 함수
def progress_function(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage = bytes_downloaded / total_size * 100

    # Streamlit의 진행률 표시
    progress_bar.progress(int(percentage))
    progress_text.text(f"진행률: {int(percentage)}%")

# CSS
st.set_page_config(page_title="YTD", page_icon="🚀", layout="wide")
st.markdown(f"""
            <style>
            .stApp {{
                background-image: url("https://images.unsplash.com/photo-1516557070061-c3d1653fa646?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=2070&q=80"); 
                background-attachment: fixed;
                background-size: cover;
                color: #f5f5f5; /* 진한 흰색 */
            }}
            .stMarkdown, .stRadio, .stButton, .stTextInput, .stSelectbox, h1, h2, h3 {{
                color: #f5f5f5; /* 진한 흰색 */
            }}
            div.stDivider > div {{
                border-top: 1px solid #f5f5f5; /* 구분선을 진한 흰색으로 변경 */
            }}
            </style>
            """, unsafe_allow_html=True)



@st.cache(allow_output_mutation=True)
def get_info(url):
    yt = YouTube(url)
    streams = yt.streams.filter(progressive=True, type='video')
    details = {}
    details["image"] = yt.thumbnail_url
    details["streams"] = streams
    details["title"] = yt.title
    details["length"] = yt.length
    itag, resolutions, vformat, frate = ([] for i in range(4))
    for i in streams:
        res = re.search(r'(\d+)p', str(i))
        typ = re.search(r'video/(\w+)', str(i))
        fps = re.search(r'(\d+)fps', str(i))
        tag = re.search(r'(\d+)', str(i))
        itag.append(str(i)[tag.start():tag.end()])
        resolutions.append(str(i)[res.start():res.end()])
        vformat.append(str(i)[typ.start():typ.end()])
        frate.append(str(i)[fps.start():fps.end()])
    details["resolutions"] = resolutions
    details["itag"] = itag
    details["fps"] = frate
    details["format"] = vformat
    return details

st.markdown("## YouTube Downloader 🚀")
url = st.text_input("Paste URL here 👇", placeholder='https://www.youtube.com/')
if url:
    v_info = get_info(url)
    col1, col2 = st.columns([1, 1.5], gap="small")
    with st.container():
        with col1:            
            st.image(v_info["image"])   
        with col2:
            st.markdown("### Video Details ⚙️")
            res_inp = st.selectbox('__Select Resolution__', v_info["resolutions"])
            id = v_info["resolutions"].index(res_inp)            
            st.write(f"__Title:__ {v_info['title']}")
            st.write(f"__Length:__ {v_info['length']} sec")
            st.write(f"__Resolution:__ {v_info['resolutions'][id]}")
            st.write(f"__Frame Rate:__ {v_info['fps'][id]}")
            st.write(f"__Format:__ {v_info['format'][id]}")
            # file_name = st.text_input('__Save as 🎯__', placeholder=v_info['title'])

                
        
video_or_audio = st.radio("비디오 or 오디오?", ('비디오', '오디오'))
        
        # 진행률 표시 위젯 생성
progress_bar = st.progress(0)
progress_text = st.empty()

# 다운로드 버튼 생성
if st.button("다운로드"):
    if url:
        try:
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
