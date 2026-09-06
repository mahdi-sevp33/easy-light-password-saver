import os
import stat

from cryptography.fernet import Fernet

from database.connection import secure_db_connect


class Vault:
    def __init__(self, key_path=None):
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        self.key_path = key_path or os.path.join(project_root, '.vault_key')
        self.key = self._load_or_create_key()
        self.fernet = Fernet(self.key)
        self.db = secure_db_connect()

    def _load_or_create_key(self):
        if os.path.exists(self.key_path):
            with open(self.key_path, 'rb') as f:
                return f.read()

        key = Fernet.generate_key()
        with open(self.key_path, 'wb') as f:
            f.write(key)

        # restrict permissions to owner
        try:
            os.chmod(self.key_path, stat.S_IRUSR | stat.S_IWUSR)
        except Exception:
            pass

        return key

    def ensure_table(self):
        conn = self.db.connect()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS vault_entries (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    site VARCHAR(255) NOT NULL,
                    login VARCHAR(255),
                    password VARBINARY(1024) NOT NULL,
                    notes TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            conn.commit()
        finally:
            try:
                cursor.close()
            except Exception:
                pass
            conn.close()

    def add_entry(self, site, login, password_plain, notes=None):
        token = self.fernet.encrypt(password_plain.encode())
        conn = self.db.connect()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO vault_entries (site, login, password, notes) VALUES (%s, %s, %s, %s)",
                (site, login, token, notes),
            )
            conn.commit()
            return cursor.lastrowid
        finally:
            try:
                cursor.close()
            except Exception:
                pass
            conn.close()

    def list_entries(self):
        conn = self.db.connect()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT id, site, login, created_at FROM vault_entries ORDER BY created_at DESC")
            return cursor.fetchall()
        finally:
            try:
                cursor.close()
            except Exception:
                pass
            conn.close()

    def get_entry(self, entry_id):
        conn = self.db.connect()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT id, site, login, password, notes, created_at FROM vault_entries WHERE id = %s", (entry_id,))
            row = cursor.fetchone()
            if not row:
                return None

            # row: (id, site, login, password_blob, notes, created_at)
            password_blob = row[3]
            try:
                password_plain = self.fernet.decrypt(password_blob).decode()
            except Exception:
                password_plain = None

            return {
                "id": row[0],
                "site": row[1],
                "login": row[2],
                "password": password_plain,
                "notes": row[4],
                "created_at": row[5],
            }
        finally:
            try:
                cursor.close()
            except Exception:
                pass
            conn.close()

