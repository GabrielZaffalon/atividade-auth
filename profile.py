import os
import sys
import requests
from dotenv import load_dotenv

load_dotenv()
BASE = "https://api.wagnerloch.com.br"
LIMIT_TIME = 10


def mascarar(secret):
    if not secret:
        return "(vazio)"
    if len(secret) <= 8:
        return "*" * len(secret)
    return f"{secret[:4]}...{secret[-4:]}"


email = os.getenv("API_EMAIL")
password = os.getenv("API_SENHA")
missing = [nome for nome, value in [("API_EMAIL", email), ("API_SENHA", password)] if not value]
if missing:
    print("Erro: defina " + " e ".join(missing) + " no .env antes de executar.")
    sys.exit(1)

credentials = {"email": email, "password": password}
response = requests.post(f"{BASE}/auth/login", json=credentials, timeout=LIMIT_TIME)
response.raise_for_status()

data = response.json()
print("Campos da resposta do login:", list(data.keys()))
token = data["token"]
print("Token obtido:", mascarar(token))

profile = requests.get(
    f"{BASE}/auth/profile",
    headers={"Authorization": f"Bearer {token}"},
    timeout=LIMIT_TIME,
)

if profile.status_code == 401:
    print("[erro] 401: credencial ausente, errada ou expirada.")
elif profile.status_code == 403:
    print("[erro] 403: credencial valida, mas sem permissao.")
else:
    profile.raise_for_status()
    print("Perfil:", profile.json())