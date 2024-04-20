from flask import *
from database import *
client=Blueprint('client',__name__)

@client.route('/cl_homepage')
def clhome():
    return render_template('clienthomepage.html')

@client.route('/Viewlawdetails',methods=['GET','POST'])
def viewlaw():
    data={}
    qry="select * from law_details"

    data['viewlaw']=select(qry)

    return render_template('cl_viewlawdetails.html',data=data)

@client.route("/makecomplaint",methods=['GET','POST'])
def mkcom():
    data={}
    qry="select * from complaint"
    data['viewcomp']=select(qry)

    if 'send' in request.form:
        desc=request.form['desc']

        qry="insert into complaint values(null,'%s','%s','pending',now())"%(session['client_id'],desc)
        insert(qry)
        return '''<script>alert('ADD successful');window.location="/makecomplaint"</script>'''
    return render_template("cl_makecomplaint.html",data=data)

@client.route('/viewadvocate',methods=['GET','POST'])
def aadv():
    data={}
    qry="select * from advocate"
    
    data['viewadv']=select (qry)
    return render_template('cl_viewadvocatedetails.html',data=data)

@client.route('/viewcasedetails',methods=['GET','POST'])
def viewcdet():
    data={}
    
    qry="SELECT * FROM casetype INNER JOIN caseentry USING(type_id) WHERE client_id='%s'"%(session['client_id'])
    data['viewcasedet']=select(qry)

    return render_template('cl_viewcasedetails.html',data=data)

@client.route('/caseentry',methods=['GET','POST'])
def caseent():
    data={}
    qry="select * from caseentry where client_id='%s'"%((session['client_id']))
    qry2="select * from client"
    qry3="select * from casetype"   

    data['casetypee']=select(qry3)
    data['cliente']=select(qry2)
    data['casee']=select(qry)

    if 'submit' in request.form:
        type=request.form['Type']
        title=request.form['title']
        Description=request.form['Des']
        casedate=request.form['case_date']
        policestation=request.form['police_station']
        casefeeamount=request.form['case_fee_amount']
        pincode=request.form['pincode']
        phone=request.form['phone']

        qry5="insert into caseentry values(null,'%s','%s','%s','%s','%s','%s','%s','%s','%s','status')"%(type,title,Description,casedate,policestation,casefeeamount,pincode,phone,(session['client_id']))
        insert(qry5)
        return '''<script>alert('ADD successful');window.location="/caseentry"</script>'''


    return render_template('cl_caseentry.html',data=data)

@client.route('/sendfeedback',methods=['GET','POST'])
def feedback():
    data={}
    qry="select * from feedback"

    data['sndfeed']=select(qry)
    if 'submit' in request.form:
        description=request.form['desc']

        qry1="insert into feedback values(null,'%s','%s',now())"%(session['client_id'],description)
        res=insert(qry1)


    return render_template('/cl_feedback.html',data=data)

@client.route('/sendmessage',methods=['GET','POST'])
def message():
    data={}
    qry="select * from message where client_id='%s'"%(session['client_id'])
    qry="select * from advocate"
    data['viewmsg']=select(qry)
    data['advocate']=select(qry)
    if 'submit' in request.form:
        advocate=request.form['advocate']
        description=request.form['msg_desc']
        # reply=request.form['reply']

        qry1="insert into message values(null,'%s','%s','reply','%s',now())"%(session['client_id'],description,advocate)
        insert(qry1)
    


    return render_template('/cl_sendmessage.html',data=data)

@client.route('/viewreplay',methods=['GET','POST'])
def viewrply():
    data={}
    qry="select * from message where client_id='%s'"%(session['client_id'])
    data['viewrply']=select(qry)

    return render_template('/cl_viewreply.html',data=data)


@client.route('/makepayment',methods=['GET','POST'])
def makepayment():
    id=request.args['id']
    amt=request.args['amt']
    if 'pay' in request.form:
        qry="insert payment values(null,'%s','%s','%s',now())"%(session['client_id'],id,amt)
        insert(qry)
    return render_template('makepayment.html')