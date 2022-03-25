from flask import Flask, render_template, request,flash,redirect, send_from_directory
from flask_pymongo import PyMongo 

app=Flask(__name__)
app.config['SECRET_KEY']='thisisasecret'
app.config['MONGO_URI']= 'mongodb://localhost:27017/wad'
mongo=PyMongo(app)
#2 part
@app.route('/')
def home_page():
    return render_template('index.html')
@app.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'GET':
        return render_template('auth/signup.html')

@app.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'GET':
        return render_template('auth/signup.html')
    else:
            username = request.form.get('username')
            password = request.form.get('password')
            if mongo.db.users.count_documents({'username':username}) != 0:
                flash('Username already exists')
                return redirect('/signup')
            else:
                mongo.db.users.insert_one({
                    'username': username,
                    'password': generate_password_hash(password)
                })
                flash('Nice')
                return redirect('/auth/')
@app.route('/auth', methods=['GET','POST'])
def auth():
    if request.method == 'GET':
        return render_template('auth/auth.html')
    else:
        username = request.form.get('username')
        password = request.form.get('password')
        user=mongo.db.users.find_one({'username':username})
        if user and check_password_hash(user['password'],password):
            return rendertemplate('auth/secret.html')
        else:
            flash('the data is not correct')
            return render_template('auth/auth.html')

#3 part
ALLOWED_EXTENSIONS = {'gif','png','jpg','jpeg'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS
@app.route ('/upload',methods=['GET','POST'])
def upload():
    if request.method == 'GET':
        return render_template('upload/upload.html')
    else:
        if 'image' not in request.files:
            flash('cant find the file')
            return redirect(request.url)
        file=request.files['image']
        if not file or file.filename =='':
            flash('no file' )
            return redirect(request.url)
        if not allowed_file(file.filename):
             flash('wrong extension')
             return redirect(request.url)
        filename=secure_filename(file,filename)
        file.save(os.path.join('upload',filename))
        return redirect(f'/uploaded/{filename}')
@app.route('/uploaded/<path:filename>')
def uploaded(filename):
    return send_from_directory('upload',filename)

if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)

       

