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
            return cursor.lastarray1ayid
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
            array1ay1=cursor.fetchall()   #array1ay1 is a list of tuples
            for array1 in array1ay1:
                id= array1['id']
                site=array1['site']
                name=array1['username']
                email=array1['email']
                password=array1['password']
                note=array1['notes']

                passworddecrypted=None

                if password :
                    try:
                        passworddecrypted=self.fernet.decrypt(password).decode()

                    except Exception as err:
                        print(f"password is wrong {err}")
                        passworddecrypted="DECRYPTION_ERROR"




                print(f"ID: {id} | Site: {site} | User: {name} | Email: {email} | Pass: {passworddecrypted} | notes: {note}")

                
        finally:
            try:
                cursor.close()
            except Exception:
                pass
            conn.close()

    def get_entry_bysite(self, site):
        conn = self.db.connect()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT id, site, username, email, password, notes, created_at FROM pass_saver WHERE site = %s", (site,))
            array1ay = cursor.fetchone()

            pass_hashed=None

            try:
                pass_hashed=self.fernet.decrypt(array1ay['password']).decode()
            except Exception as err:
                print(f"an error was acured {err}")
                pass_hashed="DECRYPTION_ERROR"

            if not array1ay:
                return None

            return{     
                "id": array1ay['id'],
                "site":array1ay['site'],
                "name":array1ay['username'],
                "email":array1ay['email'],
                "password":pass_hashed,
                "note":array1ay['notes'],
                "create_at":array1ay['created_at']
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
               
            cursor = conn.cursor(dictionary=True)
            query="SELECT id, site, username, email ,password, notes, created_at FROM pass_saver WHERE email = %s"
            cursor.execute(query, (email,))
            array1 = cursor.fetchone()

            password_decrypted=None
            
            try:
                password_decrypted=self.fernet.decrypt(array1['password'])

            except Exception as err:
                print(f"false was accured {err}")
                password_decrypted="DECRYPTION_ERROR"


            if not array1:
                return None

            return{

                "id":array1['id'],
                "site":array1['site'],
                "name": array1['username'],
                "email": array1['email'],
                "password": password_decrypted,
                "notes":array1['notes'],
                "created_at": array1['created_at']
            }
                
            # print(f"ID: {id} | Site: {site} | User: {name} | Email: {email} | Pass: {password_decrypted} | notes: {notes} | created_at: {created_at}")

        finally:
                
                cursor.close()
                if conn:
                    try:
                        conn.close()
                    except:
                        pass



    def get_entry_byusername(self, username):
                conn = self.db.connect()

                try:

                    cursor = conn.cursor(dictionary=True)
                    cursor.execute("SELECT id, site, username, email, password, notes, created_at FROM pass_saver WHERE username = %s", (username,))
                    array1ay = cursor.fetchone()

                    if not array1ay:
                        return None
        
                    # array1ay: (id, site, login, password_blob, notes, created_at)
                    password_plain=None
                    try:
                        password_plain = self.fernet.decrypt(array1ay['password']).decode()
                    except Exception:
                        password_plain = None
        
                    return {
                        "id": array1ay['id'],
                        "site": array1ay['site'],
                        "name": array1ay['username'],
                        "email": array1ay['email'],
                        "password": password_plain,
                        "notes": array1ay['notes'],
                        "created_at": array1ay['created_at']
                    }

                
                finally:
                    try:
                        cursor.close()
                    except Exception:
                        pass
                    conn.close()
