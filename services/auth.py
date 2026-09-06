
import getpass
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from mysql.connector import cursor

from database.connection import secure_db_connect


class Auth:

    def __init__(self):
        self.db = secure_db_connect()
        self.ph = PasswordHasher()

    

    def register_user(self):       # برای ست کردن پسوردونام کاربری
        conn = self.db.connect()
        if conn is None:
            print("Database connection failed")
            return False

        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT password,name  FROM vault_entries ")
        

            if cursor.fetchone():
                print("a user already exist please use from method login user")
                return False


            username = input("Set app username: ").strip()
            password=getpass.getpass("please enter your password: ")
            if not username or not password:
                print("Username and password cannot be empty")
                return False

            password_hash = self.ph.hash(password)
            cursor.execute(
                "INSERT INTO vault_entries (name, password) VALUES (%s, %s)",
                (username, password_hash)
            )
            print("User and Pass created successfully")
            conn.commit()
            print("your username and your password registered successfully")
            return True
        finally:
            if "cursor" in locals():
                cursor.close()
            conn.close()


    def login_user(self,username,password):
    
        conn=self.db.connect()

        if not conn:
            return False
        cursor=None
        try:
            cursor=conn.cursor(dictionary=True)
            cursor.execute("SELECT password FROM vault_entries WHERE name=%s",[username])
            user_record=cursor.fetchone()
            try:
                self.ph.verify(user_record["password"],password)
                return True
            except VerifyMismatchError:
                return False
        finally:
            if "cursor" in locals():
                cursor.close()
            conn.close()


    def changePass(self):
        print("if you want to change your pass at first enter your current pass")
        currpass = getpass.getpass("your pass: ")

        conn1 = self.db.connect()
        if conn1 is None:
            print("database connection failed")
            return False

        cursor=None

        try:
            cursor1=conn1.cursor(dictionary=True)

            cursor1.execute("SELECT password FROM system_access")

            row1 = cursor1.fetchone()

            if not row1:
                print("No user found")
                return False

            try:
                self.ph.verify(row1["password"],currpass)
            except:
                return False

            new_password=getpass.getpass("enter your new pass: ")
            confirm_pass=getpass.getpass("enter again you pass for confirm: ")

            if not new_password:
                print("your new password is empty")
                return False

            if new_password!=confirm_pass:
                print("password do not match")
                return False

            new_hashed_password=self.ph.hash(new_password)

            cursor1.execute("UPDATE vault_entries SET password=%s",new_hashed_password)

            conn1.commit()
            print("password was succesfuly updated")
            return True

        finally:
            if cursor1:
                cursor1.close()

            conn1.close()


        #after password was correct

            try:
                self.ph.verify(row1["password_hash"], currpass)
                return self.savingpass()

            except VerifyMismatchError:
                print("your password is wrong try again")
                return False

    def savingpass(self):
        print("please enter your new pass")
        newpass = input("pass: ")

        passnew = self.ph.hash(newpass)
        conn1 = self.db.connect()
        cursor1 = conn1.cursor()

        query3 = "UPDATE vault_entries SET password = %s "
        cursor1.execute(query3, (passnew,))

        print("your pass was updated")
        conn1.commit()
        conn1.close()

        return True

            




    
