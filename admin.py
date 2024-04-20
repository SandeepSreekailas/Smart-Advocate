from flask import *
from database import *
admin=Blueprint('admin',__name__)


@admin.route('/ad_homepage')
def home():
    return render_template('adminhomepage.html')

    

@admin.route('/ad_Manageadvocate',methods=['Get','POST'])
def Manageadvocate():
    data={}
    qry="select * from advocate"

    data['use']=select(qry)
    if 'submit' in request.form:
        firstname=request.form['fname']
        lastname=request.form['lname']
        qualification=request.form['quali']
        gender=request.form['Gender']
        phone=request.form['Phone']
        email=request.form['mail']
        housename=request.form['house_name']
        place=request.form['Place']
        username=request.form['uname']
        password=request.form['passwd']

        qry1="insert into login values(null,'%s','%s','advocate')"%(username,password)
        res=insert(qry1)

        qry="insert into advocate values(null,'%s','%s','%s','%s','%s','%s','%s','%s','%s')"%(res,firstname,lastname,qualification,gender,phone,email,housename,place)
        insert(qry)
        return redirect(url_for('admin.Manageadvocate'))
    if 'action' in request.args:
        id=request.args['rid']
        action=request.args['action']
            
    else:
        action='none'
    if action=='delete':
        qry3="delete from advocate where adv_id='%s'"%(id)
        delete(qry3)
        return redirect(url_for('admin.Manageadvocate'))
        
    if action=='update':
        qry4="select * from advocate where adv_id='%s'"%(id)
        res4=select(qry4)
        if res4:
            data['up']=res4
            if 'update' in request.form:
                firstname=request.form['fname']
                lastname=request.form['lname']
                qualification=request.form['quali']
                gender=request.form['Gender']
                phone=request.form['Phone']
                email=request.form['mail']
                housename=request.form['house_name']
                place=request.form['Place']

                qry4="update advocate set first_name='%s',last_name='%s',Qualification='%s',Gender='%s',Phone='%s',Email='%s',house_name='%s',place='%s' where adv_id='%s'"%(firstname,lastname,qualification,gender,phone,email,housename,place,id)
                update(qry4)
                return '''<script>alert('update successful');window.location="/ad_Manageadvocate"</script>'''

        
        
    return render_template('ad_manageadvocate.html',data=data)

# @admin.route('/update_form',methods=['GET','POST'])
# def updateform():
#     id=request.args['rid']
#     data={}
#     qry="select * from advocate where adv_id='%s'"%(id)

#     data['up']=select(qry)
#     if 'submit' in request.form:
#         firstname=request.form['fname']
#         lastname=request.form['lname']
#         qualification=request.form['quali']
#         gender=request.form['Gender']
#         phone=request.form['Phone']
#         email=request.form['mail']
#         housename=request.form['house_name']
#         place=request.form['Place']

#         qry4="update advocate set first_name='%s',last_name='%s',Qualification='%s',Gender='%s',Phone='%s',Email='%s',house_name='%s',place='%s' where adv_id='%s'"%(firstname,lastname,qualification,gender,phone,email,housename,place,id)
#         update(qry4)
#         return '''<script>alert('update successful');window.location="/ad_Manageadvocate"</script>'''
    
#     return render_template('update_form.html',data=data)
@admin.route('/viewclient',methods=['GET','POST'])
def client():
    data={}
    qry="select * from client"
    
    data['view']=select (qry)
    return render_template('ad_viewclient.html',data=data)

@admin.route('/ad_Managecasetype',methods=['GET','POST'])
def casetype():
    data={}
    qry="select * from casetype"

    data['case']=select(qry)
    if 'submit' in request.form:
        typename=request.form['type_name']
        Description=request.form['Desc']

        qry1="insert into casetype values(null,'%s','%s')"%(typename,Description)
        insert(qry1)
        return redirect(url_for('admin.casetype'))
    if 'action' in request.args:
        id=request.args['tid']
        action=request.args['action']
        
    else:
        action='none'
    if action=='delete':
        qry3="delete from casetype where type_id='%s'"%(id)
        delete(qry3)
        return redirect(url_for('admin.casetype'))
    
    if action=='update':
        qry4="select * from casetype where type_id='%s'"%(id)
        res4=select(qry4)
        if res4:
            data['upd']=res4
            if 'update' in request.form:
                typename=request.form['type_name']
                Description=request.form['Desc']


                qry4="update casetype set type_name='%s',Description='%s' where type_id='%s'"%(typename,Description,id)
                update(qry4)
                return '''<script>alert('update successful');window.location="/ad_Managecasetype"</script>'''

    
    
    return render_template('ad_managecasetype.html',data=data)

