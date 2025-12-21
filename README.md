---

# 🗳️ AI-Integrated E-Voting System

A comprehensive Streamlit-based e-voting system using custom DSA (Hash Tables, Trie, Segment Tree) with secure SHA-256 vote handling and real-time results.

---

## 📋 Overview

This project demonstrates advanced DSA concepts including:

* **Hash Tables** with chaining for O(1) data access
* **Trie (Prefix Tree)** for efficient candidate search
* **List + Sorting** algorithms for leaderboard ranking
* **Segment Tree** for range queries (demo)
* **SHA-256 hashing** for vote integrity

---

## 🏗️ Architecture

```
e_voting_system/
│
├── app.py                        # Main Streamlit entry point
│
├── core/                         # Core algorithms and utilities
│   ├── data_structures.py        # HashTable, Trie, SegmentTree
│   ├── security.py               # SecurityManager (hashing, IDs)
│   ├── persistence.py            # DataPersistence (JSON storage)
│   └── utils.py                  # Helper functions
│
├── modules/                      # Functional modules
│   ├── registration.py           # Voter & Candidate registration
│   ├── voting.py                 # Vote casting logic
│   ├── results.py                # Results & Analytics
│   ├── dsa_dashboard.py          # DSA analysis dashboard
│   └── admin.py                  # Admin panel
│
├── data/                         # Data storage (auto-generated)
│   ├── voters.json
│   ├── candidates.json
│   ├── votes.json
│   └── metadata.json
│
└── requirements.txt              # Python dependencies
```

---

## 🚀 Installation & Setup

### Prerequisites

* Python 3.8 or higher
* pip package manager

### Step 1: Clone/Download the Project

```bash
cd e_voting_system
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Run the Application

```bash
streamlit run app.py
```

The application will open in your default browser at `http://localhost:8501`

---

## 📖 User Guide

### 1. **Home Page**

* View system statistics
* Monitor voter turnout
* See current leaders

### 2. **Voter Registration**

* Register new voters with name, age, and email
* Receive unique Voter ID (format: V123ABC456DEF)
* View all registered voters

### 3. **Candidate Registration**

* Register candidates with name and party
* Automatic insertion into Trie for fast search
* View all candidates

### 4. **Cast Vote**

* Two-step authentication process
* Select candidate from list
* Secure vote recording with SHA-256 hash

### 5. **Results & Analytics**

* Real-time leaderboard (sorted using O(N log N) algorithm)
* Interactive Plotly charts
* Turnout metrics and analysis
* Export results to CSV

### 6. **DSA Dashboard**

* Educational showcase of all DSA used
* Hash table statistics and load factors
* Trie prefix search demo
* Time/space complexity analysis

### 7. **Admin Panel** 🔐

* **Password:** `admin123`
* System statistics
* Backup & restore functionality
* Data export (CSV)
* System controls

---

## 🔧 Technical Details

### Data Structures

#### Hash Table

* **Implementation:** Chaining for collision resolution
* **Time Complexity:** O(1) average for insert/lookup/delete
* **Usage:** Stores voters, candidates, and votes
* **Features:** Load factor tracking, collision statistics

#### Trie (Prefix Tree)

* **Implementation:** Character-based tree structure
* **Time Complexity:** O(L) where L = word length
* **Usage:** Candidate name autocomplete and search
* **Features:** Prefix matching, efficient storage

#### List + Sorting

* **Implementation:** Python's Timsort (hybrid merge+insertion sort)
* **Time Complexity:** O(N log N)
* **Usage:** Leaderboard ranking
* **Features:** Stable sort, optimized for real-world data

#### Set

* **Implementation:** Python's built-in hash-based set
* **Time Complexity:** O(1) average
* **Usage:** Track voted voter IDs
* **Features:** Fast membership testing, duplicate prevention

### Security Features

1. **Vote Integrity:** SHA-256 hashing of vote data
2. **Unique IDs:** Cryptographically secure ID generation
3. **Duplicate Prevention:** Set-based voted tracking
4. **Data Validation:** Comprehensive input validation

### Persistence

* **Storage Format:** JSON files
* **Backup:** gzip compression
* **Auto-save:** Immediate persistence after each operation
* **Restore:** Versioned backup restoration

