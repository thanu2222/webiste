from flask import Flask, render_template, request
import sqlite3
from sqlite3 import Error

app = Flask(__name__)
DATABASE = "games"


def create_connection(db_file):
    try:
        connection = sqlite3.connect(db_file)
        return connection
    except Error as e:
        print(e)
    return None


@app.route('/')
def render_home():
    return render_template("index.html")


@app.route('/country')
def render_wii():
    query = "SELECT Rank, GameTitle, Platform, Year, Fa, Publisher FROM games_table WHERE Platform = 'Wii' OR" \
            " Platform = 'Country'"
    con = create_connection(DATABASE)
    cur = con.cursor()
    cur.execute(query)
    games_list = cur.fetchall()
    con.close()
    return render_template("page.html", items=games_list, name="Wii")



@app.route('/search', methods=['GET', 'Post'])
def render_search():
    searching = request.form['search']
    query = "SELECT Rank, GameTitle, Platform, Year, Fa, Publisher FROM games_table WHERE GameTitle like ? OR" \
            " Platform like ? OR Year like ? OR Fa like ? OR Publisher like ?"
    search = "%" + searching + "%"
    con = create_connection(DATABASE)
    cur = con.cursor()
    cur.execute(query, (search, search, search, search, search))
    games_list = cur.fetchall()
    con.close()
    return render_template("page.html", items=games_list, name=searching, searched=True)


if __name__ == '__main__':
    app.run()
