from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)

# MySQL connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'La contrasena97'
app.config['MYSQL_DB'] = 'contacts_with_python'
mysql = MySQL(app)

# settings
app.secret_key = 'mysecretkey'


@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute('select * from contact')
    data = cur.fetchall()
    return render_template('index.html', contacts=data)


@app.route('/add_contact', methods=['POST'])
def add_contact():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        cur = mysql.connection.cursor()
        cur.execute('insert into contact (name, phone, email) values (%s, %s, %s)', (name, phone, email))
        mysql.connection.commit()
        flash('Contact added successfully')
        return redirect(url_for('index'))


@app.route('/edit_contact/<id>')
def get_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('select * from contact where id = {0}'.format(id))
    data = cur.fetchall()
    return render_template('edit-contact.html', contact=data[0])

@app.route('/update_contact/<id>', methods=['POST'])
def update_contact(id):
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        cur = mysql.connection.cursor()
        cur.execute("""
            update contact
            set name = %s,
                phone = %s,
                email = %s
            where id = %s
        """, (name, phone, email, id))
        mysql.connection.commit()
        flash('Contact update sucessfully')
        return redirect(url_for('index'))

@app.route('/delete_contact/<string:id>')
def delete_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('delete from contact where id={0}'.format(id))
    mysql.connection.commit()
    flash('Contact removed successfully')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(port=3000, debug=True)
