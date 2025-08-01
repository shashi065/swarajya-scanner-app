import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

# -- Page config for wide layout --
st.set_page_config(layout="wide", page_title="Swarajya Scanner Dashboard")

# Sample user past queries data - replace with real data source
sample_queries = [
    {"query": "What are fundamental rights?", "url": "https://swarajyscanner.org/queries/1", "date": "2025-07-20"},
    {"query": "How to file a public grievance?", "url": "https://swarajyscanner.org/queries/2", "date": "2025-07-21"},
    {"query": "Right to education information", "url": "https://swarajyscanner.org/queries/3", "date": "2025-07-22"},
    {"query": "Latest constitutional amendments", "url": "https://swarajyscanner.org/queries/4", "date": "2025-07-23"},
    {"query": "Citizen duties overview", "url": "https://swarajyscanner.org/queries/5", "date": "2025-07-24"},
]

# Convert to DataFrame for display
df_queries = pd.DataFrame(sample_queries)
df_queries['date'] = pd.to_datetime(df_queries['date'])

# Simulate user activity data (e.g., queries per day) - replace with real
today = datetime.today()
dates = [today - timedelta(days=i) for i in range(15)]
activity_counts = [1,2,1,3,0,4,2,1,3,2,5,1,0,2,3]
df_activity = pd.DataFrame({"date": dates, "queries": activity_counts})
df_activity = df_activity.sort_values("date")

# --- Layout ---

# Top: Account Settings button left aligned
with st.container():
    col1, col2 = st.columns([1, 10])
    with col1:
        if st.button("⚙️ Account Settings"):
            st.info("Account Settings page coming soon!")
    with col2:
        st.markdown("<h1 style='text-align:center;'>Swarajya Scanner Dashboard</h1>", unsafe_allow_html=True)

st.markdown("---")

# Main dashboard: two columns
col_left, col_right = st.columns([3, 5])

with col_left:
    st.subheader("Your Past Queries")
    
    # Construct clickable links column
    def make_clickable(url, text):
        return f'<a href="{url}" target="_blank" rel="noopener noreferrer">{text}</a>'

    df_queries_display = df_queries.copy()
    df_queries_display['Query'] = df_queries_display.apply(lambda row: make_clickable(row['url'], row['query']), axis=1)
    df_queries_display['Date'] = df_queries_display['date'].dt.strftime('%Y-%m-%d')
    
    # Show as a table with clickable links in the Query column
    st.write(
        df_queries_display[['Query', 'Date']].to_html(escape=False, index=False),
        unsafe_allow_html=True
    )
    
    st.markdown("---")
    
    # Additional metric or stats widgets
    total_queries = len(df_queries)
    most_recent_date = df_queries['date'].max().strftime('%Y-%m-%d')
    
    st.metric(label="Total Queries", value=total_queries)
    st.metric(label="Most Recent Query Date", value=most_recent_date)

with col_right:
    st.subheader("Your Activity Over Time")
    # Line chart for activity over last 15 days
    fig = px.line(df_activity, x='date', y='queries', markers=True,
                  title='Queries Submitted Per Day',
                  labels={"date": "Date", "queries": "Number of Queries"})
    fig.update_layout(hovermode="x unified")
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Recent activity notification or messages
    st.subheader("Recent Activity")
    if activity_counts[-1] > 0:
        st.success(f"You submitted {activity_counts[-1]} queries today. Keep it up!")
    else:
        st.info("No queries submitted today. How about exploring some topics?")
    
    # Welcome note or tips
    st.markdown("""
    ### Welcome to Swarajya Scanner!
    Explore the Constitution in your pocket, raise issues and track public discourse.
    - Use the 'Account Settings' to manage your profile.
    - Check your query history on the left.
    - View your activity trends on the right.
    """)

# Initialize dark mode in session state if not present
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

# Sidebar toggle for dark mode
dark_mode = st.sidebar.checkbox("🌙 Dark Mode", value=st.session_state.dark_mode)
st.session_state.dark_mode = dark_mode

# Inject CSS based on dark_mode state
if st.session_state.dark_mode:
    st.markdown("""
        <style>
        body, .stApp {
            background-color: #181818 !important;
            color: #FFFFFF !important;  /* white text in dark mode */
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
            color: #000000 !important;  /* black text in light mode */
        }
        .stButton > button, .stTextInput > div > input {
            background-color: #0073e6 !important;
            color: white !important;
        }
        </style>
    """, unsafe_allow_html=True)
