from flask import *
from models.user import *
import datetime

app = Flask (__name__, template_folder = 'views', static_folder = 'statics')
app.config['SECRET_KEY'] = 'F34TF$($e34D';

# End of new stuff

#Comienza lo bueno

@app.route('/logout')
def logout():
  if session:
    session.clear()
    return ("Sesion finalizada")
  else:
    return ("Usted nunca inicio sesion")

@app.route('/')
def index():
  return render_template('main.html')

@app.route('/iniciar_sesion')
def iniciar_sesion():
  if session:
    return redirect(url_for('welcome', email=session['email']))
  return render_template('iniciar sesion.html')

@app.route('/registrarse')
def registrarse():
  return render_template('registrarse.html')

@app.route('/sign', methods=['POST'])
def sign():
  email = request.form['Email']
  password = request.form['Password']
  nombre = request.form['Nombre']
  apellido = request.form['Apellido']
  user = User(email = email)
  if (user.email==None):
    #no esta registrado
    if (user.newUser(email=email, password=password, nombre=nombre, apellido=apellido)):
      return ("Usuario registrado exitosamente")
    else:
      return ("No se registro el usuario, intente de nuevo")
  else:
    return ("El usuario ya esta registrado")

@app.route('/welcome', methods=['GET', 'POST'])
def welcome():
  if request.method=='POST':
    email= request.form['Email']
    password = request.form['Password']
    user = User(email=email)    
    if user.password and user.password==password:
      session['email'] = request.form['Email'] #Revisar session
      session['time'] = datetime.datetime.now()
      return render_template('welcome.html', email=session['email'], rec_ladrillo=user.rec_ladrillo, rec_rosquilla=user.rec_rosquilla, rec_energia=user.rec_energia, edif_fab=user.edif_fab, edif_kwik=user.edif_kwik, edif_planta=user.edif_planta, uni_homero=user.uni_homero, uni_lisa=user.uni_lisa, uni_bart=user.uni_bart, uni_bob=user.uni_bob)
    else:
      return "Usuario invalido"
  if request.method=='GET':
    if session:
      user = User(email=session['email'])
      #Se actualizan los recursos
      user.actualizarRecursos(delta = ((datetime.datetime.now()-session['time']).total_seconds()), email = user.email)
      session['time'] = datetime.datetime.now()
      user= User(email=session['email'])
      return render_template('welcome.html', email=session['email'], rec_ladrillo=user.rec_ladrillo, rec_rosquilla=user.rec_rosquilla, rec_energia=user.rec_energia, edif_fab=user.edif_fab, edif_kwik=user.edif_kwik, edif_planta=user.edif_planta, uni_homero=user.uni_homero, uni_lisa=user.uni_lisa, uni_bart=user.uni_bart, uni_bob=user.uni_bob)
    else:
      return "Usted no ha iniciado sesion"

@app.route('/preparacion')
def preparacion():
  if session:
    user = User(email=session['email'])
    return render_template('preparacion.html', uni_1=user.uni_homero, uni_2=user.uni_lisa, uni_3=user.uni_bart, uni_4=user.uni_bob)
  else:
    return "Usted no ha iniciado sesion"

@app.route('/getOponentes')
def getOponentes():
  if session:
    user = User(email=session['email'])
    oponentes = user.getOponentes(email=session['email'])
    return json.dumps(oponentes)
  else:
    return "Usted no ha iniciado sesion"

@app.route('/getUnidades')
def getUnidades():
  if session:
    user = User(email=session['email'])
    unidades = user.getUnidades(email=session['email'])
    return json.dumps(unidades)
  else:
    return "Usted no ha iniciado sesion"

@app.route('/getScores')
def getScores():
  usuarios = getAll()
  return json.dumps(usuarios)

@app.route('/combate')
def combate():
  return render_template('combate.html')


@app.route('/seleccionar_oponente')
def seleccionar_oponente():
  return render_template('seleccionaroponente.html')

@app.route('/subir_fab')
def subir_fab():
  user = User(email=session['email'])
  costo_level=3*(user.edif_fab)*(user.edif_fab)+13
  if user.rec_ladrillo-costo_level*0.7 > 0 and user.rec_rosquilla-costo_level*0.3>0:
    #subir nivel
    user.subirNivel(edif = 'edif_fab', email=session['email'], costo = costo_level)
    return str(user.edif_fab+1)
  else:
    return str(user.edif_fab)

@app.route('/subir_kwik')
def subir_kwik():
  user = User(email=session['email'])
  costo_level=2*(user.edif_kwik)*(user.edif_kwik)*(user.edif_kwik)+8*(user.edif_kwik)+14
  if user.rec_ladrillo-costo_level*0.7 > 0 and user.rec_rosquilla-costo_level*0.3>0:
    #subir nivel
    user.subirNivel(edif = 'edif_kwik', email=session['email'], costo = costo_level)
    return str(user.edif_kwik+1)
  else:
    return str(user.edif_kwik)

@app.route('/subir_planta')
def subir_planta():
  user = User(email=session['email'])
  costo_level=10*(user.edif_planta)*(user.edif_planta)+1
  if user.rec_ladrillo-costo_level*0.7 > 0 and user.rec_rosquilla-costo_level*0.3>0:
    #subir nivel
    user.subirNivel(edif = 'edif_planta', email=session['email'], costo = costo_level)
    return str(user.edif_planta+1)
  else:
    return str(user.edif_planta)

@app.route('/comprar_homero')
def comprar_homero():
  user = User(email=session['email'])
  if user:
    user.subirUnidad(unidad='uni_homero', email= session['email'])
    return str(user.uni_homero+1)
  else:
    return str(user.uni_homero)

@app.route('/comprar_lisa')
def comprar_lisa():
  user = User(email=session['email'])
  if user:
    user.subirUnidad(unidad='uni_lisa', email= session['email'])
    return str(user.uni_lisa+1)
  else:
    return str(user.uni_lisa)

@app.route('/comprar_bart')
def comprar_bart():
  user = User(email=session['email'])
  if user:
    user.subirUnidad(unidad='uni_bart', email= session['email'])
    return str(user.uni_bart+1)

@app.route('/comprar_bob')
def comprar_bob():
  user = User(email=session['email'])
  if user:
    user.subirUnidad(unidad='uni_bob', email= session['email'])
    return str(user.uni_bob+1)


if __name__ == '__main__':
  app.debug = True
  app.run( host = '0.0.0.0', port = 5000 )