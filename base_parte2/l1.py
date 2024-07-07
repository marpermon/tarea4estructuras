import math
import gzip
import os
from cache import Cache
import matplotlib.pyplot as plt

# Parámetros del caché L1
l1_cache_size = 32  # kB
l1_cache_assoc = 8
block_size = 64  # bytes
l1_repl_policy = "l"
l1_hit_time = 4  # ciclos de reloj
miss_penalty = 500  # ciclos de reloj

# Directorio de archivos de trace
trace_dir = r".\..\traces\traces"

# Obtener todos los archivos de trace en el directorio
trace_files = [os.path.join(trace_dir, f) for f in os.listdir(trace_dir) if f.endswith('.gz')]

# Verificar que los archivos existen
for trace_file in trace_files:
    if not os.path.exists(trace_file):
        print(f"El archivo {trace_file} no se encuentra en la ruta especificada.")
        exit(1)

def simulate_cache(trace_file, l1_cache):
    with gzip.open(trace_file, 'rt') as trace_fh:
        for line in trace_fh:
            line = line.rstrip()
            access_type, hex_str_address = line.split(" ")
            address = int(hex_str_address, 16)
            l1_cache.access(access_type, address)

results = []

# Simulación para cada archivo de trace
for trace_file in trace_files:
    l1_cache = Cache(l1_cache_size, l1_cache_assoc, block_size, l1_repl_policy)
    simulate_cache(trace_file, l1_cache)
    
    l1_miss_rate = l1_cache.total_misses / l1_cache.total_access
    amat = l1_hit_time + (l1_miss_rate * miss_penalty)
    results.append((os.path.basename(trace_file), amat, l1_cache.total_misses, l1_cache.total_access))

# Calcular media geométrica del AMAT
amat_values = [result[1] for result in results]
geo_mean_amat = math.exp(sum(math.log(amat) for amat in amat_values) / len(amat_values))

# Mostrar resultados
print("Resultados de la simulación:")
print("Trace\t\t\tAMAT\t\tMisses\t\tAccesses")
for result in results:
    print(f"{result[0]}\t{result[1]:.2f}\t\t{result[2]}\t\t{result[3]}")

print(f"\nMedia geométrica del AMAT: {geo_mean_amat:.2f}")

# Crear gráfica de AMAT por trace
trace_names = [result[0] for result in results]
amat_values = [result[1] for result in results]

plt.figure(figsize=(12, 6))
plt.bar(trace_names, amat_values, color='blue')
plt.xlabel('Trace')
plt.ylabel('AMAT')
plt.title('AMAT por Trace')
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()
