from math import log2, floor
import random

class Cache:
    def __init__(self, cache_capacity, cache_assoc, block_size, repl_policy):
        self.total_access = 0
        self.total_misses = 0
        self.cache_capacity = int(cache_capacity)
        self.cache_assoc = int(cache_assoc)
        self.block_size = int(block_size)
        self.repl_policy = repl_policy
        self.set_ = int(log2(((self.cache_capacity * 2**10) / self.block_size) / self.cache_assoc))
        self.cache_table = [[] for _ in range(2 ** self.set_)]

    def print_info(self):
        print("Parámetros del caché:")
        print("\tCapacidad:\t\t\t" + str(self.cache_capacity) + "kB")
        print("\tAssociatividad:\t\t\t" + str(self.cache_assoc))
        print("\tTamaño de Bloque:\t\t\t" + str(self.block_size) + "B")
        print("\tPolítica de Reemplazo:\t\t\t" + str(self.repl_policy))

    def print_stats(self):
        print("Resultados de la simulación")
        miss_rate = (100.0 * self.total_misses) / self.total_access
        miss_rate = "{:.3f}".format(miss_rate)
        result_str = str(self.total_misses) + "," + miss_rate + "%"
        print(result_str)

    def access(self, access_type, address):
        self.total_access += 1
        offset = int(log2(self.block_size))  # tamaño del offset
        tag = address >> (offset + self.set_)
        index = (tag << self.set_) ^ (address >> offset)  # esto es igual a tag con 0s xor el tag con el set
        if tag not in self.cache_table[index]:
            self.total_misses += 1
            if len(self.cache_table[index]) < self.cache_assoc:  # si todavía hay campo en el set
                self.cache_table[index].insert(0, tag)  # el dato más reciente debe estar al inicio de la lista
            else:  # si ya está lleno, utilizamos política de reemplazo
                if self.repl_policy == 'l':  # lru
                    self.cache_table[index].pop(self.cache_assoc - 1)  # eliminamos el último elemento de la lista
                    self.cache_table[index].insert(0, tag)
                else:  # random
                    way = random.randint(0, self.cache_assoc - 1)  # elige una de las ways al azar
                    self.cache_table[index].pop(way)  # eliminamos un elemento al azar de la lista
                    self.cache_table[index].insert(0, tag)
            return True  # Miss
        else:
            self.cache_table[index].remove(tag)  # eliminamos el elemento
            self.cache_table[index].insert(0, tag)  # lo volvemos a poner, pero al inicio
            return False  # Hit


