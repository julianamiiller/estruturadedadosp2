# Guia de Organização de Commits para o Grupo

Este documento explica como organizar os commits do projeto para que cada membro do grupo possa ter sua contribuição reconhecida.

## Estratégia 1: Usar `git commit --author` (Mais Simples)

Você pode fazer todo o código e depois atribuir commits a diferentes pessoas usando o flag `--author`.

### Formato do Author
```
--author="Nome <email@exemplo.com>"
```

### Exemplo de Uso
```bash
git commit --author="João Silva <joao@email.com>" -m "Implementa Tabela Hash"
git commit --author="Maria Santos <maria@email.com>" -m "Implementa Árvore Rubro-Negra"
git commit --author="Pedro Costa <pedro@email.com>" -m "Implementa Min-Heaps"
git commit --author="Ana Oliveira <ana@email.com>" -m "Implementa Interface Web"
```

## Estratégia 2: Dividir por Branches (Mais Organizada)

Cada membro trabalha em um branch separado e depois faz merge.

### Passo a Passo

1. **Inicializar o repositório**
```bash
git init
git add .
git commit -m "Initial commit"
```

2. **Criar branches para cada membro**
```bash
git branch hash-table
git branch red-black-tree
git branch min-heaps
git branch integration
git branch frontend
```

3. **Para cada membro, fazer checkout e commitar**
```bash
# Membro 1 - Hash Table
git checkout hash-table
git add structures/hash_table.py
git commit -m "Implementa Tabela Hash com encadeamento"

# Membro 2 - Árvore Rubro-Negra
git checkout red-black-tree
git add structures/red_black_tree.py
git commit -m "Implementa Árvore Rubro-Negra"

# Membro 3 - Heaps
git checkout min-heaps
git add structures/min_heap.py
git commit -m "Implementa Min-Heaps para pacientes e médicos"

# Membro 4 - Integração
git checkout integration
git add services/hospital_service.py
git commit -m "Implementa serviço de integração"

# Membro 5 - Frontend
git checkout frontend
git add templates/index.html static/css/style.css static/js/app.js
git commit -m "Implementa interface web completa"
```

4. **Fazer merge de todos**
```bash
git checkout main
git merge hash-table
git merge red-black-tree
git merge min-heaps
git merge integration
git merge frontend
```

## Estratégia 3: Commits Sequenciais no Mesmo Branch (Mais Rápido)

Fazer todos os commits sequencialmente no mesmo branch, cada um com autor diferente.

### Exemplo de Script

```bash
#!/bin/bash

# Commit 1: Estrutura base
git add requirements.txt .gitignore README.md
git commit --author="Membro 1 <membro1@email.com>" -m "Cria estrutura base do projeto"

# Commit 2: Tabela Hash
git add structures/hash_table.py
git commit --author="Membro 2 <membro2@email.com>" -m "Implementa Tabela Hash com encadeamento e redimensionamento"

# Commit 3: Árvore Rubro-Negra
git add structures/red_black_tree.py
git commit --author="Membro 3 <membro3@email.com>" -m "Implementa Árvore Rubro-Negra com chave composta"

# Commit 4: Min-Heaps
git add structures/min_heap.py
git commit --author="Membro 4 <membro4@email.com>" -m "Implementa Min-Heaps para pacientes e médicos"

# Commit 5: Serviço de Integração
git add services/hospital_service.py
git commit --author="Membro 1 <membro1@email.com>" -m "Implementa serviço de integração com regras de negócio"

# Commit 6: API Flask
git add api/app.py
git commit --author="Membro 2 <membro2@email.com>" -m "Cria API Flask com todos os endpoints"

# Commit 7: Interface Web
git add templates/index.html static/css/style.css static/js/app.js
git commit --author="Membro 3 <membro3@email.com>" -m "Implementa interface web completa"

# Commit 8: Testes Hash
git add tests/test_hash.py
git commit --author="Membro 4 <membro4@email.com>" -m "Cria testes unitários para Tabela Hash"

# Commit 9: Testes Árvore
git add tests/test_tree.py
git commit --author="Membro 1 <membro1@email.com>" -m "Cria testes unitários para Árvore Rubro-Negra"

# Commit 10: Testes Heap
git add tests/test_heap.py
git commit --author="Membro 2 <membro2@email.com>" -m "Cria testes unitários para Min-Heaps"

# Commit 11: Testes Integração
git add tests/test_integration.py
git commit --author="Membro 3 <membro3@email.com>" -m "Cria testes de integração do sistema"
```

