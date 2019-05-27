from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
import db_connection as SQL

app = Flask(__name__)

# coneccion con mysql
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'BazanaLuis'
app.config['MYSQL_PASSWORD'] = 'bazana1997'
app.config['MYSQL_DB'] = 'league_manager'
mysql = MySQL(app)

app.secret_key = 'mysecret'


@app.route('/')
def Home():
    return render_template('home.html')

# agregar jugador


@app.route('/Player')
def Index():
    return render_template('add_player.html')


@app.route('/add_player', methods=['POST'])
def add_player():
    if request.method == 'POST':
        Nombre = request.form['Nombre']
        LastName = request.form['LastName']
        LastLastName = request.form['LastLastName']
        Curp = request.form['Curp']
        City = request.form['City']
        Block = request.form['Block']
        Street = request.form['Street']
        No = request.form['No']
        IdTeam = request.form['IdTeam']
        Expulsion = request.form['Expulsion']
        Reprimands = request.form['Reprimands']
        Annotations = request.form['Annotations']
        Appearances = request.form['Appearances']

        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO player(Nombre, LastName, LastLastName, Curp, City, Block, Street, No, IdTeam, Expulsion, Reprimands, Annotations, Appearances) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                    (Nombre, LastName, LastLastName, Curp, City, Block, Street, No, IdTeam, Expulsion, Reprimands, Annotations, Appearances))
        mysql.connection.commit()
        flash('Player added')
        return redirect(url_for('Index'))

#show player
@app.route('/show_player')
def show_player():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM player')
    data = cur.fetchall()
    return render_template('show_player.html', player=data)


# Eliminar jugador


@app.route('/Delete/<string:id>')
def Delete_player(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM player WHERE IdJugador = {}".format(id))
    mysql.connection.commit()
    flash('Player removed')
    return redirect(url_for('Index'))

# Editad Jugador


@app.route('/Edit/<string:id>')
def Edit_player(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM player WHERE IdJugador = {}".format(id))
    data = cur.fetchall()
    return render_template('Edit_player.html', player=data[0])


@app.route('/update/<id>', methods=['POST'])
def update_contact(id):
    if request.method == 'POST':
        Nombre = request.form['Nombre']
        ApellidoP = request.form['ApellidoP']
        ApellidoM = request.form['ApellidoM']
        Curp = request.form['Curp']
        Ciudad = request.form['Ciudad']
        Colonia = request.form['Colonia']
        Calle = request.form['Calle']
        No = request.form['No']
        cur = mysql.connection.cursor()
        cur.execute("""
			UPDATE players 
			SET Nombre = %s,
				ApellidoP = %s,
				ApellidoM = %s,
				Curp = %s,
				Ciudad = %s,
				Colonia = %s,
				Calle = %s,
				No = %s
			WHERE IdJugador = {}
			""".format(id), (Nombre, ApellidoP, ApellidoM, Curp, Ciudad, Colonia, Calle, No ))
        mysql.connection.commit()
        flash('Player update')
        return redirect(url_for('Index'))

# Agregar resultados


@app.route('/Results')
def Results():
    return render_template('resultados.html')


@app.route('/add_results')
def Add_Results():
    if request.method == 'POST':
        Jornada = request.form['Jornada']
        Lugar = request.form['Lugar']
        Arbitro = request.form['Arbitro']
        Local = request.form['Local']
        Visitante = request.form['Visitante']

        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO results(Jornada, Lugar, Arbitro, Local, Visitante) VALUES(%s,%s,%s,%s,%s)',
                    (Jornada, Lugar, Arbitro, Local, Visitante))
        mysql.connection.commit()

# Estadisticas


@app.route('/Estadisticas')
def Estadisticas():
    return render_template('Estadisticas.html')


# Perfil
@app.route('/Perfil')
def Perfil():
    return render_template('Perfil.html')

#crer perfil 

@app.route('/CrearPerfil')
def CrearPerfil():  
    return render_template('CrearPerfil.html')

@app.route('/Crear_Perfil', methods=['POST'])
def Crear_Perfil():  
    if request.method == 'POST':
        Nombre = request.form['Nombre']
        LastName = request.form['LastName']
        LastLastName = request.form['LastLastName']
        City = request.form['City']
        Block = request.form['Block']
        Street = request.form['Street']
        No = request.form['No']
        Email = request.form['Email']
        Password = request.form['Password']
       
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO user(Nombre, LastName, LastLastName, City, Block, Street, No, Email, Password) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                    (Nombre, LastName, LastLastName, City, Block, Street, No, Email, Password))
        mysql.connection.commit()
        flash('perfil creado')
        return redirect(url_for('CrearPerfil'))




@app.route('/OpcionCuenta')
def OpcionCuenta():
    return render_template('OpcionCuenta.html')

#informacion de equipo

@app.route('/Info_Team')
def InfTeam():
    return render_template('Info_Team.html')


@app.route('/add_Team', methods=['POST'])
def add_Team():
    pass


if __name__ == '__main__':
    app.run(port=3000, debug=True)
