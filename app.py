from flask import Flask , render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/criminal'#/dbname
app.secret_key = 'abc'
db = SQLAlchemy(app)

@app.route('/',methods = ['GET', 'POST'])
def home():
    return render_template("home.html")
    
@app.route('/aboutus',methods = ['GET', 'POST'])
def aboutus():
    return render_template("AboutUs.html")

class Sign(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(50), unique=True, nullable=False)
    lastname = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    phone = db.Column(db.String(10), unique=True, nullable=False)
    gender = db.Column(db.String(6), unique=True, nullable=False)
    password = db.Column(db.String(10), unique=True, nullable=False)

@app.route('/signup', methods = ['GET', 'POST'])
def signup():
    if(request.method=='POST'):
        firstname=request.form.get('firstname')
        lastname=request.form.get('lastname')
        email=request.form.get('email')
        phone=request.form.get('phone')
        gender=request.form.getlist('gender')
        password=request.form.get('psw')
        entry= Sign(firstname=firstname,lastname=lastname,email=email,phone=phone,gender=gender,password=password)
        db.session.add(entry)
        db.session.commit()
        return render_template("success.html")
    return render_template("Sign Up.html")

@app.route('/loginpolice',methods = ['GET', 'POST'])
def loginpolice():
    if(request.method=='POST'):
        y = 0
        email=request.form.get('police_email')
        password=request.form.get('psw')
        police=Police.query.all()
        for z in police:
            if(email==z.police_email or password==z.police_id):
                y=1
                session['name']=z.police_name
                return redirect(url_for('police'))

    return render_template("loginpolice.html")


@app.route('/login', methods = ['GET', 'POST'])
def login(): 
    if(request.method=='POST'):
        y = 0
        email=request.form.get('email')
        password=request.form.get('psw')
        
        admin_email = 'admin987@gmail.com'
        admin_password = 'admin101'
        if(email==admin_email and password==admin_password):
            return redirect(url_for('admin'))


        #tablename
        Check = Sign.query.all()

        for x in Check:
             if(email==x.email and password==x.password):
                 y = 1
                 return render_template("fir.html")
        if y == 0:
            return render_template('error.html')
              
    return render_template('Login.html')

class Fir(db.Model):
    police_station_id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(50), unique=True, nullable=False)
    lastname = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    date_of_birth = db.Column(db.Date, unique=True, nullable=False)
    phone = db.Column(db.String(10), unique=True, nullable=False)
    gender = db.Column(db.String(10), unique=True, nullable=False)
    nationality = db.Column(db.String(30), unique=True, nullable=False)
    occupation = db.Column(db.String(30), unique=True, nullable=False)
    address = db.Column(db.String(70), unique=True, nullable=False)
    date_of_registration = db.Column(db.Date, unique=True, nullable=False)
    complaint = db.Column(db.String(50), unique=True, nullable=False)
    crime_category = db.Column(db.String(20), unique=True, nullable=False)
    place_of_occurence = db.Column(db.String(50), unique=True, nullable=False)
    police_station = db.Column(db.String(50), unique=True, nullable=False)

@app.route('/fir', methods = ['GET', 'POST'])
def fir():
    if(request.method=='POST'):
        firstname=request.form.get('firstname')
        lastname=request.form.get('lastname')
        email=request.form.get('email')
        date_of_birth=request.form.get('date_of_birth')
        phone=request.form.get('phone')
        gender=request.form.getlist('gender')
        nationality=request.form.get('nationality')
        occupation=request.form.get('occupation')
        address=request.form.get('address')
        date_of_registration=request.form.get('date_of_registration')
        complaint=request.form.get('complaint')
        crime_category=request.form.get('crime_category')
        place_of_occurence=request.form.get('place_of_occurence')
        police_station=request.form.get('police_station')
        entry= Fir(firstname=firstname,lastname=lastname,email=email,date_of_birth=date_of_birth,phone=phone,gender=gender,nationality=nationality,
                     occupation=occupation,address=address,date_of_registration=date_of_registration,complaint=complaint,
                     crime_category=crime_category,place_of_occurence=place_of_occurence,police_station=police_station)
        db.session.add(entry)
        db.session.commit()
        return render_template("yes.html")

