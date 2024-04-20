from flask import *
from database import *
public=Blueprint('public',__name__)

@public.route('/')
def home():
 
    return render_template('home.html')
    

@public.route('/login',methods=['GET','POST'])
def login():
    if 'submit' in request.form:
        username=request.form['uname']
        password=request.form['passwd']
        qry="select * from login where Username='%s' and Password='%s'"%(username,password)
        res=select(qry)

        if res:
            session['logid']=res[0]['log_id']

            if res[0]['Type']=='admin':
                return redirect(url_for('admin.home'))
            elif res[0]['Type']=='advocate':
                qy= "select * from advocate where log_id='%s'"%(session['logid']) 
                re=select(qy)
                session['adv_id']=re[0]['adv_id']
                return redirect(url_for('advocate.Advhome'))
            elif res[0]['Type']=='client':
                py="select * from client where log_id='%s'"%(session['logid'])
                pe=select(py)
                session['client_id']=pe[0]['client_id']
                return redirect(url_for('client.clhome'))
        else:
            return """<script>alert('invalid request');window.location='login'</script>"""

    return render_template('login.html')

@public.route('/client',methods=['GET','POST'])
def client():
    if 'submit' in request.form:
        firstname=request.form['fname']
        lastname=request.form['lname']
        gender=request.form['Gender']
        phone=request.form['Phone']
        dob=request.form['Dob']
        email=request.form['mail']
        housename=request.form['house_name']
        place=request.form['Place']
        pincode=request.form['pincode']
        username=request.form['uname']
        password=request.form['passwd']

        qry1="insert into login values(null,'%s','%s','client')"%(username,password)
        res=insert(qry1)

        qry="insert into client values(null,'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"%(res,firstname,lastname,gender,dob,phone,email,housename,place,pincode)
        insert(qry)
    return render_template('client.html')

@public.route('/logout')
def logout():
  
    return redirect(url_for('public.home'))