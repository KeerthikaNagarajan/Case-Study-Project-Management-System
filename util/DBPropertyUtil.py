class DBPropertyUtil:
    @staticmethod
    def get_connection_string(property_file):
        try:
            with open(property_file, 'r') as file:
                properties = {}
                for line in file:
                    if '=' in line:
                        key, value = line.strip().split('=', 1)
                        properties[key.strip()] = value.strip()

                hostname = properties.get('hostname', 'localhost')
                dbname = properties.get('dbname', 'project_management_system')
                username = properties.get('username', 'root')
                password = properties.get('password', '')
                port = properties.get('port', '3306')

                return f"mysql+pymysql://{username}:{password}@{hostname}:{port}/{dbname}"
        except FileNotFoundError:
            raise Exception("Property file not found")
        except Exception as e:
            raise Exception(f"Error reading property file: {str(e)}")