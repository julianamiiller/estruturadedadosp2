# SIGAE — Sistema Integrado de Gestão e Atendimento Hospitalar

O **SIGAE** é um sistema web desenvolvido para gerenciar o fluxo de triagem, filas de espera e atendimento médico em ambiente hospitalar. Todas as operações são executadas em memória utilizando estruturas de dados implementadas em Python, sem dependência de banco de dados externo.

## Funcionalidades

- **Triagem e Classificação de Risco:** Cadastro de pacientes seguindo os 5 níveis do Protocolo de Manchester (1 = Emergência até 5 = Não Urgente), com suporte à reclassificação dinâmica de prioridade e cancelamento.
- **Busca Unificada de Pacientes:** Localização rápida de prontuários por ID numérico ou por nome (busca exata ou parcial).
- **Gestão do Corpo Clínico:** Cadastro de médicos no plantão, seleção automática do profissional com menor carga de atendimentos e consulta em tempo real da disponibilidade de qualquer médico (disponível ou em atendimento).
- **Controle de Atendimento:** Chamada simultânea do paciente mais urgente e do médico mais disponível, acompanhamento do atendimento ativo e liberação automática do médico após a conclusão.
- **Monitoramento de Filas e Estruturas:** Visualização em tempo real da fila por prioridade, da ordem cronológica de chegada e do estado interno da Tabela Hash, da Árvore Rubro-Negra e dos Min-Heaps.
- **Validação de Integridade:** Verificação automática da consistência entre todas as estruturas em memória e simulação de colisões na Tabela Hash.

## Tecnologias

- **Backend:** Python 3.x, Flask e Flask-CORS
- **Frontend:** HTML5, CSS3 e JavaScript

## Arquitetura do Projeto

```text
estruturadedadosp2/
├── app.py                     # API REST em Flask e servidor da interface web
├── requirements.txt           # Dependências do projeto
├── structures/
│   ├── hash_table.py          # Tabela Hash com encadeamento e redimensionamento
│   ├── red_black_tree.py      # Árvore Rubro-Negra para ordenação por chegada
│   └── min_heap.py            # Min-Heaps indexados (pacientes e médicos)
├── services/
│   └── hospital_service.py    # Orquestração atômica e regras de negócio
├── templates/
│   └── index.html             # Interface principal do sistema
├── static/
│   ├── css/style.css          # Estilos da aplicação
│   └── js/app.js              # Lógica de interação no navegador
└── tests/
    ├── test_hash.py           # Testes da Tabela Hash
    ├── test_tree.py           # Testes da Árvore Rubro-Negra
    ├── test_heap.py           # Testes dos Min-Heaps
    └── test_integration.py    # Testes de integração do sistema
```

## Como Executar

1. Instale as dependências:
```bash
pip install -r requirements.txt
```

2. Inicie o servidor:
```bash
python app.py
```

3. Acesse no navegador:
```text
http://localhost:5000
```

## Testes

Para validar as estruturas e os fluxos do sistema, execute:

```bash
python tests/test_hash.py
python tests/test_tree.py
python tests/test_heap.py
python tests/test_integration.py
```
