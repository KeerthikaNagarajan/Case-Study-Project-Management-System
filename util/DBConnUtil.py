import mysql.connector
from mysql.connector import Error


class DBConnUtil:
    @staticmethod
    def get_connection(connection_string):
        try:
            parts = connection_string.split('://')[1].split('@')
            user_pass = parts[0].split(':')
            host_port_db = parts[1].split('/')
            host_port = host_port_db[0].split(':')

            username = user_pass[0]
            password = user_pass[1] if len(user_pass) > 1 else ''
            host = host_port[0]
            port = host_port[1] if len(host_port) > 1 else '3306'
            database = host_port_db[1]

            connection = mysql.connector.connect(
                host=host,
                user=username,
                password=password,
                database=database,
                port=port
            )

            if connection.is_connected():
                print("Connected to MySQL database")
                return connection
        except Error as e:
            print(f"Error while connecting to MySQL: {e}")
            return None