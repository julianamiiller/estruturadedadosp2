"""
Min-Heap para priorização.
Heap de pacientes: prioridade 1 (emergência) até 5. Desempate: chegada, ID.
Heap de médicos: menor número de atendimentos. Desempate: ordem de cadastro, ID.
"""

class HeapItem:
    """Item do heap com referência para posição."""
    def __init__(self, priority, key, value, tiebreaker1=None, tiebreaker2=None):
        self.priority = priority
        self.key = key
        self.value = value
        self.tiebreaker1 = tiebreaker1  # Para desempate (chegada ou cadastro)
        self.tiebreaker2 = tiebreaker2  # Para desempate (ID)
        self.heap_index = -1  # Posição atual no heap
    
    def __lt__(self, other):
        """Compara itens para ordenação no heap."""
        if self.priority != other.priority:
            return self.priority < other.priority
        if self.tiebreaker1 is not None and other.tiebreaker1 is not None:
            if self.tiebreaker1 != other.tiebreaker1:
                return self.tiebreaker1 < other.tiebreaker1
        if self.tiebreaker2 is not None and other.tiebreaker2 is not None:
            return self.tiebreaker2 < other.tiebreaker2
        return self.key < other.key


class MinHeap:
    """Min-Heap com suporte a alteração de prioridade em O(log n)."""
    
    def __init__(self, heap_type='patient'):
        """
        Inicializa o heap.
        
        Args:
            heap_type: 'patient' ou 'doctor' para definir comportamento
        """
        self.heap = []
        self.heap_type = heap_type
        self.size = 0
        self.key_to_item = {}  # Mapeamento chave -> HeapItem para alteração rápida
    
    def _parent(self, i):
        """Retorna índice do pai."""
        return (i - 1) // 2
    
    def _left(self, i):
        """Retorna índice do filho esquerdo."""
        return 2 * i + 1
    
    def _right(self, i):
        """Retorna índice do filho direito."""
        return 2 * i + 2
    
    def _swap(self, i, j):
        """Troca dois elementos e atualiza índices."""
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]
        self.heap[i].heap_index = i
        self.heap[j].heap_index = j
    
    def _heapify_up(self, i):
        """Sobe um elemento para manter propriedade do heap."""
        while i > 0:
            parent = self._parent(i)
            if self.heap[i] < self.heap[parent]:
                self._swap(i, parent)
                i = parent
            else:
                break
    
    def _heapify_down(self, i):
        """Desce um elemento para manter propriedade do heap."""
        n = len(self.heap)
        while True:
            smallest = i
            left = self._left(i)
            right = self._right(i)
            
            if left < n and self.heap[left] < self.heap[smallest]:
                smallest = left
            if right < n and self.heap[right] < self.heap[smallest]:
                smallest = right
            
            if smallest != i:
                self._swap(i, smallest)
                i = smallest
            else:
                break
    
    def insert(self, priority, key, value, tiebreaker1=None, tiebreaker2=None):
        """
        Insere um item no heap.
        
        Args:
            priority: Prioridade (1-5 para pacientes, atendimentos para médicos)
            key: Chave única (ID)
            value: Dados do item
            tiebreaker1: Primeiro critério de desempate
            tiebreaker2: Segundo critério de desempate
        """
        if key in self.key_to_item:
            return False  # Já existe
        
        item = HeapItem(priority, key, value, tiebreaker1, tiebreaker2)
        item.heap_index = len(self.heap)
        self.heap.append(item)
        self.key_to_item[key] = item
        self._heapify_up(len(self.heap) - 1)
        self.size += 1
        return True
    
    def extract_min(self):
        """
        Remove e retorna o item de menor prioridade.
        
        Returns:
            Tupla (priority, key, value) ou None se heap vazio
        """
        if len(self.heap) == 0:
            return None
        
        min_item = self.heap[0]
        last_item = self.heap.pop()
        
        del self.key_to_item[min_item.key]
        self.size -= 1
        
        if len(self.heap) > 0:
            self.heap[0] = last_item
            last_item.heap_index = 0
            self._heapify_down(0)
        
        return (min_item.priority, min_item.key, min_item.value)
    
    def peek(self):
        """
        Retorna o item de menor prioridade sem remover.
        
        Returns:
            Tupla (priority, key, value) ou None se heap vazio
        """
        if len(self.heap) == 0:
            return None
        
        item = self.heap[0]
        return (item.priority, item.key, item.value)
    
    def update_priority(self, key, new_priority, new_tiebreaker1=None, new_tiebreaker2=None):
        """
        Altera a prioridade de um item existente.
        
        Args:
            key: Chave do item
            new_priority: Nova prioridade
            new_tiebreaker1: Novo primeiro critério de desempate (opcional)
            new_tiebreaker2: Novo segundo critério de desempate (opcional)
            
        Returns:
            True se atualizado, False se não encontrado
        """
        if key not in self.key_to_item:
            return False
        
        item = self.key_to_item[key]
        old_priority = item.priority
        
        item.priority = new_priority
        if new_tiebreaker1 is not None:
            item.tiebreaker1 = new_tiebreaker1
        if new_tiebreaker2 is not None:
            item.tiebreaker2 = new_tiebreaker2
        
        # Decide se precisa subir ou descer
        if new_priority < old_priority:
            self._heapify_up(item.heap_index)
        else:
            self._heapify_down(item.heap_index)
        
        return True
    
    def remove(self, key):
        """
        Remove um item específico do heap.
        
        Args:
            key: Chave do item
            
        Returns:
            True se removido, False se não encontrado
        """
        if key not in self.key_to_item:
            return False
        
        item = self.key_to_item[key]
        index = item.heap_index
        
        # Troca com o último
        last_item = self.heap.pop()
        del self.key_to_item[key]
        self.size -= 1
        
        if index < len(self.heap):
            self.heap[index] = last_item
            last_item.heap_index = index
            self._heapify_down(index)
            self._heapify_up(index)
        
        return True
    
    def contains(self, key):
        """Verifica se uma chave existe no heap."""
        return key in self.key_to_item
    
    def get_priority(self, key):
        """Retorna a prioridade de um item."""
        if key in self.key_to_item:
            return self.key_to_item[key].priority
        return None
    
    def get_all_keys(self):
        """Retorna todas as chaves armazenadas."""
        return list(self.key_to_item.keys())
    
    def to_list(self):
        """Retorna todos os itens como lista ordenada por prioridade."""
        return [(item.priority, item.key, item.value) for item in self.heap]
    
    def get_heap_info(self):
        """Retorna informações do heap para visualização."""
        return {
            'size': self.size,
            'type': self.heap_type,
            'items': [
                {
                    'priority': item.priority,
                    'key': item.key,
                    'value': item.value,
                    'tiebreaker1': item.tiebreaker1,
                    'tiebreaker2': item.tiebreaker2,
                    'index': item.heap_index
                }
                for item in self.heap
            ]
        }
    
    def validate(self):
        """
        Valida a propriedade do heap.
        
        Returns:
            True se válido, False caso contrário
        """
        n = len(self.heap)
        
        # Verifica índices
        for i, item in enumerate(self.heap):
            if item.heap_index != i:
                return False
        
        # Verifica propriedade de heap
        for i in range(n):
            left = self._left(i)
            right = self._right(i)
            
            if left < n and self.heap[left] < self.heap[i]:
                return False
            if right < n and self.heap[right] < self.heap[i]:
                return False
        
        # Verifica consistência do mapeamento
        for key, item in self.key_to_item.items():
            if item.key != key:
                return False
            if item.heap_index >= n or self.heap[item.heap_index] != item:
                return False
        
        return True


