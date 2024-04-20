from flask import *
from database import *
import uuid
from blk import *


advocate=Blueprint('advocate',__name__)

@advocate.route('/adv_homepage')
def Advhome():
    return render_template('advocatehomepage.html')

@advocate.route('/Managelawdetails',methods=['GET','POST'])
def lawdetails():
    data={}
    qry="select * from law_details"

    data['law']=select(qry)
    if 'submit' in request.form:
        title=request.form['title']
        ipc_code=request.form['ipc_code']
        description=request.form['desc']
        penalty=request.form['penalty']

        qry1="insert into law_details values(null,'%s','%s','%s','%s')"%(title,ipc_code,description,penalty)
        insert(qry1)
        return redirect(url_for('advocate.lawdetails'))
    if 'action' in request.args:
        id=request.args['lid']
        action=request.args['action']
        
    else:
        action='none'
    if action=='delete':
        qry3="delete from law_details where law_id='%s'"%(id)
        delete(qry3)
        return redirect(url_for('advocate.lawdetails'))
    
    if action=='update':
        qry4="select * from law_details where law_id='%s'"%(id)
        res4=select(qry4)
        if res4:
            data['upd']=res4
            if 'update' in request.form:
                title=request.form['title']
                ipc_code=request.form['ipc_code']
                description=request.form['desc']
                penalty=request.form['penalty']


                qry7="update law_details set title='%s',ipc_code='%s',description='%s',penalty='%s' where law_id='%s'"%(title,ipc_code,description,penalty,id)
                update(qry7)
                return '''<script>alert('update successful');window.location="/Managelawdetails"</script>'''
    
    return render_template('adv_lawdetails.html',data=data)

@advocate.route('/adv_viewclient',methods=['GET','POST'])
def adv_viewclient():
    data={}
    qry="select * from client"
    
    data['view']=select (qry)
    return render_template('adv_viewclient.html',data=data)

@advocate.route('/adv_viewfeedback',methods=['GET','POST'])
def adv_viewfeedback():
    data={}
    qry="select * from feedback inner join client using (client_id)"
    
    data['viewfeedback']=select (qry)
    return render_template('adv_viewfeedback.html',data=data)



@advocate.route('/viewassignedcase',methods=['GET','POST'])
def asscase():
    data={}
    qry="SELECT * FROM caseallocation INNER JOIN caseentry USING(case_id) WHERE adv_id='%s'"%(session['adv_id'])
    data['assigncase']=select(qry)
    return render_template('adv_viewassignedcase.html',data=data)


@advocate.route('/addcasenotes',methods=['GET','POST'])
def casenote():
    id=request.args['id']

    if 'submit' in request.form:
        description=request.form['desc']

        qry="insert into notes values(null,'%s','%s',curdate(),'%s')"%(id,session['adv_id'],description)
        insert(qry)
        return '''<script>alert('ADD successful');window.location="/viewassignedcase"</script>'''


    return render_template('adv_casenotes.html')




# @advocate.route('/uploadcasefiles',methods=['GET','POST'])
# def upcasefiles():
#     case_id=request.args['aid']

#     if 'upload' in request.form:
#        title =request.form['file']
#        f=request.files['file_path']
#        path="static/"+str(uuid.uuid4())+f.filename
#        f.save(path)
      

#     #    qry="insert into files values(null,'%s','%s','%s')"%(title,id,path) 
#     #    insert(qry)

#        return '''<script>alert('ADD successful');window.location="/viewassignedcase"</script>'''

#     return render_template('/adv_uploadcasefiles.html',id=id)




@advocate.route('/uploadcasefiles',methods=['GET','POST'])
def upcasefiles():
    case_id=request.args['aid']

    if 'upload' in request.form:
        title=request.form['file']
        f = request.files['file_path']
        path="static/" + str(uuid.uuid4())+ f.filename
        f.save(path)
        with open(compiled_contract_path) as file:
            contract_json = json.load(file)  # load contract info as JSON
            contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions
        contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)
        id=web3.eth.get_block_number()
        message = contract.functions.add_files_uploads(int(id),int(case_id),title,path).transact()
        print(message)
        # qry="insert into files values(null,'%s','%s','%s')"%(title,id,path)
        # insert(qry)
        return '''<script>alert('ADD successful');window.location="/viewassignedcase"</script>'''

    return render_template('/adv_uploadcasefiles.html',id=case_id)




# @advocate.route('/viewfiles',methods=['GET','POST'])
# def viewfiles():
#     id=request.args['id']
#     data={}
#     qry="select * from files where case_id='%s'"%(id)
#     data['view']=select(qry)
       
#     return render_template('adv_viewcasefiles.html',data=data)



@advocate.route('/viewfiles',methods=['GET','POST'])
def viewfiles():
    case_id = request.args['id']
    # if not session.get('lid') is None:
    data = {}
    with open(compiled_contract_path) as file:
        contract_json = json.load(file)  # load contract info as JSON
        contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions
    contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)
    blocknumber = web3.eth.get_block_number()
    res = []
    try:
        for i in range(blocknumber, 0, -1):
            a = web3.eth.get_transaction_by_block(i, 0)
            decoded_input = contract.decode_function_input(a['input'])
            print(decoded_input, "///////////////////")
            if str(decoded_input[0]) == "<Function add_files_uploads(uint256,uint256,string,string)>":
                if int(decoded_input[1]['case_id']) == int(case_id):
                    res.append(decoded_input[1])
    except Exception as e:
        print("", e)
    data['med'] = res
    return render_template("adv_viewcasefiles.html",data=data)




@advocate.route('/viewmessage',methods=['GET','POST'])
def viewmsg():
    data={}
    qry="select * from message where adv_id='%s'"%(session['adv_id'])
    data['viewmsg']=select(qry)

    return render_template('/adv_viewmessage.html',data=data)


@advocate.route("/sendreply",methods=['GET','POST'])
def sendreply():
    id=request.args['id']

    if 'SEND' in request.form:
        reply=request.form['rep']

        qry="update message set Reply='%s' where message_id='%s'"%(reply,id)
        update(qry)
        return '''<script>alert('SEND successful');window.location="/viewmessage"</script>'''
    return render_template("adv_sendreply.html")