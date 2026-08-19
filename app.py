
import random
import string


from services.auth import auth

def entry_check():

    bb=auth.autintication
    if(bb==True):
        return
    else:
        print("your pass is wrong")
        


print("welcome to our app");
print("whats your name");


entry_check()


Name=input("name: ")

print("length of pass is between carector(6|20)");
print("you want a special pass 1 or a random 2")

# ///////////////////////////////////////////////////////////////

stateis=int(input("if you want a customize path enter 1 else enter 2:  "))
path_length=int(input("please enter number of your charecktor between 6 & 20"))

# ////////////////////////////////////////////////////////////////////////////////////////////


Email="null@gmail.com"



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

            

        print("your password is",password)

        return password
         


def status2():
    
    charachters=string.ascii_letters + string.digits + string.punctuation;

    password="".join(random.choice(charachters) for _ in range(path_length));

    print("your password is",password);

    return  password
    




if(stateis==1):
    Pasw=status1()
if(stateis==2):
    Pasw=status2()



#-----------------------------------------------------------------------------------------





