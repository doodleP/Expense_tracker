from flask import Flask, render_template, url_for, request, redirect
import mysql.connector
from dotenv import load_dotenv
import os
import pandas as pd

load_dotenv()

app = Flask(__name__)

conn = mysql.connector.connect(
    host = os.getenv('DB_HOST'),
    user = os.getenv('DB_USER'),
    password = os.getenv('DB_PASSWORD'),
    database = os.getenv('DB_NAME')
)
cursor = conn.cursor()

@app.route('/')          #homepage

def index():
    cursor.execute("SELECT * FROM expense")
    records = cursor.fetchall()

    if not records:
        table = '<h3>Whoops! Nothing here yet. Fill in some entries!</h3>'

    else:
    
        df = pd.DataFrame(records, columns = ['ID', 'Date', 'Category', 'Amount', 'Description'])

        df['Delete'] = df['ID'].apply(lambda x: f'<a href="/delete/{x}" class="del-btn">🗑️</a>')
        df.drop('ID', axis=1, inplace=True)
        table = df.to_html(classes='table table-striped', index=False, escape=False, border=0, justify='center')

    return render_template("index.html", table = table)

@app.route('/add_expense', methods=['POST'])    #add expense 
def add_entry():
    date = request.form['date']
    category = request.form['category']
    amount = request.form['amount']
    description = request.form['description']

    if description.strip() == '':
        cursor.execute("INSERT INTO expense (date, category, amount, description) VALUES (%s, %s, %s, NULL)", (date, category, amount))
    else:
        cursor.execute("INSERT INTO expense (date, category, amount, description) VALUES (%s, %s, %s, %s)", (date, category, amount, description))
    conn.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:expense_id>')     #delete expense 
def delete_entry(expense_id):
    cursor.execute("DELETE FROM expense WHERE id = %s", (expense_id,))
    conn.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