@app.route('/admin', methods = ['GET', 'POST'])
def admin():
     return render_template('adminn.html')

@app.route('/police', methods = ['GET', 'POST'])
def police():
    name=session['name']
    return render_template('policee.html',name=name)

@app.route('/viewfir', methods = ['GET', 'POST'])
def viewfir():
     data=Fir.query.all()
     return render_template('view fir.html', ViewFir=data)

@app.route('/criminalrecords', methods = ['GET', 'POST'])
def criminalrecords():
     data=Criminal.query.all()
     return render_template('criminalrecords.html', CriminalRecords=data)

@app.route('/criminal_records/<string:criminal_id>', methods = ['GET', 'POST'])
def criminal_records(criminal_id):
     criminal = Criminal.query.filter_by(criminal_id=criminal_id).first()
     criminal.criminal_status='currently inspecting'
     db.session.commit()
     data=Criminal.query.all()
     return render_template('criminalrecords.html', CriminalRecords=data)

@app.route('/criminal_records1/<string:criminal_id>', methods = ['GET', 'POST'])
def criminal_records1(criminal_id):
     criminal = Criminal.query.filter_by(criminal_id=criminal_id).first()
     criminal.criminal_status='currently not inspecting'
     db.session.commit()
     data=Criminal.query.all()
     return render_template('criminalrecords.html', CriminalRecords=data)

class Criminal(db.Model):
    criminal_id = db.Column(db.Integer, primary_key=True)
    criminal_name = db.Column(db.String(50), unique=True, nullable=False)
    criminal_mobile = db.Column(db.String(50), unique=True, nullable=False)
    criminal_age = db.Column(db.Integer, unique=True, nullable=False)
    criminal_email = db.Column(db.String(50), unique=True, nullable=False)
    criminal_gender = db.Column(db.String(10), unique=True, nullable=False)
    criminal_address = db.Column(db.String(50), unique=True, nullable=False)
    criminal_status = db.Column(db.String(50), unique=True, nullable=False)

@app.route('/insertcriminalrecords', methods = ['GET', 'POST'])
def insertcriminalrecords():
    if(request.method=='POST'):
        criminal_name=request.form.get('criminal_name')
        criminal_mobile=request.form.get('criminal_mobile')
        criminal_age=request.form.get('criminal_age')
        criminal_email=request.form.get('criminal_email')
        criminal_gender=request.form.getlist('criminal_gender')
        criminal_address=request.form.get('criminal_address')
        criminal_status='currently not inspecting'
        entry= Criminal(criminal_name=criminal_name,criminal_mobile=criminal_mobile,criminal_age=criminal_age,
                     criminal_email=criminal_email,criminal_gender=criminal_gender,criminal_address=criminal_address,criminal_status=criminal_status)
        db.session.add(entry)
        db.session.commit()
    return render_template('insertcriminalrecords.html')

@app.route('/viewcriminalrecords', methods = ['GET', 'POST'])
def viewthecriminalrecords():
     data1=Criminal.query.all()
     return render_template('viewthecriminalrecords.html', ViewtheCriminalRecords=data1)

