# This is a sample Python script.
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import os
#from app import app
import urllib.request
from datetime import date
from flask import Flask, flash, request, redirect, url_for, render_template
from flask import Flask, render_template, redirect, request, session
from flask import Flask, render_template
import firebase_admin
import random
from firebase_admin import credentials
import os
from flask import Flask, request, jsonify
from firebase_admin import credentials, firestore, initialize_app
cred = credentials.Certificate("privatekey.json")
firebase_admin.initialize_app(cred)
UPLOAD_FOLDER = 'static/uploads/'
app = Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
from werkzeug.utils import secure_filename
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

@app.route('/')
def homepage():
    try:
        return render_template("index.html")
    except Exception as e:
        return str(e)

@app.route('/staffforgotpassword')
def staffforgotpassword():
    try:
        return render_template("staffforgotpassword.html")
    except Exception as e:
        return str(e)

@app.route('/staffenterotppage')
def staffenterotppage():
    try:
        return render_template("staffenterotppage.html")
    except Exception as e:
        return str(e)

@app.route('/staffchecking', methods=['POST'])
def staffchecking():
    try:
        if request.method == 'POST':
            uname = request.form['uname']
            email = request.form['email']
        print("Uname : ", uname, " Email : ", email);
        db = firestore.client()
        dbref = db.collection('newstaff')
        userdata = dbref.get()
        data = []
        for doc in userdata:
            print(doc.to_dict())
            print(f'{doc.id} => {doc.to_dict()}')
            data.append(doc.to_dict())
        flag = False
        for temp in data:
            if uname == temp['UserName'] and email == temp['EmailId']:
                session['username'] = uname
                session['emailid'] = email
                session['userid'] = temp['id']
                flag = True
                break
        if (flag):
            otp = random.randint(1000, 9999)
            print("OTP : ", otp)
            session['toemail'] = email
            session['uname'] = uname
            session['otp'] = otp
            print("User Id : ", session['userid'])
            return render_template("staffgenerateotp.html", uname=uname, toemail=email, otp=otp,
                                                        redirecturl= 'http://127.0.0.1:5000/staffenterotppage')
        else:
            return render_template("staffforgotpassword.html", msg="UserName/EmailId is Invalid")
    except Exception as e:
        return str(e)

@app.route('/staffcheckotppage', methods=['POST'])
def staffcheckotppage():
    if request.method == 'POST':
        storedotp=session['otp']
        enteredotp = request.form['otp']
        print("Entered OTP : ", enteredotp, " Stored OTP : ", storedotp)
        if(int(storedotp)==int(enteredotp)):
            return render_template("staffpasswordchangepage.html", msg="You can update your password")
        else:
            return render_template("staffenterotppage.html", msg="Incorrect OTP")
    return render_template("staffenterotppage.html", msg="Incorrect OTP")

@app.route('/staffpasswordchangepage', methods=['POST'])
def staffpasswordchangepage():
    print("Password Change Page")
    if request.method == 'POST':
        uname = request.form['uname']
        pwd = request.form['pwd']

        db = firestore.client()
        newstaff_ref = db.collection('newstaff')
        staffdata = newstaff_ref.get()
        data = []
        for doc in staffdata:
            print(doc.to_dict())
            print(f'{doc.id} => {doc.to_dict()}')
            data.append(doc.to_dict())
        id=""
        for doc in data:
            print("Document : ", doc)
            if(doc['UserName']==uname):
                id=doc['id']
        db = firestore.client()
        data_ref = db.collection(u'newstaff').document(id)
        data_ref.update({u'Password': pwd})
        print("Password Updated Success")
        return render_template("stafflogin.html", msg="Password Updated Success")
    return render_template("stafflogin.html", msg="Password Not Updated")

@app.route('/index')
def indexpage():
    try:
        return render_template("index.html")
    except Exception as e:
        return str(e)

@app.route('/hospitallogin')
def hospitallogin():
    try:
        msg=""
        return render_template("hospitallogin.html", msg="")
    except Exception as e:
        return str(e)

@app.route('/logout')
def logoutpage():
    try:
        return render_template("index.html")
    except Exception as e:
        return str(e)

@app.route('/about')
def aboutpage():
    try:
        return render_template("about.html")
    except Exception as e:
        return str(e)

@app.route('/hospitalsearchprescription')
def hospitalsearchprescription():
    try:
        return render_template("hospitalsearchprescription.html")
    except Exception as e:
        return str(e)

@app.route('/services')
def servicespage():
    try:
        return render_template("services.html")
    except Exception as e:
        return str(e)

@app.route('/gallery')
def gallerypage():
    try:
        return render_template("gallery.html")
    except Exception as e:
        return str(e)

@app.route('/adminlogin')
def adminloginpage():
    try:
        return render_template("adminlogin.html",msg="")
    except Exception as e:
        return str(e)

@app.route('/userlogin')
def userloginpage():
    try:
        return render_template("userlogin.html")
    except Exception as e:
        return str(e)

@app.route('/stafflogin')
def staffloginpage():
    try:
        return render_template("stafflogin.html")
    except Exception as e:
        return str(e)

@app.route('/staffviewprofile')
def staffviewprofile():
    try:
        id = session['userid']
        db = firestore.client()
        dbref = db.collection('newstaff')
        userdata = dbref.get()
        data={}
        for doc in userdata:
            temp = doc.to_dict()
            if(id==temp['id']):
                data = {'id':temp['id'],
                    'FirstName':temp['FirstName'],
                    'LastName':temp['LastName'],
                    'EmailId':temp['EmailId'],
                    'PhoneNumber':temp['PhoneNumber'],
                    'Specialization': temp['Specialization'],
                    'Qualification': temp['Qualification']}
                break
        print("User Data ", data)
        return render_template("staffviewprofile.html", data=data)
    except Exception as e:
        return str(e)

