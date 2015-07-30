import psycopg2

class User:
  def __init__(self, email = None):
    if email:
      connection = psycopg2.connect('dbname=ati user=ati password=ati host=localhost')
      query = connection.cursor()
      query.execute('select * from usuarios where email=%s', (email,))
      result = query.fetchone()
      query.execute('select nombreunidad, disponible from unidades where email=%s', (email,))
      unidades = query.fetchall()
      if result:
        self.email = result[0]
        self.password = result[1]
        self.nombre = result[2]
        self.apellido = result[3]
        self.puntuacion = result[4]
        self.rec_ladrillo = result[5]
        self.rec_rosquilla = result[6]
        self.rec_energia = result[7]
        self.edif_fab = result[8]
        self.edif_kwik = result[9]
        self.edif_planta = result[10]
        for elemento in unidades:
          if elemento[0]=='uni_homero':
            self.uni_homero=elemento[1]
          if elemento[0]=='uni_lisa':
            self.uni_lisa=elemento[1]
          if elemento[0]=='uni_bart':
            self.uni_bart=elemento[1]
          if elemento[0]=='uni_bob':
            self.uni_bob=elemento[1] 
      else:
        self.email = None
        self.password = None
        self.nombre = None
        self.apellido = None
        self.puntuacion = None
        self.rec_ladrillo = None
        self.rec_rosquilla = None
        self.rec_energia = None
        self.edif_fab = None
        self.edif_kwik = None
        self.edif_planta = None
      query.close()
      connection.close()

  def update(self, nombre = None, password = None, apellido=None):
    if nombre and password:
      connection = psycopg2.connect('dbname=ati user=ati password=ati host=localhost')
      query = connection.cursor()
      query.execute('update usuarios set nombre=%s, password=%s, apellido=%s where email=%s', (nombre, password, apellido, self.email,))
      connection.commit()
      self.nombre = nombre
      self.password = password
      self.apellido = apellido
      query.close()
      connection.close()
      return True
    else:
      return False

  def newUser(self, email=None, password=None, nombre=None, apellido=None):
    if email and nombre and password and apellido:
      connection = psycopg2.connect('dbname=ati user=ati password=ati host=localhost')
      query = connection.cursor()
      query.execute('insert into usuarios (email, password, nombre, apellido, puntuacion, rec_ladrillo, rec_rosquilla, rec_energia, edif_fab, edif_kwik, edif_planta) values (%s, %s, %s, %s, 0, 0, 0, 0, 0, 0, 0)', (email, password, nombre, apellido,))
      query.execute('insert into unidades (nombreunidad, ataque, defensa, carga, tipo, recporuni, puntos, email, disponible) values (%s, 10, 25, 15, %s, 15, 80, %s, 0)', ('uni_homero', 'distancia',email))
      query.execute('insert into unidades (nombreunidad, ataque, defensa, carga, tipo, recporuni, puntos, email, disponible) values (%s, 12, 20, 30, %s,8, 90, %s, 0)', ('uni_lisa', 'distancia',email))
      query.execute('insert into unidades (nombreunidad, ataque, defensa, carga, tipo, recporuni, puntos, email, disponible) values (%s, 11, 10, 20, %s, 9, 120, %s, 0)', ('uni_bart', 'distancia',email))
      query.execute('insert into unidades (nombreunidad, ataque, defensa, carga, tipo, recporuni, puntos, email, disponible) values (%s, 15, 15, 10, %s, 12, 77, %s, 0)', ('uni_bob', 'distancia',email))
      connection.commit()
      query.close()
      connection.close()
      return True
    else:
      return False


  def destroy(self):
    if self.email:
      connection = psycopg2.connect('dbname=ati user=ati password=ati host=localhost')
      query = connection.cursor()
      query.execute('delete from usuarios where email=%s', (self.email,))
      connection.commit()
      self.email = None
      self.nombre = None
      self.password = None
      query.close()
      connection.close()
      return True
    else:
      return False

  def to_json(self, usuario=None):
    return "{ \"email\": \"%s\", \"password\": \"%s\", \"nombre\": \"%s\" ,\"apellido\": \"%s\", \"puntuacion\": \"%s\", \"rec_ladrillo\": \"%s\", \"rec_rosquilla\": \"%s\", \"rec_energia\": \"%s\", \"edif_fab\": \"%s\", \"edif_kwik\": \"%s\", \"edif_planta\": \"%s\"}"%(usuario[0],usuario[1],usuario[2],usuario[3],usuario[4],usuario[5],usuario[6],usuario[7],usuario[8],usuario[9],usuario[10],usuario[11],)

  def actualizarRecursos(self, delta=None, email=None):
    if delta and email:
      connection = psycopg2.connect('dbname=ati user=ati password=ati host=localhost')
      query = connection.cursor()
      query.execute('select rec_ladrillo, rec_rosquilla, rec_energia, edif_fab, edif_kwik, edif_planta from usuarios where email=%s', (email,))
      result = query.fetchone()
      val = result[0] + delta*(0.9*result[3]+0.1) #val es el nuevo valor del recurso ladrillo
      query.execute('update usuarios set rec_ladrillo = %s where email=%s', (val, email))
      val = result[1] + delta*(0.00014*result[4]+0.2)
      query.execute('update usuarios set rec_rosquilla = %s where email=%s', (val, email))
      val = result[2] + delta*(0.00018*result[5]+0.4)
      query.execute('update usuarios set rec_energia = %s where email=%s', (val, email))
      connection.commit()
      query.close()
      connection.close()
      return True
    else:
      return False

  def subirNivel(self, edif=None, email=None, costo = None):
    if edif and email and costo:
      connection = psycopg2.connect('dbname=ati user=ati password=ati host=localhost')
      query = connection.cursor()
      if edif=='edif_fab':
        query.execute('select rec_ladrillo, rec_rosquilla, edif_fab from usuarios where email=%s', (email,))
        result=query.fetchone()
      if edif=='edif_kwik':
        query.execute('select rec_ladrillo, rec_rosquilla, edif_kwik from usuarios where email=%s', (email,))
        result=query.fetchone()
      if edif=='edif_planta':
        query.execute('select rec_ladrillo, rec_rosquilla, edif_planta from usuarios where email=%s', (email,))
        result=query.fetchone()
      nuevo_recurso=result[0]-costo*0.7
      query.execute('update usuarios set rec_ladrillo=%s where email=%s', (nuevo_recurso, email,))
      nuevo_recurso=result[1]-costo*0.3
      query.execute('update usuarios set rec_rosquilla=%s where email=%s', (nuevo_recurso, email,))
      nuevo_nivel=result[2]+1
      if edif=='edif_fab':
        query.execute('update usuarios set edif_fab=%s where email=%s', (nuevo_nivel, email,))
      if edif=='edif_kwik':
        query.execute('update usuarios set edif_kwik=%s where email=%s', (nuevo_nivel, email,))
      if edif=='edif_planta':
        query.execute('update usuarios set edif_planta=%s where email=%s', (nuevo_nivel, email,))
      connection.commit()
      query.close()
      connection.close()
      return True
    else:
      return False

  def subirUnidad(self, unidad=None, email=None):
    if unidad and email:
      connection = psycopg2.connect('dbname=ati user=ati password=ati host=localhost')
      query = connection.cursor()
      query.execute('select recporuni, disponible from unidades where nombreunidad=%s and email=%s', (unidad, email,))
      result = query.fetchone()
      query.execute('select rec_rosquilla from usuarios where email=%s', (email,))
      rosquilla= query.fetchone()
      if rosquilla[0] - result[0] > 0:
        query.execute('update usuarios set rec_rosquilla=%s where email=%s', ((rosquilla[0]-result[0]), email,))
        query.execute('update unidades set disponible=%s where email=%s and nombreunidad=%s', (result[1]+1, email, unidad))
      #Se actualiza la puntuacion del jugador
      query.execute('select disponible, puntos from unidades where email=%s', (email,))
      result= query.fetchall()
      puntos_jugador = 0
      for uni in result:
        puntos_jugador += uni[1]*uni[0]
      query.execute('update usuarios set puntuacion=%s where email=%s', (puntos_jugador, email,))
      connection.commit()
      query.close()
      connection.close()
      return True
    else:
      return False

  def getOponentes(self, email=None):
    if email:
      calificados=[]
      connection = psycopg2.connect('dbname=ati user=ati password=ati host=localhost')
      query = connection.cursor()
      query.execute('select puntuacion from usuarios where email=%s', (email,))
      puntuacion_jugador = query.fetchone()
      query.execute('select * from usuarios where email!=%s', (email,))
      result = query.fetchall()
      #Clasificamos los usuarios
      i=0
      for usuario in result:
        if abs(usuario[4]-puntuacion_jugador[0])<=puntuacion_jugador[0]*0.2: #Califica con el 20%
          calificados.append('{ \"email\": \"%s\", \"password\": \"%s\", \"nombre\": \"%s\" ,\"apellido\": \"%s\", \"puntuacion\": \"%s\", \"rec_ladrillo\": \"%s\", \"rec_rosquilla\": \"%s\", \"rec_energia\": \"%s\", \"edif_fab\": \"%s\", \"edif_kwik\": \"%s\", \"edif_planta\": \"%s\"}'%(usuario[0],usuario[1],usuario[2],usuario[3],usuario[4],usuario[5],usuario[6],usuario[7],usuario[8],usuario[9],usuario[10],))
          i+=1
      if len(calificados)==0:
        for usuario in result:
          if abs(usuario[4]-puntuacion_jugador[0])<=puntuacion_jugador[0]*0.25: #Califica con el 20%
            calificados.append('{ \"email\": \"%s\", \"password\": \"%s\", \"nombre\": \"%s\" ,\"apellido\": \"%s\", \"puntuacion\": \"%s\", \"rec_ladrillo\": \"%s\", \"rec_rosquilla\": \"%s\", \"rec_energia\": \"%s\", \"edif_fab\": \"%s\", \"edif_kwik\": \"%s\", \"edif_planta\": \"%s\"}'%(usuario[0],usuario[1],usuario[2],usuario[3],usuario[4],usuario[5],usuario[6],usuario[7],usuario[8],usuario[9],usuario[10],))
            i+=1
      connection.commit()
      query.close()
      connection.close()
      return calificados
    else:
      return None

  def getUnidades(self, email=None):
    if email:
      calificados=[]
      connection = psycopg2.connect('dbname=ati user=ati password=ati host=localhost')
      query = connection.cursor()
      query.execute('select disponible, nombreunidad, defensa from unidades where email=%s', (email,))
      unidades = query.fetchall()
      #Clasificamos los usuarios
      for unidad in unidades:
        calificados.append('{ \"disponible\": \"%s\", \"nombreunidad\": \"%s\", \"defensa\": \"%s\"}'%(usuario[0],usuario[1],usuario[2],))
      connection.commit()
      query.close()
      connection.close()
      return calificados
    else:
      return None

def getAll():
  calificados=[]
  connection = psycopg2.connect('dbname=ati user=ati password=ati host=localhost')
  query = connection.cursor()
  query.execute('select email, puntuacion from usuarios order by puntuacion desc limit 100')
  usuarios = query.fetchall()
  #Clasificamos los usuarios
  for usuario in usuarios:
    calificados.append('{ \"email\": \"%s\", \"puntuacion\": \"%s\"}'%(usuario[0],usuario[1],))
  connection.commit()
  query.close()
  connection.close()
  return calificados
  


