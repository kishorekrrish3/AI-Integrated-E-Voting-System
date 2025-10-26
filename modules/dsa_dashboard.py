"""
DSA Dashboard Module
Educational showcase of data structures and algorithms
"""

import streamlit as st
from modules.registration import initialize_session_state

def display_dashboard():
    """Display DSA analysis and complexity visualizations"""
    initialize_session_state()

    st.header("🧮 DSA Dashboard")
    st.markdown("Educational showcase of Data Structures & Algorithms used in the system")

    # Tab navigation
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Overview", 
        "🔢 Hash Table", 
        "🌲 Trie", 
        "⏱️ Complexity Analysis"
    ])

    with tab1:
        display_overview()

    with tab2:
        display_hashtable_analysis()

    with tab3:
        display_trie_analysis()

    with tab4:
        display_complexity_analysis()

def display_overview():
    """Display overview of all DSA components"""
    st.subheader("🎯 System Architecture Overview")

    st.markdown("""
    This e-voting system leverages custom-implemented data structures for optimal performance:

    ### 🔑 Key Data Structures:
    """)

    col1, col2 = st.columns(2)

    with col1:
        st.info("""
        **1. Hash Table (Chaining)**
        - Stores: Voters, Candidates, Votes
        - Operations: O(1) average
        - Collision Resolution: Chaining
        - Usage: Primary storage mechanism
        """)

        st.success("""
        **2. Trie (Prefix Tree)**
        - Stores: Candidate names
        - Operations: O(L) where L = word length
        - Features: Autocomplete, prefix search
        - Usage: Fast candidate lookup
        """)

    with col2:
        st.warning("""
        **3. Python Set**
        - Stores: Voted voter IDs
        - Operations: O(1) average
        - Purpose: Prevent duplicate voting
        - Usage: Integrity checking
        """)

        st.error("""
        **4. List + Sorting**
        - Stores: Candidate rankings
        - Operations: O(N log N)
        - Algorithm: Timsort (Python's sorted())
        - Usage: Leaderboard generation
        """)

    st.markdown("---")

    # System statistics
    st.subheader("📊 Current System Statistics")

    ht_voters = st.session_state.voters.get_stats()
    ht_candidates = st.session_state.candidates.get_stats()
    ht_votes = st.session_state.votes.get_stats()
    trie_stats = st.session_state.candidate_trie.get_stats()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Voters Hash Table Size", ht_voters['table_size'])
        st.metric("Items Stored", ht_voters['total_items'])
        st.metric("Load Factor", f"{ht_voters['load_factor']:.3f}")

    with col2:
        st.metric("Candidates Hash Table Size", ht_candidates['table_size'])
        st.metric("Items Stored", ht_candidates['total_items'])
        st.metric("Collisions", ht_candidates['collisions'])

    with col3:
        st.metric("Votes Hash Table Size", ht_votes['table_size'])
        st.metric("Items Stored", ht_votes['total_items'])
        st.metric("Trie Words", trie_stats['total_words'])