@app.route('/hospitalviewprofile')
def hospitalviewprofile():
    try:
        id=session['userid']
        db = firestore.client()
        dbref = db.collection('newhospital')
        userdata = dbref.get()
        data={}
        for doc in userdata:
            temp = doc.to_dict()
            if(id==temp['id']):
                data = {'HospitalId':temp['id'],
                    'HospitalName':temp['HospitalName'],
                    'EmailId':temp['EmailId'],
                    'PhoneNumber': temp['PhoneNumber'],
                    'Address':temp['Address']}
                break
        print("User Data ", data)
        return render_template("hospitalviewprofile.html", data=data)
    except Exception as e:
        return str(e)

@app.route('/userviewprofile')
def userviewprofile():
    try:
        id=session['userid']
        db = firestore.client()
        dbref = db.collection('newuser')
        userdata = dbref.get()
        data={}
        for doc in userdata:
            temp = doc.to_dict()
            if(id==temp['id']):
                data = {'id':temp['id'],
                    'FirstName':temp['FirstName'],
                    'LastName':temp['LastName'],
                    'EmailId':temp['EmailId'],
                    'FileName':temp['FileName'],
                    'PhoneNumber':temp['PhoneNumber'],
                    'AadharNumber':temp['AadharNumber']}
                break
        print("User Data ", data)
        return render_template("userviewprofile.html", data=data)
    except Exception as e:
        return str(e)

@app.route('/newuser')
def newuser():
    try:
        msg=""
        return render_template("newuser.html", msg=msg)
    except Exception as e:
        return str(e)

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/addnewuser', methods=['POST'])
def addnewuser():
    try:
        print("Add New User page")
        if request.method == 'POST':
            if 'file' not in request.files:
                flash('No file part')
                return redirect(request.url)
            file = request.files['file']
            if file.filename == '':
                flash('No image selected for uploading')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                id = str(random.randint(1000, 9999))
                filename="Img"+str(id)+".jpg"
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                # print('upload_image filename: ' + filename)
                fname = request.form['fname']
                lname = request.form['lname']
                uname = request.form['uname']
                pwd = request.form['pwd']
                email = request.form['emailid']
                phnum = request.form['phonenumber']
                address = request.form['address']
                aadharnumber = request.form['aadhar']
                json = {'id': id,
                        'FirstName': fname, 'LastName': lname,
                        'UserName': uname, 'Password': pwd,
                        'EmailId': email, 'PhoneNumber': phnum,
                        'Address': address, 'AadharNumber': aadharnumber,'FileName': filename}
                db = firestore.client()
                newuser_ref = db.collection('newuser')
                id = json['id']
                newuser_ref.document(id).set(json)
                flash('Image successfully uploaded and displayed below')
                print("User Inserted Success")
                return render_template("newuser.html", msg="New User Added Success")
                #return render_template('upload.html', filename=filename)
            else:
                flash('Allowed image types are -> png, jpg, jpeg, gif')
                return redirect(request.url)
            """
            fname = request.form['fname']
            lname = request.form['lname']
            uname = request.form['uname']
            pwd = request.form['pwd']
            email = request.form['emailid']
            phnum = request.form['phonenumber']
            address = request.form['address']
            id = str(random.randint(1000, 9999))
            json = {'id': id,
                    'FirstName': fname,'LastName':lname,
                    'UserName': uname,'Password':pwd,
                    'EmailId': email,'PhoneNumber':phnum,
                    'Address': address, 'filename':filename}
            db = firestore.client()
            newuser_ref = db.collection('newuser')
            id = json['id']
            newuser_ref.document(id).set(json)
        return render_template("newuser.html", msg="New User Added Success")
    """
    except Exception as e:
        return str(e)

@app.route('/addnewstaff', methods=['POST'])
def addnewstaff():
    try:
        print("Add New Staff page")
        if request.method == 'POST':
            fname = request.form['fname']
            lname = request.form['lname']
            uname = request.form['uname']
            pwd = request.form['pwd']
            email = request.form['email']
            phnum = request.form['phonenumber']
            address = request.form['address']
            hospitalname = request.form['hospitalname']
            specialization = request.form['specialization']
            qualification = request.form['qualification']
            id = str(random.randint(1000, 9999))
            json = {'id': id,
                    'FirstName': fname,'LastName':lname,
                    'UserName': uname,'Password':pwd,
                    'EmailId': email,'PhoneNumber':phnum,
                    'Address': address,'HospitalId':hospitalname,
                    'Qualification':qualification,'Specialization':specialization}
            db = firestore.client()
            newuser_ref = db.collection('newstaff')
            id = json['id']
            newuser_ref.document(id).set(json)
            db = firestore.client()
            newstaff_ref = db.collection('newhospital')
            staffdata = newstaff_ref.get()
            data = []
            for doc in staffdata:
                print(doc.to_dict())
                print(f'{doc.id} => {doc.to_dict()}')
                data.append(doc.to_dict())
        return render_template("adminaddstaff.html", msg="New Staff Added Success",data=data)
    except Exception as e:
        return str(e)

@app.route('/adminaddhospital', methods=['POST'])
def adminaddhospital():
    try:
        print("Add New Hospital page")
        if request.method == 'POST':
            hname = request.form['hname']
            uname = request.form['uname']
            pwd = request.form['pwd']
            email = request.form['email']
            phnum = request.form['phonenumber']
            address = request.form['address']
            id = str(random.randint(1000, 9999))
            json = {'id': id,
                    'HospitalName': hname,
                    'UserName': uname,'Password':pwd,
                    'EmailId': email,'PhoneNumber':phnum,
                    'Address': address}
            db = firestore.client()
            newuser_ref = db.collection('newhospital')
            id = json['id']
            newuser_ref.document(id).set(json)
        return render_template("adminaddhospital.html", msg="New Hospital Added Success")
    except Exception as e:
        return str(e)

@app.route('/contact')
def contactpage():
    try:
        return render_template("contact.html")
    except Exception as e:
        return str(e)

