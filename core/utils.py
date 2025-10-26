"""
Utils Module
Helper functions for validation, formatting, and calculations
"""

import re
from datetime import datetime

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_age(age):
    """Validate age is valid integer and >= 18"""
    try:
        age_int = int(age)
        return 18 <= age_int <= 120
    except:
        return False

def validate_name(name):
    """Validate name contains only letters and spaces"""
    return bool(name) and all(c.isalpha() or c.isspace() for c in name)

def format_voter_data(name, age, email, voter_id):
    """Format voter data for storage"""
    return {
        'voter_id': voter_id,
        'name': name.strip(),
        'age': int(age),
        'email': email.lower().strip(),
        'registered_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'has_voted': False
    }

def format_candidate_data(name, party, candidate_id):
    """Format candidate data for storage"""
    return {
        'candidate_id': candidate_id,
        'name': name.strip(),
        'party': party.strip(),
        'registered_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'votes': 0
    }

def format_vote_data(voter_id, candidate_id, vote_hash):
    """Format vote data for storage"""
    return {
        'voter_id': voter_id,
        'candidate_id': candidate_id,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'vote_hash': vote_hash
    }

def calculate_turnout(total_voters, total_votes):
    """Calculate voter turnout percentage"""
    if total_voters == 0:
        return 0.0
    return round((total_votes / total_voters) * 100, 2)

def calculate_vote_percentage(candidate_votes, total_votes):
    """Calculate percentage of votes for a candidate"""
    if total_votes == 0:
        return 0.0
    return round((candidate_votes / total_votes) * 100, 2)

def sort_candidates_by_votes(candidates_dict):
    """Sort candidates by votes in descending order using list and sorted()"""
    # Convert dict to list of tuples
    candidates_list = [(cid, data) for cid, data in candidates_dict.items()]

    # Sort using Python's sorted() - O(N log N)
    sorted_list = sorted(candidates_list, key=lambda x: x[1].get('votes', 0), reverse=True)

    return sorted_list

def get_top_n_candidates(candidates_dict, n=3):
    """Get top N candidates by votes"""
    sorted_candidates = sort_candidates_by_votes(candidates_dict)
    return sorted_candidates[:n]

def format_time_ago(timestamp_str):
    """Convert timestamp to 'time ago' format"""
    try:
        timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')
        now = datetime.now()
        diff = now - timestamp

        if diff.days > 0:
            return f"{diff.days} day(s) ago"
        elif diff.seconds >= 3600:
            return f"{diff.seconds // 3600} hour(s) ago"
        elif diff.seconds >= 60:
            return f"{diff.seconds // 60} minute(s) ago"
        else:
            return "Just now"
    except:
        return "Unknown"

def generate_leaderboard_text(candidates_dict):
    """Generate formatted leaderboard text"""
    sorted_candidates = sort_candidates_by_votes(candidates_dict)

    if not sorted_candidates:
        return "No candidates registered yet."

    text = "🏆 LEADERBOARD\n" + "="*50 + "\n"

    for rank, (cid, data) in enumerate(sorted_candidates, 1):
        medal = "🥇" if rank == 1 else "🥈" if rank == 2 else "🥉" if rank == 3 else f"{rank}."
        text += f"{medal} {data['name']} ({data['party']}) - {data['votes']} votes\n"

    return text

def sanitize_string(text):
    """Sanitize string for safe storage and display"""
    return text.strip()[:200]  # Limit length and trim

def is_valid_voter_id_format(voter_id):
    """Check if voter ID matches expected format: V123ABC456DEF"""
    pattern = r'^V\d{3}[A-Z]{3}\d{3}[A-Z]{3}$'
    return re.match(pattern, voter_id) is not None

def is_valid_candidate_id_format(candidate_id):
    """Check if candidate ID starts with C"""
    return candidate_id.startswith('C') and len(candidate_id) >= 5

def get_system_stats(voters, candidates, votes):
    """Calculate comprehensive system statistics"""
    total_voters = len(voters)
    total_candidates = len(candidates)
    total_votes = len(votes)

    # Count voters who have voted
    voted_count = sum(1 for v in voters.values() if v.get('has_voted', False))

    turnout = calculate_turnout(total_voters, voted_count)

    return {
        'total_voters': total_voters,
        'total_candidates': total_candidates,
        'total_votes': total_votes,
        'voted_count': voted_count,
        'turnout_percentage': turnout,
        'pending_voters': total_voters - voted_count
    }
