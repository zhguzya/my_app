from flask import Flask, request
import requests
from flask_restx import Resource, Api
import time 
# from hh import get_hh_vacancy
# from hua_token import refresh_access_token
from mikrotik import get_traffic_from_mikrotik, get_dhcp_table_from_mikrotik
from db import create_db_tables, get_data_from_db
from config import DATABASE_NAME, SCHEMA_FILE

create_db_tables(DATABASE_NAME, SCHEMA_FILE)

app = Flask(__name__)
api = Api(app)

'''
@api.route('/hello')
class HelloWorld(Resource):
    def get(self):
        #time.sleep(5)
        return {'msg': 'hello, world'}

@api.route('/hh')
class HH(Resource):
    def get(self):
        url = 'https://api.hh.ru/vacancies'
        #time.sleep(5)
        return get_hh_vacancy(url)

@api.route('/hua')
class Hua(Resource):
    def get(self):
        return refresh_access_token()
'''

@api.route('/get_mikrotik_data_from_db')
class MikrotikDataFromDB(Resource):
    def get(self):
        return get_data_from_db()
    
# @api.route('/get_dhcp_table_mikrotik_from_db')
# class DhcpTableDB(Resource):
#     def get(self):
#         return get_dhcp_table_from_db()
    

@api.route('/refresh_data_from_mikrotik')
class RefreshDataFromMikrotik(Resource):
    def get(self):
        dhcp_mikrotik = get_dhcp_table_from_mikrotik()
        traffic_mikrotik = get_traffic_from_mikrotik()
        return {"dhcp": dhcp_mikrotik, "traffic": traffic_mikrotik, "msg": "Data updated"}

if __name__ == '__main__':
    # # app.run(host='0.0.0.0', port=8181, debug = True)
    app.run(debug = True)