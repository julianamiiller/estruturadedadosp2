"""
Testes unitários para Tabela Hash.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from structures.hash_table import HashTable


def test_hash_insert():
    """Testa inserção na tabela hash."""
    hash_table = HashTable(initial_capacity=10)
    
    # Inserir um item
    result = hash_table.insert(1, {'name': 'Teste 1'})
    assert result == True, "Inserção deve retornar True"
    assert hash_table.size == 1, "Tamanho deve ser 1"
    
    # Inserir outro item
    result = hash_table.insert(2, {'name': 'Teste 2'})
    assert result == True, "Inserção deve retornar True"
    assert hash_table.size == 2, "Tamanho deve ser 2"
    
    print("✓ test_hash_insert passou")


def test_hash_get():
    """Testa busca na tabela hash."""
    hash_table = HashTable(initial_capacity=10)
    
    hash_table.insert(1, {'name': 'Teste 1'})
    hash_table.insert(2, {'name': 'Teste 2'})
    
    # Buscar item existente
    result = hash_table.get(1)
    assert result is not None, "Deve encontrar o item"
    assert result['name'] == 'Teste 1', "Deve retornar o valor correto"
    
    # Buscar item inexistente
    result = hash_table.get(99)
    assert result is None, "Deve retornar None para item inexistente"
    
    print("✓ test_hash_get passou")


def test_hash_remove():
    """Testa remoção na tabela hash."""
    hash_table = HashTable(initial_capacity=10)
    
    hash_table.insert(1, {'name': 'Teste 1'})
    hash_table.insert(2, {'name': 'Teste 2'})
    
    # Remover item existente
    result = hash_table.remove(1)
    assert result == True, "Remoção deve retornar True"
    assert hash_table.size == 1, "Tamanho deve ser 1"
    
    # Tentar remover item inexistente
    result = hash_table.remove(99)
    assert result == False, "Remoção deve retornar False para item inexistente"
    
    print("✓ test_hash_remove passou")


def test_hash_collision():
    """Testa tratamento de colisões."""
    hash_table = HashTable(initial_capacity=10)
    
    # IDs 5 e 15 colidem (5 % 10 = 5, 15 % 10 = 5)
    hash_table.insert(5, {'name': 'Colisão 1'})
    hash_table.insert(15, {'name': 'Colisão 2'})
    
    # Ambos devem ser encontrados
    result1 = hash_table.get(5)
    result2 = hash_table.get(15)
    
    assert result1 is not None, "Primeiro item deve ser encontrado"
    assert result2 is not None, "Segundo item deve ser encontrado"
    assert result1['name'] == 'Colisão 1', "Primeiro item correto"
    assert result2['name'] == 'Colisão 2', "Segundo item correto"
    
    print("✓ test_hash_collision passou")


def test_hash_resize():
    """Testa redimensionamento automático."""
    hash_table = HashTable(initial_capacity=4, load_factor=0.75)
    
    # Inserir itens até passar o fator de carga
    for i in range(4):
        hash_table.insert(i, {'name': f'Teste {i}'})
    
    # Capacidade deve ter dobrado
    assert hash_table.capacity == 8, "Capacidade deve ter dobrado"
    assert hash_table._resize_count == 1, "Deve ter redimensionado uma vez"
    
    # Todos os itens ainda devem ser acessíveis
    for i in range(4):
        result = hash_table.get(i)
        assert result is not None, f"Item {i} deve ser encontrado após redimensionamento"
    
    print("✓ test_hash_resize passou")


def test_hash_validate():
    """Testa validação da tabela hash."""
    hash_table = HashTable(initial_capacity=10)
    
    hash_table.insert(1, {'name': 'Teste 1'})
    hash_table.insert(2, {'name': 'Teste 2'})
    
    # Deve ser válida
    assert hash_table.validate() == True, "Tabela deve ser válida"
    
    print("✓ test_hash_validate passou")


def test_hash_update():
    """Testa atualização de valor existente."""
    hash_table = HashTable(initial_capacity=10)
    
    hash_table.insert(1, {'name': 'Original'})
    assert hash_table.size == 1, "Tamanho deve ser 1"
    
    # Inserir mesma chave deve atualizar
    result = hash_table.insert(1, {'name': 'Atualizado'})
    assert result == False, "Inserção de chave existente deve retornar False"
    assert hash_table.size == 1, "Tamanho não deve aumentar"
    
    # Valor deve estar atualizado
    result = hash_table.get(1)
    assert result['name'] == 'Atualizado', "Valor deve estar atualizado"
    
    print("✓ test_hash_update passou")


def run_all_hash_tests():
    """Executa todos os testes da Hash."""
    print("\n=== Testes da Tabela Hash ===")
    test_hash_insert()
    test_hash_get()
    test_hash_remove()
    test_hash_collision()
    test_hash_resize()
    test_hash_validate()
    test_hash_update()
    print("=== Todos os testes da Hash passaram! ===\n")


if __name__ == '__main__':
    run_all_hash_tests()
