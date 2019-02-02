import pymysql as sql
db = sql.connect("localhost", "root", "", "qabank")

iigi g

def account_creation():
    create = input("Would you like to create a new account? y/n")
    if create == "y":
        accholder = input("Enter name of account holder:")
        gender = input("Enter gender of account holder: m/f")
        add = input("Enter current address of account holder:")
        acctype = input("Would you like to open a (current) or (savings) account:")
        if acctype == "savings":
            c = db.cursor()
            c.execute("Select COUNT(AccountNo)from Accounts where AccountNo like('S%')")
            data = c.fetchall()
            count = int(data[0][0])
            count = int(count) + 1
            if count < 10:
                num = "00" + str(count)
                if (count > 10) and (count < 100):
                    num = "0" + str(count)
                    if count > 100:
                        num = str(count)                                        #this section counts the number of records containing
            if gender.lower() == "m":                                           #either current or savings account to generate a new serial number
                accno = "SM" + num
            elif gender.lower() == "f":
                accno = "SF" + num
        if acctype == "current":
            c = db.cursor()
            c.execute("Select Count(AccountNo)from Accounts where AccountNo like('C%')")
            data = c.fetchall()
            count = int(data[0][0])
            count = int(count) + 1
            if count < 10:
                num = "00" + str(count)
                if (count > 10) and (count < 100):
                    num = "0" + str(count)
                    if count > 100:
                        num = str(count)
            if gender == "m":
                accno = "CM" + num
            elif gender == "f":
                accno = "CF" + num
        c = db.cursor()
        c.execute("Insert into accounts(AccountNo,AccountHolder,Address) values (%s,%s,%s)", (accno, accholder, add))
        db.commit()
        initial = 0
        date = "4thMay2018"
        c.execute("insert into withdraws(accountno,amount,date1) values (%s,%s,%s)", (accno, initial, date))      #used to initiate an amount "0",
        c.execute("insert into deposits(accountno,amount,date1) values (%s,%s,%s)", (accno, initial, date))       #which will be used in withdraw method if there is
        print("Your account number is:", accno)                                                                   # no existing amount
        db.commit()
        #db.close()


def deposits():
    accno = input("Enter account number")
    amount = int(input("Enter amount to deposit:"))
    date = "4thMay2018"
    c = db.cursor()
    c.execute("Insert into deposits(accountno,Amount,date1) values (%s,%s,%s)", (accno, amount, date))
    db.commit()


def withdraws():                                                        #this method allows the user to withdraw an amount
    accno = input("Enter account number:")                              #depending on whether there are sufficient funds
    amount = int(input("Enter amount to withdraw:"))
    date = "4thMay2018"
    if accno[0].lower() == "S":
        c = db.cursor()
        c.execute("select SUM(amount)from deposits where accountno = %s", accno)
        dep1 = c.fetchall()
        dep = int(dep1[0][0])
        c = db.cursor()
        c.execute("select SUM(amount)from withdraws where accountno = %s", accno)
        withdraw1 = c.fetchall()
        withdraw = int(withdraw1[0][0])
        tot_balance = dep - withdraw
        if tot_balance > amount:
            c = db.cursor()
            c.execute("insert into withdraws(accountno,amount,date1) values (%s,%s,%s)", (accno, amount, date))
            new_bal = tot_balance - amount
            print("New balance is: ", new_bal)
        else:
            print("Withdrawal amount is over limit, insufficient funds")
    if accno[0].lower() == "C":
        c = db.cursor()
        c.execute("select SUM(amount)from deposits where accountno = %c", accno)
        dep1 = c.fetchall()
        dep = int(dep1[0][0])
        c = db.cursor()
        c.execute("select SUM(amount)from withdraws where accountno = %c", accno)
        withdraw1 = c.fetchall()
        withdraw = int(withdraw1[0][0])
        tot_balance = dep - withdraw
        if tot_balance > amount:
            c = db.cursor()
            c.execute("insert into withdraws(accountno,amount,date1) values (%s,%s,%s)", (accno, amount, date))
            new_bal = tot_balance - amount
            print("New balance is: ", new_bal)
        else:
            print("Withdrawal amount is over limit, insufficient funds")


def list_accounts():                                                                                  # This section generates a report on existing records
    input1 = input("""Which accounts would you like to view?
                    (all(A)/current(C)/savings(S)/male or female account holders(M/F))""")

    if input1.lower() == "a":
        c = db.cursor()
        c.execute("select * from accounts")
        data = c.fetchall()
        print("accountno | acccountholder | address")
        for x in data:
            print(x[0],x[1],x[2])
        db.close()
    elif input1.lower() == "a":
        c = db.cursor()
        c.execute("select * from accounts where accountno like ('C%')")
        data = c.fetchall()
        print("accountno | acccountholder | address")
        for x in data:
            print(x[0], x[1], x[2])
        db.close()
    elif input1.lower() == "s":
        c = db.cursor()
        c.execute("select * from accounts where accountno like ('S%')")
        data = c.fetchall()
        print("accountno | acccountholder | address")
        for x in data:
            print(x[0], x[1], x[2])
    elif input1.lower() == "m":
        c = db.cursor()
        c.execute("select * from accounts where accountno like ('_M%')")
        data = c.fetchall()
        print("accountno | acccountholder | address")
        for x in data:
            print(x[0], x[1], x[2])
    elif input1.lower() == "f":
        c = db.cursor()
        c.execute("select * from accounts where accountno like ('_F%')")
        data = c.fetchall()
        print("accountno | acccountholder | address")
        for x in data:
            print(x[0], x[1], x[2])


def main():
    select="e"
    while select!="E" or select!="e":
        print("Welcome to QA Banking")
        print("""Navigate around with the following options
              Enter A - Create new Account
              Enter B - Deposit
              Enter C - Withdraw
              Enter E - Exit""")

        print("""Manager-menu
              Enter Z - Access accounts info""")

        select = input("Select:")
        if select.lower() == "a":
            account_creation()
        elif select.lower() == "b":
            deposits()
        elif select.lower() == "c":
            withdraws()
        elif select.lower() == "z":
            user = input("Enter Manager ID:")                                                #this creates a login which only allows a manager to access all records
            password = input("Enter Password:")
            if user.lower() == "shafeeq" and password.lower() == "number1":
                list_accounts()
            else:
                print("""Wrong ID or Password"
                """)



main()