@app.route('/addnewhospital')
def addnewhospital():
    try:
        return render_template("adminaddhospital.html")
    except Exception as e:
        return str(e)

@app.route('/adminlogincheck', methods=['POST'])
def adminlogincheck():
    if request.method == 'POST':
        uname = request.form['uname']
        pwd = request.form['pwd']
    print("Uname : ", uname, " Pwd : ", pwd);
    if uname == "admin" and pwd == "admin":
        return render_template("adminmainpage.html")
    else:
        return render_template("adminlogin.html", msg="UserName/Password is Invalid")

@app.route('/hospitallogincheck', methods=['POST'])
def hospitallogincheck():
    if request.method == 'POST':
        uname = request.form['uname']
        pwd = request.form['pwd']
    print("Uname : ", uname, " Pwd : ", pwd);
    db = firestore.client()
    dbref = db.collection('newhospital')
    userdata = dbref.get()
    data = []
    for doc in userdata:
        print(doc.to_dict())
        print(f'{doc.id} => {doc.to_dict()}')
        data.append(doc.to_dict())
    flag=False
    for temp in data:
        if uname == temp['UserName'] and pwd == temp['Password']:
            session['userid'] = temp['id']
            flag=True
            break
    if(flag):
        return render_template("hospitalmainpage.html")
    else:
        return render_template("hospitallogin.html", msg="UserName/Password is Invalid")

@app.route('/userlogincheck', methods=['POST'])
def userlogincheck():
    if request.method == 'POST':
        uname = request.form['uname']
        pwd = request.form['pwd']
    print("Uname : ", uname, " Pwd : ", pwd);
    db = firestore.client()
    dbref = db.collection('newuser')
    userdata = dbref.get()
    data = []
    for doc in userdata:
        print(doc.to_dict())
        print(f'{doc.id} => {doc.to_dict()}')
        data.append(doc.to_dict())
    flag=False
    for temp in data:
        if uname == temp['UserName'] and pwd == temp['Password']:
            session['userid'] = temp['id']
            flag=True
            break
    if(flag):
        return render_template("usermainpage.html")
    else:
        return render_template("userlogin.html", msg="UserName/Password is Invalid")

@app.route('/stafflogincheck', methods=['POST'])
def stafflogincheck():
    if request.method == 'POST':
        uname = request.form['uname']
        pwd = request.form['pwd']
    print("Uname : ", uname, " Pwd : ", pwd);
    db = firestore.client()
    dbref = db.collection('newstaff')
    userdata = dbref.get()
    data = []
    for doc in userdata:
        print(doc.to_dict())
        print(f'{doc.id} => {doc.to_dict()}')
        data.append(doc.to_dict())
    flag=False
    for temp in data:
        if uname == temp['UserName'] and pwd == temp['Password']:
            session['userid'] = temp['id']
            flag=True
            break
    if(flag):
        return render_template("staffmainpage.html")
    else:
        return render_template("stafflogin.html", msg="UserName/Password is Invalid")

@app.route('/adminmainpage')
def adminmainpage():
    try:
        return render_template("adminmainpage.html")
    except Exception as e:
        return str(e)

@app.route('/adminaddstaff')
def adminaddstaffpage():
    try:
        db = firestore.client()
        newstaff_ref = db.collection('newhospital')
        staffdata = newstaff_ref.get()
        data = []
        for doc in staffdata:
            print(doc.to_dict())
            print(f'{doc.id} => {doc.to_dict()}')
            data.append(doc.to_dict())
        print("Hospital Data ", data)
        return render_template("adminaddstaff.html", data=data)
    except Exception as e:
        return str(e)

@app.route('/staffaccept_rejectappointment')
def staffaccept_rejectappointment():
    try:
        args = request.args
        id = args['id']
        status = args['status']
        db = firestore.client()
        data_ref = db.collection(u'newappointment').document(id)
        data_ref.update({u'AppointmentStatus': status})
        id = session['userid']
        db = firestore.client()
        newdata_ref = db.collection('newappointment')
        newdata = newdata_ref.get()
        tempdata = []
        for doc in newdata:
            # print(doc.to_dict())
            # print(f'{doc.id} => {doc.to_dict()}')
            tempdata.append(doc.to_dict())
        print("Appointment Data ", tempdata)
        data = []
        for doc in tempdata:
            if (id == doc['StaffId'] and doc['AppointmentStatus'] == 'Applied'):
                data.append(doc)
        return render_template("staffcheckappointments.html", data=data)

    except Exception as e:
        return str(e)

@app.route('/staffcheckappointments')
def staffcheckappointments():
    try:
        id=session['userid']
        db = firestore.client()
        newdata_ref = db.collection('newappointment')
        newdata = newdata_ref.get()
        tempdata=[]
        for doc in newdata:
            #print(doc.to_dict())
            #print(f'{doc.id} => {doc.to_dict()}')
            tempdata.append(doc.to_dict())
        print("Appointment Data " , tempdata)
        data=[]
        for doc in tempdata:
            if(id==doc['StaffId'] and doc['AppointmentStatus']=='Applied'):
                data.append(doc)
        return render_template("staffcheckappointments.html", data=data)
    except Exception as e:
        return str(e)

@app.route('/hospitalsearchprescriptionpage_patientid', methods=['POST'])
def hospitalsearchprescriptionpage_patientid():
    try:
        patientid = request.form['patientid']
        db = firestore.client()
        newdata_ref = db.collection('newprescription')
        newdata = newdata_ref.get()
        tempdata = []
        for doc in newdata:
            # print(doc.to_dict())
            # print(f'{doc.id} => {doc.to_dict()}')
            tempdata.append(doc.to_dict())
        print("Appointment Data ", tempdata)
        data = []
        for doc in tempdata:
            if (patientid == doc['PatientId']):
                data.append(doc)
        return render_template("hospitalsearchprescription1.html", data=data)
    except Exception as e:
        return str(e)


