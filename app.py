"""
AI-Integrated E-Voting System v4.0.0
Main Streamlit Application Entry Point
"""

import streamlit as st
from modules import registration, voting, results, dsa_dashboard, admin

# Page configuration
st.set_page_config(
    page_title="AI-Integrated E-Voting System",
    page_icon="🗳️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        padding: 1rem 0;
    }
    .version-badge {
        background-color: #28a745;
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 15px;
        font-size: 0.9rem;
        font-weight: bold;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        font-weight: 600;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

def main():
    """Main application function"""

    # Sidebar navigation
    st.sidebar.title("🗳️ E-Voting System")
    st.sidebar.markdown("---")

    # Navigation menu
    pages = [
        "🏠 Home",
        "📝 Voter Registration",
        "🎯 Candidate Registration",
        "🗳️ Cast Vote",
        "📊 Results & Analytics",
        "🧮 DSA Dashboard",
        "🔐 Admin Panel"
    ]

    choice = st.sidebar.radio("Navigate", pages, label_visibility="collapsed")

    st.sidebar.markdown("---")
    st.sidebar.info("""
    **Version:** 4.0.0

    **Features:**
    - Hash Table Storage
    - Trie-based Search
    - Secure Vote Hashing
    - Real-time Analytics
    - Admin Controls

    **Tech Stack:**
    - Python 3.x
    - Streamlit
    - Plotly
    - Custom DSA
    """)

    st.sidebar.markdown("---")
    st.sidebar.success("🔒 Secure & Transparent")

    # Main title
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div class="main-header">🗳️ AI-Integrated E-Voting System</div>', unsafe_allow_html=True)
        st.markdown('<p style="text-align: center;"><span class="version-badge">v4.0.0 - List/Sort Ranking</span></p>', unsafe_allow_html=True)

    st.markdown("---")

    # Route to appropriate page
    if choice == "🏠 Home":
        registration.display_home()

    elif choice == "📝 Voter Registration":
        registration.voter_registration_page()

    elif choice == "🎯 Candidate Registration":
        registration.candidate_registration_page()

    elif choice == "🗳️ Cast Vote":
        voting.cast_vote_page()

    elif choice == "📊 Results & Analytics":
        results.results_dashboard()

    elif choice == "🧮 DSA Dashboard":
        dsa_dashboard.display_dashboard()

    elif choice == "🔐 Admin Panel":
        admin.admin_panel_page()

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 1rem;">
        <p>🔐 Secure • 🚀 Fast • 📊 Transparent</p>
        <p style="font-size: 0.8rem;">Powered by Custom DSA Implementation | © 2024 E-Voting System</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
