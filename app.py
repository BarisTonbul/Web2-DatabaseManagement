from flask import Flask , render_template,request,redirect,url_for,json,flash
from flask_mysqldb import MySQL
from pymysql.cursors import DictCursor#to fetch as dictionary

app= Flask(__name__)

#configure db
app.config['MYSQL_HOST']= 'localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_DB']='sportclub'
mysql = MySQL(app)
#this is for using flask.flash() method
app.secret_key='12345'

##FIRST PAGE
@app.route("/")
def firstPage():
    return redirect(url_for("signup"))#signup fonksiyonuna yonlendirdi
##SIGNUP
@app.route("/signup.html",methods=["GET","POST"])
def signup():
    if request.method=="POST":
        req=request.form
        username=req.get("username")
        email=req.get("email")
        password=req.get("password")
        print(username,email,password)
        if not len(password) >= 10:
            flash("Password must be at least 10 characters in length","danger")#For bootstrap changes
            return redirect(request.url)#render ayni html adresinde farkli bir html sayfasi goruntuleyebilir   
        flash("account created","danger")#For bootstrap changes
        return redirect("/index.html")#Belirtilen sayfaya veya fonksiyona gonderir adresi degistirir
    return render_template("/signup.html")
##INDEX HTML
@app.route("/index.html",methods=["GET","POST"])
def index():
    return render_template("/index.html")
##INFO
@app.route("/info.html",)        
def info():
    #DIRECTING TO INFO TABLE;
    return render_template("info.html")
@app.route("/showtables.html")
##SHOWING TABLES 
def showtables():
    cur = mysql.connection.cursor()
    ##GETTING TABLE ROW LENGTHS
    customerNumbers = cur.execute("select * from customer")
    gymNumbers = cur.execute("select * from gym")
    ptNumbers = cur.execute("select * from personal_trainer")
    subscribeNumbers = cur.execute("select * from subscribe")
    workNumbers = cur.execute("select * from works")
    ##ASSIGN THEM TO A VARIABLE USE ON HTML PAGE
    return render_template("showtables.html",
    customerNumbers=customerNumbers,
    gymNumbers=gymNumbers,
    ptNumbers=ptNumbers,
    subscribeNumbers=subscribeNumbers,
    workNumbers=workNumbers,)
