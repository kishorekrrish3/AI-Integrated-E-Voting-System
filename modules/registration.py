"""
Registration Module
Handles voter and candidate registration
"""

import streamlit as st
from core.data_structures import HashTable, Trie
from core.security import SecurityManager
from core.persistence import DataPersistence
from core import utils

def initialize_session_state():
    """Initialize session state variables"""
    if 'voters' not in st.session_state:
        st.session_state.voters = HashTable(size=200)
    if 'candidates' not in st.session_state:
        st.session_state.candidates = HashTable(size=100)
    if 'votes' not in st.session_state:
        st.session_state.votes = HashTable(size=500)
    if 'candidate_trie' not in st.session_state:
        st.session_state.candidate_trie = Trie()
    if 'voted_set' not in st.session_state:
        st.session_state.voted_set = set()
    if 'security_manager' not in st.session_state:
        st.session_state.security_manager = SecurityManager()
    if 'persistence' not in st.session_state:
        st.session_state.persistence = DataPersistence('e_voting_system/data')
    if 'data_loaded' not in st.session_state:
        load_all_data()
        st.session_state.data_loaded = True

def load_all_data():
    """Load all data from JSON files into memory"""
    persistence = DataPersistence('e_voting_system/data')
    persistence.initialize_default_files()

    # Load voters
    voters_data = persistence.load_data('voters.json')
    for voter_id, voter_info in voters_data.items():
        st.session_state.voters.insert(voter_id, voter_info)
        if voter_info.get('has_voted', False):
            st.session_state.voted_set.add(voter_id)

    # Load candidates
    candidates_data = persistence.load_data('candidates.json')
    for candidate_id, candidate_info in candidates_data.items():
        st.session_state.candidates.insert(candidate_id, candidate_info)
        st.session_state.candidate_trie.insert(candidate_info['name'], candidate_info)

    # Load votes
    votes_data = persistence.load_data('votes.json')
    for vote_id, vote_info in votes_data.items():
        st.session_state.votes.insert(vote_id, vote_info)

def save_all_data():
    """Save all data from memory to JSON files"""
    persistence = st.session_state.persistence

    persistence.save_data('voters.json', st.session_state.voters.to_dict())
    persistence.save_data('candidates.json', st.session_state.candidates.to_dict())
    persistence.save_data('votes.json', st.session_state.votes.to_dict())

def display_home():
    """Display home page with statistics"""
    initialize_session_state()

    st.header("🏠 Welcome to AI-Integrated E-Voting System")
    st.markdown("### System Overview")

    # Get statistics
    stats = utils.get_system_stats(
        st.session_state.voters.get_all(),
        st.session_state.candidates.get_all(),
        st.session_state.votes.get_all()
    )

    # Display metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("👥 Total Voters", stats['total_voters'])
        st.metric("✅ Voted", stats['voted_count'])

    with col2:
        st.metric("🎯 Candidates", stats['total_candidates'])
        st.metric("⏳ Pending", stats['pending_voters'])

    with col3:
        st.metric("🗳️ Total Votes", stats['total_votes'])
        st.metric("📊 Turnout", f"{stats['turnout_percentage']}%")

    with col4:
        ht_stats = st.session_state.voters.get_stats()
        st.metric("🔢 Load Factor", f"{ht_stats['load_factor']:.2f}")
        st.metric("⚡ Collisions", ht_stats['collisions'])

    st.markdown("---")

    # Live statistics
    st.subheader("📈 Live Statistics")

    col1, col2 = st.columns(2)

    with col1:
        st.info(f"""
        **Voter Statistics:**
        - Registered: {stats['total_voters']}
        - Voted: {stats['voted_count']}
        - Pending: {stats['pending_voters']}
        - Turnout Rate: {stats['turnout_percentage']}%
        """)

    with col2:
        st.info(f"""
        **System Health:**
        - Hash Table Size: {ht_stats['table_size']}
        - Hash Table Items: {ht_stats['total_items']}
        - Utilization: {ht_stats['utilization']:.1f}%
        - Max Chain Length: {ht_stats['max_chain_length']}
        """)

    # Top candidates
    if stats['total_candidates'] > 0:
        st.subheader("🏆 Current Leaders")
        top_3 = utils.get_top_n_candidates(st.session_state.candidates.get_all(), 3)

        for rank, (cid, data) in enumerate(top_3, 1):
            medal = "🥇" if rank == 1 else "🥈" if rank == 2 else "🥉"
            st.success(f"{medal} **{data['name']}** ({data['party']}) - {data['votes']} votes")

    st.markdown("---")
    st.info("👈 Use the sidebar to navigate through the system")

