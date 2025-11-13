import pymysql
from prettytable import PrettyTable


try:
    db=pymysql.connect(host="localhost",user="root",database='arnav',password='Arnav@2007$')
    print("Database connection successful")
except:
    print("Database connection unsuccessful")

cur=db.cursor()
query="create table if not exists CONFIDENTIAL (CRIMINAL_ID INT PRIMARY KEY, NAME varchar(30), AGE INT, CRIME varchar(30), SENTENCE varchar(30), STATUS varchar(30));"
cur.execute(query)
db.commit()


# Function to add a new criminal record
def add_record():
    try:
        cur.execute("Select criminal_id from confidential;")
        c=cur.fetchall()
        if len(c)==0:
            pass
        t=()
        sno = int(input("Enter Criminal ID: "))
        t=t+(sno,)
        if t in c:
            print("Sorry, cannot have same criminal id for two criminals \n")
            return 

        name = input("Enter Name: ")
        name2=name.replace(" ","")
        if name2.isalpha()==False or len(name2)==0:
            print("Enter a name please \n")
            return

        age = int(input("Enter Age: "))
        if age>100 or age<10:
            print("Please enter a valid age \n")
            return

        crime = input("Enter Crime: ")
        sentence = input("Enter Sentence: ")

        status = input("Enter Case Status (open/closed): ")  # Input for case status
        if status.lower()=="open" or status.lower()=="closed":
            pass
        else:
            print("Please enter status as either open of closed \n")
            return

        query1="insert into confidential values({},'{}',{},'{}','{}','{}');".format(sno,name.upper(),age,crime.upper(),sentence.upper(),status.upper())
        cur.execute(query1)
        db.commit()
        print("Record added \n")

    except Exception as e:
        print("Error:",e,"\n") 

# Function to display all records
def display_records():
    try:
        cur.execute("select count(*) from confidential order by criminal_id;")
        x=cur.fetchone()[0]
        table=PrettyTable(["Criminal ID", "Name", "Age", "Crime", "Sentence", "Case Status"])
        if x==0:
            print("No records in the database")
            print("Start adding \n")
            return
        if x>0:
            for i in range(1,x+1):
                query2="select * from confidential where criminal_id = {};".format(i)
                cur.execute(query2)
                x=cur.fetchone()
                table.add_row([x[0], x[1], x[2], x[3], x[4], x[5]])
        print(table)
        print("\n")
        db.commit()
    except Exception as e:
        print("Error:",e,"\n")

# Function to display all closed records
def closed_records():
    try:
        cur.execute("select count(*) from confidential;")
        p=cur.fetchone()[0]
        table=PrettyTable(["Criminal ID", "Name", "Age", "Crime", "Sentence", "Case Status"])
        if p==0:
            print("There are no records in the database")
            print("Add some records for this function to work")
        cur.execute("select criminal_id from confidential where status='closed';")
        y=cur.fetchone()[0]
        if p>0:
            if y==0:
                print("None of the cases are closed")
            if y>0:
                print("--- Closed Criminal Records ---")
                query3="select * from confidential where status='closed';"
                cur.execute(query3)
                x=cur.fetchall()
                for i in x:
                    table.add_row([i[0], i[1], i[2], i[3], i[4], i[5]])
        db.commit()
        print(table)
        print("\n")
    except Exception as e:
        print("Error:",e,"\n")

#Function to close a case with the given criminal id
def caseclosed(n):
    try:
        query4="select * from confidential;"
        cur.execute(query4)
        x=cur.fetchall()
        cur.execute("select * from confidential where status='CLOSED';")
        y=cur.fetchall()
        for i in x:

            if i[0]==n and i[5].lower()=='open':
                query_="update confidential set status='CLOSED' where criminal_id = {};".format(n)
                cur.execute(query_)
                print("Record",n, "updated")
            
            elif i[0]==n and i[5].lower()=='closed':
                print("Record",n,"is already closed")
        cur.execute("Select criminal_id from confidential;")
        t=()
        t+=(n,)
        z=cur.fetchall()
        if t not in z:
            print("Record",n, "does not exist")
        db.commit()
        print("\n")
    except Exception as e:
        print("Error:",e,"\n")

#Function to use criminal id to search for a particular record
def search_record(ids):
    try:
        cur.execute("select criminal_id from confidential;")
        x=cur.fetchall()
        table=PrettyTable(["Criminal ID", "Name", "Age", "Crime", "Sentence", "Case Status"])
        flag=0
        for i in x:
            if ids in i:
                flag=1
                cur.execute("select * from confidential where criminal_id={};".format(ids))
                t=cur.fetchone()
                table.add_row([t[0], t[1], t[2], t[3], t[4], t[5]])

        if flag==1:
            print(table)

        else:
            print("Record",ids,"does not exist in the database")
        db.commit()
        print("\n")
    except Exception as e:
        print("Error:",e,"\n")