@app.route('/hospitalsearchprescriptionpage_aadharnum', methods=['POST'])
def hospitalsearchprescriptionpage_aadharnum():
    try:
        aadharnum = request.form['aadharnum']

        db = firestore.client()
        dbref = db.collection('newuser')
        userdata = dbref.get()
        tempdata = []
        for doc in userdata:
            print(doc.to_dict())
            print(f'{doc.id} => {doc.to_dict()}')
            tempdata.append(doc.to_dict())

        patientid = ""
        for doc in tempdata:
            if(doc['AadharNumber']==aadharnum):
                patientid=doc['id']
                break

        db = firestore.client()
        newdata_ref = db.collection('newprescription')
        newdata = newdata_ref.get()
        tempdata = []
        for doc in newdata:
            # print(doc.to_dict())
            # print(f'{doc.id} => {doc.to_dict()}')
            tempdata.append(doc.to_dict())
        print("Appointment Data ", tempdata)
        data = []
        for doc in tempdata:
            if (patientid == doc['PatientId']):
                data.append(doc)
        return render_template("hospitalsearchprescription1.html", data=data)
    except Exception as e:
        return str(e)


@app.route('/staffviewprescriptions')
def staffviewprescriptions():
    try:
        id=session['userid']
        db = firestore.client()
        newdata_ref = db.collection('newprescription')
        newdata = newdata_ref.get()
        tempdata=[]
        for doc in newdata:
            #print(doc.to_dict())
            #print(f'{doc.id} => {doc.to_dict()}')
            tempdata.append(doc.to_dict())
        print("Appointment Data " , tempdata)
        data=[]
        for doc in tempdata:
            if(id==doc['StaffId']):
                data.append(doc)
        return render_template("staffviewprescriptions.html", data=data)
    except Exception as e:
        return str(e)

@app.route('/hospitalviewprescriptions')
def hospitalviewprescriptions():
    try:
        id=session['userid']
        db = firestore.client()
        newdata_ref = db.collection('newprescription')
        newdata = newdata_ref.get()
        tempdata=[]
        for doc in newdata:
            #print(doc.to_dict())
            #print(f'{doc.id} => {doc.to_dict()}')
            tempdata.append(doc.to_dict())
        print("Appointment Data " , tempdata)
        data=[]
        for doc in tempdata:
            if(id==doc['HospitalId']):
                data.append(doc)
        return render_template("hospitalviewprescriptions.html", data=data)
    except Exception as e:
        return str(e)

@app.route('/adminviewprescriptions')
def adminviewprescriptions():
    try:
        id=session['userid']
        db = firestore.client()
        newdata_ref = db.collection('newprescription')
        newdata = newdata_ref.get()
        tempdata=[]
        for doc in newdata:
            #print(doc.to_dict())
            #print(f'{doc.id} => {doc.to_dict()}')
            tempdata.append(doc.to_dict())
        print("Appointment Data " , tempdata)
        data=[]
        for doc in tempdata:
            if(id==doc['HospitalId']):
                data.append(doc)
        return render_template("adminviewprescriptions.html", data=data)
    except Exception as e:
        return str(e)

@app.route('/hospitalviewfulldetails')
def hospitalviewfulldetails():
    try:
        args = request.args
        id = args['id']
        db = firestore.client()
        newdata_ref = db.collection('newprescription')
        newdata = newdata_ref.get()
        tempdata=[]
        for doc in newdata:
            #print(doc.to_dict())
            #print(f'{doc.id} => {doc.to_dict()}')
            tempdata.append(doc.to_dict())
        print("Appointment Data " , tempdata)
        data={}
        for temp in tempdata:
            if(id==temp['id']):
                data = {'StaffId': temp['StaffId'],
                             'StaffFirstName': temp['StaffFirstName'],
                             'StaffLastName': temp['StaffLastName'],
                             'StaffEmailId': temp['StaffEmailId'],
                             'StaffPhoneNumber': temp['StaffPhoneNumber'],
                             'Specialization': temp['Specialization'], 'StaffAddress': temp['StaffAddress'],
                             'Qualification': temp['Qualification'], 'HospitalId': temp['HospitalId'],
                             'PatientId': temp['PatientId'],
                             'PatientFirstName': temp['PatientFirstName'],
                             'PatientLastName': temp['PatientLastName'],
                             'PatientEmailId': temp['PatientEmailId'],
                             'PatientPhoneNumber': temp['PatientPhoneNumber'],
                             'Dialysis': temp['Dialysis'], 'AppointmentDate': temp['AppointmentDate'],
                             'PatientAddress': temp['PatientAddress'],
                             'AppointmentTime': temp['AppointmentTime'],
                             'Prescription1':temp['Prescription1'],'Prescription2':temp['Prescription2'],
                        'Prescription3': temp['Prescription3'], 'Prescription4': temp['Prescription4'],
                        'Prescription5': temp['Prescription5']}
        print("Data : ", data['HospitalId'])

        db = firestore.client()
        newdata_ref = db.collection('newhospital')
        newdata = newdata_ref.get()

        tempdata = []
        for doc in newdata:
            # print(doc.to_dict())
            # print(f'{doc.id} => {doc.to_dict()}')
            tempdata.append(doc.to_dict())

        hospitalname=""
        for temp in tempdata:
            print(temp)
            if(data['HospitalId']==temp['id']):
                hospitalname=temp['HospitalName']
                break

        db = firestore.client()
        newdata_ref = db.collection('newuser')
        newdata = newdata_ref.get()

        tempdata = []
        for doc in newdata:
            # print(doc.to_dict())
            # print(f'{doc.id} => {doc.to_dict()}')
            tempdata.append(doc.to_dict())

        aadharnum = ""
        filename=""
        for temp in tempdata:
            if (data['PatientId'] == temp['id']):
                aadharnum = temp['AadharNumber']
                filename =  temp['FileName']
                break

        print("Aadhar Num : ", aadharnum, " File Name : ", filename)
        return render_template("staffviewfulldetails.html", data=data, aadharnum=aadharnum, filename=filename,
                               hospitalname=hospitalname)
    except Exception as e:
        return str(e)


