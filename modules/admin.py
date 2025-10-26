"""
Admin Panel Module
Password-protected administrative operations
"""

import streamlit as st
from datetime import datetime
from modules.registration import initialize_session_state, save_all_data

ADMIN_PASSWORD = "admin123"

def admin_panel_page():
    """Admin panel with password protection"""
    initialize_session_state()

    st.header("🔐 Admin Panel")

    # Check authentication
    if 'admin_authenticated' not in st.session_state:
        st.session_state.admin_authenticated = False

    if not st.session_state.admin_authenticated:
        display_login()
    else:
        display_admin_dashboard()

def display_login():
    """Display admin login form"""
    st.markdown("### 🔒 Admin Authentication Required")
    st.info("Default password: admin123")

    with st.form("admin_login"):
        password = st.text_input("Enter Admin Password", type="password")
        login = st.form_submit_button("Login", use_container_width=True)

        if login:
            if password == ADMIN_PASSWORD:
                st.session_state.admin_authenticated = True
                st.success("✅ Authentication successful!")
                st.rerun()
            else:
                st.error("❌ Invalid password")

def display_admin_dashboard():
    """Display admin dashboard with various controls"""
    st.success("✅ Logged in as Administrator")

    if st.button("🚪 Logout"):
        st.session_state.admin_authenticated = False
        st.rerun()

    st.markdown("---")

    # Tab navigation
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 System Stats",
        "💾 Backup & Restore",
        "📥 Data Export",
        "⚙️ System Controls"
    ])

    with tab1:
        display_system_statistics()

    with tab2:
        display_backup_controls()

    with tab3:
        display_export_controls()

    with tab4:
        display_system_controls()

def display_system_statistics():
    """Display comprehensive system statistics"""
    st.subheader("📊 System Statistics")

    # Get file statistics
    persistence = st.session_state.persistence
    file_stats = persistence.get_file_stats()

    st.markdown("### 📁 Data Files Information")

    for filename, stats in file_stats.items():
        with st.expander(f"📄 {filename}"):
            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("Records", stats['record_count'])
            with col2:
                st.metric("Size", f"{stats['size_kb']} KB")
            with col3:
                st.write(f"**Modified:** {stats['modified']}")

    st.markdown("---")

    # Hash Table Statistics
    st.markdown("### 🔢 Hash Table Statistics")

    col1, col2, col3 = st.columns(3)

    with col1:
        voters_stats = st.session_state.voters.get_stats()
        st.info(f"""
        **Voters Hash Table:**
        - Size: {voters_stats['table_size']}
        - Items: {voters_stats['total_items']}
        - Load Factor: {voters_stats['load_factor']:.3f}
        - Collisions: {voters_stats['collisions']}
        - Max Chain: {voters_stats['max_chain_length']}
        - Utilization: {voters_stats['utilization']:.1f}%
        """)

    with col2:
        candidates_stats = st.session_state.candidates.get_stats()
        st.info(f"""
        **Candidates Hash Table:**
        - Size: {candidates_stats['table_size']}
        - Items: {candidates_stats['total_items']}
        - Load Factor: {candidates_stats['load_factor']:.3f}
        - Collisions: {candidates_stats['collisions']}
        - Max Chain: {candidates_stats['max_chain_length']}
        - Utilization: {candidates_stats['utilization']:.1f}%
        """)

    with col3:
        votes_stats = st.session_state.votes.get_stats()
        st.info(f"""
        **Votes Hash Table:**
        - Size: {votes_stats['table_size']}
        - Items: {votes_stats['total_items']}
        - Load Factor: {votes_stats['load_factor']:.3f}
        - Collisions: {votes_stats['collisions']}
        - Max Chain: {votes_stats['max_chain_length']}
        - Utilization: {votes_stats['utilization']:.1f}%
        """)

    st.markdown("---")

    # Trie Statistics
    st.markdown("### 🌲 Trie Statistics")
    trie_stats = st.session_state.candidate_trie.get_stats()

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Words", trie_stats['total_words'])
    with col2:
        st.metric("Maximum Depth", trie_stats['max_depth'])

    st.markdown("---")

    # System metadata
    st.markdown("### ℹ️ System Metadata")
    metadata = persistence.load_data('metadata.json')

    st.json(metadata)