def display_hashtable_analysis():
    """Display hash table analysis and statistics"""
    st.subheader("🔢 Hash Table Analysis")

    st.markdown("""
    ### Implementation Details:
    - **Collision Resolution:** Chaining (using lists)
    - **Hash Function:** Python's built-in `hash()` with modulo
    - **Load Factor:** Items / Table Size
    - **Dynamic:** Can grow as needed
    """)

    # Get statistics for all hash tables
    voters_stats = st.session_state.voters.get_stats()
    candidates_stats = st.session_state.candidates.get_stats()
    votes_stats = st.session_state.votes.get_stats()

    st.markdown("---")
    st.subheader("📊 Comparative Statistics")

    # Create comparison table
    comparison_data = {
        'Hash Table': ['Voters', 'Candidates', 'Votes'],
        'Size': [voters_stats['table_size'], candidates_stats['table_size'], votes_stats['table_size']],
        'Items': [voters_stats['total_items'], candidates_stats['total_items'], votes_stats['total_items']],
        'Load Factor': [
            f"{voters_stats['load_factor']:.3f}",
            f"{candidates_stats['load_factor']:.3f}",
            f"{votes_stats['load_factor']:.3f}"
        ],
        'Collisions': [voters_stats['collisions'], candidates_stats['collisions'], votes_stats['collisions']],
        'Max Chain': [voters_stats['max_chain_length'], candidates_stats['max_chain_length'], votes_stats['max_chain_length']],
        'Utilization %': [
            f"{voters_stats['utilization']:.1f}",
            f"{candidates_stats['utilization']:.1f}",
            f"{votes_stats['utilization']:.1f}"
        ]
    }

    st.table(comparison_data)

    st.markdown("---")
    st.subheader("💡 Performance Insights")

    # Calculate average load factor
    avg_load_factor = (voters_stats['load_factor'] + candidates_stats['load_factor'] + votes_stats['load_factor']) / 3
    total_collisions = voters_stats['collisions'] + candidates_stats['collisions'] + votes_stats['collisions']

    col1, col2 = st.columns(2)

    with col1:
        if avg_load_factor < 0.7:
            st.success(f"✅ **Optimal Load Factor:** {avg_load_factor:.3f}")
            st.write("The hash tables are operating efficiently with low collision probability.")
        elif avg_load_factor < 1.0:
            st.warning(f"⚠️ **Moderate Load Factor:** {avg_load_factor:.3f}")
            st.write("Performance is acceptable but consider resizing if data grows significantly.")
        else:
            st.error(f"❌ **High Load Factor:** {avg_load_factor:.3f}")
            st.write("Consider increasing table size to improve performance.")

    with col2:
        st.metric("Total Collisions Across All Tables", total_collisions)
        st.write(f"Collision Rate: {(total_collisions / max(1, sum([voters_stats['total_items'], candidates_stats['total_items'], votes_stats['total_items']])) * 100):.2f}%")

    st.markdown("---")
    st.subheader("🔍 Live Hash Table Lookup Demo")

    demo_type = st.selectbox("Select Hash Table", ["Voters", "Candidates", "Votes"])

    if demo_type == "Voters":
        all_items = st.session_state.voters.get_all()
        if all_items:
            selected_key = st.selectbox("Select Voter ID", list(all_items.keys()))
            if st.button("Lookup"):
                result = st.session_state.voters.get(selected_key)
                st.success(f"Found in O(1) time!")
                st.json(result)

    elif demo_type == "Candidates":
        all_items = st.session_state.candidates.get_all()
        if all_items:
            selected_key = st.selectbox("Select Candidate ID", list(all_items.keys()))
            if st.button("Lookup"):
                result = st.session_state.candidates.get(selected_key)
                st.success(f"Found in O(1) time!")
                st.json(result)

    else:  # Votes
        all_items = st.session_state.votes.get_all()
        if all_items:
            selected_key = st.selectbox("Select Vote ID", list(all_items.keys()))
            if st.button("Lookup"):
                result = st.session_state.votes.get(selected_key)
                st.success(f"Found in O(1) time!")
                st.json(result)

def display_trie_analysis():
    """Display Trie structure analysis"""
    st.subheader("🌲 Trie (Prefix Tree) Analysis")

    st.markdown("""
    ### Implementation Details:
    - **Purpose:** Fast prefix-based candidate name search
    - **Structure:** Tree where each node represents a character
    - **Search Time:** O(L) where L is the length of the search string
    - **Space:** O(ALPHABET_SIZE × N × L) in worst case
    """)

    trie_stats = st.session_state.candidate_trie.get_stats()

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Total Words Stored", trie_stats['total_words'])
        st.metric("Maximum Depth", trie_stats['max_depth'])

    with col2:
        st.info("""
        **Advantages:**
        - Fast prefix matching
        - Memory-efficient for common prefixes
        - Enables autocomplete functionality
        - No collision handling needed
        """)

    st.markdown("---")
    st.subheader("🔍 Interactive Prefix Search Demo")

    prefix_input = st.text_input("Enter prefix to search candidates:", "")

    if prefix_input:
        results = st.session_state.candidate_trie.starts_with(prefix_input)

        st.info(f"⏱️ Search completed in O({len(prefix_input)}) time")

        if results:
            st.success(f"✅ Found {len(results)} candidate(s) matching '{prefix_input}':")

            for result in results:
                data = result['data']
                st.write(f"- **{data['name']}** ({data['party']}) - {data['votes']} votes")
        else:
            st.warning(f"❌ No candidates found with prefix '{prefix_input}'")

    st.markdown("---")
    st.subheader("📊 Trie Visualization Concept")

    st.markdown("""
    ```
    Example Trie Structure for candidates:

    Root
    ├── A
    │   ├── L
    │   │   ├── I
    │   │   │   └── C (Alice) ✓
    │   ├── N
    │       └── N (Ann) ✓
    ├── B
    │   ├── O
    │       └── B (Bob) ✓
    └── C
        ├── H
            └── A (Charles) ✓

    Searching "A" returns: Alice, Ann
    Searching "AL" returns: Alice
    Searching "B" returns: Bob
    ```
    """)