@app.route('/staffviewfulldetails')
def staffviewfulldetails():
    try:
        args = request.args
        id = args['id']

        db = firestore.client()
        newdata_ref = db.collection('newprescription')
        newdata = newdata_ref.get()
        tempdata=[]
        for doc in newdata:
            #print(doc.to_dict())
            #print(f'{doc.id} => {doc.to_dict()}')
            tempdata.append(doc.to_dict())
        print("Appointment Data " , tempdata)
        data={}
        for temp in tempdata:
            if(id==temp['id']):
                data = {'StaffId': temp['StaffId'],
                             'StaffFirstName': temp['StaffFirstName'],
                             'StaffLastName': temp['StaffLastName'],
                             'StaffEmailId': temp['StaffEmailId'],
                             'StaffPhoneNumber': temp['StaffPhoneNumber'],
                             'Specialization': temp['Specialization'], 'StaffAddress': temp['StaffAddress'],
                             'Qualification': temp['Qualification'], 'HospitalId': temp['HospitalId'],
                             'PatientId': temp['PatientId'],
                             'PatientFirstName': temp['PatientFirstName'],
                             'PatientLastName': temp['PatientLastName'],
                             'PatientEmailId': temp['PatientEmailId'],
                             'PatientPhoneNumber': temp['PatientPhoneNumber'],
                             'Dialysis': temp['Dialysis'], 'AppointmentDate': temp['AppointmentDate'],
                             'PatientAddress': temp['PatientAddress'],
                             'AppointmentTime': temp['AppointmentTime'],
                             'Prescription1':temp['Prescription1'],'Prescription2':temp['Prescription2'],
                        'Prescription3': temp['Prescription3'], 'Prescription4': temp['Prescription4'],
                        'Prescription5': temp['Prescription5']
                        }
        print("Data : ", data['HospitalId'])

        db = firestore.client()
        newdata_ref = db.collection('newhospital')
        newdata = newdata_ref.get()

        tempdata = []
        for doc in newdata:
            # print(doc.to_dict())
            # print(f'{doc.id} => {doc.to_dict()}')
            tempdata.append(doc.to_dict())

        hospitalname=""
        for temp in tempdata:
            print(temp)
            if(data['HospitalId']==temp['id']):
                hospitalname=temp['HospitalName']
                break

        db = firestore.client()
        newdata_ref = db.collection('newuser')
        newdata = newdata_ref.get()

        tempdata = []
        for doc in newdata:
            # print(doc.to_dict())
            # print(f'{doc.id} => {doc.to_dict()}')
            tempdata.append(doc.to_dict())

        aadharnum = ""
        filename=""
        for temp in tempdata:
            if (data['PatientId'] == temp['id']):
                aadharnum = temp['AadharNumber']
                filename =  temp['FileName']
                break

        print("Aadhar Num : ", aadharnum, " File Name : ", filename)
        return render_template("staffviewfulldetails.html", data=data, aadharnum=aadharnum, filename=filename,
                               hospitalname=hospitalname)
    except Exception as e:
        return str(e)

@app.route('/adminviewfulldetails')
def adminviewfulldetails():
    try:
        args = request.args
        id = args['id']

        db = firestore.client()
        newdata_ref = db.collection('newprescription')
        newdata = newdata_ref.get()
        tempdata=[]
        for doc in newdata:
            #print(doc.to_dict())
            #print(f'{doc.id} => {doc.to_dict()}')
            tempdata.append(doc.to_dict())
        print("Appointment Data " , tempdata)
        data={}
        for temp in tempdata:
            if(id==temp['id']):
                data = {'StaffId': temp['StaffId'],
                             'StaffFirstName': temp['StaffFirstName'],
                             'StaffLastName': temp['StaffLastName'],
                             'StaffEmailId': temp['StaffEmailId'],
                             'StaffPhoneNumber': temp['StaffPhoneNumber'],
                             'Specialization': temp['Specialization'], 'StaffAddress': temp['StaffAddress'],
                             'Qualification': temp['Qualification'], 'HospitalId': temp['HospitalId'],
                             'PatientId': temp['PatientId'],
                             'PatientFirstName': temp['PatientFirstName'],
                             'PatientLastName': temp['PatientLastName'],
                             'PatientEmailId': temp['PatientEmailId'],
                             'PatientPhoneNumber': temp['PatientPhoneNumber'],
                             'Dialysis': temp['Dialysis'], 'AppointmentDate': temp['AppointmentDate'],
                             'PatientAddress': temp['PatientAddress'],
                             'AppointmentTime': temp['AppointmentTime'],
                             'Prescription1':temp['Prescription1'],'Prescription2':temp['Prescription2'],
                        'Prescription3': temp['Prescription3'], 'Prescription4': temp['Prescription4'],
                        'Prescription5': temp['Prescription5']
                        }
        print("Data : ", data['HospitalId'])

        db = firestore.client()
        newdata_ref = db.collection('newhospital')
        newdata = newdata_ref.get()

        tempdata = []
        for doc in newdata:
            # print(doc.to_dict())
            # print(f'{doc.id} => {doc.to_dict()}')
            tempdata.append(doc.to_dict())

        hospitalname=""
        for temp in tempdata:
            print(temp)
            if(data['HospitalId']==temp['id']):
                hospitalname=temp['HospitalName']
                break

        db = firestore.client()
        newdata_ref = db.collection('newuser')
        newdata = newdata_ref.get()

        tempdata = []
        for doc in newdata:
            # print(doc.to_dict())
            # print(f'{doc.id} => {doc.to_dict()}')
            tempdata.append(doc.to_dict())

        aadharnum = ""
        filename=""
        for temp in tempdata:
            if (data['PatientId'] == temp['id']):
                aadharnum = temp['AadharNumber']
                filename =  temp['FileName']
                break

        print("Aadhar Num : ", aadharnum, " File Name : ", filename)
        return render_template("adminviewfulldetails.html", data=data, aadharnum=aadharnum, filename=filename,
                               hospitalname=hospitalname)
    except Exception as e:
        return str(e)