---

## 📊 Features

✅ **Voter Management**

* Registration with validation
* Unique voter ID generation
* Duplicate email prevention

✅ **Candidate Management**

* Registration with party affiliation
* Trie-based fast search
* Vote count tracking

✅ **Voting System**

* Secure authentication
* One person, one vote enforcement
* Tamper-proof vote recording

✅ **Analytics**

* Real-time results
* Interactive visualizations
* Turnout metrics
* Exportable data

✅ **Admin Controls**

* System statistics
* Backup/restore operations
* Data export capabilities
* System health monitoring

---

## 🎯 DSA Complexity Summary

| Operation            | Data Structure    | Time Complexity | Space Complexity |
| -------------------- | ----------------- | --------------- | ---------------- |
| Insert Voter         | Hash Table        | O(1) avg        | O(1)             |
| Lookup Voter         | Hash Table        | O(1) avg        | O(1)             |
| Insert Candidate     | Hash Table + Trie | O(1) + O(L)     | O(1) + O(L)      |
| Search Candidate     | Trie              | O(L)            | O(1)             |
| Cast Vote            | Hash Table + Set  | O(1)            | O(1)             |
| Check if Voted       | Set               | O(1)            | O(1)             |
| Generate Leaderboard | List + Sort       | O(N log N)      | O(N)             |
| Range Query          | Segment Tree      | O(log N)        | O(N)             |

*L = length of word/string, N = number of elements*

---

## 🔐 Admin Credentials

* **Username:** Admin (implicit)
* **Password:** `admin123`

---

## 📝 Default Configuration

* **Voters Hash Table Size:** 200
* **Candidates Hash Table Size:** 100
* **Votes Hash Table Size:** 500
* **Minimum Voting Age:** 18
* **Data Directory:** `e_voting_system/data/`

---

## 🛠️ Customization

### Change Admin Password

Edit `modules/admin.py`:

```python
ADMIN_PASSWORD = "your_new_password"
```

### Adjust Hash Table Sizes

Edit `modules/registration.py` in `initialize_session_state()`:

```python
st.session_state.voters = HashTable(size=500)  # Increase size
```

### Modify UI Theme

Edit custom CSS in `app.py`:

```python
st.markdown("""
<style>
    /* Your custom styles here */
</style>
""", unsafe_allow_html=True)
```

---

## 📦 Backup & Restore

### Create Backup

1. Navigate to Admin Panel
2. Go to "Backup & Restore" tab
3. Click "Create Backup Now"
4. Backups stored in `data/backups/` as `.json.gz` files

### Restore Backup

1. Navigate to Admin Panel
2. Go to "Backup & Restore" tab
3. Select backup timestamp
4. Click "Restore"
5. Refresh page to see restored data

---

## 🐛 Troubleshooting

### Issue: Module not found error

**Solution:** Ensure you're running from the correct directory:

```bash
cd e_voting_system
streamlit run app.py
```

### Issue: Data not persisting

**Solution:** Check write permissions for `data/` directory

### Issue: Streamlit not found

**Solution:** Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 📚 Educational Use

This project is excellent for:

* Learning DSA implementations
* Understanding hash tables and collision resolution
* Studying Trie data structures
* Exploring sorting algorithms
* Building real-world applications with Streamlit

---

## 🤝 Contributing

Feel free to fork and enhance:

* Add more visualizations
* Implement additional DSA
* Enhance security features
* Improve UI/UX
* Add unit tests

---

## 🎓 Learning Resources

* **Hash Tables:** [GeeksforGeeks](https://www.geeksforgeeks.org/hashing-data-structure/)
* **Trie:** [CP-Algorithms](https://cp-algorithms.com/string/trie.html)
* **Time Complexity:** [Big O Cheat Sheet](https://www.bigocheatsheet.com/)
* **Streamlit Docs:** [streamlit.io](https://docs.streamlit.io/)

---

## 🙏 Acknowledgments

Built with:

* **Streamlit** - Fast web app framework
* **Plotly** - Interactive visualizations
* **Python** - Core language
* **Custom DSA** - Hand-coded data structures