##CUSTOMER table
@app.route("/customertable.html",methods = ["GET","POST"])
def customertable():
    cur=mysql.connection.cursor()#defining cursor
    #CHECKING IF USER SUBMITS A NEW RECORD 
    if request.method == "POST":
        if request.form['submit_button'] == 'add':
            try:
                #GETTING RECORD VALUES FROM HTML INPUTS
                ID=request.form.get("ID")
                NAME=request.form.get("NAME")
                GENDER=request.form.get("GENDER")
                AGE=request.form.get("AGE")
                #INSERT VALUES INTO TABLE
                cur.execute("insert into customer(c_id,c_name,c_gender,c_age) values(%s, %s, %s, %s)",(ID,NAME,GENDER,AGE))
                mysql.connection.commit()##SAVE CHANGES PERMANANTLY
                cur.close()
                #RELOAD PAGE USING REDIRECT COMMAND(I TRIED RENDER_TEMPLETE BUT IT DIDNT WORK PROPERLY)
                flash("OPERATION SUCCESFULL!!!","danger")
                return redirect(url_for("customertable"))# <-- CUSTOMERTABLE IS FUNCTION
            except:
                flash("ERROR@@@","danger")
                return redirect(request.url)
        elif request.form['submit_button'] == 'remove':
            try:
                ID=request.form.get("ID_remove")
                #USING [] INSTEAD OF () SOLVED MY PROBLEM. I COULDNT REMOVE ABOVE 3 DIGIT NUMBER ID
                cur.execute("delete from customer where c_id = %s ",[ID])
                mysql.connection.commit()##SAVE CHANGES PERMANANTLY
                cur.close()
                flash("OPERATION SUCCESFULL!!!","danger")
                return redirect(url_for("customertable"))
            except:
                flash("ERROR@@@","danger")
                return redirect(url_for("customertable"))
        elif request.form['submit_button'] == 'submit':
            try:
                code=request.form.get("code")#getting code from input
                #using {} brackets instead of using %s ,solved my type error problem.
                cur.execute("{0}".format(code))
                mysql.connection.commit()##SAVE CHANGES PERMANANTLY
                cur.close()
                flash("OPERATION SUCCESFULL!!!","danger")
                return redirect(url_for("customertable"))
            except:
                flash("ERROR@@@","danger")
                return redirect(request.url)
        #these are for complex operations
        elif request.form['submit_button'] == 'execute1':
            resultValue=cur.execute("select customer.*,subscribe.g_id from customer inner join subscribe on customer.c_id=subscribe.c_id")
            ##CONTROL IF THERE ARE ANY DATA EXIST 
            if resultValue>0:
                results=cur.fetchall()
                x=1#to add list headline in html
                return render_template("/customertable.html",results=results,x=x)
        elif request.form['submit_button'] == 'execute2':
            try:
                ID=request.form.get("ID_execute")
                resultValue=cur.execute("select pt_name  from personal_trainer where pt_id=ANY(select pt_id from works where g_id=ANY (select g_id from subscribe where c_id =%s))",[ID])
                ##CONTROL IF THERE ARE ANY DATA EXIST 
                if resultValue>0:
                    result=cur.fetchall()
                    cur.execute("select * from customer")
                    results=cur.fetchall()
                    x=2#to add list headline in html
                    flash("OPERATION SUCCESFULL!!!","danger")
                return render_template("/customertable.html",result=result,x=x,results=results)
            except:
                flash("ERROR@@@","danger")
                return redirect(request.url)
        elif request.form['submit_button'] == 'return':#To return tables page
            return redirect(url_for("showtables"))
    else: #this is the base page. when it loads just this page does this operations
        cur = mysql.connection.cursor()
        resultValue = cur.execute("select * from customer")#taking all customer info
        ##CONTROL IF THERE ARE ANY DATA EXIST 
        if resultValue>0:
            results=cur.fetchall()
            return render_template("/customertable.html",results=results)
##GYM table
@app.route("/gymtable.html",methods = ["GET","POST"])
def GYM():
    cur=mysql.connection.cursor()
    if request.method == "POST":
        if request.form['submit_button'] == 'add':
            try:
                #GETTING RECORD VALUES FROM HTML INPUTS
                ID=request.form.get("ID")
                NAME=request.form.get("NAME")
                #INSERT VALUES INTO TABLE
                cur.execute("insert into gym(g_id,g_name) values(%s, %s)",(ID,NAME))
                mysql.connection.commit()##SAVE CHANGES PERMANANTLY
                cur.close()
                #RELOAD PAGE USING REDIRECT COMMAND(I TRIED RENDER_TEMPLETE BUT IT DIDNT WORK PROPERLY)
                flash("OPERATION SUCCESFULL!!!","danger")
                return redirect(url_for("GYM"))# <-- GYM IS FUNCTION TO RETURN
            except:
                flash("ERROR@@@","danger")
                return redirect(request.url)
        elif request.form['submit_button'] == 'remove':
            try:
                ID=request.form.get("ID_remove")
                #USING [] INSTEAD OF () SOLVED MY PROBLEM. I COULDNT REMOVE ABOVE 3 DIGIT NUMBER ID
                cur.execute("delete from gym where g_id = %s ",[ID])
                mysql.connection.commit()##SAVE CHANGES PERMANANTLY
                cur.close()
                flash("OPERATION SUCCESFULL!!!","danger")
                return redirect(url_for("GYM"))
            except:
                flash("ERROR@@@","danger")
                return redirect(request.url)
        elif request.form['submit_button'] == 'submit':
            try:
                code=request.form.get("code")#getting code from input
                #using {} brackets instead of using %s ,solved my type error problem.
                cur.execute("{0}".format(code))
                mysql.connection.commit()##SAVE CHANGES PERMANANTLY
                cur.close()
                flash("OPERATION SUCCESFULL!!!","danger")
                return redirect(url_for("GYM"))
            except:
                flash("ERROR@@@","danger")
                return redirect(request.url)
        #these are for complex operations
        elif request.form['submit_button'] == 'execute1':
            resultValue=cur.execute("select gym.*,works.pt_id from gym inner join works on gym.g_id=works.g_id")
            ##CONTROL IF THERE ARE ANY DATA EXIST 
            if resultValue>0:
                results=cur.fetchall()
                x=1#to add list headline in html
                return render_template("/gymtable.html",results=results,x=x)
        elif request.form['submit_button'] == 'execute2':
            try:
                ID=request.form.get("ID_execute")
                resultValue=cur.execute("select max(c_age) as Oldest_member from customer where c_id=ANY (select c_id from subscribe where g_id=%s)",[ID])
                ##CONTROL IF THERE ARE ANY DATA EXIST 
                if resultValue>0:
                    result=cur.fetchall()
                    cur.execute("select * from gym")
                    results=cur.fetchall()
                    x=2#to add list headline in html
                    flash("OPERATION SUCCESFULL!!!","danger")
                    return render_template("/gymtable.html",result=result,x=x,results=results)
            except:
                flash("ERROR@@@","danger")
                return redirect(request.url)
        elif request.form['submit_button'] == 'return':
            return redirect(url_for("showtables"))
    else:
        cur = mysql.connection.cursor()
        resultValue = cur.execute("select * from gym")#taking all GYM info
        ##CONTROL IF THERE ARE ANY DATA EXIST 
        if resultValue>0:
            results=cur.fetchall()
            return render_template("/gymtable.html",results=results)
