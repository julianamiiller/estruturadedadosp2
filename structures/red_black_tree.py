"""
Árvore Rubro-Negra com chave composta (horário, ID).
Chave: (horário, ID) para ordenação por ordem de chegada.
Implementa inserção, busca, remoção e percurso em ordem.
"""

class Color:
    RED = True
    BLACK = False


class RBNode:
    """Nó da árvore rubro-negra."""
    def __init__(self, key, value):
        self.key = key  # Tupla (horário, ID)
        self.value = value  # Dados do paciente
        self.left = None
        self.right = None
        self.parent = None
        self.color = Color.RED


class RedBlackTree:
    """Árvore Rubro-Negra para ordenação por ordem de chegada."""
    
    def __init__(self):
        self.NIL = RBNode(None, None)
        self.NIL.color = Color.BLACK
        self.NIL.left = None
        self.NIL.right = None
        self.root = self.NIL
        self.size = 0
    
    def _left_rotate(self, x):
        """Rotação para esquerda."""
        y = x.right
        x.right = y.left
        
        if y.left != self.NIL:
            y.left.parent = x
        
        y.parent = x.parent
        
        if x.parent is None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        
        y.left = x
        x.parent = y
    
    def _right_rotate(self, x):
        """Rotação para direita."""
        y = x.left
        x.left = y.right
        
        if y.right != self.NIL:
            y.right.parent = x
        
        y.parent = x.parent
        
        if x.parent is None:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        
        y.right = x
        x.parent = y
    
    def _fix_insert(self, node):
        """Conserta a árvore após inserção."""
        while node.parent and node.parent.color == Color.RED:
            if node.parent == node.parent.parent.left:
                uncle = node.parent.parent.right
                
                if uncle.color == Color.RED:
                    # Caso 1: tio vermelho
                    node.parent.color = Color.BLACK
                    uncle.color = Color.BLACK
                    node.parent.parent.color = Color.RED
                    node = node.parent.parent
                else:
                    if node == node.parent.right:
                        # Caso 2: tio preto, nó é filho direito
                        node = node.parent
                        self._left_rotate(node)
                    
                    # Caso 3: tio preto, nó é filho esquerdo
                    node.parent.color = Color.BLACK
                    node.parent.parent.color = Color.RED
                    self._right_rotate(node.parent.parent)
            else:
                # Espelhado
                uncle = node.parent.parent.left
                
                if uncle.color == Color.RED:
                    node.parent.color = Color.BLACK
                    uncle.color = Color.BLACK
                    node.parent.parent.color = Color.RED
                    node = node.parent.parent
                else:
                    if node == node.parent.left:
                        node = node.parent
                        self._right_rotate(node)
                    
                    node.parent.color = Color.BLACK
                    node.parent.parent.color = Color.RED
                    self._left_rotate(node.parent.parent)
        
        self.root.color = Color.BLACK
    
    def insert(self, key, value):
        """
        Insere um nó na árvore.
        
        Args:
            key: Tupla (horário, ID)
            value: Dados do paciente
            
        Returns:
            True se inserido, False se já existia
        """
        # Verifica se já existe
        if self.search(key) is not None:
            return False
        
        new_node = RBNode(key, value)
        new_node.left = self.NIL
        new_node.right = self.NIL
        
        y = None
        x = self.root
        
        while x != self.NIL:
            y = x
            if new_node.key < x.key:
                x = x.left
            else:
                x = x.right
        
        new_node.parent = y
        
        if y is None:
            self.root = new_node
        elif new_node.key < y.key:
            y.left = new_node
        else:
            y.right = new_node
        
        new_node.color = Color.RED
        self._fix_insert(new_node)
        self.size += 1
        return True
    
    def search(self, key):
        """
        Busca um nó pela chave.
        
        Args:
            key: Tupla (horário, ID)
            
        Returns:
            Valor associado ou None se não encontrado
        """
        node = self.root
        while node != self.NIL:
            if key == node.key:
                return node.value
            elif key < node.key:
                node = node.left
            else:
                node = node.right
        return None
    
    def _minimum(self, node):
        """Retorna o nó mínimo a partir de um dado nó."""
        while node.left != self.NIL:
            node = node.left
        return node
    
    def _transplant(self, u, v):
        """Transplanta subárvore."""
        if u.parent is None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent
    
    def _fix_delete(self, x):
        """Conserta a árvore após remoção."""
        while x != self.root and x.color == Color.BLACK:
            if x == x.parent.left:
                w = x.parent.right
                
                if w.color == Color.RED:
                    w.color = Color.BLACK
                    x.parent.color = Color.RED
                    self._left_rotate(x.parent)
                    w = x.parent.right
                
                if w.left.color == Color.BLACK and w.right.color == Color.BLACK:
                    w.color = Color.RED
                    x = x.parent
                else:
                    if w.right.color == Color.BLACK:
                        w.left.color = Color.BLACK
                        w.color = Color.RED
                        self._right_rotate(w)
                        w = x.parent.right
                    
                    w.color = x.parent.color
                    x.parent.color = Color.BLACK
                    w.right.color = Color.BLACK
                    self._left_rotate(x.parent)
                    x = self.root
            else:
                w = x.parent.left
                
                if w.color == Color.RED:
                    w.color = Color.BLACK
                    x.parent.color = Color.RED
                    self._right_rotate(x.parent)
                    w = x.parent.left
                
                if w.right.color == Color.BLACK and w.left.color == Color.BLACK:
                    w.color = Color.RED
                    x = x.parent
                else:
                    if w.left.color == Color.BLACK:
                        w.right.color = Color.BLACK
                        w.color = Color.RED
                        self._left_rotate(w)
                        w = x.parent.left
                    
                    w.color = x.parent.color
                    x.parent.color = Color.BLACK
                    w.left.color = Color.BLACK
                    self._right_rotate(x.parent)
                    x = self.root
        
        x.color = Color.BLACK
    
    def delete(self, key):
        """
        Remove um nó pela chave.
        
        Args:
            key: Tupla (horário, ID)
            
        Returns:
            True se removido, False se não encontrado
        """
        z = self.root
        while z != self.NIL:
            if key == z.key:
                break
            elif key < z.key:
                z = z.left
            else:
                z = z.right
        
        if z == self.NIL:
            return False
        
        y = z
        y_original_color = y.color
        
        if z.left == self.NIL:
            x = z.right
            self._transplant(z, z.right)
        elif z.right == self.NIL:
            x = z.left
            self._transplant(z, z.left)
        else:
            y = self._minimum(z.right)
            y_original_color = y.color
            x = y.right
            
            if y.parent == z:
                x.parent = y
            else:
                self._transplant(y, y.right)
                y.right = z.right
                y.right.parent = y
            
            self._transplant(z, y)
            y.left = z.left
            y.left.parent = y
            y.color = z.color
        
        if y_original_color == Color.BLACK:
            self._fix_delete(x)
        
        self.size -= 1
        return True
    
    def inorder_traversal(self):
        """
        Percurso em ordem (in-order).
        
        Returns:
            Lista de valores em ordem de chegada
        """
        result = []
        
        def _inorder(node):
            if node != self.NIL:
                _inorder(node.left)
                result.append(node.value)
                _inorder(node.right)
        
        _inorder(self.root)
        return result
    
    def inorder_traversal_with_keys(self):
        """
        Percurso em ordem retornando chaves e valores.
        
        Returns:
            Lista de tuplas (chave, valor) em ordem de chegada
        """
        result = []
        
        def _inorder(node):
            if node != self.NIL:
                _inorder(node.left)
                result.append((node.key, node.value))
                _inorder(node.right)
        
        _inorder(self.root)
        return result
    
    def get_all_keys(self):
        """Retorna todas as chaves armazenadas."""
        return [key for key, _ in self.inorder_traversal_with_keys()]
    
    def validate(self):
        """
        Valida as propriedades da árvore rubro-negra.
        
        Returns:
            True se válida, False caso contrário
        """
        # Propriedade 1: Raiz é preta
        if self.root.color != Color.BLACK:
            return False
        
        # Propriedade 2: Não há dois vermelhos seguidos
        def _check_red_red(node):
            if node == self.NIL:
                return True
            if node.color == Color.RED:
                if node.left.color == Color.RED or node.right.color == Color.RED:
                    return False
            return _check_red_red(node.left) and _check_red_red(node.right)
        
        if not _check_red_red(self.root):
            return False
        
        # Propriedade 3: Todos os caminhos têm mesma quantidade de nós negros
        def _black_height(node):
            if node == self.NIL:
                return 1
            
            left_height = _black_height(node.left)
            right_height = _black_height(node.right)
            
            if left_height == -1 or right_height == -1 or left_height != right_height:
                return -1
            
            return left_height + (1 if node.color == Color.BLACK else 0)
        
        if _black_height(self.root) == -1:
            return False
        
        return True
    
    def get_black_height(self):
        """Retorna a altura negra da árvore."""
        def _black_height(node):
            if node == self.NIL:
                return 1
            left = _black_height(node.left)
            return left + (1 if node.color == Color.BLACK else 0)
        return _black_height(self.root)
    
    def get_tree_info(self):
        """Retorna informações da árvore para visualização."""
        def _build_tree_info(node, depth=0):
            if node == self.NIL:
                return None
            return {
                'key': node.key,
                'value': node.value,
                'color': 'RED' if node.color == Color.RED else 'BLACK',
                'depth': depth,
                'left': _build_tree_info(node.left, depth + 1),
                'right': _build_tree_info(node.right, depth + 1)
            }
        
        return {
            'size': self.size,
            'black_height': self.get_black_height(),
            'root': _build_tree_info(self.root)
        }
