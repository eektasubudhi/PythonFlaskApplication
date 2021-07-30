from flask import Flask, render_template, send_file, request, redirect, url_for, session 
import os 


app = Flask(__name__)

app.config['UPLOAD_EXTENSIONS'] = ['.txt']
app.config['UPLOAD_FOLDER'] = '/home/ubuntu/flaskapp/tempfiles/' 

class User:
	def __init__(self, username, password, firstname, lastname, email, filename):
		self.username = username
		self.password = password
		self.firstname = firstname
		self.lastname = lastname
		self.email = email
		self.filename = filename
	def __repr__(self):
		return f'<User: {self.username}>'


@app.route('/')
def index():
	return render_template('index.html')


users =[]
users.append(User('@@','@@','1','adminuse','adminuse@useadmin.co','0'))
@app.route('/register', methods = ['POST'])
def register(): 
	fileitem = request.files['file']
	UN = request.form['username']
	PW = request.form['password']
	FN = request.form['firstname']
	LN = request.form['lastname']
	EM = request.form['email']

	if fileitem.filename:
		file_ext = os.path.splitext(fileitem.filename)[1]
		if file_ext not in app.config['UPLOAD_EXTENSIONS']:
			return render_template("index.html",messgae = "File not supported!! Please upload a .txt type file")	
		
		fileitem.save(os.path.join(app.config['UPLOAD_FOLDER'],fileitem.filename))
		
		savedfilename = fileitem.filename
		#fileitem.save(fileitem.filename)
		#f = open((os.path.join(app.config['UPLOAD_FOLDER'], fileitem.filename)), "r")
		#data = f.read()
		#wordsinfile = data.split()
		#wordcount = len(wordsinfile)
	else: savedfilename =""

	for x in users:
		if x.username == UN and x.password == PW:
			return render_template("login.html",messgae = "User already exist! Login to view details")

	users.append(User(UN,PW,FN,LN,EM,savedfilename))
	print(users,"next")
	print(savedfilename,"savedfilename")

	return render_template('register.html')

@app.route('/login', methods = ['GET', 'POST'])
def login():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		user = [x for x in users if x.username == username][0]
		if us and user.password == password:
			redirect(url_for('profile'))
	else:
		return render_template('login.html')

@app.route('/profile', methods = ['POST'])
def profile():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		savedfilename = 0
		print(username, 'username in pro')
		print(password, 'pass in pro')
		if username not in [i.username for i in users]: 
			return render_template("login.html",messgae = "No user found")
		for x in users:
			print(x.username,'x.usern')
			print(x.password,'x.pass')
			if x.username == username:
				if(x.password == password):
					firstname = x.firstname
					lastname = x.lastname
					email = x.email
					savedfilename = x.filename
				else:
					return render_template("login.html",messgae = "Wrong password")
		
		if savedfilename :
			f = open((os.path.join(app.config['UPLOAD_FOLDER'], savedfilename)), "r")
			data = f.read()
			wordsinfile = data.split()
			wordcount = len(wordsinfile)
		else: 
			wordcount = 'No file uploaded'

		result = {'firstname': firstname, 'lastname': lastname, 'email': email, 'username': username, 'password': password, 'savedfilename': savedfilename}
	return render_template("profile.html", result=result, wordcount = wordcount)

@app.route('/downloadfiles/<filename>', methods = ['GET'])
def return_files_tut(filename):
    file_path = app.config['UPLOAD_FOLDER'] + filename
    return send_file(file_path, as_attachment=True, attachment_filename='')

if __name__ == '__main__':
  app.run()
