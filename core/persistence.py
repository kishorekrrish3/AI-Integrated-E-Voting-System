"""
Persistence Module
Handles data storage, loading, and backup operations
"""

import json
import os
import gzip
import shutil
from datetime import datetime

class DataPersistence:
    """Manages file-based data persistence with backup support"""

    def __init__(self, data_dir='data'):
        self.data_dir = data_dir
        self.ensure_data_directory()

    def ensure_data_directory(self):
        """Create data directory if it doesn't exist"""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)

    def get_file_path(self, filename):
        """Get full path for data file"""
        return os.path.join(self.data_dir, filename)

    def save_data(self, filename, data):
        """Save data to JSON file"""
        try:
            filepath = self.get_file_path(filename)
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving {filename}: {e}")
            return False

    def load_data(self, filename):
        """Load data from JSON file"""
        try:
            filepath = self.get_file_path(filename)
            if os.path.exists(filepath):
                with open(filepath, 'r') as f:
                    return json.load(f)
            return {}
        except Exception as e:
            print(f"Error loading {filename}: {e}")
            return {}

    def create_backup(self):
        """Create compressed backup of all data files"""
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_dir = os.path.join(self.data_dir, 'backups')

            if not os.path.exists(backup_dir):
                os.makedirs(backup_dir)

            # List of files to backup
            files_to_backup = ['voters.json', 'candidates.json', 'votes.json', 'metadata.json']

            backup_count = 0
            for filename in files_to_backup:
                filepath = self.get_file_path(filename)
                if os.path.exists(filepath):
                    backup_filename = f"{filename.replace('.json', '')}_{timestamp}.json.gz"
                    backup_path = os.path.join(backup_dir, backup_filename)

                    with open(filepath, 'rb') as f_in:
                        with gzip.open(backup_path, 'wb') as f_out:
                            shutil.copyfileobj(f_in, f_out)
                    backup_count += 1

            # Update metadata
            metadata = self.load_data('metadata.json')
            metadata['last_backup'] = timestamp
            metadata['backup_count'] = metadata.get('backup_count', 0) + 1
            self.save_data('metadata.json', metadata)

            return True, f"Backed up {backup_count} files"
        except Exception as e:
            return False, f"Backup failed: {e}"

    def restore_backup(self, timestamp):
        """Restore data from a specific backup"""
        try:
            backup_dir = os.path.join(self.data_dir, 'backups')
            files_to_restore = ['voters', 'candidates', 'votes', 'metadata']

            restored_count = 0
            for filename in files_to_restore:
                backup_filename = f"{filename}_{timestamp}.json.gz"
                backup_path = os.path.join(backup_dir, backup_filename)

                if os.path.exists(backup_path):
                    restore_path = self.get_file_path(f"{filename}.json")

                    with gzip.open(backup_path, 'rb') as f_in:
                        with open(restore_path, 'wb') as f_out:
                            shutil.copyfileobj(f_in, f_out)
                    restored_count += 1

            return True, f"Restored {restored_count} files"
        except Exception as e:
            return False, f"Restore failed: {e}"

    def list_backups(self):
        """List all available backups"""
        try:
            backup_dir = os.path.join(self.data_dir, 'backups')
            if not os.path.exists(backup_dir):
                return []

            backups = {}
            for filename in os.listdir(backup_dir):
                if filename.endswith('.json.gz'):
                    # Extract timestamp
                    parts = filename.split('_')
                    if len(parts) >= 3:
                        timestamp = f"{parts[-2]}_{parts[-1].replace('.json.gz', '')}"
                        if timestamp not in backups:
                            backups[timestamp] = []
                        backups[timestamp].append(filename)

            return sorted(backups.keys(), reverse=True)
        except Exception as e:
            print(f"Error listing backups: {e}")
            return []

    def get_file_stats(self):
        """Get statistics about data files"""
        stats = {}
        files = ['voters.json', 'candidates.json', 'votes.json', 'metadata.json']

        for filename in files:
            filepath = self.get_file_path(filename)
            if os.path.exists(filepath):
                size = os.path.getsize(filepath)
                modified = datetime.fromtimestamp(os.path.getmtime(filepath))

                # Count records
                data = self.load_data(filename)
                record_count = len(data) if isinstance(data, dict) else 0

                stats[filename] = {
                    'size': size,
                    'size_kb': round(size / 1024, 2),
                    'modified': modified.strftime('%Y-%m-%d %H:%M:%S'),
                    'record_count': record_count
                }
            else:
                stats[filename] = {
                    'size': 0,
                    'size_kb': 0,
                    'modified': 'N/A',
                    'record_count': 0
                }

        return stats

    def export_to_csv(self, data, filename):
        """Export data to CSV format"""
        try:
            import csv
            filepath = self.get_file_path(filename)

            if not data:
                return False, "No data to export"

            # Get keys from first record
            keys = list(list(data.values())[0].keys())

            with open(filepath, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=keys)
                writer.writeheader()
                for record in data.values():
                    writer.writerow(record)

            return True, f"Exported to {filename}"
        except Exception as e:
            return False, f"Export failed: {e}"

    def initialize_default_files(self):
        """Initialize default JSON files if they don't exist"""
        default_files = {
            'voters.json': {},
            'candidates.json': {},
            'votes.json': {},
            'metadata.json': {
                'system_version': '4.0.0',
                'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'last_backup': None,
                'backup_count': 0
            }
        }

        for filename, default_data in default_files.items():
            filepath = self.get_file_path(filename)
            if not os.path.exists(filepath):
                self.save_data(filename, default_data)
