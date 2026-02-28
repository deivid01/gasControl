import requests

BASE_URL = 'http://127.0.0.1:8000/api'
USERS = [
    ('deivid', 'MASTER'),
    ('wellington', 'MASTER'),
    ('paulo', 'MASTER'),
    ('sandra', 'ENCARREGADO'),
    ('alessandra', 'ENCARREGADO'),
    ('yasmin', 'OPERADOR'),
    ('otilia', 'OPERADOR')
]
PASSWORD = '123456'

def test_api():
    print("Iniciando testes da API de Registro de Gás...")
    
    # Primeiro login com master para pegar as lojas e gas types
    res = requests.post(f"{BASE_URL}/token/", json={"username": "deivid", "password": PASSWORD})
    if res.status_code != 200:
        print("Falha ao logar com deivid para setup.")
        return
    token = res.json()['access']
    headers = {"Authorization": f"Bearer {token}"}
    
    stores_req = requests.get(f"{BASE_URL}/stores/", headers=headers)
    gas_req = requests.get(f"{BASE_URL}/gas-types/", headers=headers)
    
    if stores_req.status_code != 200 or gas_req.status_code != 200:
        print("Falha ao buscar lojas ou tipos de gas do backend (servidor pode estar offline).")
        return
        
    stores = stores_req.json()
    gas_types = gas_req.json()
    
    if not stores or not gas_types:
        print("Bases de dados de Loja ou Gás vazias.")
        return
        
    print(f"Encontradas {len(stores)} lojas e {len(gas_types)} tipos de gas.")
    
    gas_id = gas_types[0]['id']
    
    errors_found = 0
    success_count = 0
    
    for username, role in USERS:
        print(f"\n--- Testando usuario: {username} ({role}) ---")
        # Login
        res = requests.post(f"{BASE_URL}/token/", json={"username": username, "password": PASSWORD})
        if res.status_code != 200:
            print(f"  [ERRO] Falha no login de {username}")
            errors_found += 1
            continue
            
        user_token = res.json()['access']
        user_headers = {"Authorization": f"Bearer {user_token}"}
        
        for store in stores:
            payload = {
                "store": store['id'],
                "pdv": "CX Teste",
                "operator": username.capitalize(),
                "retriever_name": "Testador Automático",
                "gas_type": gas_id,
                "quantity": 1
            }
            create_res = requests.post(f"{BASE_URL}/withdrawals/", json=payload, headers=user_headers)
            
            if create_res.status_code == 201:
                print(f"  [OK] Retirada na loja {store['name']} criada com sucesso.")
                success_count += 1
            else:
                print(f"  [ERRO] Falha ao criar retirada na loja {store['name']}: {create_res.status_code} - {create_res.text}")
                errors_found += 1
                
    print(f"\nResumo: {success_count} sucessos, {errors_found} erros.")

if __name__ == "__main__":
    try:
        test_api()
    except Exception as e:
        print(f"Erro ao executar o teste: {e}")
