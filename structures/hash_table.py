"""
Tabela Hash com encadeamento e redimensionamento.
Chave: ID único do paciente.
Função hash: ID % capacidade.
Colisões: encadeamento (lista em cada posição).
"""

class Node:
    """Nó da lista encadeada para tratamento de colisões."""
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None


class HashTable:
    """Tabela Hash com encadeamento e redimensionamento automático."""
    
    def __init__(self, initial_capacity=10, load_factor=0.75):
        """
        Inicializa a tabela hash.
        
        Args:
            initial_capacity: Capacidade inicial da tabela
            load_factor: Fator de carga para redimensionamento
        """
        self.capacity = initial_capacity
        self.load_factor = load_factor
        self.size = 0
        self.buckets = [None] * self.capacity
        self._resize_count = 0
    
    def _hash(self, key):
        """Função hash: ID % capacidade."""
        return key % self.capacity
    
    def _resize(self):
        """Dobra a capacidade e recalcule índices de todos os itens."""
        old_buckets = self.buckets
        old_capacity = self.capacity
        
        self.capacity *= 2
        self.buckets = [None] * self.capacity
        self.size = 0
        self._resize_count += 1
        
        # Reinsere todos os itens
        for i in range(old_capacity):
            node = old_buckets[i]
            while node:
                self.insert(node.key, node.value, skip_resize=True)
                node = node.next
    
    def insert(self, key, value, skip_resize=False):
        """
        Insere um item na tabela hash.
        
        Args:
            key: ID do paciente
            value: Dados do paciente
            skip_resize: Se True, não verifica redimensionamento (usado internamente)
        """
        index = self._hash(key)
        
        # Verifica se já existe
        node = self.buckets[index]
        while node:
            if node.key == key:
                node.value = value
                return False  # Já existia, atualizou
            node = node.next
        
        # Insere no início da lista
        new_node = Node(key, value)
        new_node.next = self.buckets[index]
        self.buckets[index] = new_node
        self.size += 1
        
        # Verifica redimensionamento
        if not skip_resize and self.size / self.capacity > self.load_factor:
            self._resize()
        
        return True  # Inserido com sucesso
    
    def get(self, key):
        """
        Busca um item pela chave.
        
        Args:
            key: ID do paciente
            
        Returns:
            Valor associado ou None se não encontrado
        """
        index = self._hash(key)
        node = self.buckets[index]
        
        while node:
            if node.key == key:
                return node.value
            node = node.next
        
        return None
    
    def remove(self, key):
        """
        Remove um item pela chave.
        
        Args:
            key: ID do paciente
            
        Returns:
            True se removido, False se não encontrado
        """
        index = self._hash(key)
        node = self.buckets[index]
        prev = None
        
        while node:
            if node.key == key:
                if prev:
                    prev.next = node.next
                else:
                    self.buckets[index] = node.next
                self.size -= 1
                return True
            prev = node
            node = node.next
        
        return False
    
    def contains(self, key):
        """Verifica se uma chave existe na tabela."""
        return self.get(key) is not None
    
    def get_all_keys(self):
        """Retorna todas as chaves armazenadas."""
        keys = []
        for i in range(self.capacity):
            node = self.buckets[i]
            while node:
                keys.append(node.key)
                node = node.next
        return keys
    
    def get_all_values(self):
        """Retorna todos os valores armazenados."""
        values = []
        for i in range(self.capacity):
            node = self.buckets[i]
            while node:
                values.append(node.value)
                node = node.next
        return values
    
    def get_stats(self):
        """Retorna estatísticas da tabela hash."""
        collisions = sum(1 for bucket in self.buckets if bucket is not None)
        max_chain = max(
            self._chain_length(i) for i in range(self.capacity)
        ) if self.buckets else 0
        
        return {
            'size': self.size,
            'capacity': self.capacity,
            'load_factor': self.size / self.capacity if self.capacity > 0 else 0,
            'collisions': collisions,
            'max_chain_length': max_chain,
            'resize_count': self._resize_count
        }
    
    def _chain_length(self, index):
        """Retorna o tamanho da cadeia em um índice."""
        length = 0
        node = self.buckets[index]
        while node:
            length += 1
            node = node.next
        return length
    
    def get_buckets_info(self):
        """Retorna informações detalhadas dos buckets para visualização."""
        buckets_info = []
        for i in range(self.capacity):
            chain = []
            node = self.buckets[i]
            while node:
                chain.append({'key': node.key, 'value': node.value})
                node = node.next
            buckets_info.append({
                'index': i,
                'chain': chain
            })
        return buckets_info
    
    def validate(self):
        """
        Valida a integridade da tabela hash.
        
        Returns:
            True se válida, False caso contrário
        """
        # Verifica contagem de tamanho
        actual_size = sum(self._chain_length(i) for i in range(self.capacity))
        if actual_size != self.size:
            return False
        
        # Verifica chaves únicas
        all_keys = []
        for i in range(self.capacity):
            node = self.buckets[i]
            while node:
                if node.key in all_keys:
                    return False  # Chave duplicada
                all_keys.append(node.key)
                node = node.next
        
        return True
