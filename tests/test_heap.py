"""
Testes unitários para Min-Heap.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from structures.min_heap import MinHeap, PatientHeap, DoctorHeap


def test_heap_insert():
    """Testa inserção no heap."""
    heap = MinHeap()
    
    # Inserir itens
    result = heap.insert(3, 1, {'name': 'Teste 1'})
    assert result == True, "Inserção deve retornar True"
    assert heap.size == 1, "Tamanho deve ser 1"
    
    result = heap.insert(1, 2, {'name': 'Teste 2'})
    assert result == True, "Inserção deve retornar True"
    assert heap.size == 2, "Tamanho deve ser 2"
    
    print("✓ test_heap_insert passou")


def test_heap_extract_min():
    """Testa remoção do menor elemento."""
    heap = MinHeap()
    
    heap.insert(3, 1, {'name': 'Teste 1'})
    heap.insert(1, 2, {'name': 'Teste 2'})
    heap.insert(2, 3, {'name': 'Teste 3'})
    
    # Extrair mínimo deve ser prioridade 1
    priority, key, value = heap.extract_min()
    assert priority == 1, "Deve extrair menor prioridade"
    assert key == 2, "Deve extrair chave correta"
    assert heap.size == 2, "Tamanho deve ser 2"
    
    # Próximo mínimo deve ser prioridade 2
    priority, key, value = heap.extract_min()
    assert priority == 2, "Deve extrair próximo menor"
    
    print("✓ test_heap_extract_min passou")


def test_heap_peek():
    """Testa visualização do menor elemento sem remover."""
    heap = MinHeap()
    
    heap.insert(3, 1, {'name': 'Teste 1'})
    heap.insert(1, 2, {'name': 'Teste 2'})
    
    # Peek deve retornar menor sem remover
    priority, key, value = heap.peek()
    assert priority == 1, "Deve retornar menor prioridade"
    assert heap.size == 2, "Tamanho não deve mudar"
    
    print("✓ test_heap_peek passou")


def test_heap_update_priority():
    """Testa alteração de prioridade."""
    heap = MinHeap()
    
    heap.insert(3, 1, {'name': 'Teste 1'})
    heap.insert(5, 2, {'name': 'Teste 2'})
    
    # Atualizar prioridade do item 1 para 1
    result = heap.update_priority(1, 1)
    assert result == True, "Atualização deve retornar True"
    
    # Item 1 agora deve ser o mínimo
    priority, key, value = heap.peek()
    assert priority == 1, "Prioridade deve ter sido atualizada"
    assert key == 1, "Chave deve ser a atualizada"
    
    print("✓ test_heap_update_priority passou")


def test_heap_remove():
    """Testa remoção de item específico."""
    heap = MinHeap()
    
    heap.insert(3, 1, {'name': 'Teste 1'})
    heap.insert(1, 2, {'name': 'Teste 2'})
    
    # Remover item específico
    result = heap.remove(1)
    assert result == True, "Remoção deve retornar True"
    assert heap.size == 1, "Tamanho deve ser 1"
    
    # Item não deve mais existir
    assert heap.contains(1) == False, "Item não deve mais existir"
    
    print("✓ test_heap_remove passou")


def test_heap_validate():
    """Testa validação do heap."""
    heap = MinHeap()
    
    # Inserir itens
    for i in range(10):
        heap.insert(i, i, {'name': f'Teste {i}'})
    
    # Deve ser válido
    assert heap.validate() == True, "Heap deve ser válido"
    
    print("✓ test_heap_validate passou")


def test_patient_heap():
    """Testa heap específico de pacientes."""
    heap = PatientHeap()
    
    # Inserir pacientes com diferentes prioridades
    heap.insert_patient(1, {'name': 'Paciente 1'}, 3, 0)
    heap.insert_patient(2, {'name': 'Paciente 2'}, 1, 1)
    heap.insert_patient(3, {'name': 'Paciente 3'}, 5, 2)
    
    # Paciente mais urgente (prioridade 1) deve ser o primeiro
    priority, key, value = heap.peek()
    assert priority == 1, "Paciente mais urgente deve ser primeiro"
    assert key == 2, "Deve ser o paciente correto"
    
    print("✓ test_patient_heap passou")


def test_doctor_heap():
    """Testa heap específico de médicos."""
    heap = DoctorHeap()
    
    # Inserir médicos com diferentes cargas
    heap.insert_doctor(1, {'name': 'Médico 1'}, 5, 1)
    heap.insert_doctor(2, {'name': 'Médico 2'}, 0, 2)
    heap.insert_doctor(3, {'name': 'Médico 3'}, 2, 3)
    
    # Médico menos carregado (0 atendimentos) deve ser o primeiro
    priority, key, value = heap.peek()
    assert priority == 0, "Médico menos carregado deve ser primeiro"
    assert key == 2, "Deve ser o médico correto"
    
    print("✓ test_doctor_heap passou")


def test_heap_tiebreaker():
    """Testa critérios de desempate."""
    heap = MinHeap()
    
    # Mesma prioridade, diferentes tiebreakers
    heap.insert(1, 1, {'name': 'Teste 1'}, tiebreaker1=5, tiebreaker2=1)
    heap.insert(1, 2, {'name': 'Teste 2'}, tiebreaker1=3, tiebreaker2=2)
    
    # Deve usar tiebreaker1 (menor primeiro)
    priority, key, value = heap.peek()
    assert key == 2, "Deve usar tiebreaker1 para desempate"
    
    print("✓ test_heap_tiebreaker passou")


def test_heap_empty():
    """Testa operações em heap vazio."""
    heap = MinHeap()
    
    # Extrair de heap vazio deve retornar None
    result = heap.extract_min()
    assert result is None, "Extrair de heap vazio deve retornar None"
    
    # Peek de heap vazio deve retornar None
    result = heap.peek()
    assert result is None, "Peek de heap vazio deve retornar None"
    
    print("✓ test_heap_empty passou")


def run_all_heap_tests():
    """Executa todos os testes do Heap."""
    print("\n=== Testes do Min-Heap ===")
    test_heap_insert()
    test_heap_extract_min()
    test_heap_peek()
    test_heap_update_priority()
    test_heap_remove()
    test_heap_validate()
    test_patient_heap()
    test_doctor_heap()
    test_heap_tiebreaker()
    test_heap_empty()
    print("=== Todos os testes do Heap passaram! ===\n")


if __name__ == '__main__':
    run_all_heap_tests()