##PERSONAL TRAINER TABLE
@app.route("/pttable.html",methods = ["GET","POST"])
def personal_trainer():
    cur=mysql.connection.cursor()
    if request.method == "POST":
        if request.form['submit_button'] == 'add':
            try:
                #GETTING RECORD VALUES FROM HTML INPUTS
                ID=request.form.get("ID")
                NAME=request.form.get("NAME")
                AGE=request.form.get("AGE")
                #INSERT VALUES INTO TABLE
                cur.execute("insert into personal_trainer(pt_id,pt_name,pt_age) values(%s, %s, %s)",(ID,NAME,AGE))
                mysql.connection.commit()##SAVE CHANGES PERMANANTLY
                cur.close()
                #RELOAD PAGE USING REDIRECT COMMAND(I TRIED RENDER_TEMPLETE BUT IT DIDNT WORK PROPERLY)
                flash("OPERATION SUCCESFULL!!!","danger")
                return redirect(url_for("personal_trainer"))# <-- PERSONAL TRAINER IS FUNCTION TO RETURN
            except:
                flash("ERROR@@@","danger")
                return redirect(request.url)
        elif request.form['submit_button'] == 'remove':
            try:
                ID=request.form.get("ID_remove")
                #USING [] INSTEAD OF () SOLVED MY PROBLEM. I COULDNT REMOVE ABOVE 3 DIGIT NUMBER ID
                cur.execute("delete from personal_trainer where pt_id = %s ",[ID])
                mysql.connection.commit()##SAVE CHANGES PERMANANTLY
                cur.close()
                flash("OPERATION SUCCESFULL!!!","danger")
                return redirect(url_for("personal_trainer"))
            except:
                flash("ERROR@@@","danger")
                return redirect(request.url)
        elif request.form['submit_button'] == 'submit':
            try:
                code=request.form.get("code")#getting code from input
                #using {} brackets instead of using %s ,solved my type error problem.
                cur.execute("{0}".format(code))
                mysql.connection.commit()##SAVE CHANGES PERMANANTLY
                cur.close()
                flash("OPERATION SUCCESFULL!!!","danger")
                return redirect(url_for("personal_trainer"))
            except:
                flash("ERROR@@@","danger")
                return redirect(request.url)
        #these are for complex operations
        elif request.form['submit_button'] == 'execute1':
            resultValue=cur.execute("select personal_trainer.*,works.g_id from personal_trainer inner join works on personal_trainer.pt_id=works.pt_id")
            ##CONTROL IF THERE ARE ANY DATA EXIST 
            if resultValue>0:
                results=cur.fetchall()
                x=1#to add list headline in html
                return render_template("/pttable.html",results=results,x=x)
        elif request.form['submit_button'] == 'execute2':
            try:
                ID=request.form.get("ID_execute")
                resultValue=cur.execute("select avg(c_age) from customer where c_id = ANY (select c_id from subscribe where g_id=ANY(select g_id from works where pt_id =%s))",[ID])
                ##CONTROL IF THERE ARE ANY DATA EXIST 
                if resultValue>0:
                    result=cur.fetchall()
                    cur.execute("select * from personal_trainer")
                    results=cur.fetchall()
                    x=2#to add list headline in html
                    flash("OPERATION SUCCESFULL!!!","danger")
                    return render_template("/pttable.html",result=result,x=x,results=results)
            except:
                flash("ERROR@@@","danger")
                return redirect(request.url)
        elif request.form['submit_button'] == 'return':
            return redirect(url_for("showtables"))
    else:
        resultValue = cur.execute("select * from personal_trainer")#taking all PT info
        ##CONTROL IF THERE ARE ANY DATA EXIST 
        if resultValue>0:
            results=cur.fetchall()
            return render_template("/pttable.html",results=results)
