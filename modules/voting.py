"""
Voting Module
Handles vote casting and validation
"""

import streamlit as st
from datetime import datetime
from core import utils
from modules.registration import initialize_session_state, save_all_data

def cast_vote_page():
    """Vote casting page"""
    initialize_session_state()

    st.header("🗳️ Cast Your Vote")
    st.markdown("Enter your Voter ID to cast your vote securely")

    # Two-step process: Authentication then Voting
    if 'authenticated_voter' not in st.session_state:
        st.session_state.authenticated_voter = None

    # Step 1: Voter Authentication
    if st.session_state.authenticated_voter is None:
        with st.form("voter_authentication"):
            voter_id = st.text_input("Enter Your Voter ID*", placeholder="V123ABC456DEF")
            authenticate = st.form_submit_button("Authenticate", use_container_width=True)

            if authenticate:
                if not voter_id:
                    st.error("❌ Please enter your Voter ID")
                elif not utils.is_valid_voter_id_format(voter_id):
                    st.error("❌ Invalid Voter ID format")
                else:
                    # Check if voter exists
                    voter_data = st.session_state.voters.get(voter_id)

                    if voter_data is None:
                        st.error("❌ Voter ID not found. Please register first.")
                    elif voter_data.get('has_voted', False):
                        st.error("❌ You have already voted. Multiple voting is not allowed.")
                    else:
                        st.session_state.authenticated_voter = voter_id
                        st.success(f"✅ Welcome, **{voter_data['name']}**!")
                        st.rerun()

    # Step 2: Vote Casting
    else:
        voter_id = st.session_state.authenticated_voter
        voter_data = st.session_state.voters.get(voter_id)

        st.success(f"✅ Authenticated as: **{voter_data['name']}** (ID: {voter_id})")

        # Get all candidates
        all_candidates = st.session_state.candidates.get_all()

        if not all_candidates:
            st.warning("⚠️ No candidates are registered yet. Please try again later.")
            if st.form_submit_button("Logout"):
                st.session_state.authenticated_voter = None
                st.rerun()
            return

        st.markdown("---")
        st.subheader("📋 Select Your Candidate")

        # Display candidates with radio buttons
        candidate_options = {}
        for cid, cdata in all_candidates.items():
            label = f"{cdata['name']} ({cdata['party']})"
            candidate_options[label] = cid

        with st.form("vote_casting_form"):
            selected_label = st.radio(
                "Choose a candidate:",
                options=list(candidate_options.keys()),
                index=None
            )

            st.markdown("---")
            col1, col2 = st.columns(2)

            with col1:
                submit_vote = st.form_submit_button("🗳️ Submit Vote", use_container_width=True, type="primary")
            with col2:
                cancel = st.form_submit_button("❌ Cancel", use_container_width=True)

            if cancel:
                st.session_state.authenticated_voter = None
                st.rerun()

            if submit_vote:
                if selected_label is None:
                    st.error("❌ Please select a candidate")
                else:
                    candidate_id = candidate_options[selected_label]

                    # Process vote
                    success = process_vote(voter_id, candidate_id)

                    if success:
                        st.success("✅ Your vote has been recorded successfully!")
                        st.balloons()

                        # Show vote confirmation
                        candidate_data = st.session_state.candidates.get(candidate_id)
                        st.info(f"""
                        **Vote Confirmation:**
                        - Voter: {voter_data['name']}
                        - Voted For: {candidate_data['name']} ({candidate_data['party']})
                        - Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                        """)

                        # Clear authentication
                        st.session_state.authenticated_voter = None

                        if st.form_submit_button("Return to Home"):
                            st.rerun()
                    else:
                        st.error("❌ Failed to record vote. Please try again.")

def process_vote(voter_id, candidate_id):
    """Process and record a vote"""
    try:
        # Get current timestamp
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Generate vote hash for integrity
        security = st.session_state.security_manager
        vote_hash = security.hash_vote(voter_id, candidate_id, timestamp)

        # Create vote record
        vote_data = utils.format_vote_data(voter_id, candidate_id, vote_hash)

        # Store vote
        vote_id = f"VOTE_{len(st.session_state.votes.get_all()) + 1}"
        st.session_state.votes.insert(vote_id, vote_data)

        # Update voter status
        voter_data = st.session_state.voters.get(voter_id)
        voter_data['has_voted'] = True
        st.session_state.voters.insert(voter_id, voter_data)
        st.session_state.voted_set.add(voter_id)

        # Update candidate vote count
        candidate_data = st.session_state.candidates.get(candidate_id)
        candidate_data['votes'] = candidate_data.get('votes', 0) + 1
        st.session_state.candidates.insert(candidate_id, candidate_data)

        # Update Trie with new vote count
        st.session_state.candidate_trie.insert(candidate_data['name'], candidate_data)

        # Save all data
        save_all_data()

        return True
    except Exception as e:
        st.error(f"Error processing vote: {e}")
        return False
