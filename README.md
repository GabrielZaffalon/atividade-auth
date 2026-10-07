# atividade-auth

Atividade da disciplina **Automação e Programabilidade em Redes**. O script faz o fluxo de autenticação de uma API REST com token JWT: login, obtenção do token e consulta do perfil em uma rota protegida usando o cabeçalho `Authorization: Bearer`.

As credenciais ficam em um arquivo `.env`, carregado em tempo de execução, e não aparecem no código.

## Fluxo

| Etapa | Método | Endpoint | Resposta esperada |
|---|---|---|---|
| Criar conta | `POST` | `/auth/register` | `201 Created` |
| Login | `POST` | `/auth/login` | `200 OK` com o campo `token` |
| Consultar perfil | `GET` | `/auth/profile` | `200 OK` com token, `401 Unauthorized` sem token |

Base da API: `https://api.wagnerloch.com.br`

A conta precisa ser criada uma vez antes de rodar o script, pelo Postman ou Insomnia. O script cobre o login e a consulta do perfil.

## Estrutura

```
atividade-auth/
├── profile.py      # script principal
├── .env.exemplo    # modelo das variáveis de ambiente
├── .gitignore      # ignora .env e .venv
└── README.md
```

## Requisitos

- Python 3.10 ou superior
- Bibliotecas `requests` e `python-dotenv`

## Como executar

**1. Clonar o repositório e entrar na pasta**

```bash
git clone <url-do-repositorio>
cd atividade-auth
```

**2. Criar e ativar o ambiente virtual**

Windows (PowerShell):

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

**3. Instalar as dependências**

```bash
python -m pip install requests python-dotenv
```

**4. Configurar as credenciais**

Copie o modelo e preencha com o e-mail e a senha da conta criada:

```powershell
copy .env.exemplo .env      # Windows
```

```bash
cp .env.exemplo .env        # Linux/macOS
```

```
API_EMAIL=seu@email.com
API_SENHA=sua-senha
```

**5. Rodar o script**

```bash
python profile.py
```

## Saída esperada

```
Campos da resposta do login: ['message', 'token']
Token obtido: eyJh...IrTs
Perfil: {'id': '...', 'name': 'Seu Nome', 'email': 'seu@email.com', 'createdAt': '...'}
```

O token é exibido mascarado, com apenas os quatro primeiros e os quatro últimos caracteres.

## Tratamento de erros

| Situação | Mensagem |
|---|---|
| `API_EMAIL` ou `API_SENHA` ausente no `.env` | `Erro: defina ... no .env antes de executar.` |
| Token ausente, inválido ou expirado | `[erro] 401: credencial ausente, errada ou expirada.` |
| Token válido, mas sem permissão | `[erro] 403: credencial valida, mas sem permissao.` |
| Outros erros HTTP (como credenciais erradas no login) | exceção do `raise_for_status()` com o código de status |

As requisições têm tempo limite de 10 segundos.

## Segurança

- O `.env` está no `.gitignore` e **não deve ser versionado**. Antes de cada commit, confira com `git status` que ele não aparece na lista.
- O token JWT emitido pela API expira em **1 hora**. Basta rodar o script de novo para obter um token novo.

## Autor

Gabriel Zaffalon
