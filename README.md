# Password Manager

A secure password management application built with Python and Tkinter.

## Features

- **Password Generator** - Generate secure random passwords with customizable length and character options
- **Password Strength Checker** - Real-time password strength analysis with entropy scoring
- **Password Vault** - Encrypted storage for all your passwords with master password protection

## Download

Grab the latest `PasswordManager.exe` from the [Releases page](https://github.com/velumprismic/PasswordManager/releases). No Python required, just download and run.

## Run from Source (Developers)

1. Clone the repository:
```bash
git clone https://github.com/yourusername/PasswordManager.git
cd PasswordManager
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python main.py
```

## Features

### Password Generator
- Customizable length (8-64 characters)
- Options: Uppercase, Lowercase, Numbers, Symbols
- One-click copy to clipboard
- Real-time strength display

### Password Strength Checker
- Entropy-based scoring (0-100)
- Detects common passwords, sequential characters, and patterns
- Visual strength bar with color feedback
- Detailed analysis breakdown

### Password Vault
- Master password protection
- AES encryption (Fernet) for stored passwords
- Add, edit, and delete password entries
- Optional labels for organizing accounts
- Search functionality
- Auto-lock after 5 minutes of inactivity
- Locks when switching tabs

## Security

- Master password is hashed with PBKDF2-HMAC-SHA256 (100k iterations)
- Vault is encrypted using Fernet (AES-128-CBC)
- Salt is randomly generated and stored separately
- All data stored locally (no cloud sync)

## Requirements

- Python 3.7+
- cryptography
- pyperclip

## License

MIT License
