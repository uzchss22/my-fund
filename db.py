import mysql.connector
from mysql.connector import Error
from datetime import datetime, timedelta

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',       
            database='finance',    
            user='root', 
            password='your-passwd' # insert your pswd
        )
        return connection
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        return None

def close_db_connection(connection):
    if connection.is_connected():
        connection.close()
        print("MySQL connection is closed")

def insert_proceeds(total_proceeds, day_proceeds):
    connection = get_db_connection()
    if connection is None:
        return

    try:
        cursor = connection.cursor()

        insert_query = """
        INSERT INTO my_fund (total_proceeds, day_proceeds, insert_date)
        VALUES (%s, %s, %s)
        """

        current_date = datetime.now().strftime('%Y-%m-%d 00:00:00') # 로컬과 서버 시간대가 달라서 0시로 통일, 시간 필요하면 index.html 의 데이터 매칭 코드 utc로 변경

        cursor.execute(insert_query, (total_proceeds, day_proceeds, current_date))
        connection.commit()

        print("Record inserted successfully into my_fund table")

    except Error as e:
        print(f"Error while inserting data: {e}")

    finally:
        cursor.close()
        close_db_connection(connection)

# 해당 달의 데이터 리턴하는 함수
def fetch_data():
    connection = get_db_connection()
    if connection is None:
        return []

    try:
        cursor = connection.cursor(dictionary=True)

        one_month_ago = datetime.now() - timedelta(days=30)
        one_month_ago_str = one_month_ago.strftime('%Y-%m-%d 00:00:00')

        fetch_query = """
        SELECT total_proceeds, day_proceeds, insert_date
        FROM my_fund
        WHERE insert_date >= %s
        ORDER BY insert_date
        """
        
        cursor.execute(fetch_query, (one_month_ago_str,))
        result = cursor.fetchall()

        return result

    except Error as e:
        print(f"Error while fetching data: {e}")
        return []

    finally:
        cursor.close()
        close_db_connection(connection)
