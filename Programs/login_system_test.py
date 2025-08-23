import bcrypt
import time
import getpass

# Simulated user "database"
# bcrypt auto-generates salts when hashing
user_db = {
    "alice": bcrypt.hashpw("password123".encode(), bcrypt.gensalt()),
    "bob": bcrypt.hashpw("secure456".encode(), bcrypt.gensalt())
}

# Track login attempts and lockout time
login_attempts = {}
MAX_ATTEMPTS = 3
LOCKOUT_DURATION = 30  # seconds

def is_locked_out(username):
    entry = login_attempts.get(username)
    if not entry:
        return False

    attempts, last_attempt = entry
    if attempts >= MAX_ATTEMPTS:
        elapsed = time.time() - last_attempt
        if elapsed < LOCKOUT_DURATION:
            remaining = int(LOCKOUT_DURATION - elapsed)
            print(f"Too many failed attempts. Try again in {remaining} seconds.")
            return True
        else:
            # Reset on timeout
            login_attempts[username] = [0, time.time()]
            return False
    return False

def record_failed_attempt(username):
    if username not in login_attempts:
        login_attempts[username] = [1, time.time()]
    else:
        login_attempts[username][0] += 1
        login_attempts[username][1] = time.time()

def login():
    print("=== Secure Login System ===")
    username = input("Username: ").strip()

    if username not in user_db:
        print("Invalid username or password.")
        return

    if is_locked_out(username):
        return

    password = getpass.getpass("Password: ").encode()

    if bcrypt.checkpw(password, user_db[username]):
        print(f"Hello, {username}!")
        if username in login_attempts:
            del login_attempts[username]  # Reset on success
    else:
        print("Invalid username or password.")
        record_failed_attempt(username)

if __name__ == "__main__":
    login()
