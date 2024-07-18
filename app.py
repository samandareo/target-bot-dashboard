from flask import Flask, render_template, request, redirect, url_for, flash
import psycopg2

app = Flask(__name__)
app.secret_key = 'your_secret_key'

DATABASE_CONFIG = {
    'host': "dpg-cqb3njo8fa8c73b0bn8g-a.frankfurt-postgres.render.com",
    'database': "botdb_hc6i",
    'user': "botdb_hc6i_user",
    'password': "eP6HxjZuBxuevilm7qNVPhsK75cAWsbD",
    'port': "5432"
}

def get_db_connection():
    conn = psycopg2.connect(**DATABASE_CONFIG)
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT name,telegram_channel_msg_link,book_id FROM books')
    books = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('index.html', books=books)

@app.route('/add_book', methods=('GET', 'POST'))
def add_book():
    if request.method == 'POST':
        name = request.form['name']
        telegram_channel_msg_link = request.form['telegram_channel_msg_link']
        book_id = request.form['book_id']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO books (name, telegram_channel_msg_link, book_id) VALUES (%s, %s, %s)',
                       (name, telegram_channel_msg_link, book_id))
        conn.commit()
        cursor.close()
        conn.close()
        flash('Book added successfully!')
        return redirect(url_for('index'))
    return render_template('add_book.html')

@app.route('/delete_book', methods=('GET', 'POST'))
def delete_book():
    if request.method == 'POST':
        book_id = request.form['book_id']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM books WHERE book_id = %s', (book_id,))
        conn.commit()
        cursor.close()
        conn.close()
        flash('Book deleted successfully!')
        return redirect(url_for('index'))
    return render_template('delete_book.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
