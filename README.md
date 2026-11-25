# Sistema de Gestão Hospitalar - Triagem e Atendimento

## Descrição
Sistema web para gestão hospitalar implementando estruturas de dados próprias:
- **Tabela Hash** (1.0 ponto): Localização de pacientes por ID
- **Árvore Rubro-Negra** (1.5 pontos): Ordenação por ordem de chegada
- **2 Min-Heaps** (2.0 pontos): Priorização de pacientes e médicos
- **Integração** (1.5 pontos): Sincronização entre estruturas
- **Interface Web** (1.0 ponto): Interface completa de gestão
- **Testes e Documentação** (1.0 ponto): Validação e apresentação

**Total: 8.0 pontos**

## Tecnologias
- Python 3.x
- Flask (backend)
- HTML/CSS/JavaScript (frontend)

## Estrutura do Projeto
```
garridop2/
├── structures/
│   ├── hash_table.py      # Tabela Hash
│   ├── red_black_tree.py  # Árvore Rubro-Negra
│   └── min_heap.py        # Min-Heap (pacientes e médicos)
├── services/
│   └── hospital_service.py # Integração das estruturas
├── api/
│   └── app.py             # API Flask
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── app.js
├── templates/
│   └── index.html
├── tests/
│   ├── test_hash.py
│   ├── test_tree.py
│   ├── test_heap.py
│   └── test_integration.py
├── requirements.txt
└── README.md
```

## Complexidade das Operações

### Tabela Hash
- **Inserir**: O(1) médio, O(n) pior caso (redimensionamento)
- **Buscar**: O(1) médio, O(n) pior caso
- **Remover**: O(1) médio, O(n) pior caso
- **Redimensionamento**: O(n)

### Árvore Rubro-Negra
- **Inserir**: O(log n)
- **Buscar**: O(log n)
- **Remover**: O(log n)
- **Percurso em ordem**: O(n)
- **Validação**: O(n)

### Min-Heap
- **Inserir**: O(log n)
- **Remover raiz**: O(log n)
- **Alterar prioridade**: O(log n)
- **Validação**: O(n)

## Como Executar

1. Instalar dependências:
```bash
pip install -r requirements.txt
```

2. Executar a aplicação:
```bash
python app.py
```

3. Acessar: http://localhost:5000

## Testes
```bash
python tests/test_hash.py
python tests/test_tree.py
python tests/test_heap.py
python tests/test_integration.py
```

## Cenários de Teste

### Teste A - Colisão
Cadastrar dois IDs que caiam no mesmo bucket (ex: 5 e 15 com capacidade 10) e localizar os dois.

### Teste B - Prioridade
Reclassificar um paciente e mostrar quem vira a raiz do heap.

### Teste C - Balanceamento
Médicos com cargas diferentes, chamar pacientes e mostrar qual médico é escolhido.

## Regras de Negócio

- **Cadastrar**: ID único → Hash, Rubro-Negra, Heap
- **Localizar**: Consulta pela Hash
- **Reclassificar**: Altera prioridade no Heap sem duplicar
- **Atender**: Remove raiz do heap de pacientes e do heap de médicos
- **Concluir**: Contador do médico sobe, volta ao heap
- **Listar**: Percurso em ordem da Rubro-Negra
- **Cancelar**: Remove por ID das três estruturas

## Consistência
Todas as operações são atômicas. Se uma inserção falhar, rollback é aplicado. Não há registros órfãos nem duplicados.
