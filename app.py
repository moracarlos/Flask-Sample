from flask import *
from models.user import *

app = Flask (__name__, template_folder = 'views', static_folder = 'statics')

@app.route('/')
def index():
  return 'Sup'

@app.route('/say')
def say():
  name = request.args.get('name')
  return render_template('say.html', name = name)

@app.route('/form')
def form():
  return render_template('form.html')

@app.route('/login', methods = ['POST'])
def login():
  email = request.form['Email']
  password = request.form['Password']
  user = User(email = email)
  if user.password and user.password == password:
    return render_template('result.html', ok=1)
  return render_template('result.html', ok=0)

@app.route('/users')
def users():
  return render_template('users.html', users = Users().getAll())

# New stuff coming
@app.route('/update', methods = ['POST'])
def update():
  email = request.form['Email'].strip()
  name = request.form['Name']
  password = request.form['Password']
  user = User(email = email)
  if user.email and user.update(name = name, password = password):
    return redirect(url_for('users'))
  return render_template('result.html', ok=0)

@app.route('/get_user_json')
def getUserJSON():
  email = request.args.get('email').strip()
  user = User(email = email)
  return user.to_json()

@app.route('/delete_user')
def deleteUser():
  email = request.args.get('email')
  if email:
    user = User(email = email)
    user.destroy()
    return redirect(url_for('users'))
  return render_template('result.html', ok=0)
# End of new stuff

if __name__ == '__main__':
  app.debug = True
  app.run( host = '0.0.0.0', port = 5000 )