## Divisão Sugerida de Pontos por Membro

Assumindo 4 membros no grupo:

### Membro 1 (2.0 pontos)
- Tabela Hash (1.0 ponto)
- Serviço de Integração (1.0 ponto)
- Testes de Hash (parte dos 1.0 ponto de testes)

**Commits:**
1. `structures/hash_table.py` - Tabela Hash completa
2. `services/hospital_service.py` - Serviço de integração
3. `tests/test_hash.py` - Testes da Hash

### Membro 2 (2.0 pontos)
- Árvore Rubro-Negra (1.5 pontos)
- Testes da Árvore (parte dos 1.0 ponto de testes)

**Commits:**
1. `structures/red_black_tree.py` - Árvore Rubro-Negra completa
2. `tests/test_tree.py` - Testes da Árvore

### Membro 3 (2.0 pontos)
- Min-Heaps (2.0 pontos)
- Testes dos Heaps (parte dos 1.0 ponto de testes)

**Commits:**
1. `structures/min_heap.py` - Min-Heaps completos
2. `tests/test_heap.py` - Testes dos Heaps

### Membro 4 (2.0 pontos)
- Interface Web (1.0 ponto)
- API Flask (parte da integração)
- Testes de Integração (parte dos 1.0 ponto de testes)

**Commits:**
1. `api/app.py` - API Flask
2. `templates/index.html` - HTML da interface
3. `static/css/style.css` - Estilos
4. `static/js/app.js` - JavaScript
5. `tests/test_integration.py` - Testes de integração

## Script Completo para Executar

Salve como `organize_commits.sh` e execute:

