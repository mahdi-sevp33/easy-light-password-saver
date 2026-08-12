
import random
import string
import mysql.connector
from mysql.connector import Error
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError


print("welcome to our app");
print("whats your name");

Name=input("name: ")

print("length of pass is between carector(6|20)");
print("you want a special pass 1 or a random 2")

# ///////////////////////////////////////////////////////////////

stateis=int(input("if you want a customize path enter 1 else enter 2:  "))
path_length=int(input("please enter number of your charecktor between 6 & 20"))

# ////////////////////////////////////////////////////////////////////////////////////////////


Email="null@gmail.com"

PasWord="02938rufjcndhbcwnjkm98"






if(stateis==1):


    def status1():


        a=int(input("amount number: "));
        b=int(input("amount letter: "));
        c=int(input("amount charackter: "));

        sumall=a+b+c;
        password=[]

        if sumall>path_length:
            print("the sum of charector of your password is wrong!!")
        

        if sumall<6 or sumall>20:
            print("your path length must be beetwen 6 & 20: ")
        else:
            password=[]
            for _ in range(a):
                password.append(random.choice(string.digits));
            
            for _ in range(b):
                password.append(random.choice(string.ascii_letters));

            for _ in range(c):
                password.append(random.choice(string.punctuation));

            random.shuffle(password)

            password="".join(password)

            PasWord=password

        

            print("your password is",password)

            return
         

        

    


   
# //////////////////////////////////////////////////////////////////////////////


if(stateis==2):

    def status2():
    
        charachters=string.ascii_letters + string.digits + string.punctuation;

        password="".join(random.choice(charachters) for _ in range(path_length));

        print("your password is",password);

        return
    

#-----------------------------------------------------------------------------------------

class secure_db_connect:

    def __init__(self):

        self.db_config = {
            'host': 'localhost',
            'user': 'root',
            'password': '1234',
            'database': 'security_vault'
        }
        
        

        self.ph=PasswordHasher()

    def loginuser(self):
        print("please enter db pass  ")
        passuser=input("in this plase enter pass: ")

        try:
            conn=mysql.connector.connect(self.db_config)
            cursor=conn.cursor(dictionary="true")

            cursor.exec("SELECT password_hash FROM system_access WHERE id =1")
            row=cursor.fetchone()

            if not row:
                print("you dont enter password try again")
                return None
            

            self.ph.verify(row["pass"],passuser)

            print("connected to db!")
            return conn

        except mysql.connector.Error as e:
                print(f"connection Error: {e}")

        except mysql.connector.Error as e:
            print(f"❌ Connection Error: {e}")
            return None
        finally:
            if 'cursor' in locals(): cursor.close()

    
    

    def writeInformation(self):

        conn=mysql.connector.connect(self.db_config)
        cursor=conn.fetchon(documentation=True)

        cursor.execute("INSERT INTO users VALUES Name,Email,PassWord (name,email,password)")

        print("your data succesfuly recorded")

        return





if "__name__"=="__main__":


       #درپایتون هرفایل دارای نام است واگرفایل مستقما اجراشود نامش مین خواهدبودامااگرفایل پایتون درفایل دیگری ایمپورت شود همنام با نام همان فایل مقصدمتغیرنامش قرارمیگیرد

    gatekeeper = secure_db_connect()  #کلاس بالایی که تعریف کردیم رامیگیرد

    db_connection=gatekeeper.loginuser()  #in the top this method was defined
    db_insert=gatekeeper.writeInformation()
    
    if db_connection and db_connection.is_connected():
        #If the password is correct, db_connection becomes a live connection object to your MySQL database.
        #If the password is wrong, db_connection becomes None.

        try:

            cursor=db_connection.cursor()
            cursor1=db_insert.cursor()

            cursor.execute("SELECT NOW();")  #یک دستورواقعی ااجرامیکندتااز صحت ارتباط بادیتابیس مطمعن شودی 
            print(f"System Time from DB: {cursor.fetchone()[0]}")

        finally:
            db_connection.close()
            print("sesion was ended")










