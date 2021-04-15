# import the Flask class from the flask module
from flask import Flask, render_template, request
import sqlite3

"""
# Minimum reproductible example

# Two questions:

1. Should we call function outside route functions? so that we have them available 
mumtiple route function?
If no, what is the other better solution?

2. How to use the same arguments without repeting them?
(i. e passing same argument to multile function --> render_template())
"""
app = Flask(__name__, static_url_path='/static')

SQL_COMMAND = ''
sql_output = ()
tableName = ''
colNames = []


def readSqlite(tableName, SQL_COMMAND, path='utils/marketdataSQL.db'):
    conn = sqlite3.connect('utils/marketdataSQL.db')
    mycur = conn.cursor()
    mycur.execute(f"{SQL_COMMAND}")
    sql_output = (mycur.fetchall())

    colNames = list(map(lambda x: x[0], mycur.description))
    conn.close()

    return sql_output, colNames


@app.route('/')
def home():

    return render_template(
        'welcome.html',
        SQL_COMMAND=SQL_COMMAND,
    )


@app.route('/', methods=['POST'])
def my_form_post():
    global SQL_COMMAND
    global sql_output
    global colNames

    SQL_COMMAND = request.form['textarea']

    sql_output, colNames = readSqlite(tableName='quotes',
                                      SQL_COMMAND=SQL_COMMAND)

    widthDF = list(range(len(colNames)))

    print(widthDF)
    print("output: ", sql_output)

    return render_template(
        'welcome.html',
        SQL_COMMAND=SQL_COMMAND,
        sql_output=sql_output,
        colNames=colNames,
        widthDF=widthDF
    )


if __name__ == '__main__':
    app.run(debug=True)