class PatientHeap(MinHeap):
    """Heap específico para pacientes."""
    
    def __init__(self):
        super().__init__(heap_type='patient')
    
    def insert_patient(self, patient_id, patient_data, priority, arrival_time):
        """
        Insere um paciente.
        
        Args:
            patient_id: ID do paciente
            patient_data: Dados do paciente
            priority: Prioridade (1-5, sendo 1 a mais urgente)
            arrival_time: Horário de chegada para desempate
        """
        return self.insert(
            priority=priority,
            key=patient_id,
            value=patient_data,
            tiebreaker1=arrival_time,
            tiebreaker2=patient_id
        )


class DoctorHeap(MinHeap):
    """Heap específico para médicos."""
    
    def __init__(self):
        super().__init__(heap_type='doctor')
    
    def insert_doctor(self, doctor_id, doctor_data, completed_count, registration_order):
        """
        Insere um médico.
        
        Args:
            doctor_id: ID do médico
            doctor_data: Dados do médico
            completed_count: Número de atendimentos concluídos
            registration_order: Ordem de cadastro para desempate
        """
        return self.insert(
            priority=completed_count,
            key=doctor_id,
            value=doctor_data,
            tiebreaker1=registration_order,
            tiebreaker2=doctor_id
        )
    
    def increment_completed(self, doctor_id):
        """
        Incrementa o contador de atendimentos de um médico.
        
        Args:
            doctor_id: ID do médico
        """
        if doctor_id in self.key_to_item:
            item = self.key_to_item[doctor_id]
            self.update_priority(doctor_id, item.priority + 1)
