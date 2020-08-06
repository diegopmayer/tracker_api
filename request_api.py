import pandas as pd 
from requests import post
import json, pickle, datetime
from sqlalchemy import create_engine
from time import sleep


# Authentication
with open('user_logon.pkl', 'rb') as file:
    url_logon, url_vehicles, url_position, headers, handshake = pickle.load(file)

# json to dataframe
def json_to_dataframe(json_data):
    df = pd.DataFrame(json_data['object']).copy()
    return df

# Token
def get_token():
        
    response_logon = post(url_logon,
                            data=json.dumps(handshake),
                            headers=headers) # response array object
    token = {"token":response_logon.json()['object']
            ['token']} # store token form object
    return token

# request vehicles
def request_vehicles():
    token = get_token()
    response_vehicles = post(url_vehicles, headers=token)
    obj_vehicle = response_vehicles.json()
    df_vehicles = json_to_dataframe(obj_vehicle)
    return df_vehicles

# request positions
def request_positions():
    token = get_token()
    response_position = post(url_position, headers=token)
    obj_position = response_position.json()
    df_positions = json_to_dataframe(obj_position)
    return df_positions


# Data Preparation
# Positions
def data_preparation(df_pos_sel):
    drop_list_positions = [
        'codigorf', 'odometroGps', 'dataAquisicao', 'distanciaKmFrete',  
        'kmManual', 'horimetroManual', 'horimetroAtual', 'kmAtual',            
        'statusVenda', 'dataAtivado', 'dataCadastrado', 'dataCancelado', 
        'fuso', 'deletado', 'status', 'finalizado', 'renavam',           
        'vin', 'anoFabricacao', 'anoModelo', 'dataInstalacao', 'tipoMonitoramento',
        'marca', 'modelo', 'cor', 'descricao', 'frota', 'tipo', 'usuarioCriacao',  
        'proprietario', 'grupos', 'assistencia', 'motoristas'
    ]

    # dropping columns
    df_pos_sel = df_pos_sel.drop(drop_list_positions, axis=1).copy()

    # getting data from dictionary
    df_pos_sel['numeroStr'] = df_pos_sel['dispositivos'].apply(
        lambda x: x[0]['numeroStr'])
    df_pos_sel['posicoes'] = pd.DataFrame(df_pos_sel['dispositivos'].apply(
        lambda x: x[0]['posicoes']))

    df_pos = pd.DataFrame()
    for i in df_pos_sel['posicoes']:
        try:
            df = pd.DataFrame(i)[['sequencia', 'dataEquipamento', 'latitude', 'longitude', 'endereco', 'numerostr']]
            df = df[df['sequencia'] == df['sequencia'].max()][0:1]
            df_pos = pd.concat([df_pos, df], axis=0, ignore_index=True)
        except KeyError:
            df = pd.DataFrame([['0', '0', '0', '0', '0', '0']], columns=['sequencia', 
                    'dataEquipamento', 'latitude', 'longitude', 'endereco', 'numerostr'])
            df_pos = pd.concat([df_pos, df], axis=0, ignore_index=True)

    # Converting datatype
    df_pos_sel = pd.concat([df_pos_sel, df_pos], axis=1)
    df_pos_sel = df_pos_sel.drop(['dispositivos', 'posicoes', 'numerostr',
                'proprietarioId', 'sequencia', 'numeroStr'], axis=1).copy()
    df_pos_sel['dataEquipamento'] = df_pos_sel['dataEquipamento'].astype(int).copy()
    df_pos_sel['dataEquipamento'] = df_pos_sel['dataEquipamento'].apply(
        lambda x: datetime.datetime.fromtimestamp(x/1000).date()).copy()
    df_pos_sel['latitude'] = df_pos_sel['latitude'].astype(float).copy()
    df_pos_sel['longitude'] = df_pos_sel['longitude'].astype(float).copy()

    # Getting the date and hour in exactly time request
    df_pos_sel['date_request'] = datetime.date.today()
    df_pos_sel['time_request'] = datetime.datetime.now().hour
    
    return df_pos_sel

# Routine execution
def main():
    # Insertion Database
    df_positions = request_positions()
    data_to_db = data_preparation(df_positions)
    engine = create_engine(
        'sqlite:////home/python/PycharmProjects/Projects/tracker/tracker.db',
        echo=False)
    data_to_db.to_sql('positions', con=engine, if_exists='append', index=False)

while True:
    if __name__=='__main__':
        print(f'Starting...')
        print(f'..., {datetime.datetime.now()}')
        main()
        print(f'Finished')
        print(f'Collected from API, {datetime.datetime.now()}')
        sleep(60*60)