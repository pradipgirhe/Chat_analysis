import streamlit as st
import preprocessor
import helper
import matplotlib.pyplot as plt

# --- Page config ---
st.set_page_config(
    page_title="WhatsApp Chat Analyzer",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Load Google Fonts ---
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)

# --- Custom CSS for the whole app with Pink accent ---
st.markdown("""
<style>
/* Global */
body, .stApp {
    background: #fff;
    font-family: 'Poppins', sans-serif;
    color: #222;
}

/* Navbar */
.navbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem 3rem;
    border-bottom: 1px solid #eee;
    font-weight: 600;
    font-size: 1.25rem;
}

.navbar .logo {
    color: #e91e63;
    font-weight: 700;
    font-size: 1.5rem;
}

.navbar .nav-links a {
    color: #e91e63;
    text-decoration: none;
    margin-left: 2rem;
    font-weight: 600;
    transition: color 0.3s ease;
}
.navbar .nav-links a:hover {
    color: #f48fb1;
}

/* Main container */
.main-container {
    max-width: 900px;
    margin: 3rem auto 5rem;
    padding: 0 1rem;
}

/* Drag & Drop upload */
.upload-area {
    border: 3px dashed #e91e63;
    border-radius: 15px;
    padding: 4rem 2rem;
    text-align: center;
    cursor: pointer;
    color: #e91e63;
    font-weight: 600;
    font-size: 1.25rem;
    box-shadow: 0 6px 12px rgba(233,30,99,0.1);
    transition: all 0.3s ease;
}
.upload-area:hover {
    background: #fce4ec;
    box-shadow: 0 10px 20px rgba(233,30,99,0.3);
}

/* Select files button */
.stButton > button {
    background-color: #e91e63 !important;
    color: white !important;
    font-weight: 700;
    padding: 0.75rem 2rem;
    font-size: 1.1rem;
    border-radius: 10px;
    border: none;
    margin-top: 1rem;
    box-shadow: 0 5px 15px rgba(233,30,99,0.3);
    transition: background-color 0.3s ease;
}
.stButton > button:hover {
    background-color: #f48fb1 !important;
}

/* Thumbnails container */
.thumbnails {
    display: flex;
    gap: 1rem;
    margin-top: 1.5rem;
    overflow-x: auto;
}
.thumbnail {
    flex: 0 0 auto;
    background: #fce4ec;
    border-radius: 12px;
    padding: 0.75rem 1.5rem;
    box-shadow: 0 3px 8px rgba(233,30,99,0.1);
    font-weight: 600;
    color: #e91e63;
    white-space: nowrap;
    user-select: none;
    cursor: default;
}

/* Section titles */
.section-title {
    font-size: 1.5rem;
    font-weight: 700;
    margin-top: 3rem;
    margin-bottom: 1rem;
    color: #e91e63;
}

/* Stats cards */
.stats-row {
    display: flex;
    gap: 1rem;
    flex-wrap: wrap;
}
.stat-card {
    background: #fff0f6;
    border-radius: 15px;
    flex: 1 1 18%;
    padding: 1.5rem 1rem;
    box-shadow: 0 5px 15px rgba(233,30,99,0.1);
    text-align: center;
}
.stat-card h4 {
    color: #f48fb1;
    font-weight: 700;
    margin-bottom: 0.25rem;
}
.stat-card .value {
    font-size: 2rem;
    font-weight: 900;
    color: #e91e63;
}

/* Chart containers */
.chart-container {
    background: #fff0f6;
    border-radius: 15px;
    padding: 1rem;
    box-shadow: 0 5px 15px rgba(233,30,99,0.1);
    margin-top: 1rem;
}

/* Footer */
footer {
    text-align: center;
    margin: 3rem 0 1rem;
    font-size: 0.875rem;
    color: #999;
}
footer a {
    color: #e91e63;
    text-decoration: none;
    margin: 0 1rem;
}
footer a:hover {
    color: #f48fb1;
}

/* Responsive */
@media(max-width: 720px) {
    .stats-row {
        flex-direction: column;
    }
    .stat-card {
        flex: 1 1 100%;
    }
    .navbar {
        padding: 1rem 1.5rem;
        font-size: 1rem;
    }
}
</style>
""", unsafe_allow_html=True)


# --- Navbar ---
st.markdown("""
<nav class="navbar">
  <div class="logo">WhatsApp Analyzer</div>
  <div class="nav-links">
    <a href="https://github.com/pradipgirhe/Chat_analysis" target="_blank">GitHub</a>
    <a href="https://help.whatsapp.com" target="_blank">Help</a>
  </div>
</nav>
""", unsafe_allow_html=True)


