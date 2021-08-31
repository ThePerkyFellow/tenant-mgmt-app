import mysql.connector
import pyfiglet

def add_tenant(name,phone_no,email,bed_room,rent,floor):
    try:
        mycon = mysql.connector.connect(host='localhost', user='root', passwd='toor',database='rental_system')
        if mycon.is_connected():
            cursor=mycon.cursor()
            cursor.execute('insert into tenant_info values ("{}",{},"{}",{},{},{});'.format(name,phone_no,email,bed_room,floor,rent))
            cursor.execute('SELECT * FROM room;')
            room_data=cursor.fetchall()
            for k in room_data:
                if bed_room==k[0] and floor==k[1]:
                    cursor.execute('UPDATE room SET availability={} WHERE room_type={} and floor={};'.format(k[2]-1,bed_room,floor))
            mycon.commit()
            return ('Added!')
        else:
            print('Program Ran into Error! Try Again!')
    except:
        print('Something went wrong! Try Again Later ')
        exit()


def check_available(bed_room):
    try:
        mycon = mysql.connector.connect(host='localhost', user='root', passwd='toor',database='rental_system')
        cursor = mycon.cursor()
        floor_lst=[]
        if mycon.is_connected():
            cursor.execute('select * from room;')
            data=cursor.fetchall()
            for k in data:
                if k[0]==bed_room:
                    if 0 < k[2] <= 5:
                        floor_lst.append(k[1])
        else:
            print('Program Ran into Error! Try Again!')
        mycon.close()
        return floor_lst
            
    except:
        print('Something Went Wrong! Try Later!')
        exit()

def check_if_tenant(name):
    try:
        mycon = mysql.connector.connect(host='localhost', user='root', passwd='toor', database='rental_system')
        cursor = mycon.cursor()
        if mycon.is_connected():
            cursor.execute('select * from tenant_info;')
            data=cursor.fetchall()
            for k in data:
                if k[0]==name:
                    return True
            else:
                return False
        mycon.close()
    except:
        print('Something Went Wrong! Try Later!')
        exit()


def retrieve_info(name):
    try:
        mycon = mysql.connector.connect(host='localhost', user='root', passwd='toor', database='rental_system')
        cursor = mycon.cursor()
        if mycon.is_connected():
            cursor.execute('select * from tenant_info;')
            data = cursor.fetchall()
            for k in data:
                if k[0]==name:
                    return k
        mycon.close()
    except:
        print('Something Went Wrong! Try Later!')
        exit()
    
    
def modify_tenant(name,bed_room,floor_num,payment):
    try:
        mycon = mysql.connector.connect(host='localhost', user='root', passwd='toor', database='rental_system')
        cursor = mycon.cursor()
        if mycon.is_connected():
            cursor.execute('select * from tenant_info;')
            data = cursor.fetchall()
            for k in data:
                if k[0] == name:
                    query=('UPDATE tenant_info SET room = {}  WHERE name = "{}";'.format(bed_room,name))
                    query1=('UPDATE tenant_info SET rent = {}  WHERE name = "{}";'.format(payment,name))
                    query2=('UPDATE tenant_info SET floor = {}  WHERE name = "{}";'.format(floor_num,name))
                    cursor.execute(query)
                    cursor.execute(query1)
                    cursor.execute(query2)
                    mycon.commit()
                    print('UPDATED!')
                    break
            else:
                print('Invalid Tenant!')
    except:
        print('Something Went Wrong! Try Later!')
        exit()

def add_new_no(name,new_no):
    try:
        mycon = mysql.connector.connect(host='localhost', user='root', passwd='toor', database='rental_system')
        cursor = mycon.cursor()
        if mycon.is_connected():
            cursor.execute('select * from tenant_info;')
            data = cursor.fetchall()
            for k in data:
                if k[0] == name:
                    cursor.execute('UPDATE tenant_info SET phone = {} WHERE name = "{}";'.format(new_no, name))
                    mycon.commit()
                    print('UPDATED!')
                    break
            else:
                print('Invalid Tenant!')
    except:
        print('Something Went Wrong! Try Later!')
        exit()

def add_new_email(name,email):
    try:
        mycon = mysql.connector.connect(host='localhost', user='root', passwd='toor', database='rental_system')
        cursor = mycon.cursor()
        if mycon.is_connected():
            cursor.execute('select * from tenant_info;')
            data = cursor.fetchall()
            for k in data:
                if k[0] == name:
                    cursor.execute('UPDATE tenant_info SET email = "{}" WHERE name = "{}";'.format(email, name))
                    mycon.commit()
                    print('UPDATED!')
                    '''cursor.execute('select * from tenant_info;')
                    print(cursor.fetchall())'''
                    break
            else:
                print('Invalid Tenant!') 
    except:
        print('Something Went Wrong! Try Later!')
        exit()

