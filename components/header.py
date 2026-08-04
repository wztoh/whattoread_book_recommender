import streamlit as st


def render_header(
    title: str = "WhatToRead",
    subtitle: str = "What should I read next?",
    title_size: str = "3rem",
    subtitle_size: str = "1.3rem",
    title_color: str = "#F7F0DF",
    subtitle_color: str = "#AEC1E8",
):
    """
    Settings for main app body headers
    """

    st.markdown(
        f"""
        <h1 style='text-align: center; 
                   color: {title_color}; 
                   font-size: {title_size};
                   margin-bottom: 0px;'>
            {title}
        </h1>
        <h3 style='text-align: center; 
                   font-size: {subtitle_size};
                   margin-top: -20px;
                   background: linear-gradient(90deg, {subtitle_color} 0%, {subtitle_color} 60%, rgba(174,193,232,0) 100%);
                   -webkit-background-clip: text;
                   -webkit-text-fill-color: transparent;
                   background-clip: text;
                   color: {subtitle_color};'>
            {subtitle}
        </h3>
        """,
        unsafe_allow_html=True
    )