@app.route('/addnewprescription', methods=['POST'])
def addnewprescription():
    try:
        #hospitalid = session['hospitalid']
        appointmentid= session['appointmentid']

        ptype1 = request.form['ptype1']
        prescription1 = request.form['prescription1']
        qty1 = request.form['qty1']
        order1 = request.form['order1']

        ptype2 = request.form['ptype2']
        prescription2 = request.form['prescription2']
        qty2 = request.form['qty2']
        order2 = request.form['order2']

        ptype3 = request.form['ptype3']
        prescription3 = request.form['prescription3']
        qty3 = request.form['qty3']
        order3 = request.form['order3']

        ptype4 = request.form['ptype4']
        prescription4 = request.form['prescription4']
        qty4 = request.form['qty4']
        order4 = request.form['order4']

        ptype5 = request.form['ptype5']
        prescription5 = request.form['prescription5']
        qty5 = request.form['qty5']
        order5 = request.form['order5']

        prescriptiondata1= []
        prescriptiondata2 = []
        prescriptiondata3 = []
        prescriptiondata4 = []
        prescriptiondata5 = []
        tempdata = []
        if(prescription1):
            tempdata.append(ptype1)
            tempdata.append(prescription1)
            tempdata.append(qty1)
            tempdata.append(order1)
            prescriptiondata1=tempdata

        tempdata = []
        if (prescription2):
            tempdata.append(ptype2)
            tempdata.append(prescription2)
            tempdata.append(qty2)
            tempdata.append(order2)
            prescriptiondata2=tempdata

        tempdata = []
        if (prescription3):
            tempdata.append(ptype3)
            tempdata.append(prescription3)
            tempdata.append(qty3)
            tempdata.append(order3)
            prescriptiondata3=tempdata

        tempdata = []
        if (prescription4):
            tempdata.append(ptype4)
            tempdata.append(prescription4)
            tempdata.append(qty4)
            tempdata.append(order4)
            prescriptiondata4=tempdata

        tempdata = []
        if (prescription5):
            tempdata.append(ptype5)
            tempdata.append(prescription5)
            tempdata.append(qty5)
            tempdata.append(order5)
            prescriptiondata5=tempdata

        db = firestore.client()
        dbref = db.collection('newappointment')
        userdata = dbref.get()
        staffdata = {}
        patientdata = {}
        for doc in userdata:
            temp = doc.to_dict()
            if (appointmentid == temp['id']):
                staffdata = {'StaffId': temp['StaffId'],
                             'StaffFirstName': temp['StaffFirstName'],
                             'StaffLastName': temp['StaffLastName'],
                             'StaffEmailId': temp['StaffEmailId'],
                             'StaffPhoneNumber': temp['StaffPhoneNumber'],
                             'Specialization': temp['Specialization'], 'StaffAddress': temp['StaffAddress'],
                             'Qualification': temp['Qualification'], 'HospitalId':temp['HospitalId']}
                patientdata = {'PatientId': temp['PatientId'],
                               'PatientFirstName': temp['PatientFirstName'],
                               'PatientLastName': temp['PatientLastName'],
                               'PatientEmailId': temp['PatientEmailId'],
                               'PatientPhoneNumber': temp['PatientPhoneNumber'],
                               'Dialysis': temp['Dialysis'],'AppointmentDate': temp['AppointmentDate'],'PatientAddress': temp['PatientAddress'],
                               'AppointmentTime': temp['AppointmentTime']}
                break
        print("Staff Data : ", staffdata)
        print("Patient Data : ", patientdata)
        print("Prescription Data : ", prescriptiondata1)
        id = str(random.randint(1000, 9999))
        json = {'id': id, 'HospitalId': staffdata['HospitalId'],
                'StaffId': staffdata['StaffId'],
                'StaffFirstName': staffdata['StaffFirstName'], 'StaffLastName': staffdata['StaffLastName'],
                'StaffEmailId': staffdata['StaffEmailId'], 'StaffPhoneNumber': staffdata['StaffPhoneNumber'],
                'StaffAddress': staffdata['StaffAddress'], 'PatientId': patientdata['PatientId'],
                'PatientFirstName': patientdata['PatientFirstName'], 'PatientLastName': patientdata['PatientLastName'],
                'PatientEmailId': patientdata['PatientEmailId'], 'PatientPhoneNumber': patientdata['PatientPhoneNumber'],
                'PatientAddress': patientdata['PatientAddress'], 'Dialysis': patientdata['Dialysis'],
                'AppointmentDate': patientdata['AppointmentDate'], 'AppointmentTime': patientdata['AppointmentTime'],
                'Qualification': staffdata['Qualification'], 'Specialization': staffdata['Specialization'],
                'AppointmentStatus': 'Applied', 'Prescription1':prescriptiondata1,
                'Prescription2':prescriptiondata2,'Prescription3':prescriptiondata3,
                'Prescription4':prescriptiondata4,'Prescription5':prescriptiondata5}
        db = firestore.client()
        print("id : ", id)
        print("Json : ", json)
        data_ref = db.collection('newprescription')
        data_ref.document(id).set(json)
        return render_template("staffapplyprescription.html", data=staffdata, patientdata=patientdata)
    except Exception as e:
        return str(e)

