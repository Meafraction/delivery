from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Создаем базу данных SQLite
conn = sqlite3.connect('delivery.db')
cursor = conn.cursor()

# Создаем таблицу для заказов
cursor.execute('''
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_name TEXT NOT NULL,
        items TEXT NOT NULL,
        total_price REAL NOT NULL,
        confirmed BOOLEAN DEFAULT FALSE
    )
''')
conn.commit()

conn.close()

@app.route('/')
def index():
    return {"message": "Hello World"}

@app.route('/make_order', methods=['POST'])
def make_order():
    if request.method == 'POST':
        customer_name = request.form['customer_name']
        items = request.form['items']
        total_price = float(request.form['total_price'])

        # Добавляем заказ в базу данных
        conn = sqlite3.connect('delivery.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO orders (customer_name, items, total_price)
            VALUES (?, ?, ?)
        ''', (customer_name, items, total_price))
        conn.commit()
        conn.close()

        return redirect(url_for('index'))

@app.route('/admin')
def admin():
    # Получаем все неподтвержденные заказы
    conn = sqlite3.connect('delivery.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM orders WHERE confirmed = FALSE')
    orders = cursor.fetchall()
    conn.close()

    return render_template('admin.html', orders=orders)

@app.route('/confirm_order/<int:order_id>')
def confirm_order(order_id):
    # Подтверждаем заказ
    conn = sqlite3.connect('delivery.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE orders SET confirmed = TRUE WHERE id = ?', (order_id,))
    conn.commit()
    conn.close()

    return redirect(url_for('admin'))

if __name__ == '__main__':
    app.run(debug=True)
