# Como Executar o Projeto

## Pré-requisitos

1. **Python 3.8 ou superior** instalado
   - Verifique com: `python --version`
   - Se não tiver, baixe em: https://www.python.org/downloads/

## Passo a Passo

### 1. Abrir o Terminal

- Pressione `Win + R`
- Digite `cmd` e pressione Enter
- Ou abra o PowerShell

### 2. Navegar até o Diretório do Projeto

```cmd
cd C:\Users\Miiller\Desktop\garridop2
```

### 3. Criar Ambiente Virtual (Recomendado)

```cmd
python -m venv venv
```

### 4. Ativar o Ambiente Virtual

**No CMD:**
```cmd
venv\Scripts\activate
```

**No PowerShell:**
```cmd
venv\Scripts\Activate.ps1
```

*Se der erro no PowerShell sobre execution policy:*
```cmd
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 5. Instalar as Dependências

```cmd
pip install -r requirements.txt
```

Isso vai instalar:
- Flask 3.0.0
- Flask-CORS 4.0.0

### 6. Executar a Aplicação

```cmd
python app.py
```

Você verá algo como:
```
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://0.0.0.0:5000
```

### 7. Acessar a Aplicação

Abra seu navegador e acesse:
```
http://localhost:5000
```

## Rodar os Testes

### Testar Cada Estrutura Separadamente

**Tabela Hash:**
```cmd
python tests/test_hash.py
```

**Árvore Rubro-Negra:**
```cmd
python tests/test_tree.py
```

**Min-Heaps:**
```cmd
python tests/test_heap.py
```

**Integração:**
```cmd
python tests/test_integration.py
```

### Rodar Todos os Testes de Uma Vez

Crie um arquivo `run_all_tests.bat` na raiz do projeto:

```batch
@echo off
echo === Testes da Tabela Hash ===
python tests/test_hash.py
echo.
echo === Testes da Árvore Rubro-Negra ===
python tests/test_tree.py
echo.
echo === Testes do Min-Heap ===
python tests/test_heap.py
echo.
echo === Testes de Integração ===
python tests/test_integration.py
echo.
echo === Todos os testes concluídos ===
pause
```

Depois execute:
```cmd
run_all_tests.bat
```

## Parar a Aplicação

No terminal onde a aplicação está rodando, pressione `Ctrl + C`

## Desativar o Ambiente Virtual

```cmd
deactivate
```

## Estrutura do Projeto Após Execução

```
garridop2/
├── api/
│   └── app.py              # Servidor Flask (roda na porta 5000)
├── structures/
│   ├── hash_table.py       # Tabela Hash
│   ├── red_black_tree.py   # Árvore Rubro-Negra
│   └── min_heap.py         # Min-Heaps
├── services/
│   └── hospital_service.py # Integração das estruturas
├── templates/
│   └── index.html         # Interface web
├── static/
│   ├── css/
│   │   └── style.css      # Estilos
│   └── js/
│       └── app.js         # JavaScript
├── tests/
│   ├── test_hash.py        # Testes da Hash
│   ├── test_tree.py        # Testes da Árvore
│   ├── test_heap.py        # Testes dos Heaps
│   └── test_integration.py # Testes de integração
├── requirements.txt        # Dependências
├── README.md              # Documentação
└── COMMIT_GUIDE.md        # Guia de commits
```

## Funcionalidades da Interface

1. **Cadastro de Pacientes**
   - Nome e prioridade (1-5)
   - ID gerado automaticamente

2. **Cadastro de Médicos**
   - Nome do médico
   - ID gerado automaticamente

3. **Operações**
   - Buscar paciente por ID
   - Reclassificar prioridade
   - Cancelar paciente

4. **Atendimento**
   - Chamar próximo paciente
   - Concluir atendimento

5. **Visualização**
   - Tabela Hash (buckets e colisões)
   - Árvore Rubro-Negra (nós e cores)
   - Heap de Pacientes (fila por prioridade)
   - Heap de Médicos (médicos disponíveis)

6. **Listas**
   - Fila por prioridade
   - Ordem de chegada
   - Médicos disponíveis

7. **Validação**
   - Validar estruturas
   - Teste de colisão
   - Resetar sistema

## Solução de Problemas

### Erro: "python não é reconhecido"

**Solução:** Adicione Python ao PATH do Windows:
1. Pesquise "Editar variáveis de ambiente do sistema"
2. Clique em "Variáveis de Ambiente"
3. Em "Variáveis do sistema", edite "Path"
4. Adicione o caminho do Python (ex: `C:\Python39\` e `C:\Python39\Scripts\`)

### Erro: "pip não é reconhecido"

**Solução:** Use `python -m pip` em vez de `pip`
```cmd
python -m pip install -r requirements.txt
```

### Erro: Porta 5000 já em uso

**Solução 1:** Feche outros programas usando a porta 5000

**Solução 2:** Mude a porta em `api/app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

### Erro: Módulo não encontrado

**Solução:** Verifique se está no diretório correto e se instalou as dependências:
```cmd
cd C:\Users\Miiller\Desktop\garridop2
pip install -r requirements.txt
```

## Próximos Passos

Depois de testar localmente, quando quiser colocar no GitHub, me avise e eu te ajudo com:
- Criar repositório no GitHub
- Fazer o primeiro push
- Organizar os commits conforme o guia
- Configurar colaboradores
