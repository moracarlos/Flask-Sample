import psycopg2

class User:
  def __init__(self, email = None):
    if email:
      connection = psycopg2.connect('dbname=ati user=ati password=ati_clave host=localhost')
      query = connection.cursor()
      query.execute('select email,name,password from users where email=%s', (email,))
      result = query.fetchone()
      if result:
        self.email = result[0]
        self.name = result[1]
        self.password = result[2]
      else:
        self.email = None
        self.name = None
        self.password = None
      query.close()
      connection.close()

  def update(self, name = None, password = None):
    if name and password:
      connection = psycopg2.connect('dbname=ati user=ati password=ati_clave host=localhost')
      query = connection.cursor()
      query.execute('update users set name=%s, password=%s where email=%s', (name, password, self.email,))
      connection.commit()
      self.name = name
      self.password = password
      query.close()
      connection.close()
      return True
    else:
      return False

  def destroy(self):
    if self.email:
      connection = psycopg2.connect('dbname=ati user=ati password=ati_clave host=localhost')
      query = connection.cursor()
      query.execute('delete from users where email=%s', (self.email,))
      connection.commit()
      self.email = None
      self.name = None
      self.password = None
      query.close()
      connection.close()
      return True
    else:
      return False

  def to_json(self):
    return "{ \"email\": \"%s\", \"name\": \"%s\", \"password\": \"%s\" }"%(self.email,self.name,self.password)

class Users:
  def getAll(self):
    connection = psycopg2.connect('dbname=ati user=ati password=ati_clave host=localhost')
    query = connection.cursor()
    query.execute('select * from users')
    result = query.fetchall()
    query.close()
    connection.close()
    return result