# --- Main Container ---
with st.container():
    st.markdown('<div class="main-container">', unsafe_allow_html=True)

    # Large drag-and-drop file uploader
    uploaded_file = st.file_uploader("", type=["txt"], help="Upload your WhatsApp chat txt file", label_visibility="collapsed", key="file_upload")
    if uploaded_file:
        # Show file name as thumbnail
        st.markdown(f'<div class="thumbnails"><div class="thumbnail">{uploaded_file.name}</div></div>', unsafe_allow_html=True)

        bytes_data = uploaded_file.getvalue()
        data = bytes_data.decode("utf-8")
        df = preprocessor.preprocess(data)

        # User select box
        user_list = df['user'].unique().tolist()
        if 'group_notification' in user_list:
            user_list.remove('group_notification')
        user_list.sort()
        user_list.insert(0, 'Overall')
        selected_user = st.selectbox("Show analysis wrt:", user_list)

        # Analysis button
        if st.button("Show Analysis"):
            # Stats
            num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user, df)

            # Stats row
            st.markdown('<div class="stats-row">', unsafe_allow_html=True)
            for title, val in [
                ("Total Messages", num_messages),
                ("Total Words", words),
                ("Media Shared", num_media_messages),
                ("Total Links Shared", num_links),
            ]:
                st.markdown(f'''
                    <div class="stat-card">
                        <h4>{title}</h4>
                        <div class="value">{val}</div>
                    </div>
                ''', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

            # Timeline chart
            st.markdown('<div class="section-title">Monthly Timeline</div>', unsafe_allow_html=True)
            timeline = helper.monthly_timeline(selected_user, df)
            fig, ax = plt.subplots(figsize=(9, 3))
            ax.plot(timeline['time'], timeline['message'], color="#e91e63", linewidth=2, marker='o')
            plt.xticks(rotation=45)
            plt.grid(alpha=0.3)
            st.pyplot(fig)

            # Most busy users for Overall
            if selected_user == 'Overall':
                st.markdown('<div class="section-title">Most Busy Users</div>', unsafe_allow_html=True)
                x, new_df = helper.most_busy_users(df)
                fig, ax = plt.subplots(figsize=(8, 3))
                colors = ['#e91e63', '#f48fb1', '#f8bbd0', '#fce4ec', '#fdeef4']
                ax.bar(x.index, x.values, color=colors[:len(x)])
                plt.xticks(rotation=45)
                st.pyplot(fig)
                st.dataframe(new_df)

            # Wordcloud
            st.markdown('<div class="section-title">Wordcloud</div>', unsafe_allow_html=True)
            df_wc = helper.create_word_cloud(selected_user, df)
            fig, ax = plt.subplots(figsize=(9, 4))
            ax.imshow(df_wc, interpolation='bilinear')
            ax.axis('off')
            st.pyplot(fig)

            # Most common words
            st.markdown('<div class="section-title">Most Common Words</div>', unsafe_allow_html=True)
            most_common_df = helper.most_common_words(selected_user, df)
            fig, ax = plt.subplots(figsize=(9, 3))
            ax.barh(most_common_df[0], most_common_df[1], color="#e91e63")
            ax.invert_yaxis()
            plt.xticks(rotation=0)
            st.pyplot(fig)
            st.dataframe(most_common_df)

            # Emoji Analysis
            st.markdown('<div class="section-title">Emoji Analysis</div>', unsafe_allow_html=True)
            emoji_df = helper.emoji_helper(selected_user, df)
            col1, col2 = st.columns(2)
            with col1:
                st.dataframe(emoji_df)
            with col2:
                fig, ax = plt.subplots(figsize=(5, 5))
                ax.pie(
                    emoji_df[1].head(),
                    labels=emoji_df[0].head(),
                    autopct='%0.2f%%',
                    colors=['#e91e63', '#f48fb1', '#f8bbd0', '#fce4ec', '#fdeef4'],
                    textprops={'color': 'black', 'fontsize': 12}
                )
                st.pyplot(fig)

    else:
        st.markdown('<div class="upload-area">Drag and drop your WhatsApp chat file here<br><br>or click to select files</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


# --- Footer ---
st.markdown("""
<footer>
    <a href="https://www.whatsapp.com/legal/privacy-policy" target="_blank">Privacy Policy</a> |
    <a href="https://help.whatsapp.com" target="_blank">Help</a> |
    <a href="mailto:support@example.com">Contact</a>
</footer>
""", unsafe_allow_html=True)