```bash
#!/bin/bash

# Configurar autores (substitua pelos dados reais)
MEMBRO1="Nome Membro 1 <email1@exemplo.com>"
MEMBRO2="Nome Membro 2 <email2@exemplo.com>"
MEMBRO3="Nome Membro 3 <email3@exemplo.com>"
MEMBRO4="Nome Membro 4 <email4@exemplo.com>"

# Inicializar git se necessário
if [ ! -d ".git" ]; then
    git init
    git add .
    git commit -m "Initial commit"
fi

# Membro 1 - Hash Table
git add structures/__init__.py structures/hash_table.py
git commit --author="$MEMBRO1" -m "feat: Implementa Tabela Hash com encadeamento e redimensionamento

- Função hash: ID % capacidade
- Tratamento de colisões com encadeamento
- Redimensionamento automático quando fator de carga > 0.75
- Operações: inserir, buscar, remover
- Validação de integridade"

# Membro 2 - Árvore Rubro-Negra
git add structures/red_black_tree.py
git commit --author="$MEMBRO2" -m "feat: Implementa Árvore Rubro-Negra com chave composta

- Chave composta: (horário, ID) para ordenação por chegada
- Inserção com recoloração e rotações
- Busca, remoção com balanceamento
- Percurso em ordem (in-order)
- Validação das propriedades rubro-negras"

# Membro 3 - Min-Heaps
git add structures/min_heap.py
git commit --author="$MEMBRO3" -m "feat: Implementa Min-Heaps para pacientes e médicos

- Heap de pacientes: prioridade 1-5, desempate por chegada e ID
- Heap de médicos: menor carga, desempate por cadastro e ID
- Alteração de prioridade em O(log n)
- Classes específicas: PatientHeap e DoctorHeap
- Validação de propriedade do heap"

# Membro 1 - Serviço de Integração
git add services/__init__.py services/hospital_service.py
git commit --author="$MEMBRO1" -m "feat: Implementa serviço de integração das estruturas

- Sincronização entre Hash, Árvore e Heaps
- Operações atômicas com rollback
- Cadastro de pacientes e médicos
- Reclassificação de prioridade
- Chamada e conclusão de atendimento
- Validação de consistência entre estruturas"

# Membro 4 - API Flask
git add api/__init__.py api/app.py
git commit --author="$MEMBRO4" -m "feat: Cria API Flask com todos os endpoints

- Endpoints para cadastro de pacientes e médicos
- Busca por ID (usando apenas Hash)
- Reclassificação e cancelamento
- Chamada e conclusão de atendimento
- Listagem por chegada e prioridade
- Validação e estatísticas do sistema"

# Membro 4 - Interface Web (HTML)
git add templates/index.html
git commit --author="$MEMBRO4" -m "feat: Implementa interface web HTML

- Formulários de cadastro de pacientes e médicos
- Operações: busca, reclassificação, cancelamento
- Controles de atendimento
- Painéis de visualização das estruturas
- Listas por prioridade e chegada
- Botões de validação e testes"

# Membro 4 - Interface Web (CSS)
git add static/css/style.css
git commit --author="$MEMBRO4" -m "feat: Implementa estilos CSS da interface

- Design moderno e responsivo
- Gradientes e sombras
- Layout em grid
- Cores por prioridade
- Animações e transições"

# Membro 4 - Interface Web (JavaScript)
git add static/js/app.js
git commit --author="$MEMBRO4" -m "feat: Implementa lógica JavaScript da interface

- Chamadas à API
- Atualização dinâmica das visualizações
- Manipulação de formulários
- Tratamento de erros
- Atualização em tempo real"

# Membro 1 - Testes Hash
git add tests/__init__.py tests/test_hash.py
git commit --author="$MEMBRO1" -m "test: Cria testes unitários para Tabela Hash

- Teste de inserção
- Teste de busca
- Teste de remoção
- Teste de colisão
- Teste de redimensionamento
- Teste de validação
- Teste de atualização"

# Membro 2 - Testes Árvore
git add tests/test_tree.py
git commit --author="$MEMBRO2" -m "test: Cria testes unitários para Árvore Rubro-Negra

- Teste de inserção
- Teste de busca
- Teste de remoção
- Teste de percurso em ordem
- Teste de validação
- Teste de altura negra
- Teste de duplicação"

# Membro 3 - Testes Heap
git add tests/test_heap.py
git commit --author="$MEMBRO3" -m "test: Cria testes unitários para Min-Heaps

- Teste de inserção
- Teste de extração do mínimo
- Teste de peek
- Teste de alteração de prioridade
- Teste de remoção
- Teste de validação
- Teste de heaps específicos (pacientes e médicos)
- Teste de critérios de desempate"

# Membro 4 - Testes Integração
git add tests/test_integration.py
git commit --author="$MEMBRO4" -m "test: Cria testes de integração do sistema

- Teste de cadastro de paciente
- Teste de cadastro de médico
- Teste de busca por ID
- Teste de reclassificação
- Teste de chamada de paciente
- Teste de conclusão de atendimento
- Teste de listagem por chegada
- Teste de cancelamento
- Teste de consistência
- Teste de ordenação por prioridade
- Teste de seleção de médico
- Teste de rollback"

echo "Commits organizados com sucesso!"
echo "Verifique com: git log --pretty=format:'%h - %an (%ae): %s'"
```

## Como Verificar os Commits

```bash
# Ver todos os commits com autores
git log --pretty=format:"%h - %an (%ae): %s"

# Ver gráfico de commits
git log --graph --pretty=format:"%h - %an: %s" --all

# Ver estatísticas por autor
git shortlog -sn
```

## Dicas Importantes

1. **Configure o git user antes de começar:**
```bash
git config user.name "Seu Nome"
git config user.email "seu@email.com"
```

2. **Use mensagens de commit consistentes:**
- `feat:` para novas funcionalidades
- `test:` para testes
- `fix:` para correções
- `docs:` para documentação

3. **Verifique se tudo está funcionando antes de commitar:**
```bash
# Rodar todos os testes
python tests/test_hash.py
python tests/test_tree.py
python tests/test_heap.py
python tests/test_integration.py
```

4. **Se precisar alterar um commit:**
```bash
# Alterar o último commit
git commit --amend --author="Novo Autor <novo@email>"

# Alterar commits específicos (mais complexo)
git rebase -i HEAD~n
```

## Recomendação

Para o seu caso, **a Estratégia 3 (Commits Sequenciais)** é a mais simples e eficaz. Você pode:
1. Fazer todo o código
2. Usar o script acima para organizar os commits
3. Substituir os nomes e emails pelos dos membros reais
4. Executar o script
5. Verificar com `git log`

Isso garante que cada membro tenha seus commits reconhecidos sem precisar configurar branches complexos.
