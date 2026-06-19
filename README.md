# 🔐 Password Manager

A secure password management app built with Python and Tkinter. It comes with a password generator, strength checker, and an encrypted vault to store all your credentials locally.

## 📦 Technologies Used

- `Python 3`
- `Tkinter`
- `Cryptography (Fernet)`
- `Pyperclip`
- `PyInstaller`

## 🦄 Features

Here's what you can do with Password Manager:

- **Generate Passwords**: Customize length from 8 to 64 characters and toggle uppercase, lowercase, numbers, and symbols. Copy the result with one click.

- **Check Password Strength**: Type or paste a password to get a real-time score out of 100. The checker analyzes entropy, character diversity, common patterns, and detects weak passwords.

- **Store Passwords Securely**: Save your credentials in an encrypted vault protected by a master password. All data is encrypted locally with AES-128-CBC.

- **Organize with Labels**: Add optional labels like "Personal" or "Work" to keep multiple accounts for the same site organized. Entries are automatically sorted by site and label.

- **Search & Manage**: Search through your vault by site, username, or label. Edit or delete entries as needed.

- **Auto-Lock**: The vault locks automatically after 5 minutes of inactivity or when you switch to another tab. You'll need to re-enter your master password to access it again.

- **Copy Quickly**: Copy passwords or usernames individually with dedicated buttons.

## 📚 What I Learned

### 🔐 Cryptography and Security

- **Key Derivation**: I learned how PBKDF2 works to derive encryption keys from passwords, making brute-force attacks harder.
- **Fernet Encryption**: Understanding symmetric encryption with Fernet and how it handles AES-128-CBC under the hood.
- **Password Hashing**: Salting and hashing passwords properly before storing them, and why that matters.

### 🧩 Tkinter GUI Development

- **Theming**: Customizing ttk styles to create a dark theme without external libraries.
- **Layout Management**: Using grid and pack together effectively for clean dialog layouts.
- **Event Handling**: Binding mouse, keyboard, and notebook tab-change events for auto-lock behavior.

### ⚙️ Password Strength Analysis

- **Entropy Calculation**: Computing password entropy based on character set size and length.
- **Pattern Detection**: Using regex to find sequential characters, repeated characters, and common passwords.

### 📦 Packaging with PyInstaller

- **Onefile vs Onedir**: The tradeoffs between a single executable and a folder-based build for startup speed.

## 🚦 Running the Project

To run the project in your local environment, follow these steps:

1. Clone the repository to your local machine.
2. Run `pip install -r requirements.txt` in the project directory to install the required dependencies.
3. Run `python main.py` to start the application.
4. The app window will open. Create a master password on first launch to set up your vault.

## 🏗️ Building the Executable

To build a standalone `.exe` file:

```bash
pyinstaller --onefile --windowed --name "PasswordManager" main.py
```

The executable will be available in the `dist` folder.
