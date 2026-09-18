import os
import stat

from cryptography.fernet import Fernet

from database.connection import secure_db_connect


class Vault:
    def __init__(self, key_path=None):
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        self.key_path = key_path or os.path.join(project_root, '.vault_key')
        self.key = self._load_or_create_key()
        self.fernet = Fernet(self.key)   #ساخت کلیدی که پسوردراهش کندتابه صورت هش شده دردیتابیس ذخیره بشود
        self.db = secure_db_connect()  #برای اطمینان ازوجوددیتابیس واتصال به مریادی بی 
        self.table=self.ensure_table()  #یک باردرابتدای فراخوانی کلاس والت فراخوانی واطمینان حاصل میشودکه جدول برای ذخیره سازی اطلاعات کاربرساخته شده ووجوددارد

    def _load_or_create_key(self):
        if os.path.exists(self.key_path):
            with open(self.key_path, 'rb') as f:  # rb mean read and binary
                return f.read()  #اگرکلیددرمسیرش حضورداشت بخونشث۱۲‍

        else:
            key = Fernet.generate_key()
            with open(self.key_path, 'wb') as f: #wb means write and binary 
                f.write(key)  #اگرکلیدوجودنداشت توی اف بنویسش 

        # restrict permissions to owner
        try:
            os.chmod(self.key_path, stat.S_IRUSR | stat.S_IWUSR)  #this command is: chmod 600 .vault_key means root user can read and write only
        except Exception:
            pass

        return key

    def ensure_table(self):
        conn = self.db.connect()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS pass_saver (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    site VARCHAR(255) ,
                    username VARCHAR(255),
                    email VARCHAR(255),
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

    def add_entry(self, site, username,email, password_plain, notes=None):

        token = self.fernet.encrypt(password_plain.encode())
        conn = self.db.connect()

        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO pass_saver (site, username,email, password, notes) VALUES (%s, %s, %s, %s,%s )",
                (site, username,email, token, notes),
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
            cursor.execute("SELECT id, site, username, email ,password ,notes , created_at FROM pass_saver ORDER BY created_at DESC")
            array1=cursor.fetchall()
            for password in array1["password"]:
                array1["password"]=self.fernet.decrypt(array1["password"])
                
            return array1
        finally:
            try:
                cursor.close()
            except Exception:
                pass
            conn.close()

    def get_entry_bysite(self, site):
        conn = self.db.connect()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT id, site, username, password, notes, created_at FROM pass_saver WHERE site = %s", (site,))
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

    def get_entry_byemail(self,email):
            conn=self.db.connect()
            try:
               
                cursor = conn.cursor()
                query="SELECT id, site, username, email ,password, notes, created_at FROM pass_saver WHERE email = %s"
                cursor.execute(query, (email,))
                row = cursor.fetchone()
                # if not row:
                #     return None
    
                # row: (id, site, login, password_blob, notes, created_at)
                password_plain = row[4]
                try:
                    password_plain = self.fernet.decrypt(password_plain).decode()
                except Exception:
                    password_plain = None
    
                return {
                    "id": row[0],
                    "site": row[1],
                    "login": row[2],
                    "email": row[3],
                    "password": password_plain,
                    "notes": row[5],
                    "created_at": row[6]
                }
            except Exception as e:
                print(f'error ocurred {e}')
                return None
            finally:
                if cursor:
                    try:
                        cursor.close()
                    except:
                        pass
                if conn:
                    try:
                        conn.close()
                    except:
                        pass


            # conn=self.db.connect()
            # cursor=conn.cursor()
            # cursor.execute("SELECT email FROM pass_saver")
            # emails=cursor.fetchall()
            # for email in emails:
            #     print(email)



    def get_entry_byusername(self, username):
                conn = self.db.connect()
                try:
                    cursor = conn.cursor()
                    cursor.execute("SELECT id, site, username, password, notes, created_at FROM pass_saver WHERE username = %s", (username,))
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


