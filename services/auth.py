

import mysql.connector
from mysql.connector import Error
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

from database.connection import secure_db_connect





class auth():

    def __init__(self):
        self.db=secure_db_connect()
        self.ph=PasswordHasher()


    def autintication(self):
        print("welcome to your app")
        print("enter your cuurrent pass if you dont change password default pass is 1234")

        password=input("Password: ")

        conn=self.db.connect()
        cursor=conn.cursor()


        query1="SELECT password_hash   FROM  system_access"

        cursor.execute(query1)

        row=cursor.fetchone()

        stored_hash=row[0]
        try:
            self.ph.verify(stored_hash,password)
            return True
        except VerifyMismatchError:
            print("your password is wrong")
            return False

        finally:
            cursor.close()
            try:
                conn.close()
            except Exception:
                pass
            
    def changePass(self):
        print("if you want to change your pass at first enter your current pass")
        currpass=input("your pass: ")

        conn1=self.db.connect()
        cursor1=conn1.cursor()

        query2="SELECT password_hash FROM system_access"

        cursor1.execute(query2)

        row1=cursor1.fetch

        storedhash=row1

        try:
            self.ph(storedhash,currpass)
            return savingpass()

        except:
            print("your password is wrong try again")
        



        def savingpass(self):
            print("please enter your new pass")
            newpass=input("pass: ")

            passnew=self.ph.hash(newpass)

            query3=f"INSERT INTO system_access (password_hash) VALUES (%s)"

            cursor1.execute(query3,(passnew))

            print("your pass was updated")
            conn1.commit()

            




    