def display_complexity_analysis():
    """Display time and space complexity analysis"""
    st.subheader("⏱️ Time & Space Complexity Analysis")

    st.markdown("""
    ### 📚 Big O Notation Reference:
    - **O(1)** - Constant time (fastest)
    - **O(log N)** - Logarithmic time
    - **O(N)** - Linear time
    - **O(N log N)** - Log-linear time
    - **O(N²)** - Quadratic time
    """)

    st.markdown("---")
    st.subheader("🔢 Hash Table Operations")

    hash_table_data = {
        'Operation': ['Insert', 'Lookup', 'Delete', 'Contains'],
        'Average Time': ['O(1)', 'O(1)', 'O(1)', 'O(1)'],
        'Worst Case Time': ['O(N)', 'O(N)', 'O(N)', 'O(N)'],
        'Space': ['O(N)', 'O(1)', 'O(1)', 'O(1)'],
        'Notes': [
            'Amortized O(1) with good hash function',
            'Worst case with all collisions',
            'Must traverse chain if collision',
            'Same as lookup operation'
        ]
    }
    st.table(hash_table_data)

    st.markdown("---")
    st.subheader("🌲 Trie Operations")

    trie_data = {
        'Operation': ['Insert', 'Search', 'Prefix Search', 'Delete'],
        'Time Complexity': ['O(L)', 'O(L)', 'O(L + K)', 'O(L)'],
        'Space': ['O(ALPHABET × L)', 'O(1)', 'O(K)', 'O(1)'],
        'Notes': [
            'L = length of word',
            'L = length of search word',
            'K = number of results',
            'L = length of word to delete'
        ]
    }
    st.table(trie_data)

    st.markdown("---")
    st.subheader("📊 Sorting Operations")

    sort_data = {
        'Algorithm': ['Python sorted()', 'List creation', 'Leaderboard generation'],
        'Time Complexity': ['O(N log N)', 'O(N)', 'O(N log N)'],
        'Space': ['O(N)', 'O(N)', 'O(N)'],
        'Implementation': [
            'Timsort (hybrid of merge + insertion)',
            'Convert dict to list',
            'Sort + display operations'
        ]
    }
    st.table(sort_data)

    st.markdown("---")
    st.subheader("🎯 System-Wide Complexity Summary")

    col1, col2 = st.columns(2)

    with col1:
        st.success("""
        **Voter Registration:**
        - Validation: O(1)
        - ID Generation: O(1)
        - Storage (Hash): O(1)
        - **Total: O(1)**
        """)

        st.info("""
        **Candidate Registration:**
        - Validation: O(1)
        - Hash Insert: O(1)
        - Trie Insert: O(L)
        - **Total: O(L)**
        """)

    with col2:
        st.warning("""
        **Vote Casting:**
        - Authentication: O(1)
        - Vote Recording: O(1)
        - Update Counts: O(1)
        - **Total: O(1)**
        """)

        st.error("""
        **Results Generation:**
        - Data Collection: O(N)
        - Sorting: O(N log N)
        - Display: O(N)
        - **Total: O(N log N)**
        """)

    st.markdown("---")
    st.subheader("💡 Performance Optimization Tips")

    st.markdown("""
    1. **Hash Table Sizing:** Keep load factor < 0.75 for optimal performance
    2. **Trie Efficiency:** Most effective when many words share common prefixes
    3. **Sorting:** Results are cached until new votes are cast
    4. **Memory:** All data structures use O(N) space relative to data size
    """)
