import re
from flask import *
import sqlite3
from helper import login_required
import os.path

app=Flask(__name__)
app.secret_key="EmployeeWAY"

#homepage
@app.route("/")
def landing_page():
    return render_template("landing_page.html")

#search Salary
@app.route("/searchsalary", methods=["GET", "POST"])
def searchsalary():
    if request.method=="POST":
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(BASE_DIR, "EmployeeWay.db")
        rows=None

        id=request.form["eid"]

        if not id:
            flash("Empty Entities!")
            return redirect(url_for("searchsalary"))

        rows=None
        
        with sqlite3.connect(db_path) as conn:
            db=conn.cursor()
            rows=list(db.execute("select * from empdata where eid=?", (id,)))

        if len(rows)<1:
            flash("Invalid Employee ID")
            return redirect(url_for("searchsalary"))

        with sqlite3.connect(db_path) as conn:
            db=conn.cursor()
            rows=list(db.execute("select * from empsalary where eid=?", (id,)))

        return render_template("searchSalaryResult.html", rows=rows, id=id)

    else:
        return render_template("searchsalary.html")


#view salary slip
@app.route("/viewsalary")
def viewsalary():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "EmployeeWay.db")
    rows=None

    rows=None
    with sqlite3.connect(db_path) as conn:
        db=conn.cursor()
        rows=list(db.execute("select * from empsalary"))

    return render_template("viewsalary.html", rows=rows)



#add salary Slip
@app.route("/addsalary", methods=["GET", "POST"])
def addsalary():
    if request.method=="POST":
        id=request.form["eid"]
        salary=request.form["salary"]
        date=request.form["date"]

        if not id or not salary:
            flash("Empty Entities")
            return redirect(url_for("addsalary"))

        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(BASE_DIR, "EmployeeWay.db")
        rows=None

        rows=None
        with sqlite3.connect(db_path) as conn:
            db=conn.cursor()
            rows=list(db.execute("select * from empdata where eid=?", (id,)))

        if len(rows)<=0:
            flash("Invalid Employee ID / No Result Found")
            return redirect(url_for("addsalary"))

        with sqlite3.connect(db_path) as conn:
            db=conn.cursor()
            db.execute("insert into empsalary(eid, salary, date) values(?,?,?)", (id, salary, date))
            conn.commit()

        flash("Salary Slip Added!")
        return redirect(url_for("addsalary"))

    else:
        return render_template("addsalary.html")




#view all attendence
@app.route("/viewattendence")
def viewattendence():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "EmployeeWay.db")

    rows=None
    with sqlite3.connect(db_path) as conn:
        db=conn.cursor()
        rows=list(db.execute("select * from empattendence"))

    return render_template("viewattendence.html", rows=rows)

#search attendence
@app.route("/searchattendence", methods=["GET", "POST"])
def searchattendence():
    if request.method=="POST":
        
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(BASE_DIR, "EmployeeWay.db")

        id=request.form["eid"]
        if not id:
            flash("Empty Employee ID Field!")
            return redirect(url_for("searchattendence"))

        rows=None
        with sqlite3.connect(db_path) as conn:
            db=conn.cursor()
            rows=list(db.execute("select * from empattendence where eid=?", (id,)))

        if len(rows)<=0:
            flash("Invalid Employee ID / No Result Found")
            return redirect(url_for("searchattendence"))

        return render_template("searchAttendenceResult.html", rows=rows, id=id)

    else:
        return render_template("searchattendence.html")

#mark attendence
@app.route("/addattendence", methods=["GET", "POST"])
def addattendence():
    if request.method=="POST":
        id=request.form["eid"].strip()
        attendence=request.form["attendence"]
        date=request.form["date"].strip()

        
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(BASE_DIR, "EmployeeWay.db")

        if not date or not id:
            flash("Enitities Empty!")
            return redirect(url_for("addattendence"))

        rows=None
        with sqlite3.connect(db_path) as conn:
            db=conn.cursor()
            rows=list(db.execute("select * from empdata where eid=?", (id,)))

        if len(rows)<1:
            flash("Invalid Employee ID")
            return redirect(url_for("addattendence"))

        with sqlite3.connect(db_path) as conn:
            db=conn.cursor()
            db.execute("insert into empattendence(description,eid, date) values(?,?,?)", (attendence, id, date))
            conn.commit()

        

        flash("Attendence Marked")
        return render_template("addattendence.html")

    else:
        return render_template("addattendence.html")


#search employee
@app.route("/searchemployee", methods=["GET", "POST"])
def searchemployee():
    if request.method=="POST":
        id=request.form["eid"].strip()

        rows=None
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(BASE_DIR, "EmployeeWay.db")
        with sqlite3.connect(db_path) as conn:
            db=conn.cursor()
            rows=list(db.execute("select * from empdata where eid=?", (id,)))

        if not id:
            flash("Employee Field Empty!")
            return redirect(url_for("searchemployee"))

        return render_template("searchEmployeeResult.html", rows=rows)

    else:
        return render_template("searchemployee.html")



#view all employee
@app.route("/viewemployee")
def viewemployee():
    rows=None
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "EmployeeWay.db")
    with sqlite3.connect(db_path) as conn:
        db=conn.cursor()
        rows=list(db.execute("select * from empdata"))
        #retrievs all the account details

    if len(rows)==0:
        flash("Unable to Process Data")
        return redirect(url_for("addemployee"))

    return render_template("viewemployee.html", rows=rows)

