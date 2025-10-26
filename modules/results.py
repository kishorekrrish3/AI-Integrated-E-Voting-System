"""
Results Module
Handles election results, analytics, and visualizations
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from core import utils
from modules.registration import initialize_session_state

def results_dashboard():
    """Display election results and analytics"""
    initialize_session_state()

    st.header("📊 Election Results & Analytics")

    all_candidates = st.session_state.candidates.get_all()
    all_voters = st.session_state.voters.get_all()
    all_votes = st.session_state.votes.get_all()

    if not all_candidates:
        st.warning("⚠️ No candidates registered yet")
        return

    # Calculate statistics
    total_votes = len(all_votes)
    total_voters = len(all_voters)
    voted_count = len(st.session_state.voted_set)
    turnout = utils.calculate_turnout(total_voters, voted_count)

    # Display key metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("🗳️ Total Votes", total_votes)
    with col2:
        st.metric("👥 Total Voters", total_voters)
    with col3:
        st.metric("📊 Turnout", f"{turnout}%")
    with col4:
        winner = get_winner(all_candidates)
        st.metric("🏆 Leading", winner['name'] if winner else "N/A")

    st.markdown("---")

    # Leaderboard Section
    st.subheader("🏆 Leaderboard")
    display_leaderboard(all_candidates, total_votes)

    st.markdown("---")

    # Visualizations
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📊 Vote Distribution")
        plot_vote_distribution(all_candidates)

    with col2:
        st.subheader("🥧 Vote Share")
        plot_vote_pie_chart(all_candidates, total_votes)

    st.markdown("---")

    # Detailed Results Table
    st.subheader("📋 Detailed Results")
    display_detailed_results(all_candidates, total_votes)

    st.markdown("---")

    # Turnout Analysis
    st.subheader("📈 Turnout Analysis")
    display_turnout_analysis(total_voters, voted_count, turnout)

def display_leaderboard(candidates_dict, total_votes):
    """Display candidate leaderboard using List + Sort (O(N log N))"""
    sorted_candidates = utils.sort_candidates_by_votes(candidates_dict)

    if not sorted_candidates:
        st.info("No votes cast yet")
        return

    # Top 3 Highlight
    st.markdown("### 🥇 Top 3 Candidates")
    top_3 = sorted_candidates[:3]

    for rank, (cid, data) in enumerate(top_3, 1):
        medal = "🥇" if rank == 1 else "🥈" if rank == 2 else "🥉"
        percentage = utils.calculate_vote_percentage(data['votes'], total_votes)

        col1, col2, col3 = st.columns([3, 1, 1])
        with col1:
            st.markdown(f"### {medal} {data['name']}")
            st.caption(f"Party: {data['party']}")
        with col2:
            st.metric("Votes", data['votes'])
        with col3:
            st.metric("Share", f"{percentage}%")

    st.markdown("---")

    # Full Leaderboard
    st.markdown("### 📊 Complete Rankings")

    for rank, (cid, data) in enumerate(sorted_candidates, 1):
        percentage = utils.calculate_vote_percentage(data['votes'], total_votes)

        # Progress bar for votes
        col1, col2, col3, col4 = st.columns([1, 3, 1, 1])

        with col1:
            st.markdown(f"**#{rank}**")
        with col2:
            st.markdown(f"**{data['name']}** ({data['party']})")
        with col3:
            st.markdown(f"{data['votes']} votes")
        with col4:
            st.markdown(f"{percentage}%")

        # Visual progress bar
        if total_votes > 0:
            st.progress(data['votes'] / max(1, max(c[1]['votes'] for c in sorted_candidates)))

def plot_vote_distribution(candidates_dict):
    """Create bar chart for vote distribution using Plotly"""
    sorted_candidates = utils.sort_candidates_by_votes(candidates_dict)

    if not sorted_candidates:
        st.info("No data to display")
        return

    names = [data['name'] for _, data in sorted_candidates]
    votes = [data['votes'] for _, data in sorted_candidates]
    parties = [data['party'] for _, data in sorted_candidates]

    fig = go.Figure(data=[
        go.Bar(
            x=names,
            y=votes,
            text=votes,
            textposition='auto',
            marker=dict(
                color=votes,
                colorscale='Viridis',
                showscale=True
            ),
            hovertemplate='<b>%{x}</b><br>Votes: %{y}<extra></extra>'
        )
    ])

    fig.update_layout(
        title="Votes per Candidate",
        xaxis_title="Candidate",
        yaxis_title="Number of Votes",
        height=400,
        showlegend=False
    )

    st.plotly_chart(fig, use_container_width=True)

def plot_vote_pie_chart(candidates_dict, total_votes):
    """Create pie chart for vote share using Plotly"""
    if total_votes == 0:
        st.info("No votes cast yet")
        return

    sorted_candidates = utils.sort_candidates_by_votes(candidates_dict)

    names = [data['name'] for _, data in sorted_candidates if data['votes'] > 0]
    votes = [data['votes'] for _, data in sorted_candidates if data['votes'] > 0]

    if not names:
        st.info("No votes cast yet")
        return

    fig = go.Figure(data=[
        go.Pie(
            labels=names,
            values=votes,
            hovertemplate='<b>%{label}</b><br>Votes: %{value}<br>Share: %{percent}<extra></extra>',
            textinfo='label+percent',
            hole=0.3
        )
    ])

    fig.update_layout(
        title="Vote Share Distribution",
        height=400
    )

    st.plotly_chart(fig, use_container_width=True)

def display_detailed_results(candidates_dict, total_votes):
    """Display detailed results in a sortable table"""
    sorted_candidates = utils.sort_candidates_by_votes(candidates_dict)

    results_data = []
    for rank, (cid, data) in enumerate(sorted_candidates, 1):
        percentage = utils.calculate_vote_percentage(data['votes'], total_votes)
        results_data.append({
            'Rank': rank,
            'Candidate Name': data['name'],
            'Party': data['party'],
            'Votes Received': data['votes'],
            'Vote Share (%)': percentage,
            'Registered At': data['registered_at']
        })

    st.dataframe(results_data, use_container_width=True, hide_index=True)

    # Export option
    if st.button("📥 Export Results to CSV"):
        import pandas as pd
        df = pd.DataFrame(results_data)
        csv = df.to_csv(index=False)
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name="election_results.csv",
            mime="text/csv"
        )

def display_turnout_analysis(total_voters, voted_count, turnout):
    """Display voter turnout analysis"""
    col1, col2 = st.columns(2)

    with col1:
        # Turnout gauge chart
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=turnout,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Voter Turnout (%)"},
            delta={'reference': 50},
            gauge={
                'axis': {'range': [None, 100]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 30], 'color': "lightgray"},
                    {'range': [30, 60], 'color': "gray"},
                    {'range': [60, 100], 'color': "lightgreen"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 90
                }
            }
        ))

        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Voted vs Pending pie chart
        fig = go.Figure(data=[
            go.Pie(
                labels=['Voted', 'Pending'],
                values=[voted_count, total_voters - voted_count],
                marker=dict(colors=['#2ecc71', '#e74c3c']),
                hole=0.4
            )
        ])

        fig.update_layout(
            title="Voter Status",
            height=300
        )

        st.plotly_chart(fig, use_container_width=True)

    # Summary stats
    st.info(f"""
    **Turnout Summary:**
    - Total Registered Voters: {total_voters}
    - Voters Who Cast Votes: {voted_count}
    - Pending Voters: {total_voters - voted_count}
    - Turnout Percentage: {turnout}%
    """)

def get_winner(candidates_dict):
    """Get the candidate with the most votes"""
    sorted_candidates = utils.sort_candidates_by_votes(candidates_dict)
    if sorted_candidates and sorted_candidates[0][1]['votes'] > 0:
        return sorted_candidates[0][1]
    return None
