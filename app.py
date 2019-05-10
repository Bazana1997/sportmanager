from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)

#coneccion con mysql
app.config ['MYSQL_HOST'] = 'localhost'
app.config ['MYSQL_USER'] = 'BazanaLuis'
app.config ['MYSQL_PASSWORD'] = 'bazana1997'
app.config ['MYSQL_DB'] = 'sportmanager'
mysql = MySQL(app)

app.secret_key='mysecret'

@app.route('/')
def Home():
	return render_template('home.html')

@app.route('/Player')
def Index():
	cur = mysql.connection.cursor()
	cur.execute('SELECT * FROM players')
	data = cur.fetchall()
	return render_template('index.html', players = data)

@app.route('/add_player', methods=['POST'])
def add_player():
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
		cur.execute('INSERT INTO players(Nombre, ApellidoP, ApellidoM, Curp, Ciudad,Colonia,Calle, No) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)',(Nombre, ApellidoP, ApellidoM, Curp, Ciudad,Colonia,Calle, No))
		mysql.connection.commit()
		flash('Player added')
		return redirect(url_for('Index'))

@app.route('/Edit/<string:id>')
def Edit_player(id):
	cur = mysql.connection.cursor()
	cur.execute("SELECT * FROM players WHERE IdJugador = {}".format(id))
	data = cur.fetchall()
	return render_template('Edit_player.html', player = data[0])

@app.route('/Delete/<string:id>')
def Delete_player(id):
	cur = mysql.connection.cursor()
	cur.execute("DELETE FROM players WHERE IdJugador = {}".format(id))
	mysql.connection.commit()
	flash('Player removed')
	return redirect(url_for('Index'))

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
			""".format(id),(Nombre, ApellidoP, ApellidoM, Curp, Ciudad, Colonia, Calle, No ))
		mysql.connection.commit()
		flash('Player update')
		return redirect(url_for('Index'))


if __name__ == '__main__':
    app.run(port=3000,debug=True)
