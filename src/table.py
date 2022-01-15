import mysql.connector


def create_table(table_name):
    conn = mysql.connector.connect(host='127.0.0.1', port='3306', user='root',
                                   password='MYSQLPASSWORD', database='rank_list', charset='utf8')
    cur = conn.cursor()
    sql = "CREATE TABLE IF NOT EXISTS {} (song_rank CHAR(10) ,\
                                song_name  CHAR(50) NOT NULL UNIQUE,\
                                song_artist  CHAR(50),\
                                song_url  VARCHAR (1000),\
                                song_date CHAR(50))"

    cur.execute(sql.format(table_name))

    conn.commit()
