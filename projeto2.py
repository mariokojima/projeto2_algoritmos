import csv
import time 
import random
from arvores import Node, AVL, BST

data_for_bst = []
data_for_avl = []

# Exemplo assumindo um CSV com colunas 'id', 'name', ... e cabeçalho
# Adapte 'id_column_index' e 'name_column_index' para seu CSV
id_column_index = 10
name_column_index = 0


try:


    with open('worldcities.csv', 'r', encoding='utf-8') as file: # Use a codificação correta!
        
        # reader = csv.reader(file)
        # header = next(reader) # Pula o cabeçalho
        reader = file

        line_count = 0
        # print(len(reader))

        for linha in reader:
            row = linha.replace('"','').split(',')
            
            # print( str(line_count) + '___' + str(row[0]).replace('"','') + '__' + str(row[10]).replace('"','') )
            # line_count += 1

            # print('____')
            # print( len(row.split(',') ) )
            # print( max(id_column_index, name_column_index) )

            if len(linha) >= max(id_column_index, name_column_index): # Garante que a linha tem dados suficientes
                try:
                    # CHAVE: Use o ID como chave (convertido para int)
                    key = int(row[id_column_index])
                    # VALOR: Pode ser só o nome, ou um dicionário/objeto com mais dados
                    value = {"name": row[name_column_index]} # Exemplo: armazena um dict como valor
                    # Ou value = row[name_column_index] # Armazena só o nome

                    # Adiciona à lista para posterior inserção nas árvores
                    data_for_bst.append((key, value))
                    data_for_avl.append((key, value)) # Dados idênticos para ambas

                    line_count += 1
                    # Opcional: Limitar o número de linhas para testes iniciais
                    # if line_count >= 10000:
                    #     break
                except ValueError:
                    print(f"Aviso: Não foi possível converter ID '{row[id_column_index]}' para int na linha {line_count + 1}. Pulando linha.")
                except IndexError:
                     print(f"Aviso: Coluna faltando na linha {line_count + 1}. Pulando linha.")

        print(f"Total de {line_count} linhas lidas e processadas.")

except FileNotFoundError:
    print(f"Erro: Arquivo 'seu_arquivo.csv' não encontrado.")
    exit()
except Exception as e:
    print(f"Erro ao ler o arquivo CSV: {e}")
    exit()


# Assumindo que você tem as classes BST e AVL implementadas
bst = BST()
avl = AVL()


# CARGAS
print("\n--- Carregando dados na BST ---")
bst_tree = BST()
keys_inserted_bst = [] # Guarda as chaves que foram realmente inseridas

start_time_bst = time.perf_counter() # Mede o tempo de forma precisa

for key, value in data_for_bst:
    bst_tree.insert(key, value)
    keys_inserted_bst.append(key)

end_time_bst = time.perf_counter()
bst_insert_time = end_time_bst - start_time_bst

print(f"Tempo de carregamento da BST: {bst_insert_time:.6f} segundos, {len(data_for_bst)} registros")
try:
    bst_height = bst_tree.get_height()
    print(f"Altura final da BST: {bst_height}")
except RecursionError:
    print("Erro: Profundidade máxima de recursão excedida ao calcular altura da BST. A árvore é muito desbalanceada.")
    bst_height = -1 # Indica erro ou altura desconhecida


# --- Carregar dados na AVL ---
print("\n--- Carregando dados na AVL ---")
avl_tree = AVL()
keys_inserted_avl = [] # Guarda as chaves que foram realmente inseridas

start_time_avl = time.perf_counter()

for key, value in data_for_avl:
    avl_tree.insert(key, value)
    keys_inserted_avl.append(key)

end_time_avl = time.perf_counter()
avl_insert_time = end_time_avl - start_time_avl

print(f"Tempo de carregamento da AVL: {avl_insert_time:.6f} segundos, {len(data_for_avl)} registros")
try:
    avl_height = avl_tree.get_height()
    print(f"Altura final da AVL: {avl_height}")
except RecursionError:
     print("Erro: Profundidade máxima de recursão excedida ao calcular altura da AVL (improvável, mas possível).")
     avl_height = -1

# --- Guardar as chaves para a próxima etapa (busca) ---
# Normalmente keys_inserted_bst e keys_inserted_avl serão idênticas se
# 'data_to_load' não foi modificado entre os carregamentos.
# Usaremos uma delas para a busca.
keys_for_search = keys_inserted_bst # ou keys_inserted_avl

print(f"\nDados carregados. {len(keys_for_search)} chaves estão prontas para a etapa de busca.")







# Medir tempo de inserção na BST
start_time_bst_insert = time.perf_counter()
keys_to_insert_bst = []
for key, value in data_for_bst:
    bst.insert(key, value)
    keys_to_insert_bst.append(key) # Guarda as chaves inseridas
end_time_bst_insert = time.perf_counter()
bst_insert_time = end_time_bst_insert - start_time_bst_insert
print(f"Tempo de inserção na BST: {bst_insert_time:.6f} segundos")

# Medir tempo de inserção na AVL
start_time_avl_insert = time.perf_counter()
keys_to_insert_avl = []
for key, value in data_for_avl:
    avl.insert(key, value)
    keys_to_insert_avl.append(key) # Guarda as chaves inseridas
end_time_avl_insert = time.perf_counter()
avl_insert_time = end_time_avl_insert - start_time_avl_insert
print(f"Tempo de inserção na AVL: {avl_insert_time:.6f} segundos")


print( 'altura da árvore AVL' )
print( avl.get_height() )


print( 'altura da árvore BST' )
print( bst.get_height() )

def comparacao (quantidade):
    num_searches = quantidade
    # Selecionar chaves aleatórias *que existem* na árvore para buscar
    # Usar as listas 'keys_to_insert_bst' ou 'keys_to_insert_avl' que guardamos
    search_keys = random.sample(keys_to_insert_bst, min(num_searches, len(keys_to_insert_bst)))
    # print(search_keys)

    # Medir tempo de busca na BST
    bst_search_times = []
    start_time_bst_search = time.perf_counter()
    for key in search_keys:
        bst.search(key)
    end_time_bst_search = time.perf_counter()
    bst_search_time_total = end_time_bst_search - start_time_bst_search
    bst_search_time_avg = bst_search_time_total / len(search_keys)
    print(f"Tempo total de {len(search_keys)} buscas na BST: {bst_search_time_total:.6f} segundos")
    print(f"Tempo médio por busca na BST: {bst_search_time_avg:.8f} segundos")

    search_keys = random.sample(keys_to_insert_avl, min(num_searches, len(keys_to_insert_avl)))
    # print(search_keys)
    # Medir tempo de busca na AVL
    avl_search_times = []
    start_time_avl_search = time.perf_counter()
    for key in search_keys:
        avl.search(key)
    end_time_avl_search = time.perf_counter()
    avl_search_time_total = end_time_avl_search - start_time_avl_search
    avl_search_time_avg = avl_search_time_total / len(search_keys)
    print(f"Tempo total de {len(search_keys)} buscas na AVL: {avl_search_time_total:.6f} segundos")
    print(f"Tempo médio por busca na AVL: {avl_search_time_avg:.8f} segundos")

comparacao (100)
comparacao (1000)
comparacao (10000)
comparacao (20000)