#add employee details
@app.route("/addemployee", methods=["GET", "POST"])
def addemployee():
    if request.method=="POST":
        id=request.form["employee_id"].strip()
        fname=request.form["first_name"].strip()
        lname=request.form["last_name"].strip()
        position=request.form["position"].strip()
        number=request.form["mobile"].strip()
        email=request.form["email"].strip()
        dob=request.form["dob"].strip()
        address=request.form["address"].strip()


        if not email or not id or not fname or not lname or not dob or not position or not number or not address:
            flash("Some Entities Empty!")
            return redirect(url_for("addemployee"))

        if len(str(number))!=10:
            flash("Invalid Mobile Number!")
            return redirect(url_for("addemployee"))

        if "@" not in email or "." not in email:
            flash("Invalid Email ID")
            return redirect(url_for("addemployee"))

        table_data=None
        #below code open the sqlite file in same directory as code
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(BASE_DIR, "EmployeeWay.db")

        #sqlite to check username exists or not
        with sqlite3.connect(db_path) as conn:
            db=conn.cursor()
            table_data=list(db.execute("select * from empdata where eid=?", (id,)))

        if len(table_data) >=1:
            flash("User Already Exists!")
            return redirect(url_for("addemployee"))

        with sqlite3.connect(db_path) as conn:
            db=conn.cursor()
            db.execute("insert into empdata(eid, fname, lname, email, mnumber, address, dob, position) values(?,?,?,?, ?,?,?,?)", (id, fname, lname,email, number, address, dob, position))
            conn.commit()

        flash("Employee Added Successfully")
        return render_template("addemployee.html")

    else:
        return render_template("addemployee.html")

#login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method=="POST":
        #gets the username and password from html page
        username=request.form["username"].strip()
        password=request.form["password"].strip()

        if not username or not password:
            flash("Invalid Username or Password")
            return redirect(url_for('login'))

        table_data=None
        #below code open the sqlite file in same directory as code
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(BASE_DIR, "EmployeeWay.db")

        #sqlite to check username exists or not
        with sqlite3.connect(db_path) as conn:
            db=conn.cursor()
            table_data=list(db.execute("select * from data where username=?", (username,)))

        if len(table_data)<1 or username!= table_data[0][2] or password!=table_data[0][3]:
            flash("Invalid Username or Password")
            return redirect(url_for('login'))

        #cretes session
        session['userno']=table_data[0][0]

        print("LOGIN SUCCESSFUL")

        return render_template("index.html", name=table_data[0][1])

    else:
        return render_template("login.html")



#register page code
#register for user
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method=="POST":
        name=request.form["name"].strip()
        username=request.form["username"].strip()
        email=request.form["email"].strip()
        password=request.form["password"].strip()
        repassword=request.form["repassword"].strip()

        if not name or not password or not repassword or not username or not email:
            flash("Invalid Entries: Kindly Check")
            return redirect(url_for('register'))

        if password!=repassword:
            flash("Passwords don't match!")
            return redirect(url_for('register'))

        table_data=None
        
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(BASE_DIR, "EmployeeWay.db")

        #checks if uname exits in sqlite file
        with sqlite3.connect(db_path) as conn:
            db=conn.cursor()
            table_data=list(db.execute("select * from data where username=?",(username,)))

        if len(table_data)>0:
            flash("Username Already Exists. Change Username")
            return redirect(url_for('register'))

        with sqlite3.connect(db_path) as conn:
            db=conn.cursor()
            db.execute("insert into data(name, username, password, email) values(?,?,?,?)", (name, username, password,email))
            conn.commit()
            table_data=list(db.execute("select * from data where username=?",(username,)))
        
        #creates session
        session['userno']=table_data[0][0]

        print("REGISTER SUCCESSFUL")

        return render_template("index.html", name=name)

    else:
        return render_template("register.html")


#logout
@app.route("/logout")
@login_required
def logout():
    session.clear()     #clers session and log's out
    flash("User Logout Successful")
    return redirect(url_for("landing_page"))


#this sections is used to change the user's pass
@app.route("/change_password", methods=["GET", "POST"])
@login_required
def change_password():
    if request.method=="POST":
        oldpassword=request.form["oldpassword"]
        password=request.form["password"]
        repassword=request.form["repassword"]

        if not password or not repassword or not oldpassword:
            flash("Entries Field Empty")
            return redirect(url_for("change_password"))

        if password!=repassword:
            flash("Passwords don't match")
            return redirect(url_for("change_password"))

        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(BASE_DIR, "EmployeeWay.db")
        with sqlite3.connect(db_path) as conn:
            db=conn.cursor()

            #retreives the olpassword and checks if entered matches or not
            data=list(db.execute("select password from data where userno=?", (session["userno"],)))
            if data[0][0] != oldpassword:
                flash("Oldpassword doesnot match. Kindly Check.")
                return redirect(url_for("change_password"))

            db.execute("update data set password=? where userno=?", (password, session['userno']))
            conn.commit()

        flash("Password Changed!")
        return redirect(url_for("change_password"))

    else:
        return render_template("change_password.html")




if __name__=="__main__":
    app.run(debug=True)

