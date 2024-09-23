import pymysql.cursors
import os


def get_connection():
    connection = pymysql.connect(host=os.getenv("DB_IP", "172.17.0.1"),
                            user='mnist',
                            password='1234',
                            port = int(os.getenv("MY_PORT", "53306")),
                            database='mnistdb',
                            cursorclass=pymysql.cursors.DictCursor)
    return connection

def select(query: str, size = -1):
  conn = get_connection()
  with conn:
      with conn.cursor() as cursor:
          cursor.execute(query)
          result = cursor.fetchmany(size)

  return result
