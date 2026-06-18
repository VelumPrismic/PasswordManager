import json
import os
from typing import Optional
from .encryption import EncryptionManager


class PasswordStorage:
    """Encrypted JSON file storage for passwords."""

    VAULT_FILE = 'vault.enc'
    MASTER_FILE = 'master.dat'

    def __init__(self, data_dir: str = None):
        if data_dir is None:
            data_dir = os.path.join(os.path.expanduser('~'), '.password_manager')
        self.data_dir = data_dir
        self.vault_path = os.path.join(data_dir, self.VAULT_FILE)
        self.master_path = os.path.join(data_dir, self.MASTER_FILE)
        self.encryption = EncryptionManager()
        self._entries = []

    def setup_master(self, password: str) -> bool:
        """Set up master password for first time."""
        if os.path.exists(self.master_path):
            return False

        os.makedirs(self.data_dir, exist_ok=True)
        master_hash = EncryptionManager.hash_password(password)
        salt = self.encryption.set_password(password)

        with open(self.master_path, 'w') as f:
            f.write(master_hash)

        salt_path = os.path.join(self.data_dir, 'salt.bin')
        with open(salt_path, 'wb') as f:
            f.write(salt)

        self._save_entries()
        return True

    def unlock(self, password: str) -> bool:
        """Unlock vault with master password."""
        if not os.path.exists(self.master_path):
            return False

        with open(self.master_path, 'r') as f:
            stored_hash = f.read().strip()

        if not EncryptionManager.verify_password(password, stored_hash):
            return False

        salt_path = os.path.join(self.data_dir, 'salt.bin')
        if not os.path.exists(salt_path):
            return False

        with open(salt_path, 'rb') as f:
            salt = f.read()

        self.encryption.set_password(password, salt)
        self._load_entries()
        return True

    def is_setup(self) -> bool:
        """Check if master password is set up."""
        return os.path.exists(self.master_path)

    def _save_entries(self):
        """Save entries to encrypted file."""
        data = json.dumps(self._entries, indent=2)
        encrypted = self.encryption.encrypt(data)
        with open(self.vault_path, 'wb') as f:
            f.write(encrypted)

    def _load_entries(self):
        """Load entries from encrypted file."""
        if not os.path.exists(self.vault_path):
            self._entries = []
            return

        try:
            with open(self.vault_path, 'rb') as f:
                encrypted = f.read()
            data = self.encryption.decrypt(encrypted)
            self._entries = json.loads(data)
        except Exception:
            self._entries = []

    def add_entry(self, site: str, username: str, password: str, label: str = '') -> int:
        """Add a new password entry. Returns entry ID."""
        entry = {
            'id': len(self._entries),
            'site': site,
            'username': username,
            'password': password,
            'label': label
        }
        self._entries.append(entry)
        self._save_entries()
        return entry['id']

    def update_entry(self, entry_id: int, site: str, username: str, password: str, label: str = '') -> bool:
        """Update an existing entry."""
        for entry in self._entries:
            if entry['id'] == entry_id:
                entry['site'] = site
                entry['username'] = username
                entry['password'] = password
                entry['label'] = label
                self._save_entries()
                return True
        return False

    def delete_entry(self, entry_id: int) -> bool:
        """Delete an entry by ID."""
        for i, entry in enumerate(self._entries):
            if entry['id'] == entry_id:
                self._entries.pop(i)
                self._save_entries()
                return True
        return False

    def get_all_entries(self) -> list:
        """Get all stored entries."""
        return self._entries.copy()

    def search_entries(self, query: str) -> list:
        """Search entries by site, username, or label."""
        query = query.lower()
        return [
            e for e in self._entries
            if query in e['site'].lower() or query in e['username'].lower()
            or query in e.get('label', '').lower()
        ]
