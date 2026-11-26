"""
Serviço de integração das estruturas de dados.
Gerencia a consistência entre Hash, Árvore Rubro-Negra e Heaps.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from structures.hash_table import HashTable
from structures.red_black_tree import RedBlackTree
from structures.min_heap import PatientHeap, DoctorHeap


class HospitalService:
    """Serviço principal de gestão hospitalar."""
    
    def __init__(self):
        """Inicializa as estruturas de dados."""
        self.hash_table = HashTable(initial_capacity=10, load_factor=0.75)
        self.rb_tree = RedBlackTree()
        self.patient_heap = PatientHeap()
        self.doctor_heap = DoctorHeap()
        
        self.next_patient_id = 1
        self.next_doctor_id = 1
        self.arrival_counter = 0  # Para ordem de chegada
        
        # Rastreamento de atendimentos em andamento
        self.active_attendances = {}  # {patient_id: doctor_id}
    
    def _generate_patient_id(self):
        """Gera um novo ID de paciente."""
        patient_id = self.next_patient_id
        self.next_patient_id += 1
        return patient_id
    
    def _generate_doctor_id(self):
        """Gera um novo ID de médico."""
        doctor_id = self.next_doctor_id
        self.next_doctor_id += 1
        return doctor_id
    
    def _get_arrival_order(self):
        """Retorna e incrementa o contador de chegada."""
        arrival = self.arrival_counter
        self.arrival_counter += 1
        return arrival
    
    def register_patient(self, name, priority):
        """
        Cadastra um novo paciente.
        
        Args:
            name: Nome do paciente
            priority: Prioridade (1-5, sendo 1 a mais urgente)
            
        Returns:
            Dicionário com dados do paciente cadastrado ou erro
        """
        if priority < 1 or priority > 5:
            return {'success': False, 'error': 'Prioridade deve ser entre 1 e 5'}
        
        patient_id = self._generate_patient_id()
        arrival_order = self._get_arrival_order()
        arrival_time = arrival_order  # Simplificado: usa contador
        
        patient_data = {
            'id': patient_id,
            'name': name,
            'priority': priority,
            'arrival_time': arrival_time,
            'arrival_order': arrival_order,
            'status': 'waiting'
        }
        
        # Inserção atômica nas três estruturas
        try:
            # Hash
            hash_inserted = self.hash_table.insert(patient_id, patient_data)
            if not hash_inserted:
                raise Exception("Falha na inserção na Hash")
            
            # Árvore Rubro-Negra (chave composta: arrival_time, id)
            tree_key = (arrival_time, patient_id)
            tree_inserted = self.rb_tree.insert(tree_key, patient_data)
            if not tree_inserted:
                self.hash_table.remove(patient_id)  # Rollback
                raise Exception("Falha na inserção na Árvore")
            
            # Heap de pacientes
            heap_inserted = self.patient_heap.insert_patient(
                patient_id, patient_data, priority, arrival_time
            )
            if not heap_inserted:
                self.hash_table.remove(patient_id)  # Rollback
                self.rb_tree.delete(tree_key)  # Rollback
                raise Exception("Falha na inserção no Heap")
            
            return {'success': True, 'patient': patient_data}
        
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def register_doctor(self, name):
        """
        Cadastra um novo médico.
        
        Args:
            name: Nome do médico
            
        Returns:
            Dicionário com dados do médico cadastrado ou erro
        """
        doctor_id = self._generate_doctor_id()
        registration_order = doctor_id  # Simplificado: usa ID como ordem
        
        doctor_data = {
            'id': doctor_id,
            'name': name,
            'completed_count': 0,
            'registration_order': registration_order,
            'status': 'available'
        }
        
        # Inserção no heap de médicos
        heap_inserted = self.doctor_heap.insert_doctor(
            doctor_id, doctor_data, 0, registration_order
        )
        
        if not heap_inserted:
            return {'success': False, 'error': 'Falha na inserção do médico'}
        
        return {'success': True, 'doctor': doctor_data}
    
    def find_patient_by_id(self, patient_id):
        """
        Localiza um paciente por ID (usando apenas a Hash).
        
        Args:
            patient_id: ID do paciente
            
        Returns:
            Dados do paciente ou None se não encontrado
        """
        return self.hash_table.get(patient_id)
    
    def reclassify_patient(self, patient_id, new_priority):
        """
        Reclassifica a prioridade de um paciente.
        
        Args:
            patient_id: ID do paciente
            new_priority: Nova prioridade (1-5)
            
        Returns:
            Dicionário com resultado da operação
        """
        if new_priority < 1 or new_priority > 5:
            return {'success': False, 'error': 'Prioridade deve ser entre 1 e 5'}
        
        patient_data = self.hash_table.get(patient_id)
        if patient_data is None:
            return {'success': False, 'error': 'Paciente não encontrado'}
        
        # Atualiza na Hash
        patient_data['priority'] = new_priority
        self.hash_table.insert(patient_id, patient_data)
        
        # Atualiza no Heap
        heap_updated = self.patient_heap.update_priority(
            patient_id, new_priority, patient_data['arrival_time'], patient_id
        )
        
        if not heap_updated:
            return {'success': False, 'error': 'Falha na atualização do Heap'}
        
        # Atualiza na Árvore (precisa remover e reinserir com nova chave?)
        # Na árvore, a chave é (arrival_time, id), então não muda
        # Apenas atualiza o valor
        tree_key = (patient_data['arrival_time'], patient_id)
        tree_value = self.rb_tree.search(tree_key)
        if tree_value:
            tree_value['priority'] = new_priority
        
        return {'success': True, 'patient': patient_data}
    
    def call_next_patient(self):
        """
        Chama o próximo paciente para atendimento.
        
        Returns:
            Dicionário com paciente e médico selecionados ou erro
        """
        # Verifica se há pacientes na fila
        if self.patient_heap.size == 0:
            return {'success': False, 'error': 'Não há pacientes na fila'}
        
        # Verifica se há médicos disponíveis
        if self.doctor_heap.size == 0:
            return {'success': False, 'error': 'Não há médicos disponíveis'}
        
        # Remove paciente do heap
        patient_priority, patient_id, patient_data = self.patient_heap.extract_min()
        
        # Remove médico do heap
        doctor_priority, doctor_id, doctor_data = self.doctor_heap.extract_min()
        
        # Atualiza status
        patient_data['status'] = 'in_attendance'
        doctor_data['status'] = 'busy'
        
        # Registra atendimento ativo
        self.active_attendances[patient_id] = doctor_id
        
        # Atualiza na Hash
        self.hash_table.insert(patient_id, patient_data)
        
        return {
            'success': True,
            'patient': patient_data,
            'doctor': doctor_data
        }
    
    def conclude_attendance(self, patient_id):
        """
        Conclui o atendimento de um paciente.
        
        Args:
            patient_id: ID do paciente
            
        Returns:
            Dicionário com resultado da operação
        """
        if patient_id not in self.active_attendances:
            return {'success': False, 'error': 'Atendimento não encontrado'}
        
        doctor_id = self.active_attendances[patient_id]
        
        # Busca dados do paciente
        patient_data = self.hash_table.get(patient_id)
        if patient_data is None:
            return {'success': False, 'error': 'Paciente não encontrado'}
        
        # Atualiza status do paciente
        patient_data['status'] = 'completed'
        self.hash_table.insert(patient_id, patient_data)
        
        # Remove paciente da árvore (já foi atendido)
        tree_key = (patient_data['arrival_time'], patient_id)
        self.rb_tree.delete(tree_key)
        
        # Incrementa contador do médico e reinsere no heap
        self.doctor_heap.increment_completed(doctor_id)
        
        # Remove do atendimento ativo
        del self.active_attendances[patient_id]
        
        return {'success': True, 'patient': patient_data, 'doctor_id': doctor_id}
    
    def list_patients_by_arrival(self):
        """
        Lista pacientes por ordem de chegada (usando Árvore Rubro-Negra).
        
        Returns:
            Lista de pacientes em ordem de chegada
        """
        return self.rb_tree.inorder_traversal()
    
    def cancel_patient(self, patient_id):
        """
        Cancela/remove um paciente das três estruturas.
        
        Args:
            patient_id: ID do paciente
            
        Returns:
            Dicionário com resultado da operação
        """
        patient_data = self.hash_table.get(patient_id)
        if patient_data is None:
            return {'success': False, 'error': 'Paciente não encontrado'}
        
        # Se estiver em atendimento, não pode cancelar
        if patient_id in self.active_attendances:
            return {'success': False, 'error': 'Paciente em atendimento'}
        
        # Remove da Hash
        hash_removed = self.hash_table.remove(patient_id)
        if not hash_removed:
            return {'success': False, 'error': 'Falha na remoção da Hash'}
        
        # Remove da Árvore
        tree_key = (patient_data['arrival_time'], patient_id)
        tree_removed = self.rb_tree.delete(tree_key)
        if not tree_removed:
            # Rollback
            self.hash_table.insert(patient_id, patient_data)
            return {'success': False, 'error': 'Falha na remoção da Árvore'}
        
        # Remove do Heap
        heap_removed = self.patient_heap.remove(patient_id)
        if not heap_removed:
            # Rollback
            self.hash_table.insert(patient_id, patient_data)
            self.rb_tree.insert(tree_key, patient_data)
            return {'success': False, 'error': 'Falha na remoção do Heap'}
        
        return {'success': True, 'patient': patient_data}
    
    def get_patient_queue(self):
        """Retorna a fila de pacientes ordenada por prioridade."""
        return self.patient_heap.to_list()
    
    def get_available_doctors(self):
        """Retorna médicos disponíveis ordenados por carga."""
        return self.doctor_heap.to_list()
    
    def get_stats(self):
        """Retorna estatísticas do sistema."""
        return {
            'hash_stats': self.hash_table.get_stats(),
            'tree_stats': {
                'size': self.rb_tree.size,
                'black_height': self.rb_tree.get_black_height()
            },
            'patient_heap_stats': {
                'size': self.patient_heap.size
            },
            'doctor_heap_stats': {
                'size': self.doctor_heap.size
            },
            'active_attendances': len(self.active_attendances)
        }
    
    def validate_consistency(self):
        """
        Valida a consistência entre as três estruturas.
        
        Returns:
            Dicionário com resultado da validação
        """
        # Valida cada estrutura individualmente
        hash_valid = self.hash_table.validate()
        tree_valid = self.rb_tree.validate()
        patient_heap_valid = self.patient_heap.validate()
        doctor_heap_valid = self.doctor_heap.validate()
        
        # Verifica se os mesmos IDs estão nas três estruturas de pacientes
        hash_keys = set(self.hash_table.get_all_keys())
        tree_keys = set(self.rb_tree.get_all_keys())
        patient_heap_keys = set(self.patient_heap.get_all_keys())
        
        # A árvore usa tuplas (arrival_time, id), precisamos extrair só os IDs
        tree_ids = {key[1] for key in tree_keys}
        
        # IDs na Hash devem estar na árvore e no heap (exceto os em atendimento)
        waiting_in_hash = hash_keys - set(self.active_attendances.keys())
        consistent_ids = waiting_in_hash == tree_ids == patient_heap_keys
        
        return {
            'hash_valid': hash_valid,
            'tree_valid': tree_valid,
            'patient_heap_valid': patient_heap_valid,
            'doctor_heap_valid': doctor_heap_valid,
            'consistent_ids': consistent_ids,
            'all_valid': hash_valid and tree_valid and patient_heap_valid and doctor_heap_valid and consistent_ids
        }
    
    def get_detailed_info(self):
        """Retorna informações detalhadas para visualização."""
        return {
            'hash_buckets': self.hash_table.get_buckets_info(),
            'tree_info': self.rb_tree.get_tree_info(),
            'patient_heap': self.patient_heap.get_heap_info(),
            'doctor_heap': self.doctor_heap.get_heap_info(),
            'active_attendances': self.active_attendances
        }
