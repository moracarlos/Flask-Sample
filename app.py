from flask import *

app = Flask (__name__, template_folder = 'views', static_folder = 'statics')

@app.route('/')
def index():
  return 'Hola'

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
  if email == 'pedro.valdivieso@gmail.com' and password == '123456':
    return render_template('result.html', ok=1)
  else:
    return render_template('result.html', ok=0)

# Actividad
# Ver el users.html
@app.route('/users')
def users():
  return render_template('users.html', users = ['Pedro', 'Sherezada', 'Juan'])
# End Actividad

if __name__ == '__main__':
  app.debug = True
  app.run( host = '0.0.0.0', port = 5000 )