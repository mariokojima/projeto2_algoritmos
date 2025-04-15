import sys

# Aumenta o limite de recursão para árvores potencialmente profundas (especialmente BST não balanceada)
# Ajuste se necessário, mas cuidado com estouro de pilha real.
try:
    sys.setrecursionlimit(20000)
except Exception as e:
    print(f"Aviso: Não foi possível aumentar o limite de recursão: {e}")

# --- Estrutura do Nó (usada por ambas as árvores) ---
class Node:
    """Representa um nó em uma árvore binária."""
    def __init__(self, key, value):
        self.key = key      # Chave usada para ordenação/busca
        self.value = value  # Dados associados à chave (ex: nome, objeto, dict)
        self.left = None    # Filho esquerdo
        self.right = None   # Filho direito
        self.height = 1     # Altura do nó (usado especificamente pela AVL)

# --- Implementação da Árvore Binária de Busca (BST) ---
class BST:
    """Implementação de uma Árvore Binária de Busca."""
    def __init__(self):
        self.root = None

    def insert(self, key, value):
        """Método público para inserir um par chave-valor na árvore."""
        self.root = self._insert_recursive(self.root, key, value)

    def _insert_recursive(self, node, key, value):
        """Método recursivo auxiliar para inserção."""
        # Caso base: Se o nó atual é None, criamos um novo nó aqui
        if node is None:
            return Node(key, value)

        # Se a chave é menor, vai para a subárvore esquerda
        if key < node.key:
            node.left = self._insert_recursive(node.left, key, value)
        # Se a chave é maior, vai para a subárvore direita
        elif key > node.key:
            node.right = self._insert_recursive(node.right, key, value)
        # Se a chave já existe, atualiza o valor (pode mudar essa lógica se necessário)
        else:
            node.value = value # Atualiza o valor existente

        # Retorna o nó (possivelmente modificado)
        return node

    def search(self, key):
        """Método público para buscar um valor pela chave."""
        return self._search_recursive(self.root, key)

    def _search_recursive(self, node, key):
        """Método recursivo auxiliar para busca."""
        # Caso base 1: Nó não encontrado (chegou a None)
        # Caso base 2: Chave encontrada no nó atual
        if node is None or node.key == key:
            return node.value if node else None # Retorna o valor se encontrado, senão None

        # Se a chave buscada é menor, busca na subárvore esquerda
        if key < node.key:
            return self._search_recursive(node.left, key)
        # Se a chave buscada é maior, busca na subárvore direita
        else:
            return self._search_recursive(node.right, key)

    def get_height(self):
        """Calcula a altura da árvore."""
        return self._get_height_recursive(self.root)

    def _get_height_recursive(self, node):
        """Método recursivo para calcular a altura."""
        if node is None:
            return 0 # Altura de uma árvore vazia ou subárvore vazia é 0
        else:
            # Altura é 1 (nó atual) + altura da maior subárvore
            left_height = self._get_height_recursive(node.left)
            right_height = self._get_height_recursive(node.right)
            return 1 + max(left_height, right_height)

# --- Implementação da Árvore AVL ---
class AVL:
    """Implementação de uma Árvore AVL (Auto-Balanceada)."""
    def __init__(self):
        self.root = None

    # --- Funções Auxiliares da AVL ---
    def _get_height(self, node):
        """Retorna a altura de um nó (0 se o nó for None)."""
        if not node:
            return 0
        return node.height

    def _update_height(self, node):
        """Recalcula e atualiza a altura de um nó baseado nas alturas dos filhos."""
        if not node:
            return 0 # Não deveria acontecer em uso normal, mas seguro
        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))
        return node.height # Retorna a nova altura para conveniência

    def _get_balance(self, node):
        """Calcula o fator de balanceamento de um nó."""
        if not node:
            return 0
        # Fator de balanceamento = Altura(Esquerda) - Altura(Direita)
        return self._get_height(node.left) - self._get_height(node.right)

    # --- Rotações da AVL ---
    def _rotate_right(self, y):
        """Executa uma rotação simples à direita na subárvore com raiz y."""
        # print(f"Rotate Right em {y.key}")
        x = y.left
        T2 = x.right

        # Realiza a rotação
        x.right = y
        y.left = T2

        # Atualiza as alturas (IMPORTANTE: Atualizar y ANTES de x)
        self._update_height(y)
        self._update_height(x)

        # Retorna a nova raiz da subárvore rotacionada
        return x

    def _rotate_left(self, x):
        """Executa uma rotação simples à esquerda na subárvore com raiz x."""
        # print(f"Rotate Left em {x.key}")
        y = x.right
        T2 = y.left

        # Realiza a rotação
        y.left = x
        x.right = T2

        # Atualiza as alturas (IMPORTANTE: Atualizar x ANTES de y)
        self._update_height(x)
        self._update_height(y)

        # Retorna a nova raiz da subárvore rotacionada
        return y

    # --- Inserção na AVL ---
    def insert(self, key, value):
        """Método público para inserir um par chave-valor na árvore AVL."""
        self.root = self._insert_recursive(self.root, key, value)

    def _insert_recursive(self, node, key, value):
        """Método recursivo auxiliar para inserção e balanceamento."""
        # 1. Inserção padrão da BST
        if not node:
            return Node(key, value)

        if key < node.key:
            node.left = self._insert_recursive(node.left, key, value)
        elif key > node.key:
            node.right = self._insert_recursive(node.right, key, value)
        else:
            # Chave já existe, atualiza o valor
            node.value = value
            return node # Não precisa balancear se apenas atualizou

        # 2. Atualiza a altura do nó ancestral atual
        self._update_height(node)

        # 3. Calcula o fator de balanceamento deste nó
        balance = self._get_balance(node)

        # 4. Verifica se o nó ficou desbalanceado e aplica rotações se necessário

        # Caso Esquerda-Esquerda (Left-Left)
        if balance > 1 and key < node.left.key:
            return self._rotate_right(node)

        # Caso Direita-Direita (Right-Right)
        if balance < -1 and key > node.right.key:
            return self._rotate_left(node)

        # Caso Esquerda-Direita (Left-Right)
        if balance > 1 and key > node.left.key:
            node.left = self._rotate_left(node.left) # Rotação à esquerda no filho esquerdo
            return self._rotate_right(node)         # Rotação à direita no nó atual

        # Caso Direita-Esquerda (Right-Left)
        if balance < -1 and key < node.right.key:
            node.right = self._rotate_right(node.right) # Rotação à direita no filho direito
            return self._rotate_left(node)          # Rotação à esquerda no nó atual

        # Retorna o nó (possivelmente a nova raiz após rotação)
        return node

    # --- Busca na AVL ---
    def search(self, key):
        """Método público para buscar um valor pela chave (igual à BST)."""
        return self._search_recursive(self.root, key)

    def _search_recursive(self, node, key):
        """Método recursivo auxiliar para busca (igual à BST)."""
        if node is None or node.key == key:
            return node.value if node else None

        if key < node.key:
            return self._search_recursive(node.left, key)
        else:
            return self._search_recursive(node.right, key)

    def get_height(self):
        """Retorna a altura da árvore AVL (usa a altura armazenada no nó raiz)."""
        return self._get_height(self.root)


