
import mysql.connector
from mysql.connector import Error
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError


class secure_db_connect:

    def __init__(self):

        self.db_config = {
            'host': 'localhost',
            'user': 'root',
            'password': '1234',
            'database': 'security_vault'
        }

        def connect():
            try:
                return mysql.connector.connect(self.db_config)

            except Error as error:
                print(f"you have gotten error ${error}")
                return None

        

                

        

    #     self.ph=PasswordHasher()

    # def loginuser(self):
    #     print("please enter db pass  ")
    #     passuser=input("in this plase enter pass: ")

    #     try:
    #         conn=mysql.connector.connect(self.db_config)
    #         cursor=conn.cursor(dictionary="true")

    #         cursor.exec("SELECT password_hash FROM system_access WHERE id =1")
    #         row=cursor.fetchone()

    #         if not row:
    #             print("you dont enter password try again")
    #             return None
            

    #         self.ph.verify(row["pass"],passuser)

    #         print("connected to db!")
    #         return conn

    #     except mysql.connector.Error as e:
    #             print(f"connection Error: {e}")

    #     except mysql.connector.Error as e:
    #         print(f"❌ Connection Error: {e}")
    #         return None
    #     finally:
    #         if 'cursor' in locals(): cursor.close()

    #     return

    



# connection=secure_db_connect()

# connection.loginuser()


