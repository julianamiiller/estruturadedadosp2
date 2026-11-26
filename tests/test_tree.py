"""
Testes unitários para Árvore Rubro-Negra.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from structures.red_black_tree import RedBlackTree, Color


def test_tree_insert():
    """Testa inserção na árvore rubro-negra."""
    tree = RedBlackTree()
    
    # Inserir itens
    result = tree.insert((0, 1), {'name': 'Teste 1'})
    assert result == True, "Inserção deve retornar True"
    assert tree.size == 1, "Tamanho deve ser 1"
    
    result = tree.insert((1, 2), {'name': 'Teste 2'})
    assert result == True, "Inserção deve retornar True"
    assert tree.size == 2, "Tamanho deve ser 2"
    
    print("✓ test_tree_insert passou")


def test_tree_search():
    """Testa busca na árvore."""
    tree = RedBlackTree()
    
    tree.insert((0, 1), {'name': 'Teste 1'})
    tree.insert((1, 2), {'name': 'Teste 2'})
    
    # Buscar item existente
    result = tree.search((0, 1))
    assert result is not None, "Deve encontrar o item"
    assert result['name'] == 'Teste 1', "Deve retornar o valor correto"
    
    # Buscar item inexistente
    result = tree.search((99, 99))
    assert result is None, "Deve retornar None para item inexistente"
    
    print("✓ test_tree_search passou")


def test_tree_delete():
    """Testa remoção na árvore."""
    tree = RedBlackTree()
    
    tree.insert((0, 1), {'name': 'Teste 1'})
    tree.insert((1, 2), {'name': 'Teste 2'})
    
    # Remover item existente
    result = tree.delete((0, 1))
    assert result == True, "Remoção deve retornar True"
    assert tree.size == 1, "Tamanho deve ser 1"
    
    # Tentar remover item inexistente
    result = tree.delete((99, 99))
    assert result == False, "Remoção deve retornar False para item inexistente"
    
    print("✓ test_tree_delete passou")


def test_tree_inorder():
    """Testa percurso em ordem."""
    tree = RedBlackTree()
    
    # Inserir itens em ordem aleatória
    tree.insert((5, 5), {'name': 'Teste 5'})
    tree.insert((2, 2), {'name': 'Teste 2'})
    tree.insert((8, 8), {'name': 'Teste 8'})
    tree.insert((1, 1), {'name': 'Teste 1'})
    tree.insert((3, 3), {'name': 'Teste 3'})
    
    # Percurso em ordem deve retornar ordenado pela chave
    result = tree.inorder_traversal()
    assert len(result) == 5, "Deve retornar 5 itens"
    
    # Verificar ordem
    keys = [item['name'] for item in result]
    assert keys == ['Teste 1', 'Teste 2', 'Teste 3', 'Teste 5', 'Teste 8'], "Deve estar em ordem"
    
    print("✓ test_tree_inorder passou")


def test_tree_validate():
    """Testa validação da árvore."""
    tree = RedBlackTree()
    
    # Inserir vários itens
    for i in range(10):
        tree.insert((i, i), {'name': f'Teste {i}'})
    
    # Deve ser válida
    assert tree.validate() == True, "Árvore deve ser válida"
    
    # Raiz deve ser preta
    assert tree.root.color == Color.BLACK, "Raiz deve ser preta"
    
    print("✓ test_tree_validate passou")


def test_tree_black_height():
    """Testa cálculo da altura negra."""
    tree = RedBlackTree()
    
    # Árvore vazia tem altura negra 1 (NIL)
    assert tree.get_black_height() == 1, "Árvore vazia deve ter altura negra 1"
    
    # Inserir itens
    tree.insert((0, 1), {'name': 'Teste 1'})
    tree.insert((1, 2), {'name': 'Teste 2'})
    
    # Altura negra deve ser positiva
    height = tree.get_black_height()
    assert height > 0, "Altura negra deve ser positiva"
    
    print("✓ test_tree_black_height passou")


def test_tree_duplicate():
    """Testa inserção de chave duplicada."""
    tree = RedBlackTree()
    
    tree.insert((0, 1), {'name': 'Original'})
    assert tree.size == 1, "Tamanho deve ser 1"
    
    # Tentar inserir mesma chave
    result = tree.insert((0, 1), {'name': 'Duplicado'})
    assert result == False, "Inserção de chave duplicada deve retornar False"
    assert tree.size == 1, "Tamanho não deve aumentar"
    
    print("✓ test_tree_duplicate passou")


def run_all_tree_tests():
    """Executa todos os testes da Árvore."""
    print("\n=== Testes da Árvore Rubro-Negra ===")
    test_tree_insert()
    test_tree_search()
    test_tree_delete()
    test_tree_inorder()
    test_tree_validate()
    test_tree_black_height()
    test_tree_duplicate()
    print("=== Todos os testes da Árvore passaram! ===\n")


if __name__ == '__main__':
    run_all_tree_tests()