@app.route('/edit/<string:criminal_id>', methods = ['GET','POST'])
def edit(criminal_id):
    if(request.method=='POST'):
        criminal_name = request.form.get('criminal_name')
        criminal_mobile=request.form.get('criminal_mobile')
        criminal_age=request.form.get('criminal_age')
        criminal_email=request.form.get('criminal_email')
        criminal_gender=request.form.getlist('criminal_gender')
        criminal_address=request.form.get('criminal_address')
        criminal = Criminal.query.filter_by(criminal_id=criminal_id).first()
        criminal.criminal_name = criminal_name
        criminal.criminal_mobile = criminal_mobile
        criminal.criminal_age = criminal_age
        criminal.criminal_email = criminal_email
        criminal.criminal_gender = criminal_gender
        criminal.criminal_address = criminal_address
        db.session.commit()
        return redirect('/insertcriminalrecords')
    criminal = Criminal.query.filter_by(criminal_id=criminal_id).first()
    return render_template('edit.html',criminal=criminal)  
@app.route('/delete/<string:criminal_id>', methods = ['GET','POST'])
def delete(criminal_id):
    criminal = Criminal.query.filter_by(criminal_id=criminal_id).first()
    db.session.delete(criminal)
    db.session.commit()
    return redirect('/viewcriminalrecords')    

class Crime(db.Model):
    criminal_id = db.Column(db.Integer, primary_key=True)
    crime_criminal_id = db.Column(db.Integer, unique=True, nullable=False)
    crime_area = db.Column(db.String(50), unique=True, nullable=False)
    crime_city = db.Column(db.String(50), unique=True, nullable=False)
    crime_description = db.Column(db.String(50), unique=True, nullable=False)
    crime_type = db.Column(db.String(50), unique=True, nullable=False)
    crime_section_of_law = db.Column(db.String(50), unique=True, nullable=False)
    crime_status = db.Column(db.String(50), unique=True, nullable=False)

@app.route('/crimerecords', methods = ['GET', 'POST'])
def crimerecords():
    if(request.method=='POST'):
        crime_criminal_id=request.form.get('crime_criminal_id')
        crime_area=request.form.get('crime_area')
        crime_city=request.form.get('crime_city')
        crime_description=request.form.get('crime_description')
        crime_type=request.form.getlist('crime_type')
        crime_section_of_law=request.form.get('crime_section_of_law')
        crime_status=request.form.get('crime_status')
        entry= Crime(crime_criminal_id=crime_criminal_id,crime_area=crime_area,crime_city=crime_city,
                     crime_description=crime_description,crime_type=crime_type,crime_section_of_law=crime_section_of_law,
                     crime_status=crime_status)
        db.session.add(entry)
        db.session.commit()
    return render_template('crimerecords.html')

@app.route('/viewcrime/<string:criminal_id>', methods = ['GET', 'POST'])
def viewcrime(criminal_id):
        crime = Crime.query.filter_by(crime_criminal_id=criminal_id)
        return render_template('viewcrime.html', ViewCrime=crime)

@app.route('/viewcrime', methods = ['GET', 'POST'])
def viewcrime1():
        data2=Crime.query.all()
        return render_template('viewcrime.html', ViewCrime=data2)

@app.route('/edit/<string:crime_criminal_id>', methods = ['GET','POST'])
def edit1(crime_criminal_id):
    if(request.method=='POST'):
        crime_criminal_id = request.form.get('crime_criminal_id')
        crime_area=request.form.get('crime_area')
        crime_city=request.form.get('crime_city')
        crime_description=request.form.get('crime_description')
        crime_type=request.form.get('crime_type')
        crime_section_of_law=request.form.get('crime_section_of_law')
        crime_status=request.form.get('crime_status')
        crime = Crime.query.filter_by(crime_criminal_id=crime_criminal_id).first()
        crime.crime_criminal_id = crime_criminal_id
        crime.crime_area = crime_area
        crime.crime_city = crime_city
        crime.crime_description = crime_description
        crime.crime_type = crime_type
        crime.crime_section_of_law = crime_section_of_law
        crime.crime_status = crime_status
        db.session.commit()
        return redirect('/crimerecords')
    crime = Crime.query.filter_by(crime_criminal_id=crime_criminal_id).first()
    return render_template('edit1.html',crime=crime)  
   