##SUCSCRIBE TABLE
@app.route("/subscribetable.html",methods = ["GET","POST"])
def subscribe():
    cur=mysql.connection.cursor()
    if request.method == "POST":
        if request.form['submit_button'] == 'add':
            try:
                #GETTING RECORD VALUES FROM HTML INPUTS
                CUSTOMER_ID=request.form.get("C_ID")
                GYM_ID=request.form.get("G_ID")
                START_DATE=request.form.get("START")
                END_DATE=request.form.get("END")
                #INSERT VALUES INTO TABLE
                cur.execute("insert into subscribe(c_id,g_id,s_start_date,s_end_date) values(%s, %s, %s, %s)",(CUSTOMER_ID,GYM_ID,START_DATE,END_DATE))
                mysql.connection.commit()##SAVE CHANGES PERMANANTLY
                cur.close()
                #RELOAD PAGE USING REDIRECT COMMAND(I TRIED RENDER_TEMPLETE BUT IT DIDNT WORK PROPERLY)
                flash("OPERATION SUCCESFULL!!!","danger")
                return redirect(url_for("subscribe"))# <-- SUBSCRIBE IS FUNCTION TO RETURN
            except:
                flash("ERROR@@@","danger")
                return redirect(request.url)
        elif request.form['submit_button'] == 'remove':
            try:
                ID=request.form.get("ID_remove")
                #USING [] INSTEAD OF () SOLVED MY PROBLEM. I COULDNT REMOVE ABOVE 3 DIGIT NUMBER ID
                cur.execute("delete from subscribe where c_id = %s ",[ID])
                mysql.connection.commit()##SAVE CHANGES PERMANANTLY
                cur.close()
                flash("OPERATION SUCCESFULL!!!","danger")
                return redirect(url_for("subscribe"))
            except:
                flash("ERROR@@@","danger")
                return redirect(request.url)
        elif request.form['submit_button'] == 'submit':
            try:
                code=request.form.get("code")#getting code from input
                #using {} brackets instead of using %s ,solved my type error problem.
                cur.execute("{0}".format(code))
                mysql.connection.commit()##SAVE CHANGES PERMANANTLY
                cur.close()
                flash("OPERATION SUCCESFULL!!!","danger")
                return redirect(url_for("subscribe"))
            except:
                flash("ERROR@@@","danger")
                return redirect(request.url)
        #these are for complex operations
        elif request.form['submit_button'] == 'execute1':
            ## I USED ORDER BY BECAUSE OF THE MESS 
            resultValue=cur.execute("select subscribe.*,gym.g_name from subscribe inner join gym on subscribe.g_id=gym.g_id order by c_id ASC")
            ##CONTROL IF THERE ARE ANY DATA EXIST 
            if resultValue>0:
                results=cur.fetchall()
                x=1#to add list headline in html
                return render_template("/subscribetable.html",results=results,x=x)
        elif request.form['submit_button'] == 'execute2': 
            cur.execute("select * from subscribe order by g_id asc")
            results=cur.fetchall()
            return render_template("/subscribetable.html",results=results)
        elif request.form['submit_button'] == 'return':
            return redirect(url_for("showtables"))
    else:
        cur = mysql.connection.cursor()
        resultValue = cur.execute("select * from subscribe  order by c_id ASC")#taking all subscribe info //ordered by id
        ##CONTROL IF THERE ARE ANY DATA EXIST 
        if resultValue>0:
            results=cur.fetchall()
            return render_template("/subscribetable.html",results=results)
