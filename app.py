
import random
import string
import sys 

from services.auth import Auth

from services.vault import Vault


user=Auth()  #from file auth.py
v=Vault()    #from file vault.py




print("____Welcome to our app____")
print("1: Change entry password")
print("2: Enter app with current pass")

choice = input("Please select an option (1 or 2): ")

if choice == "1":
    if user.register_user():
        print("Password was successfully changed.")
    else:
        print("Password changing failed.")

elif choice == "2":
    usernameen1=input("please enter your username: ")
    passwordenv1=input("please enter your password entry: ")

    if user.login_user(usernameen1,passwordenv1):
        print("App opened successfully.")
    else:
        print("Access denied: Password is wrong.")
        sys.exit()

else:
    # This handles invalid inputs (anything other than 1 or 2)
    print("Invalid option selected. Please restart and choose 1 or 2.")



print("whats your name");

userName=input("name: ")

print("what is your email for this pass")

Email=input("email: ")


print("length of pass is between carector(6|20)");
print("you want a special pass 1 or a random 2")

# ///////////////////////////////////////////////////////////////

stateis=int(input("if you want a customize path enter 1 else enter 2:  "))

#____for cheking our input is true 

def checkstate(stateis):

    if stateis!=2 and stateis!=1:
        print("you might enter a number betwen 1 and 2")
        return False
    return True


while True:   #تاوقتی که کاربرعدددرست روواردنکرده این چرخه ادامه پیداکند 
    stateis=int(input("if you want a customize path enter 1 else enter 2:  "))
    if checkstate(stateis):
        break

    print("password saved truly")    
    
    


path_length=int(input("please enter number of your charecktor between 6 & 20"))

# ////////////////////////////////////////////////////////////////////////////////////////////





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
        sys.exit(1)
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

            

        print("your password is",password)
        

        return password
         


def status2():
    charachters=string.ascii_letters + string.digits + string.punctuation;

    password="".join(random.choice(charachters) for _ in range(path_length));

    if password:
    
        print("your password is",password);
        
    
    return  password
    



if(stateis==1):
    Pasw=status1()


    print(f'please add a note for your password with this name and email ${userName,Email}')
    notes=input("note: ")
    v.add_entry(userName,Email,Pasw,notes)    
    
   
if(stateis==2):
    Pasw=status2()

    print(f'please add a note for your password with this name and email ${userName,Email}')
    notes=input("note: ")
    v.add_entry(userName,Email,Pasw,notes)



#-----------------------------------------------------------------------------------------