@app.route('/staffapplyprescription')
def staffapplyprescription():
    try:
        args = request.args
        id = args['id']
        session['appointmentid'] = id
        patentid = args['patientid']
        userid = session['userid']
        print("Apply Prescription")
        db = firestore.client()
        dbref = db.collection('newappointment')
        userdata = dbref.get()
        staffdata = {}
        patientdata={}
        for doc in userdata:
            temp = doc.to_dict()
            if (id == temp['id']):
                staffdata = {'id': temp['StaffId'],
                        'FirstName': temp['StaffFirstName'],
                        'LastName': temp['StaffLastName'],
                        'EmailId': temp['StaffEmailId'],
                        'PhoneNumber': temp['StaffPhoneNumber'],
                        'Specialization': temp['Specialization'],
                        'Qualification': temp['Qualification']}
                patientdata = {'id': temp['PatientId'],
                             'FirstName': temp['PatientFirstName'],
                             'LastName': temp['PatientLastName'],
                             'EmailId': temp['PatientEmailId'],
                             'PhoneNumber': temp['PatientPhoneNumber'],
                             'Specialization': temp['Specialization'],
                             'Qualification': temp['Qualification'],
                             'Dialysis': temp['Dialysis']}
        return render_template("staffapplyprescription.html", data=staffdata, patientdata=patientdata)
    except Exception as e:
        return str(e)

@app.route('/staffcheckpatient')
def staffcheckpatient():
    try:
        id=session['userid']
        db = firestore.client()
        newdata_ref = db.collection('newappointment')
        newdata = newdata_ref.get()
        tempdata=[]
        for doc in newdata:
            #print(doc.to_dict())
            #print(f'{doc.id} => {doc.to_dict()}')
            tempdata.append(doc.to_dict())
        print("Appointment Data " , tempdata)
        data=[]
        for doc in tempdata:
            if(id==doc['StaffId'] and doc['AppointmentStatus']=='Accepted'):
                data.append(doc)
        return render_template("staffcheckpatients.html", data=data)
    except Exception as e:
        return str(e)

@app.route('/adminviewstaffs')
def adminviewstaffspage():
    try:
        db = firestore.client()
        newstaff_ref = db.collection('newstaff')
        staffdata = newstaff_ref.get()
        data=[]
        for doc in staffdata:
            print(doc.to_dict())
            print(f'{doc.id} => {doc.to_dict()}')
            data.append(doc.to_dict())
        print("Staff Data " , data)
        return render_template("adminviewstaffs.html", data=data)
    except Exception as e:
        return str(e)

@app.route('/hospitalviewdoctors')
def hospitalviewdoctors():
    try:
        #id = session['userid']
        db = firestore.client()
        newstaff_ref = db.collection('newstaff')
        staffdata = newstaff_ref.get()
        data=[]
        for doc in staffdata:
            print(doc.to_dict())
            print(f'{doc.id} => {doc.to_dict()}')
            data.append(doc.to_dict())
        print("Staff Data " , data)
        return render_template("hospitalviewstaffs.html", data=data)
    except Exception as e:
        return str(e)

@app.route('/addnewappointment', methods=['POST'])
def addnewappointment():
    try:
        if request.method == 'POST':
            staffid = request.form['staffid']
            stafffirstname = request.form['stafffirstname']
            stafflastname = request.form['stafflastname']
            staffemailid = request.form['staffemailid']
            staffphonenumber = request.form['staffphonenumber']
            staffaddress= request.form['staffaddress']
            qualification= request.form['qualification']
            specialization= request.form['specialization']
            patid= request.form['patid']
            hospitalid = request.form['hospitalid']
            patfirstname= request.form['patfirstname']
            patlastname= request.form['patlastname']
            patemailid= request.form['patemailid']
            patphonenumber= request.form['patphonenumber']
            pataddress= request.form['pataddress']
            dialysis= request.form['dialysis']
            appdate= request.form['appdate']
            apptime= request.form['apptime']
            id = str(random.randint(1000, 9999))
            json = {'id': id, 'HospitalId':hospitalid,
                    'StaffId': staffid,
                    'StaffFirstName': stafffirstname,'StaffLastName':stafflastname,
                    'StaffEmailId': staffemailid,'StaffPhoneNumber':staffphonenumber,
                    'StaffAddress': staffaddress, 'PatientId':patid,
                    'PatientFirstName': patfirstname, 'PatientLastName': patlastname,
                    'PatientEmailId': patemailid, 'PatientPhoneNumber': patphonenumber,
                    'PatientAddress': pataddress, 'Dialysis': dialysis,
                    'AppointmentDate':appdate,'AppointmentTime':apptime,
                    'Qualification':qualification,'Specialization':specialization,
                    'AppointmentStatus':'Applied'}
            db = firestore.client()
            data_ref = db.collection('newappointment')
            id = json['id']
            data_ref.document(id).set(json)
        db = firestore.client()
        newdata_ref = db.collection('newappointment')
        newdata = newdata_ref.get()
        data = []
        for doc in newdata:
            print(doc.to_dict())
            print(f'{doc.id} => {doc.to_dict()}')
            data.append(doc.to_dict())
        print("Appointment Data ", data)
        return render_template("userviewappointments.html", data=data)
    except Exception as e:
        return str(e)

@app.route('/usermakeappointment')
def usermakeappointment():
    try:
        db = firestore.client()
        newstaff_ref = db.collection('newstaff')
        staffdata = newstaff_ref.get()
        data=[]
        for doc in staffdata:
            print(doc.to_dict())
            print(f'{doc.id} => {doc.to_dict()}')
            data.append(doc.to_dict())
        print("Staff Data " , data)
        return render_template("usermakeappointment.html", data=data)
    except Exception as e:
        return str(e)