def delete_tenant(name):
    
        mycon = mysql.connector.connect(host='localhost', user='root', passwd='toor', database='rental_system')
        cursor = mycon.cursor()
        if mycon.is_connected():
            cursor.execute('select * from tenant_info;')
            data = cursor.fetchall()
            for k in data:
                if k[0] == name:
                    bedroom = k[3]
                    floor = k[4]
                    cursor.execute('DELETE FROM tenant_info WHERE name="{}";'.format(name))
                    mycon.commit()
                    cursor.execute('SELECT * FROM room;')
                    room_data = cursor.fetchall()
                    for k in room_data:
                        if bedroom == k[0] and floor == k[1]:
                            cursor.execute('UPDATE room SET availability=availability+1 WHERE room_type={} and floor={};'.format(bedroom,floor))
                            mycon.commit()
                            break
                    break
                
            else:
                print('Invalid Tenant!')
        



def new_tenant():
    try:
        name = input('Enter Your Full Name: ')
        phone_no = int(input('Enter Your Phone no (without +91): '))
        email = input('Enter Your Valid Email Address: ')
        bed_room = int(input('Enter Your Room Choice (1,2 or 3 Available):'))

        if bed_room==1:
            rent=12000
        elif bed_room==2:
            rent=18000
        elif bed_room==3:
            rent=25000
        else:
            print('Invalid No of rooms entered')
            new_tenant()

        floors = check_available(bed_room)
        print(bed_room,'BHK Available on Floors:')
        for i in floors:
            print(i)
        option = int(input('Enter Your Floor of Choice: '))
        if option in floors :
            add_tenant(name,phone_no,email,bed_room,rent,option)
            print(f' Your rent : {rent} \n Contact Head Office for Payment ')
        else:
            print('Floor Not Available')
    except:
        print('Something Went wrong, Please try again')
        exit()

def exist_tenant():
    global option
    name = input('Enter Your Full Name: ')
    if check_if_tenant(name):
        info = retrieve_info(name)
        # print his info

        option = int(input(' 1) Change Room \n 2) Change Information \n 3) Leave House \n 4) Quit \n Enter Your Option : '))
        if option == 1:
            old_room = info[3]
            if old_room==1:
                old_rent=12000
            elif old_room==2:
                old_rent=18000
            elif old_room==3:
                old_rent=25000
            print(f'Current room : {old_room}')
            change = int(input('Enter Room No to Change to:'))
            if change==1:
                rent=12000
            elif change==2:
                rent=18000
            elif change==3:
                rent=25000
            else:
                print('Invalid No of rooms entered')
            floors = check_available(change)
            for floor in floors:
                print(f'Available floor {floor}')
            option = int(input('Enter Your Floor of Choice: '))
            if option in floors:
                modify_tenant(name,change,option,rent) 
                new_rent = rent - old_rent
                if new_rent>0:               
                    print(f' Increase In Rent = {new_rent} \n Contact Head Office for Further Information ')
                else:
                    new_rent *=-1
                    print(f' Decrease In Rent = {new_rent} \n Contact Head Office for Further Information ')


            else:
                print('Floor Not Available')

        elif option == 2:
            option2 = int(input('Choose What You Want to Change? \n 1) Phone Number \n 2) Email Address \n Enter Your Option : '))
            if option2 == 1:
                new_no = int(input('Enter New Mobile No : '))
                add_new_no(name,new_no)
            elif option2 == 2:
                new_email = input('Enter Your New Email : ')
                add_new_email(name,new_email)
            else:
                print('Invalid Option')
        
        elif option == 3:
            with open('reason.txt','a') as file:
                reasons = input('Enter the Reason You are leaving ')
                reason = name + ' Reason For Leaving : \n' + reasons + '\n\n'
                file.write(reason)
                 
            delete_tenant(name)
            print('Okay You No Longer Own the House! Kindly vacate  ')

        elif option == 4:
            print('Thank You for Logging In Tenant! Have a good day')
            exit()
        else:
            print('Wrong option selected ! Try Later')
            exit()
    else:
        print('You are not a tenant yet! Please rent a house to become a tenant here')
        do = input('Do you want to become a tenant here (Y/N) : ')
        if do == 'Y' or do == 'y':
            new_tenant()
        elif do == 'N' or do == 'n':
            print('Thank you, Have a Good day')
            exit()
        else:
            print('Wrong option !')
            exit()

# main
thestuff = pyfiglet.figlet_format("Tenant Management System")
print(thestuff)
main_menu = int(input('Choose option \n 1) New tenant \n 2) Existing tenant \n 3) Quit \n Enter Option : '))
if main_menu == 1:
    new_tenant()
elif main_menu == 2:
    exist_tenant()
elif main_menu == 3:
    print('Thank you, Have a good day')
    exit()
else:
    print('Wrong option given !,please try later')
    exit()