#Function to delete a record from the database
def delete_record(crim):
    try:
        cur.execute("select criminal_id from confidential;")
        x=cur.fetchall()
        flag=0
        for i in x:
            if crim in i:
                flag=1
                cur.execute("delete from confidential where criminal_id={};".format(crim))
    
        if flag==1:
            print("Record",crim,"was successfully deleted")
        else:
            print("Sorry, record",crim,"could not be found")
        db.commit()
        print("\n")
    except Exception as e:
        print("Error:",e,"\n")

#Function to update the sentence of a criminal
def update_record(sent):
    try:
        cur.execute("select criminal_id from confidential;")
        x=cur.fetchall()
        flag=0
        g=()
        g+=(sent,)

        if g not in x:
            print("Record searched for does not exist \n")
            return
        if g in x:
            flag=1
            newdate=input("Enter the updated sentence of the criminal: ")
            x=newdate.upper()
            cur.execute("update confidential set sentence='{}' where criminal_id={};".format(x,sent))
        if flag==1:
            print("Record",sent,"successfully updated")
        db.commit()
        print("\n")
    except Exception as e:
        print("Error:",e,"\n")


#MAIN MENU
print("WELCOME TO ST. MARKS CRIMINAL LOG DEPARTMENT")

while True:
    try:
        print("Menu:")
        print("Please choose one of the above options")
        print("1. Add New Record")
        print("2. Display All Records")
        print("3. Display Closed Records")
        print("4. Close Certain Records")
        print("5. Search Record")
        print("6. Delete Record")
        print("7. Update Record")
        print("8. Exit")
        print("\n")
        choice = int(input("Enter your choice: ",))
        print("\n")

        if choice==1:
            add_record()

        if choice==2:
            display_records()

        if choice==3:
            closed_records()

        if choice==4:
            cur.execute("select count(*) from confidential;")
            v=cur.fetchone()[0]
            if v==0:
                print("No records in database for closing \n")
            if v>0:
                l=eval(input("Enter the records you want to close in the form of a list: "))
                if len(l)==0:
                    print("List cannot be empty \n")
                else:
                    for i in l:
                        if l.count(i)>1:
                            for z in range(l.count(i)-1):
                                l.remove(i)
                    l.sort()
                    for j in range(len(l)):
                        caseclosed(l[j])

        if choice==5:
            cur.execute("select count(*) from confidential;")
            v=cur.fetchone()[0]
            if v==0:
                print("No records in database for searching \n")
            if v>0:
                ids=eval(input("Enter list of criminal ids of record to be searched: "))
                for i in ids:
                    if str(i).isdigit()==False:
                        print("Cannot process with",i)
                        ids.remove(i)
                if len(ids)==0:
                    print("Cannot enter enter empty list \n")
                else:
                    for i in ids:
                        if ids.count(i)>1:
                            for z in range(ids.count(i)-1):
                                ids.remove(i)
                    ids.sort()
                    for j in range(len(ids)):
                        search_record(ids[j])

        if choice==6:
            cur.execute("select count(*) from confidential;")
            v=cur.fetchone()[0]
            if v==0:
                print("No records in database for deletion \n")
            if v>0:
                crim=eval(input("Enter list of criminal ids of record to be deleted: "))
                for i in crim:
                    if str(i).isdigit()==False:
                        print("Cannot process with",i)
                        crim.remove(i)
                if len(crim)==0:
                    print("Cannot enter empty list \n")
                else:
                    for i in crim:
                        if crim.count(i)>1:
                            for z in range(crim.count(i)-1):
                                crim.remove(i)
                    crim.sort()
                    for j in range(len(crim)):
                        delete_record(crim[j])

        if choice==7:
            j=0
            lv=lq=[]                                                 #LIST TO KEEP TRACK OF RECORDS THAT WERE UPDATED
            cur.execute("select count(*) from confidential;")
            v=cur.fetchone()[0]
            if v==0:
                print("No records in database for updation \n")
            if v>0:
                q=int(input("How many records do you want to update: "))
        
                if q>v:
                    print("Number entered is more than number of records in database")
                    print("Updating for all records")
                    while j<v:
                        k=int(input("Enter ID of criminal whose record has been updated: "))
                        cur.execute("select criminal_id from confidential;")
                        c=cur.fetchall()
                        cj=()
                        cj=cj+(k,)
                        if cj in c:
                            lv.append(k)
                            if lv.count(k)==1:
                                update_record(k)
                                j+=1

                            elif lv.count(k)>1:
                                print("You have already updated this record")
                                lv.remove(k)                             #REMOVING DOUBLE ELEMENTS TO ENSURE SINGULARITY                
                        
                        if cj not in c:
                            print("This id is not in database \n")

                else:
                    while j<q:
                        k=int(input("Enter ID of criminal whose record has been updated: "))
                        lq.append(k)
                        if lq.count(k)==1:
                            update_record(k)
                            j+=1

                        elif lq.count(k)>1:
                            print("You have already updated this record")
                            lq.remove(k) 

        if choice==8:
            print("Thank you for visiting")
            break

        if choice not in (1,2,3,4,5,6,7,8):
            print("Please select a valid choice \n")

    except Exception as e:
        print("Error:",e,"\n")
db.commit()
cur.close()