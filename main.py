import sqlite3
import random
import pandas as pd
import math
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import datetime
def cardgenerator(n):
    digits = [i for i in range(0, 10)]
    r = ""
    for i in range(n):
        index = math.floor(random.random() * 10)
        r += str(digits[index])
    return int(r)
def signup(name,email,accno,card,password,account,branch):
    id = cursor.execute("SELECT id FROM Customers ORDER BY ID DESC LIMIT 1").fetchall()
    idu=id[0][0]
    print(idu)
    sign = f"insert into Customers values({idu+1},'{name}','{email}',{accno},'{card}','{password}','{account}','{branch}')"
    time = cursor.execute("select datetime('now','localtime')").fetchall()
    bal = f"insert into Balance values('{time[0][0]}',{idu+1},'{card}',0,0,0)"
    print(sign)
    cursor.execute(sign)
    sqliteConnection.commit()
    # print(cursor.execute(bal).fetchall())
    sqliteConnection.commit()
def transaction(card,amt,type=None):
    print(card)
    bal=cursor.execute(f"select Balance from Balance where CardNo={card};").fetchall()
    print(bal)
    bal=bal[0][0]
    if type is None:
        return bal
    print(bal)
    if type:
        print(card)
        depo=f"update Balance set deposit={amt},Balance={bal+amt} where CardNo= {card};"
        time = cursor.execute("select datetime('now','localtime')").fetchall()
        depoi=f"insert into Transact values({time[0][0]},{card},'deposit',{amt},{bal},{bal+amt})"
        # depo=f"update Balance set TransType='Deposit', Amount={amt},BalBefore={bal},BalAfter={bal+amt} where CardNo={card}"
        cursor.execute(depo)
        cursor.execute(depoi)
        sqliteConnection.commit()

    else:
        print("hELLO")
        witd = f"update Balance set withdraw={amt},Balance={bal - amt} where CardNo={card}"
        time = cursor.execute("select datetime('now','localtime')").fetchall()
        widoi=f"insert into Transact values({card},'Withdrawal',{amt},{bal},{bal+amt},'{time[0][0]}')"
        cursor.execute(witd)
        cursor.execute(widoi)
        sqliteConnection.commit()
def sendmoney(sender,card,amt):
    transaction(sender,amt,0)
    transaction(card,amt,1)
    print("Successfull")
def recentTrans(card):
    df=pd.read_sql_query(f"select * from Transact where CardNo= {card}",sqliteConnection)
    printstats(df,'Summary')
def printstats(df,name):
    fig, ax = plt.subplots(figsize=(12, 4))
    ax.axis('tight')
    ax.axis('off')
    the_table = ax.table(cellText=df.values, colLabels=df.columns, loc='center')
    pp = PdfPages(f"{name}.pdf")
    pp.savefig(fig, bbox_inches='tight')
    pp.close()
try:

    sqliteConnection = sqlite3.connect('Bankdata.db')
    createtable = '''CREATE TABLE Customers (id INTEGER PRIMARY KEY,  name TEXT NOT NULL, email TEXT NOT NULL UNIQUE,AccountNo INTEGER UNIQUE,
                                CardNo REAL NOT NULL,Password TEXT NOT NULL UNIQUE,Account TEXT,Branch TEXT);'''

    createtable2 = '''CREATE TABLE Balance (Time datetime,id INTEGER PRIMARY KEY, CardNo  REAL NOT NULL UNIQUE,deposit NUMERIC,withdraw NUMERIC,Balance NUMERIC);'''
    createtable3='''CREATE TABLE Transact (Time datetime,CardNo REAL NOT NULL ,TransType TEXT,Amount NUMERIC,BalBefore NUMERIC,BalAfter NUMERIC);'''
    # insert = "insert into Customers values(1,'Shaun','shaun@gmail.com',1234,'Pass')"
    insert="Insert into Customers values(0,'--------','-------',000000,'-----','------','------','-------')"
    cursor = sqliteConnection.cursor()
    print("Successfully Connected to SQLite")
    # cursor.execute("DROP TABLE IF EXISTS Balance")
    # cursor.execute("Drop table if exists Customers")
    # cursor.execute(createtable2)
    # cursor.execute(createtable)
    # cursor.execute(insert)
    # print(a)
    # cursor.execute("Alter table Balance add Time datetime;")
    # time=cursor.execute("select datetime('now','localtime')").fetchall()
    # print(f'''UPDATE Balance SET Time = '{time[0][0]}' where CardNo=473396.0;''')
    # cursor.execute(f'''UPDATE Transact SET Time = '{time[0][0]}' where CardNo=473396.0;''')
    print("Welecone to Our Bank !!")
    name=input("Please Enter Your Name : ")
    email = input("Please Enter Your Email : ")
    password=input("Pleas Enter a password : ")
    account="Savings"
    branch = "Mumbai"

    card = cardgenerator(6)
    accno= cardgenerator(4)
    print(f"Your Card No is {card} and Account No is {accno}\n Store it carefully for future use")
    # signup(name,email,accno,card,password,account,branch)
    print("sIGNuP sUCDCESSFUL")
    df = pd.read_sql_query('Select * from Customers', sqliteConnection)
    bala = pd.read_sql_query('Select * from Transact', sqliteConnection)
    print(df.head())
    print(bala.head())
    # bal=transaction(92800,100)
    sendmoney(473396,92800,50)
    # print(bal)
    op=cursor.execute("Select * from Customers").fetchall()
    df=pd.read_sql_query('Select * from Customers',sqliteConnection)
    bala=pd.read_sql_query('Select * from Balance',sqliteConnection)
    trans=pd.read_sql_query('Select * from Transact  where TransType="Withdrawal"',sqliteConnection)
    print(df.head())
    print(bala.head())
    print(trans.head())
    print(op)
    # sendmoney()
    sqliteConnection.commit()
    print("SQLite table created")
    # cursor.execute("Show Databases;")
    recentTrans(473396)
    cursor.close()
except sqlite3.Error as error:
    print("Error while creating a sqlite table", error)
finally:
    if sqliteConnection:
        sqliteConnection.close()
        print("sqlite connection is closed")
        # printstats(bala,'hello')