class Contact(db.Model):
    contact_id = db.Column(db.Integer, primary_key=True)
    contact_firstname = db.Column(db.String(50), unique=True, nullable=False)
    contact_lastname = db.Column(db.String(50), unique=True, nullable=False)
    contact_email = db.Column(db.String(50), unique=True, nullable=False)
    contact_phone = db.Column(db.String(50), unique=True, nullable=False)
    contact_gender = db.Column(db.String(50), unique=True, nullable=False)
    contact_complaint = db.Column(db.String(50), unique=True, nullable=False)

@app.route('/contactus', methods = ['GET', 'POST'])
def contactus():
    if(request.method=='POST'):
        contact_firstname=request.form.get('contact_firstname')
        contact_lastname=request.form.get('contact_lastname')
        contact_email=request.form.get('contact_email')
        contact_phone=request.form.get('contact_phone')
        contact_gender=request.form.getlist('contact_gender')
        contact_complaint=request.form.get('contact_complaint')
        entry= Contact(contact_firstname=contact_firstname,contact_lastname=contact_lastname,contact_email=contact_email,
                       contact_phone=contact_phone,contact_gender=contact_gender,contact_complaint=contact_complaint)
        db.session.add(entry)
        db.session.commit()
        return render_template("success.html")
    return render_template("contactus.html")

@app.route('/viewcontact', methods = ['GET', 'POST'])
def viewcontact():
     data3=Contact.query.all()
     return render_template('viewcontact.html', ViewContact=data3)

class Police(db.Model):
    police_id = db.Column(db.Integer, primary_key=True)
    police_station_id = db.Column(db.Integer,unique=True, nullable=False )
    police_name = db.Column(db.String(50), unique=True, nullable=False)
    police_email = db.Column(db.String(50), unique=True, nullable=False)
    police_age = db.Column(db.String(50), unique=True, nullable=False)
    police_gender = db.Column(db.String(50), unique=True, nullable=False)

@app.route('/policedetails', methods = ['GET', 'POST'])
def policedetails():
    if(request.method=='POST'):
        police_station_id=request.form.get('police_station_id')
        police_name=request.form.get('police_name')
        police_email=request.form.get('police_email')
        police_age=request.form.get('police_age')
        police_gender=request.form.getlist('police_gender')
        entry= Police(police_station_id=police_station_id,police_name=police_name,police_email=police_email,police_age=police_age,police_gender=police_gender)
        db.session.add(entry)
        db.session.commit()
    return render_template('policedetails.html')

@app.route('/viewpolicedetails', methods = ['GET', 'POST'])
def viewpolicerecords():
     data4=Police.query.all()
     return render_template('viewpolicedetails.html', ViewPoliceDetails=data4)

class Station(db.Model):
    station_id = db.Column(db.Integer, primary_key=True)
    station_name = db.Column(db.String(50), unique=True, nullable=False)
    station_area = db.Column(db.String(50), unique=True, nullable=False)
    station_city = db.Column(db.String(50), unique=True, nullable=False)

@app.route('/policestation', methods = ['GET', 'POST'])
def policestation():
    if(request.method=='POST'):
        station_id=request.form.get('station_id')
        station_name=request.form.get('station_name')
        station_area=request.form.get('station_area')
        station_city=request.form.get('station_city')
        entry= Station(station_name=station_name,station_area=station_area,station_city=station_city)
        db.session.add(entry)
        db.session.commit()
    return render_template('policestation.html')

@app.route('/viewpolicestation/<string:station_id>', methods = ['GET', 'POST'])
def station(station_id):
        station = Station.query.filter_by(station_id=station_id)
        return render_template('viewstation.html', ViewStation=station)

@app.route('/policestationdetails', methods = ['GET', 'POST'])
def policestationdetails():
        data2=Station.query.all()
        return render_template('viewstation.html', ViewStation=data2)

if __name__ == '__main__':
   app.run(debug = True)