##WORKS TABLE
@app.route("/workstable.html",methods = ["GET","POST"])
def works():
    cur=mysql.connection.cursor()
    if request.method == "POST":
        if request.form['submit_button'] == 'add':
            try:
                #GETTING RECORD VALUES FROM HTML INPUTS
                PT_ID=request.form.get("PT_ID")
                GYM_ID=request.form.get("GYM_ID")
                #INSERT VALUES INTO TABLE
                cur.execute("insert into works(pt_id,g_id) values(%s, %s)",(PT_ID,GYM_ID))
                mysql.connection.commit()##SAVE CHANGES PERMANANTLY
                cur.close()
                #RELOAD PAGE USING REDIRECT COMMAND(I TRIED RENDER_TEMPLETE BUT IT DIDNT WORK PROPERLY)
                flash("OPERATION SUCCESFULL!!!","danger")
                return redirect(url_for("works"))# <-- WORKS  IS FUNCTION TO RETURN
            except:
                flash("ERROR@@@","danger")
                return redirect(request.url)
        elif request.form['submit_button'] == 'remove':
            try:
                ID=request.form.get("ID_remove")
                #USING [] INSTEAD OF () SOLVED MY PROBLEM. I COULDNT REMOVE ABOVE 3 DIGIT NUMBER ID
                cur.execute("delete from works where pt_id = %s ",[ID])
                mysql.connection.commit()##SAVE CHANGES PERMANANTLY
                cur.close()
                flash("OPERATION SUCCESFULL!!!","danger")
                return redirect(url_for("works"))
            except:
                flash("ERROR@@@","danger")
                return redirect(request.url)
        elif request.form['submit_button'] == 'submit':
            try:
                code=request.form.get("code")#getting code from input
                #using {} brackets instead of using %s ,solved my type error problem.
                cur.execute("{0}".format(code))
                mysql.connection.commit()##SAVE CHANGES PERMANANTLY
                cur.close()
                flash("OPERATION SUCCESFULL!!!","danger")
                return redirect(url_for("works"))
            except:
                flash("ERROR@@@","danger")
                return redirect(request.url)
        #these are for complex operations
        elif request.form['submit_button'] == 'execute1':
            ## I USED ORDER BY BECAUSE OF THE MESS 
            resultValue=cur.execute("select works.*,personal_trainer.pt_name from works inner join personal_trainer on works.pt_id=personal_trainer.pt_id")
            ##CONTROL IF THERE ARE ANY DATA EXIST 
            if resultValue>0:
                results=cur.fetchall()
                x=1#to add list headline in html
                return render_template("/workstable.html",results=results,x=x)
        elif request.form['submit_button'] == 'execute2':
                cur.execute("select * from works order by g_id asc")
                results=cur.fetchall()
                return render_template("/workstable.html",results=results)
        elif request.form['submit_button'] == 'return':
            return redirect(url_for("showtables"))
    else:
        cur = mysql.connection.cursor()
        resultValue = cur.execute("select * from works")#taking all works info //ordered by id
        ##CONTROL IF THERE ARE ANY DATA EXIST 
        if resultValue>0:
            results=cur.fetchall()
            return render_template("/workstable.html",results=results)


if __name__ =="__main__":
    app.run(debug=True)