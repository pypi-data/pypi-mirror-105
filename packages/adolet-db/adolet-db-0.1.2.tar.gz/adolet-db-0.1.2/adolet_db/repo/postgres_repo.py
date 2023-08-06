import requests
import pickle
import os
from typing import Dict, Any, TypeVar, List
from adolet_db.common import is_args_none

CACHE_FILE = 'cache_postgres_repo.cache'


class PostgresRepo:
    def __init__(self, email: str, api_key: str):
        self.email = email
        self.api_key = api_key
        self.URL = 'http://api.postgres.adolet.com'
        # Save connection details upon instantiation
        self.conn_details: Dict[str, Any] = self.authenticate_db()

    def clear_cache(self) -> bool:
        if os.path.exists(CACHE_FILE):
            os.remove(CACHE_FILE)
            print("SUCCESS - Cache has been cleared")
            return True

        print("FAILURE - There is no cache to be clear")
        return False

    def authenticate_db(self) -> Dict[str, Any]:
        try:
            params = {'email': self.email, 'api_key': self.api_key}
            res = requests.get(
                f'{self.URL}/authenticate-db-api',
                params=params,
            )

            res = res.json()
            return res

        except:
            raise Exception(
                "There is an error with .authenticate_db() in postgres_repo.py"
            )

    def insert(self, table_name: str, dto: Dict[str, Any]) -> Dict[str, Any]:
        is_args_none(args=list(locals().values()))
        try:
            dto.pop('id')
            params = {
                'email': self.email,
                'api_key': self.api_key,
                'table_name': table_name,
                'columns': list(dto.keys()),
                'values': list(dto.values()),
            }

            # Send connection details in REST API if given
            if self.conn_details is not None:
                params['dbname'] = self.conn_details['dbname']
                params['user'] = self.conn_details['user']
                params['password'] = self.conn_details['password']
                params['host'] = self.conn_details['host']
                params['port'] = self.conn_details['port']

            res = requests.get(f'{self.URL}/insert-api', params=params)
            res = res.json()
            return res

        except:
            raise Exception(
                "There is an error with .insert() in postgres_repo.py")

    def delete(self, table_name: str, id: int) -> Dict[str, Any]:
        is_args_none(args=list(locals().values()))
        try:
            params = {
                'email': self.email,
                'api_key': self.api_key,
                'table_name': table_name,
                'id': int(id),
            }

            # Send connection details in REST API if given
            if self.conn_details is not None:
                params['dbname'] = self.conn_details['dbname']
                params['user'] = self.conn_details['user']
                params['password'] = self.conn_details['password']
                params['host'] = self.conn_details['host']
                params['port'] = self.conn_details['port']

            res = requests.get(f'{self.URL}/delete-api', params=params)
            res = res.json()
            return res

        except:
            raise Exception(
                "There is an error with .delete() in postgres_repo.py")

    def run_query(self, sql_query: str) -> List[Dict[str, Any]]:
        is_args_none(args=list(locals().values()))
        try:
            params = {
                'email': self.email,
                'api_key': self.api_key,
                'sql_query': sql_query,
            }

            # Send connection details in REST API if given
            if self.conn_details is not None:
                params['dbname'] = self.conn_details['dbname']
                params['user'] = self.conn_details['user']
                params['password'] = self.conn_details['password']
                params['host'] = self.conn_details['host']
                params['port'] = self.conn_details['port']

            res = requests.get(f'{self.URL}/run-query-api', params=params)
            res = res.json()
            return res

        except:
            raise Exception(
                "There is an error with .run_query() in postgres_repo.py")
