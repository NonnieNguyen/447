from flask import Flask, render_template, request
import sqlite3 as sql
app = Flask(__name__)

@app.route('/')
def home():
   return render_template('home.html')

@app.route('/remove')
def remove():

   con = sql.connect("database.db")
   con.row_factory = sql.Row
   
   cur = con.cursor()
   cur.execute("select * from students")
   
   rows = cur.fetchall()   
   con.close()
   return render_template("remove.html",rows = rows)

@app.route('/removerec', methods = ['POST', 'GET'])
def removerec():
   if request.method == 'POST':
      try:
         nm = request.form['nm']
         
         with sql.connect("database.db") as con:
            cur = con.cursor()
            cur.execute("SELECT name FROM students WHERE name=?",(nm,))

            if cur.fetchone():
               cur.execute("DELETE FROM students WHERE name=?",(nm,))
               con.commit()
               msg = "Record successfully removed"

            else:
               con.rollback()
               msg = "Could not find user"

      except:
         con.rollback()
         msg = "error in removing operation"
      
      finally:

         con.close()
         return render_template("result.html",msg = msg)


@app.route('/enternew')
def new_student():
   return render_template('student.html')   

@app.route('/addrec',methods = ['POST', 'GET'])
def addrec():
   if request.method == 'POST':
      try:
         nm = request.form['nm']
         id = request.form['id']
         point = request.form['point']
         
         with sql.connect("database.db") as con:
            cur = con.cursor()
            
            cur.execute("INSERT INTO students (name,id,point) VALUES (?,?,?)",(nm,id,point) )
            
            con.commit()
            msg = "Record successfully added"
      except:
         con.rollback()
         msg = "error in insert operation"
      
      finally:
         con.close()
         return render_template("result.html",msg = msg)

@app.route('/list')
def list():
   con = sql.connect("database.db")
   con.row_factory = sql.Row
   
   cur = con.cursor()
   cur.execute("select * from students")
   
   rows = cur.fetchall()
   con.close()
   return render_template("list.html",rows = rows)

@app.route('/search')
def search():
   con = sql.connect("database.db")
   con.row_factory = sql.Row
   
   cur = con.cursor()
   cur.execute("select * from students")
   
   rows = cur.fetchall()
   con.close()
   return render_template("search.html",rows = rows)

@app.route('/searchrec',methods = ['POST', 'GET'])
def searchrec():
   if request.method == 'POST':
      try:
         nm = request.form['nm']
         id = request.form['id']
         
         con = sql.connect("database.db")
         con.row_factory = sql.Row

         cur = con.cursor()
         cur.execute("SELECT * FROM students WHERE name = ? OR id = ?", (nm,id))

         rows = cur.fetchall()
         msg = "All User(s) named " + nm +" and User(s) with ID of " + id
      except:
         con.rollback()
         msg = "User was not found"
      
      finally:
         con.close()
         return render_template("sresult.html",msg = msg, rows = rows)

if __name__ == '__main__':
   conn = sql.connect('database.db')
   print ("Opened database successfully")

   conn.execute('CREATE TABLE IF NOT EXISTS students (name TEXT, id TEXT, point TEXT)')
   print ("Table created successfully")
   conn.close()
   app.run(debug = True)