@app.route('/userviewappointments')
def userviewappointments():
    try:
        id = session['userid'];
        print("User Id : ", id)
        db = firestore.client()
        newdata_ref = db.collection('newappointment')
        newdata = newdata_ref.get()
        tempdata=[]
        for doc in newdata:
            #print(doc.to_dict())
            #print(f'{doc.id} => {doc.to_dict()}')
            tempdata.append(doc.to_dict())
        data=[]
        for doc in tempdata:
            print("Doc : ", doc)
            if(id==doc['PatientId']):
                """
                data = {'id': id,
                        'PatientId': doc['PatientId'],
                        'PatientFirstName': doc['PatientFirstName'], 'PatientLastName': doc['PatientLastName'],
                        'PatientEmailId': doc['PatientEmailId'], 'PatientPhoneNumber': doc['PatientPhoneNumber'],
                        'PatientAddress': doc['PatientAddress'], 'StaffId': doc['StaffId'],
                        'StaffFirstName': doc['StaffFirstName'], 'StaffLastName': doc['StaffLastName'],
                        'StaffEmailId': doc['StaffEmailId'], 'StaffPhoneNumber': doc['StaffPhoneNumber'],
                        'StaffAddress': doc['StaffAddress'], 'Dialysis': doc['Dialysis'],
                        'Specialization':doc['Specialization'],'Qualification':doc['Qualification'],
                        'AppointmentTime':doc['AppointmentTime'],'AppointmentDate':doc['AppointmentDate']}
                """
                data.append(doc)
        return render_template("userviewappointments.html", data=data)
    except Exception as e:
        return str(e)

@app.route('/userviewdescriptions')
def userviewdescriptions():
    try:
        args = request.args
        id = args['id']
        db = firestore.client()
        newdata_ref = db.collection('newappointment')
        newdata = newdata_ref.get()
        tempdata=[]
        for doc in newdata:
            print(doc.to_dict())
            print(f'{doc.id} => {doc.to_dict()}')
            tempdata.append(doc.to_dict())
        data={}
        for doc in tempdata:
            if(id==doc['id']):
                data = {'id': id,
                        'PatientId': doc['PatientId'],
                        'PatientFirstName': doc['PatientFirstName'], 'PatientLastName': doc['PatientLastName'],
                        'PatientEmailId': doc['PatientEmailId'], 'PatientPhoneNumber': doc['PatientPhoneNumber'],
                        'PatientAddress': doc['PatientAddress'], 'StaffId': doc['StaffId'],
                        'StaffFirstName': doc['StaffFirstName'], 'StaffLastName': doc['StaffLastName'],
                        'StaffEmailId': doc['StaffEmailId'], 'StaffPhoneNumber': doc['StaffPhoneNumber'],
                        'StaffAddress': doc['StaffAddress'], 'Dialysis': doc['Dialysis'],
                        'Specialization':doc['Specialization'],'Qualification':doc['Qualification'],
                        'AppointmentTime':doc['AppointmentTime'],'AppointmentDate':doc['AppointmentDate']}
        return render_template("userviewdescriptions.html", row=data)
    except Exception as e:
        return str(e)

@app.route('/usermakeappointment1')
def usermakeappointment1():
    try:
        args = request.args
        id = args['id']
        #hospitalId = args['hospitalId']
        #session['hospitalid']=hospitalId
        userid = session['userid'];
        db = firestore.client()
        newstaff_ref = db.collection('newstaff')
        staffdata = newstaff_ref.get()
        tempdata=[]
        for doc in staffdata:
            print(doc.to_dict())
            print(f'{doc.id} => {doc.to_dict()}')
            tempdata.append(doc.to_dict())
        data={}
        for doc in tempdata:
            if(id==doc['id']):
                data = {'id': id,
                        'FirstName': doc['FirstName'], 'LastName': doc['LastName'],
                        'EmailId': doc['EmailId'], 'PhoneNumber': doc['PhoneNumber'],
                        'Address': doc['Address'], 'HospitalId': doc['HospitalId'],
                        'Specialization':doc['Specialization'],'Qualification':doc['Qualification'],
                        }
        print("Staff Data " , data)

        newuser_ref = db.collection('newuser')
        userdata = newuser_ref.get()
        tempdata = []
        for doc in userdata:
            print(doc.to_dict())
            print(f'{doc.id} => {doc.to_dict()}')
            tempdata.append(doc.to_dict())
        userdata = {}
        for doc in tempdata:
            if (userid == doc['id']):
                userdata = {'id': userid,
                        'FirstName': doc['FirstName'], 'LastName': doc['LastName'],
                        'EmailId': doc['EmailId'], 'PhoneNumber': doc['PhoneNumber'],
                        'Address': doc['Address']}
        print("User Data ", userdata)
        today = str(date.today())
        print(today)
        return render_template("usermakeappointment1.html", data=data, userdata=userdata, today=today)
    except Exception as e:
        return str(e)

@app.route('/adminviewhospitals')
def adminviewhospitals():
    try:
        db = firestore.client()
        newstaff_ref = db.collection('newhospital')
        staffdata = newstaff_ref.get()
        data=[]
        for doc in staffdata:
            print(doc.to_dict())
            print(f'{doc.id} => {doc.to_dict()}')
            data.append(doc.to_dict())
        print("Hospital Data " , data)
        return render_template("adminviewhospitals.html", data=data)
    except Exception as e:
        return str(e)

@app.route('/adminviewusers')
def adminviewuserspage():
    try:
        db = firestore.client()
        dbref = db.collection('newuser')
        userdata = dbref.get()
        data = []
        for doc in userdata:
            print(doc.to_dict())
            print(f'{doc.id} => {doc.to_dict()}')
            data.append(doc.to_dict())
        print("Staff Data ", data)
        return render_template("adminviewusers.html", data=data)
    except Exception as e:
        return str(e)

@app.route('/hospitalviewusers')
def hospitalviewusers():
    try:
        db = firestore.client()
        dbref = db.collection('newuser')
        userdata = dbref.get()
        data = []
        for doc in userdata:
            print(doc.to_dict())
            print(f'{doc.id} => {doc.to_dict()}')
            data.append(doc.to_dict())
        print("Staff Data ", data)
        return render_template("hospitalviewusers.html", data=data)
    except Exception as e:
        return str(e)

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    app.debug = True
    app.run()