def display_backup_controls():
    """Display backup and restore controls"""
    st.subheader("💾 Backup & Restore")

    persistence = st.session_state.persistence

    # Create backup
    st.markdown("### 📦 Create Backup")
    st.write("Create a compressed backup of all system data")

    if st.button("Create Backup Now", use_container_width=True):
        with st.spinner("Creating backup..."):
            success, message = persistence.create_backup()
            if success:
                st.success(f"✅ {message}")
            else:
                st.error(f"❌ {message}")

    st.markdown("---")

    # List backups
    st.markdown("### 📋 Available Backups")
    backups = persistence.list_backups()

    if backups:
        st.info(f"Found {len(backups)} backup(s)")

        for backup_timestamp in backups:
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"🗂️ Backup: {backup_timestamp}")
            with col2:
                if st.button(f"Restore", key=f"restore_{backup_timestamp}"):
                    with st.spinner("Restoring backup..."):
                        success, message = persistence.restore_backup(backup_timestamp)
                        if success:
                            st.success(f"✅ {message}")
                            st.warning("⚠️ Please refresh the page to see restored data")
                        else:
                            st.error(f"❌ {message}")
    else:
        st.warning("No backups found. Create your first backup!")

    st.markdown("---")
    st.info("""
    **Backup Information:**
    - Backups are stored in `data/backups/` directory
    - Files are compressed using gzip
    - Each backup includes all JSON data files
    - Restore operations overwrite current data
    """)

def display_export_controls():
    """Display data export controls"""
    st.subheader("📥 Data Export")

    st.markdown("Export system data in various formats")

    persistence = st.session_state.persistence

    # Export voters
    st.markdown("### 👥 Export Voters")
    if st.button("Export Voters to CSV", use_container_width=True):
        voters_data = st.session_state.voters.get_all()
        if voters_data:
            success, message = persistence.export_to_csv(voters_data, 'voters_export.csv')
            if success:
                st.success(f"✅ {message}")

                # Provide download
                import pandas as pd
                df = pd.DataFrame.from_dict(voters_data, orient='index')
                csv = df.to_csv(index=False)
                st.download_button(
                    "📥 Download Voters CSV",
                    csv,
                    "voters_export.csv",
                    "text/csv"
                )
        else:
            st.warning("No voter data to export")

    st.markdown("---")

    # Export candidates
    st.markdown("### 🎯 Export Candidates")
    if st.button("Export Candidates to CSV", use_container_width=True):
        candidates_data = st.session_state.candidates.get_all()
        if candidates_data:
            success, message = persistence.export_to_csv(candidates_data, 'candidates_export.csv')
            if success:
                st.success(f"✅ {message}")

                import pandas as pd
                df = pd.DataFrame.from_dict(candidates_data, orient='index')
                csv = df.to_csv(index=False)
                st.download_button(
                    "📥 Download Candidates CSV",
                    csv,
                    "candidates_export.csv",
                    "text/csv"
                )
        else:
            st.warning("No candidate data to export")

    st.markdown("---")

    # Export votes
    st.markdown("### 🗳️ Export Votes")
    if st.button("Export Votes to CSV", use_container_width=True):
        votes_data = st.session_state.votes.get_all()
        if votes_data:
            success, message = persistence.export_to_csv(votes_data, 'votes_export.csv')
            if success:
                st.success(f"✅ {message}")

                import pandas as pd
                df = pd.DataFrame.from_dict(votes_data, orient='index')
                csv = df.to_csv(index=False)
                st.download_button(
                    "📥 Download Votes CSV",
                    csv,
                    "votes_export.csv",
                    "text/csv"
                )
        else:
            st.warning("No vote data to export")

def display_system_controls():
    """Display system control operations"""
    st.subheader("⚙️ System Controls")

    st.warning("⚠️ Use these controls with caution!")

    # Manual save
    st.markdown("### 💾 Manual Save")
    st.write("Force save all data to JSON files")

    if st.button("Save All Data Now", use_container_width=True):
        with st.spinner("Saving data..."):
            save_all_data()
            st.success("✅ All data saved successfully!")

    st.markdown("---")

    # System information
    st.markdown("### ℹ️ System Information")

    col1, col2 = st.columns(2)

    with col1:
        st.info(f"""
        **Version:** 4.0.0
        **Architecture:** Multi-File Modular
        **Storage:** Local JSON
        **Compression:** gzip
        """)

    with col2:
        st.info(f"""
        **Current Time:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        **Data Directory:** e_voting_system/data
        **Admin Status:** Authenticated ✅
        """)

    st.markdown("---")

    # Clear cache
    st.markdown("### 🔄 Clear Cache")
    st.write("Clear Streamlit's cache (requires page refresh)")

    if st.button("Clear Cache", use_container_width=True):
        st.cache_data.clear()
        st.success("✅ Cache cleared! Refresh the page.")

    st.markdown("---")

    # Danger zone
    st.markdown("### ⚠️ Danger Zone")

    with st.expander("🔴 Reset System (Destructive)", expanded=False):
        st.error("""
        **WARNING:** This will delete all data including:
        - All registered voters
        - All registered candidates
        - All cast votes
        - All backups

        This action cannot be undone!
        """)

        confirm = st.text_input("Type 'DELETE ALL DATA' to confirm")

        if st.button("🗑️ Reset System", type="primary"):
            if confirm == "DELETE ALL DATA":
                # This is just a placeholder - actual implementation would reset data
                st.error("Reset functionality disabled in this demo for safety")
                st.info("In production, this would clear all data files")
            else:
                st.warning("Confirmation text does not match")
