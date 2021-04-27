from flask import Flask
from flask import render_template
from flask import url_for
from flask import request
import sqlite3 as sql 
from flask_bootstrap import Bootstrap
app = Flask(__name__)
Bootstrap(app)
@app.route ("/home")
def new_home():
    return render_template("home.html")
    

#creates database
def create_database():
        conn=sql.connect("final.db")
        conn.execute("CREATE TABLE  items  (itemname TEXT, itemcost INTEGER, itemID INTEGER )") 
        conn.execute("CREATE TABLE  cart   (  cartid INTEGER primary key, qtyitem1 INTEGER, qtyitem2 INTEGER, qtyitem3 INTEGER, personid INTEGER, isordered INTEGER DEFAULT 0)")
        conn.execute("CREATE TABLE  person ( emailadd text, name text , personID INTEGER primary key)")
        
        
        conn.close()

#create_database()

@app.route ("/add", methods=['POST'])
def addcart():
    if request.method == "POST":
               qtyitem1 = request.form["q1"]
               qtyitem2 = request.form["q2"]
               qtyitem3 = request.form["q3"]
        
    with sql.connect("final.db") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO cart(qtyitem1, qtyitem2, qtyitem3) VALUES (?,?,?)", [qtyitem1,qtyitem2,qtyitem3])
    con.commit
    return render_template("presshere1.html")

@app.route ("/newperson")
def newperson():
    return render_template("person.html")
@app.route ("/addperson", methods=['POST'])
def addperson():
    if request.method == "POST":
               global email
               email = request.form["emadd"]
               name = request.form["nm"]
        
    with sql.connect("final.db") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO person(emailadd, name) VALUES (?,?)", [email,name])
    con.commit
    con = sql.connect("final.db")
    #con.row_factory = sql.Row

    cur = con.cursor()
    cur.execute("SELECT personID  FROM  person ORDER BY personID DESC LIMIT 1")

    

    global uid
    uid = cur.fetchone()[0]
    with sql.connect("final.db") as con:
                cur = con.cursor()
                cur.execute("UPDATE cart set PersonID = ? ORDER BY cartid DESC LIMIT 1", [uid])
                cur.execute("UPDATE cart set isordered = 1  ORDER BY cartid DESC LIMIT 1")
    return render_template("presshere2.html")

    
@app.route ("/invoice")
def invoice():
       con = sql.connect("final.db")
       con.row_factory = sql.Row
       global uid
       cur = con.cursor()
       cur.execute("SELECT qtyitem1  FROM  cart where personID = ? ORDER BY cartid DESC",[uid])
       
       qty1 = cur.fetchone()[0]
       if qty1 == "":
        qty1 = 0
       cur.execute("SELECT qtyitem2  FROM  cart where personID = ? ORDER BY cartid DESC",[uid])
       
       qty2 = cur.fetchone()[0]
       if qty2 == "":
        qty2 = 0
       cur.execute("SELECT qtyitem3  FROM  cart where personID = ? ORDER BY cartid DESC",[uid])
       
       qty3 = cur.fetchone()[0]
       if qty3 == "":
        qty3 = 0

       cur.execute("SELECT itemcost from items where itemid = 1")
       cost1= cur.fetchone()[0] * qty1

       cur.execute("SELECT itemcost from items where itemid = 2")
       cost2= cur.fetchone()[0] * qty2

       cur.execute("SELECT itemcost from items where itemid = 3")
       cost3= cur.fetchone()[0] * qty3

       subtotalcost = float( cost1 + cost2 + cost3)

       salestax = 1.09

       totalcost =float( subtotalcost * salestax)
       return render_template("invoice.html", qty1 = qty1, qty2 = qty2, qty3 = qty3, cost1 = cost1, cost2 = cost2, cost3 = cost3, subtotalcost = subtotalcost, totalcost = totalcost )
        