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

# Parámetros del caché L2
l2_cache_size = 256  # kB
l2_cache_assoc = 8
l2_repl_policy = "l"
l2_hit_time = 12  # ciclos de reloj

# Parámetros del caché L3
l3_cache_sizes = [512, 1024]  # kB
l3_cache_assocs = [16, 32]
l3_repl_policy = "l"
l3_hit_time = 60  # ciclos de reloj

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

def simulate_cache(trace_file, l1_cache, l2_cache, l3_cache=None):
    with gzip.open(trace_file, 'rt') as trace_fh:
        for line in trace_fh:
            line = line.rstrip()
            access_type, hex_str_address = line.split(" ")
            address = int(hex_str_address, 16)

            # Acceso a L1
            is_l1_miss = l1_cache.access(access_type, address)
            
            if is_l1_miss:
                # Acceso a L2 si L1 falla
                is_l2_miss = l2_cache.access(access_type, address)
                if is_l2_miss and l3_cache:
                    # Acceso a L3 si L2 falla
                    is_l3_miss = l3_cache.access(access_type, address)
                    if is_l3_miss:
                        l3_cache.access(access_type, address)  # Traer a L3
                    l2_cache.access(access_type, address)  # Traer a L2
                elif is_l2_miss:
                    l2_cache.access(access_type, address)  # Traer a L2
                l1_cache.access(access_type, address)  # Traer a L1

results = []

# Probar todas las combinaciones de tamaño y asociatividad de L3
for l3_cache_size in l3_cache_sizes:
    for l3_cache_assoc in l3_cache_assocs:
        amats = []
        for trace_file in trace_files:
            l1_cache = Cache(l1_cache_size, l1_cache_assoc, block_size, l1_repl_policy)
            l2_cache = Cache(l2_cache_size, l2_cache_assoc, block_size, l2_repl_policy)
            l3_cache = Cache(l3_cache_size, l3_cache_assoc, block_size, l3_repl_policy)
            
            simulate_cache(trace_file, l1_cache, l2_cache, l3_cache)
            
            l1_miss_rate = l1_cache.total_misses / l1_cache.total_access
            l2_miss_rate = l2_cache.total_misses / l2_cache.total_access
            l3_miss_rate = l3_cache.total_misses / l3_cache.total_access
            amat = l1_hit_time + (l1_miss_rate * (l2_hit_time + (l2_miss_rate * (l3_hit_time + (l3_miss_rate * miss_penalty)))))
            amats.append(amat)
        
        # Calcular media geométrica del AMAT para la configuración actual
        geo_mean_amat = math.exp(sum(math.log(amat) for amat in amats) / len(amats))
        results.append((l3_cache_size, l3_cache_assoc, geo_mean_amat))

# Mostrar resultados
print("Resultados de la simulación:")
print("L3 Size (kB)\tL3 Assoc\tAMAT (Geometric Mean)")
for result in results:
    print(f"{result[0]}\t\t{result[1]}\t\t{result[2]:.2f}")

# Ordenar traces por AMAT de solo L1
l1_amats = []
for trace_file in trace_files:
    l1_cache = Cache(l1_cache_size, l1_cache_assoc, block_size, l1_repl_policy)
    with gzip.open(trace_file, 'rt') as trace_fh:
        for line in trace_fh:
            line = line.rstrip()
            access_type, hex_str_address = line.split(" ")
            address = int(hex_str_address, 16)
            l1_cache.access(access_type, address)
    
    l1_miss_rate = l1_cache.total_misses / l1_cache.total_access
    amat = l1_hit_time + (l1_miss_rate * miss_penalty)
    l1_amats.append((trace_file, amat))

l1_amats.sort(key=lambda x: x[1])

# Mejor caso de L1+L2
l1_l2_amats = []
for trace_file, _ in l1_amats:
    l1_cache = Cache(l1_cache_size, l1_cache_assoc, block_size, l1_repl_policy)
    l2_cache = Cache(l2_cache_size, l2_cache_assoc, block_size, l2_repl_policy)
    
    simulate_cache(trace_file, l1_cache, l2_cache)  # Sin L3
    
    l1_miss_rate = l1_cache.total_misses / l1_cache.total_access
    l2_miss_rate = l2_cache.total_misses / l2_cache.total_access
    amat = l1_hit_time + (l1_miss_rate * (l2_hit_time + (l2_miss_rate * miss_penalty)))
    l1_l2_amats.append(amat)

# Mejor caso de L1+L2+L3
l1_l2_l3_amats = []
best_l3_config = min(results, key=lambda x: x[2])  # Encuentra la mejor configuración de L3
best_l3_size = best_l3_config[0]
best_l3_assoc = best_l3_config[1]

for trace_file, _ in l1_amats:
    l1_cache = Cache(l1_cache_size, l1_cache_assoc, block_size, l1_repl_policy)
    l2_cache = Cache(l2_cache_size, l2_cache_assoc, block_size, l2_repl_policy)
    l3_cache = Cache(best_l3_size, best_l3_assoc, block_size, l3_repl_policy)
    
    simulate_cache(trace_file, l1_cache, l2_cache, l3_cache)
    
    l1_miss_rate = l1_cache.total_misses / l1_cache.total_access
    l2_miss_rate = l2_cache.total_misses / l2_cache.total_access
    l3_miss_rate = l3_cache.total_misses / l3_cache.total_access
    amat = l1_hit_time + (l1_miss_rate * (l2_hit_time + (l2_miss_rate * (l3_hit_time + (l3_miss_rate * miss_penalty)))))
    l1_l2_l3_amats.append(amat)

# Generar gráficos
trace_names = [os.path.basename(trace_file).split('.')[0] for trace_file, _ in l1_amats]

plt.figure(figsize=(12, 6))
plt.plot(trace_names, [x[1] for x in l1_amats], label='Solo L1')
plt.plot(trace_names, l1_l2_amats, label='Mejor L1+L2')
plt.plot(trace_names, l1_l2_l3_amats, label='Mejor L1+L2+L3')
plt.xlabel('Trace')
plt.ylabel('AMAT')
plt.title('Comparación de AMAT')
plt.xticks(rotation=45, ha='right')
plt.legend()
plt.show()