@admin.route('/viewcomplaints',methods=['GET','POST'])
def complaints():
    data={}
    qry="select * from complaint"
    
    data['viewcomplaint']=select (qry)
    return render_template('ad_viewcomplaints.html',data=data)

@admin.route('/sendreplyy',methods=['GET','POST'])
def sndreply():
    id=request.args['id']

    if 'SENDD' in request.form:
        reply=request.form['rep']

        qry="update complaint set Reply='%s' where complaint_id='%s'"%(reply,id)
        update(qry)
        return '''<script>alert('Sent Successful');window.location='/viewcomplaints'</script>'''
    return render_template("ad_sendreply.html")

@admin.route('/ad_Managecases',methods=['GET','POST'])
def cases():
    data={}
    qry="select * from caseentry"
    qry2="select * from client"
    qry3="select * from casetype"

    data['casetype']=select(qry3)
    data['client']=select(qry2)
    data['case']=select(qry)
    if 'submit' in request.form:
        type=request.form['Type']
        title=request.form['title']
        Description=request.form['Des']
        casedate=request.form['case_date']
        policestation=request.form['police_station']
        casefeeamount=request.form['case_fee_amount']
        pincode=request.form['pincode']
        client=request.form['client']
        phone=request.form['phone']

        qry5="insert into caseentry values(null,'%s','%s','%s','%s','%s','%s','%s','%s','%s','status')"%(type,title,Description,casedate,policestation,casefeeamount,pincode,phone,client)
        insert(qry5)
        return redirect(url_for('admin.cases'))
    
    if 'action' in request.args:
        id=request.args['cid']
        action=request.args['action']
        
    else:
        action='none'
    if action=='delete':
        qry6="delete from caseentry where case_id='%s'"%(id)
        delete(qry6)
        return redirect(url_for('admin.cases'))
    
    if action=='update':
        qry4="select * from caseentry where case_id='%s'"%(id)
        res4=select(qry4)
        if res4:
            data['cid']=res4
            if 'update' in request.form:
                title=request.form['title']
                Description=request.form['Des']
                casedate=request.form['case_date']
                policestation=request.form['police_station']
                casefeeamount=request.form['case_fee_amount']
                pincode=request.form['pincode']
                phone=request.form['phone']
                

                qry7="update caseentry set Title='%s',Description='%s',case_date='%s',police_station='%s',case_fee_amount='%s',Pincode='%s',Phone='%s'  where case_id='%s'"%(title,Description,casedate,policestation,casefeeamount,pincode,phone,id)
                update(qry7)
                return '''<script>alert('update successful');window.location="/ad_Managecases"</script>'''
    


    return render_template('ad_managecases.html',data=data)

@admin.route('/viewfeedback',methods=['GET','POST'])
def feedback():
    data={}
    qry="select * from feedback inner join client using (client_id)"
    
    data['viewfeedback']=select (qry)
    return render_template('ad_viewfeedback.html',data=data)

@admin.route('/viewpayment',methods=['GET','POST'])
def payment():
    data={}
    qry="select * from payment "
    
    data['viewpayment']=select (qry)
    return render_template('ad_viewpayment.html',data=data)

@admin.route('/Assigncasetoadvocate',methods=['GET','POST'])
def assign():
    data={}
    qry="select * from caseentry"
    data['case']=select(qry)
    print(data['case'])
     
    return render_template('ad_assigncasetoadvocate.html',data=data)


@admin.route('/advocateccase',methods=['GET','POST'])
def adcase():
    data={}
    id=request.args['pid']
    qry2="select * from caseentry where case_id='%s'"%(id)
    res2=select(qry2)
    if res2:
        data['view']=res2


    qry="select * from advocate"
    data['adv']=select(qry)
    if 'submit' in request.form:
        advocate=request.form['Advocate']
        qry1="insert into caseallocation values(null,'%s','%s','datetime','status')"%(advocate,id)
        insert(qry1)
        return '''<script>alert('update successful');window.location="/Assigncasetoadvocate"</script>'''
 
    return render_template('assigncase.html',data=data)