def voter_registration_page():
    """Voter registration page"""
    initialize_session_state()

    st.header("📝 Voter Registration")
    st.markdown("Register as a new voter to participate in elections")

    with st.form("voter_registration_form"):
        col1, col2 = st.columns(2)

        with col1:
            name = st.text_input("Full Name*", placeholder="Enter your full name")
            age = st.number_input("Age*", min_value=18, max_value=120, value=18)

        with col2:
            email = st.text_input("Email Address*", placeholder="your.email@example.com")

        submitted = st.form_submit_button("Register Voter", use_container_width=True)

        if submitted:
            # Validation
            if not name or not email:
                st.error("❌ Please fill all required fields")
            elif not utils.validate_name(name):
                st.error("❌ Name should contain only letters and spaces")
            elif not utils.validate_email(email):
                st.error("❌ Invalid email format")
            elif not utils.validate_age(age):
                st.error("❌ You must be at least 18 years old to register")
            else:
                # Check duplicate email
                all_voters = st.session_state.voters.get_all()
                email_exists = any(v['email'] == email.lower() for v in all_voters.values())

                if email_exists:
                    st.error("❌ This email is already registered")
                else:
                    # Generate voter ID
                    security = st.session_state.security_manager
                    voter_id = security.generate_voter_id()

                    # Format and save voter data
                    voter_data = utils.format_voter_data(name, age, email, voter_id)
                    st.session_state.voters.insert(voter_id, voter_data)

                    # Save to file
                    save_all_data()

                    st.success("✅ Voter registered successfully!")
                    st.info(f"**Your Voter ID:** `{voter_id}`")
                    st.warning("⚠️ Please save this ID. You'll need it to cast your vote.")

    # Display registered voters
    st.markdown("---")
    st.subheader("👥 Registered Voters")

    all_voters = st.session_state.voters.get_all()
    if all_voters:
        st.info(f"Total Registered Voters: {len(all_voters)}")

        # Search functionality
        search_term = st.text_input("🔍 Search by name or email", "")

        voters_list = []
        for voter_id, voter_data in all_voters.items():
            if search_term.lower() in voter_data['name'].lower() or search_term.lower() in voter_data['email'].lower():
                voters_list.append({
                    'Voter ID': voter_id,
                    'Name': voter_data['name'],
                    'Age': voter_data['age'],
                    'Email': voter_data['email'],
                    'Status': '✅ Voted' if voter_data.get('has_voted', False) else '⏳ Pending',
                    'Registered': voter_data['registered_at']
                })

        if voters_list:
            st.dataframe(voters_list, use_container_width=True, hide_index=True)
        else:
            st.info("No voters found matching your search")
    else:
        st.info("No voters registered yet")

def candidate_registration_page():
    """Candidate registration page"""
    initialize_session_state()

    st.header("🎯 Candidate Registration")
    st.markdown("Register as a candidate for the election")

    with st.form("candidate_registration_form"):
        col1, col2 = st.columns(2)

        with col1:
            name = st.text_input("Candidate Name*", placeholder="Enter candidate name")

        with col2:
            party = st.text_input("Party Name*", placeholder="Enter party name")

        submitted = st.form_submit_button("Register Candidate", use_container_width=True)

        if submitted:
            if not name or not party:
                st.error("❌ Please fill all required fields")
            elif not utils.validate_name(name):
                st.error("❌ Name should contain only letters and spaces")
            else:
                # Check duplicate name
                all_candidates = st.session_state.candidates.get_all()
                name_exists = any(c['name'].lower() == name.lower() for c in all_candidates.values())

                if name_exists:
                    st.error("❌ A candidate with this name is already registered")
                else:
                    # Generate candidate ID
                    security = st.session_state.security_manager
                    candidate_id = security.generate_candidate_id()

                    # Format and save candidate data
                    candidate_data = utils.format_candidate_data(name, party, candidate_id)
                    st.session_state.candidates.insert(candidate_id, candidate_data)
                    st.session_state.candidate_trie.insert(name, candidate_data)

                    # Save to file
                    save_all_data()

                    st.success(f"✅ Candidate registered successfully!")
                    st.info(f"**Candidate ID:** `{candidate_id}`")

    # Display registered candidates
    st.markdown("---")
    st.subheader("🎯 Registered Candidates")

    all_candidates = st.session_state.candidates.get_all()
    if all_candidates:
        st.info(f"Total Registered Candidates: {len(all_candidates)}")

        # Search using Trie
        search_prefix = st.text_input("🔍 Search by name prefix (using Trie)", "")

        if search_prefix:
            results = st.session_state.candidate_trie.starts_with(search_prefix)
            if results:
                st.success(f"Found {len(results)} candidate(s) matching '{search_prefix}'")
                for result in results:
                    data = result['data']
                    st.write(f"- **{data['name']}** ({data['party']}) - {data['votes']} votes")
            else:
                st.info(f"No candidates found starting with '{search_prefix}'")

        # Display all candidates
        candidates_list = []
        for candidate_id, candidate_data in all_candidates.items():
            candidates_list.append({
                'Candidate ID': candidate_id,
                'Name': candidate_data['name'],
                'Party': candidate_data['party'],
                'Votes': candidate_data['votes'],
                'Registered': candidate_data['registered_at']
            })

        # Sort by votes
        candidates_list = sorted(candidates_list, key=lambda x: x['Votes'], reverse=True)
        st.dataframe(candidates_list, use_container_width=True, hide_index=True)
    else:
        st.info("No candidates registered yet")
