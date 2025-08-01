import streamlit as st
import pandas as pd
import plotly.express as px

# -- Page config --
st.set_page_config(layout="wide", page_title="Swarajya Scanner Leaderboard")

st.title("🏆 Swarajya Scanner Leaderboard")

# Example data for leaderboard (replace with real data from your backend)
data = [
    {"Rank": 1, "Username": "raj_swaraj", "Points": 1500, "Profile": "https://swarajyscanner.org/users/raj_swaraj"},
    {"Rank": 2, "Username": "anita_jain", "Points": 1420, "Profile": "https://swarajyscanner.org/users/anita_jain"},
    {"Rank": 3, "Username": "vikram88", "Points": 1300, "Profile": "https://swarajyscanner.org/users/vikram88"},
    {"Rank": 4, "Username": "mira_das", "Points": 1200, "Profile": "https://swarajyscanner.org/users/mira_das"},
    {"Rank": 5, "Username": "suresh_k", "Points": 1150, "Profile": "https://swarajyscanner.org/users/suresh_k"},
    {"Rank": 6, "Username": "deepa_shah", "Points": 1100, "Profile": "https://swarajyscanner.org/users/deepa_shah"},
    {"Rank": 7, "Username": "prateek", "Points": 1050, "Profile": "https://swarajyscanner.org/users/prateek"},
    {"Rank": 8, "Username": "neha_verma", "Points": 930, "Profile": "https://swarajyscanner.org/users/neha_verma"},
    {"Rank": 9, "Username": "arvind_nair", "Points": 850, "Profile": "https://swarajyscanner.org/users/arvind_nair"},
    {"Rank": 10, "Username": "jyoti_m", "Points": 800, "Profile": "https://swarajyscanner.org/users/jyoti_m"},
]

df = pd.DataFrame(data)

# Search filter
search_username = st.text_input("Search username", "")

if search_username.strip():
    df_filtered = df[df['Username'].str.contains(search_username.strip(), case=False)]
else:
    df_filtered = df.copy()

# Sortable Table with clickable profile links
def make_clickable(url, text):
    return f'<a href="{url}" target="_blank" rel="noopener">{text}</a>'

df_filtered['Profile Link'] = df_filtered.apply(lambda row: make_clickable(row['Profile'], 'View Profile'), axis=1)
df_display = df_filtered[['Rank', 'Username', 'Points', 'Profile Link']]

st.markdown("### Leaderboard Table")
st.write(
    df_display.to_html(escape=False, index=False),
    unsafe_allow_html=True
)

st.markdown("---")

# Summary stats
total_users = len(df)
top_user = df.loc[df['Points'].idxmax()]

col1, col2, col3 = st.columns(3)
col1.metric("Total Users on Leaderboard", total_users)
col2.metric("Top Scorer", top_user['Username'])
col3.metric("Top Score", top_user['Points'])

st.markdown("---")

# Visual leaderboard - Bar chart of top 10
st.markdown("### Top 10 Users by Points")
fig = px.bar(df.sort_values('Points', ascending=False), x='Points', y='Username', orientation='h',
             text='Points', height=400,
             labels={'Points': 'Points', 'Username': 'User'},
             title="Top 10 Swarajya Scanner Contributors")
fig.update_traces(textposition='outside')
fig.update_layout(yaxis=dict(autorange="reversed"), margin=dict(l=100, r=20, t=40, b=40))
st.plotly_chart(fig, use_container_width=True)

st.markdown("""
---
*Leaderboard ranks users based on points accumulated through contributions such as raising public issues, contributing to discussions, and community engagement.*
""")

# Optional: Add any other features/features like badges, filters for timeframe etc. here

if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

dark_mode = st.sidebar.toggle("🌙 Dark Mode", value=st.session_state.dark_mode)
st.session_state.dark_mode = dark_mode

# Inject CSS based on dark_mode state
if st.session_state.dark_mode:
    st.markdown("""
        <style>
        body, .stApp {
            background-color: #181818 !important;
            color: #f4f4f9 !important;
        }
        .stButton > button, .stTextInput > div > input {
            background-color: #333 !important;
            color: #f4f4f9 !important;
        }
        </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
        <style>
        body, .stApp {
            background-color: #f4f4f9 !important;
            color: #333 !important;
        }
        .stButton > button, .stTextInput > div > input {
            background-color: #0073e6 !important;
            color: white !important;
        }
        </style>
    """, unsafe_allow_html=True)
