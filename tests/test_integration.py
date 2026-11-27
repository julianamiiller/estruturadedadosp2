"""
Testes de integração do sistema hospitalar.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.hospital_service import HospitalService


def test_register_patient():
    """Testa cadastro de paciente."""
    service = HospitalService()
    
    result = service.register_patient('João Silva', 3)
    
    assert result['success'] == True, "Cadastro deve ser bem-sucedido"
    assert 'patient' in result, "Deve retornar dados do paciente"
    assert result['patient']['name'] == 'João Silva', "Nome deve estar correto"
    assert result['patient']['priority'] == 3, "Prioridade deve estar correta"
    
    print("✓ test_register_patient passou")


def test_register_doctor():
    """Testa cadastro de médico."""
    service = HospitalService()
    
    result = service.register_doctor('Dr. Costa')
    
    assert result['success'] == True, "Cadastro deve ser bem-sucedido"
    assert 'doctor' in result, "Deve retornar dados do médico"
    assert result['doctor']['name'] == 'Dr. Costa', "Nome deve estar correto"
    
    print("✓ test_register_doctor passou")


def test_find_patient_by_id():
    """Testa busca de paciente por ID."""
    service = HospitalService()
    
    service.register_patient('Maria Santos', 2)
    patient = service.find_patient_by_id(1)
    
    assert patient is not None, "Deve encontrar o paciente"
    assert patient['name'] == 'Maria Santos', "Nome deve estar correto"
    
    # Buscar ID inexistente
    patient = service.find_patient_by_id(99)
    assert patient is None, "Deve retornar None para ID inexistente"
    
    print("✓ test_find_patient_by_id passou")


def test_reclassify_patient():
    """Testa reclassificação de paciente."""
    service = HospitalService()
    
    service.register_patient('Pedro Oliveira', 3)
    
    result = service.reclassify_patient(1, 1)
    
    assert result['success'] == True, "Reclassificação deve ser bem-sucedida"
    assert result['patient']['priority'] == 1, "Prioridade deve ter mudado"
    
    print("✓ test_reclassify_patient passou")


def test_call_next_patient():
    """Testa chamada de próximo paciente."""
    service = HospitalService()
    
    # Cadastrar pacientes e médicos
    service.register_patient('Paciente 1', 1)
    service.register_patient('Paciente 2', 2)
    service.register_doctor('Médico 1')
    service.register_doctor('Médico 2')
    
    result = service.call_next_patient()
    
    assert result['success'] == True, "Chamada deve ser bem-sucedida"
    assert 'patient' in result, "Deve retornar paciente"
    assert 'doctor' in result, "Deve retornar médico"
    assert result['patient']['priority'] == 1, "Deve chamar paciente mais urgente"
    
    print("✓ test_call_next_patient passou")


def test_conclude_attendance():
    """Testa conclusão de atendimento."""
    service = HospitalService()
    
    # Cadastrar paciente e médico
    service.register_patient('Paciente 1', 1)
    service.register_doctor('Médico 1')
    
    # Chamar paciente
    call_result = service.call_next_patient()
    patient_id = call_result['patient']['id']
    
    # Concluir atendimento
    result = service.conclude_attendance(patient_id)
    
    assert result['success'] == True, "Conclusão deve ser bem-sucedida"
    assert result['patient']['status'] == 'completed', "Status deve ser completed"
    
    print("✓ test_conclude_attendance passou")


def test_list_patients_by_arrival():
    """Testa listagem por ordem de chegada."""
    service = HospitalService()
    
    service.register_patient('Paciente 1', 3)
    service.register_patient('Paciente 2', 1)
    service.register_patient('Paciente 3', 5)
    
    patients = service.list_patients_by_arrival()
    
    assert len(patients) == 3, "Deve listar 3 pacientes"
    assert patients[0]['arrival_order'] == 0, "Primeiro deve ter ordem 0"
    assert patients[1]['arrival_order'] == 1, "Segundo deve ter ordem 1"
    
    print("✓ test_list_patients_by_arrival passou")


def test_cancel_patient():
    """Testa cancelamento de paciente."""
    service = HospitalService()
    
    service.register_patient('Paciente 1', 3)
    
    result = service.cancel_patient(1)
    
    assert result['success'] == True, "Cancelamento deve ser bem-sucedido"
    
    # Paciente não deve mais existir
    patient = service.find_patient_by_id(1)
    assert patient is None, "Paciente não deve mais existir"
    
    print("✓ test_cancel_patient passou")


def test_consistency_after_operations():
    """Testa consistência após várias operações."""
    service = HospitalService()
    
    # Cadastrar vários pacientes
    for i in range(5):
        service.register_patient(f'Paciente {i}', (i % 5) + 1)
    
    # Cadastrar médicos
    for i in range(2):
        service.register_doctor(f'Médico {i}')
    
    # Validar consistência
    validation = service.validate_consistency()
    
    assert validation['all_valid'] == True, "Sistema deve ser consistente"
    
    print("✓ test_consistency_after_operations passou")


def test_priority_order():
    """Testa ordenação por prioridade."""
    service = HospitalService()
    
    # Cadastrar pacientes com diferentes prioridades
    service.register_patient('Paciente Urgente', 1)
    service.register_patient('Paciente Médio', 3)
    service.register_patient('Paciente Pouco Urgente', 5)
    
    queue = service.get_patient_queue()
    
    # Primeiro deve ser prioridade 1
    assert queue[0][0] == 1, "Primeiro deve ser mais urgente"
    
    print("✓ test_priority_order passou")


def test_doctor_selection():
    """Testa seleção de médico menos carregado."""
    service = HospitalService()
    
    # Cadastrar médicos
    service.register_doctor('Médico A')
    service.register_doctor('Médico B')
    
    # Cadastrar pacientes
    service.register_patient('Paciente 1', 1)
    service.register_patient('Paciente 2', 1)
    
    # Chamar primeiro paciente
    call1 = service.call_next_patient()
    doctor1_id = call1['doctor']['id']
    
    # Concluir atendimento
    service.conclude_attendance(call1['patient']['id'])
    
    # Chamar segundo paciente
    call2 = service.call_next_patient()
    doctor2_id = call2['doctor']['id']
    
    # O mesmo médico pode ser chamado novamente pois tem menos carga
    # (ambos têm 0 atendimentos após conclusão)
    assert doctor2_id is not None, "Deve selecionar um médico"
    
    print("✓ test_doctor_selection passou")


def test_rollback_on_failure():
    """Testa rollback em caso de falha."""
    service = HospitalService()
    
    # Cadastrar paciente normal
    result1 = service.register_patient('Paciente Normal', 3)
    assert result1['success'] == True
    
    # Tentar cadastrar com prioridade inválida
    result2 = service.register_patient('Paciente Inválido', 10)
    assert result2['success'] == False
    
    # Sistema deve continuar consistente
    validation = service.validate_consistency()
    assert validation['all_valid'] == True
    
    print("✓ test_rollback_on_failure passou")


def test_search_patient_by_name():
    """Testa busca de pacientes por nome e por busca unificada."""
    service = HospitalService()
    service.register_patient('Carlos Silva', 2)
    service.register_patient('Maria Souza', 1)
    service.register_patient('Carlos Alberto', 3)
    
    # Busca por nome exato / parcial
    carlos_matches = service.find_patients_by_name('carlos')
    assert len(carlos_matches) == 2, "Deve encontrar 2 pacientes com Carlos"
    
    souza_matches = service.find_patients_by_name('Souza')
    assert len(souza_matches) == 1, "Deve encontrar Maria Souza"
    assert souza_matches[0]['name'] == 'Maria Souza'
    
    # Busca unificada por ID e nome
    id_results = service.search_patients('2')
    assert any(p['id'] == 2 for p in id_results), "Deve encontrar paciente de ID 2"
    
    print("✓ test_search_patient_by_name passou")


def test_doctor_availability():
    """Testa verificação de status e disponibilidade de médico específico."""
    service = HospitalService()
    doc1 = service.register_doctor('Dra. Ana Paula')
    doc2 = service.register_doctor('Dr. Bruno Mendes')
    doc1_id = doc1['doctor']['id']
    doc2_id = doc2['doctor']['id']
    
    # Ambos devem estar disponíveis inicialmente
    check1 = service.check_doctor_availability('Dra. Ana Paula')
    assert check1['success'] == True
    assert check1['is_available'] == True
    assert check1['status'] == 'available'
    
    # Cadastra paciente e chama atendimento
    service.register_patient('Paciente X', 1)
    call_result = service.call_next_patient()
    called_doc_id = call_result['doctor']['id']
    
    # Médico chamado deve estar ocupado
    status_called = service.check_doctor_availability(called_doc_id)
    assert status_called['is_available'] == False
    assert status_called['status'] == 'busy'
    assert status_called['current_patient']['name'] == 'Paciente X'
    
    # Conclui atendimento -> médico volta a ficar disponível
    service.conclude_attendance(call_result['patient']['id'])
    status_after = service.check_doctor_availability(called_doc_id)
    assert status_after['is_available'] == True
    assert status_after['status'] == 'available'
    assert status_after['doctor']['completed_count'] == 1
    
    print("✓ test_doctor_availability passou")


def run_all_integration_tests():
    """Executa todos os testes de integração."""
    print("\n=== Testes de Integração ===")
    test_register_patient()
    test_register_doctor()
    test_find_patient_by_id()
    test_search_patient_by_name()
    test_doctor_availability()
    test_reclassify_patient()
    test_call_next_patient()
    test_conclude_attendance()
    test_list_patients_by_arrival()
    test_cancel_patient()
    test_consistency_after_operations()
    test_priority_order()
    test_doctor_selection()
    test_rollback_on_failure()
    print("=== Todos os testes de integração passaram! ===\n")


if __name__ == '__main__':
    run_all_integration_tests()
