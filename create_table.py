import sqlite3


def create_table(cursor, query_positions):
    cursor.execute(query_positions)


query_vehicles = '''CREATE TABLE IF NOT EXISTS vehicles (
            id INTEGER, dataCadastrado TEXT, status TEXT,
            anoFabricacao INTEGER, anoModelo INTEGER, placa TEXT,
            marca TEXT, modelo TEXT, cor TEXT, descricao TEXT, tipo TEXT,
            proprietario TEXT)
            '''

query_positions = '''CREATE TABLE IF NOT EXISTS positions (
            id INTEGER, placa TEXT, dataEquipamento TEXT, latitude REAL,
            longitude REAL, endereco TEXT, date_request TEXT, 
            time_request INTEGER)
            '''

# Connection to DB 
conn = sqlite3.Connection('tracker.db')
cursor = conn.cursor()

# Create table
create_table(cursor, query_vehicles)
create_table(cursor, query_positions)