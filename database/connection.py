import os
import getpass
from dotenv import load_dotenv  # pip install python-dotenv
import mysql.connector
from mysql.connector import Error
 
 
class secure_db_connect:
 
    def __init__(self, host=None, user=None, password=None, database=None):
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        self.env_path = os.path.join(project_root, '.env')
 
        # Load whatever is already saved in .env into the environment
        if os.path.exists(self.env_path):
            load_dotenv(self.env_path)
 
        self.db_config = {
            'host': host or os.getenv('MYSQL_HOST', 'localhost'),
            'user': user or os.getenv('MYSQL_USER'),
            'password': password or os.getenv('MYSQL_PASSWORD'),
            'database': database or os.getenv('MYSQL_DATABASE', 'security_vault')
        }
 
        if not self.db_config['user']:
            self.db_config['user'] = input('Enter MariaDB username: ').strip()
            self._save_env('MYSQL_USER', self.db_config['user'])
 
        if not self.db_config['password']:
            self.db_config['password'] = getpass.getpass('Enter MariaDB password: ')
            self._save_env('MYSQL_PASSWORD', self.db_config['password'])
 
        if os.getenv('MYSQL_UNIX_SOCKET'):
            self.db_config['unix_socket'] = os.getenv('MYSQL_UNIX_SOCKET')
 
        # (removed the dead "enter your name" block — user is always set by this point)
 
    def _save_env(self, key, value):
        env_file = self.env_path
        if not os.path.exists(env_file):
            with open(env_file, 'w', encoding='utf-8') as file:
                file.write(f'{key}="{value}"\n')
            return
 
        with open(env_file, 'r', encoding='utf-8') as file:
            lines = file.readlines()
 
        updated = False
        new_lines = []
        for line in lines:
            if line.strip().startswith(f'{key}='):
                new_lines.append(f'{key}="{value}"\n')
                updated = True
            else:
                new_lines.append(line)
 
        if not updated:
            new_lines.append(f'{key}="{value}"\n')
 
        with open(env_file, 'w', encoding='utf-8') as file:
            file.writelines(new_lines)
 
    def connect(self):
        try:
            return mysql.connector.connect(**self.db_config)
        except Error as error:
            print(f"you have gotten error {error}")
            raise
 
