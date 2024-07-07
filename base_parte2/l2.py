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
l2_cache_sizes = [64, 128]  # kB
l2_cache_assocs = [8, 16]
l2_repl_policy = "l"
l2_hit_time = 12  # ciclos de reloj
miss_penalty = 500  # ciclos de reloj

# Directorio de archivos de trace
trace_dir = r".\..\traces\traces

# Obtener todos los archivos de trace en el directorio
trace_files = [os.path.join(trace_dir, f) for f in os.listdir(trace_dir) if f.endswith('.gz')]

# Verificar que los archivos existen
for trace_file in trace_files:
    if not os.path.exists(trace_file):
        print(f"El archivo {trace_file} no se encuentra en la ruta especificada.")
        exit(1)

def simulate_cache(trace_file, l1_cache, l2_cache):
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
                if is_l2_miss:
                    l2_cache.access(access_type, address)  # Traer a L2
                l1_cache.access(access_type, address)  # Traer a L1

results = []

# Probar todas las combinaciones de tamaño y asociatividad de L2
for l2_cache_size in l2_cache_sizes:
    for l2_cache_assoc in l2_cache_assocs:
        amats = []
        for trace_file in trace_files:
            l1_cache = Cache(l1_cache_size, l1_cache_assoc, block_size, l1_repl_policy)
            l2_cache = Cache(l2_cache_size, l2_cache_assoc, block_size, l2_repl_policy)
            
            simulate_cache(trace_file, l1_cache, l2_cache)
            
            l1_miss_rate = l1_cache.total_misses / l1_cache.total_access
            l2_miss_rate = l2_cache.total_misses / l2_cache.total_access
            amat = l1_hit_time + (l1_miss_rate * (l2_hit_time + (l2_miss_rate * miss_penalty)))
            amats.append(amat)
        
        # Calcular media geométrica del AMAT para la configuración actual
        geo_mean_amat = math.exp(sum(math.log(amat) for amat in amats) / len(amats))
        results.append((l2_cache_size, l2_cache_assoc, geo_mean_amat))

# Mostrar resultados
print("Resultados de la simulación:")
print("L2 Size (kB)\tL2 Assoc\tAMAT (Geometric Mean)")
for result in results:
    print(f"{result[0]}\t\t{result[1]}\t\t{result[2]:.2f}")

# Crear gráfica de AMAT para cada configuración de L2
configurations = [f"L2 {result[0]}kB {result[1]}-way" for result in results]
geo_mean_amats = [result[2] for result in results]

plt.figure(figsize=(12, 6))
plt.bar(configurations, geo_mean_amats, color='green')
plt.xlabel('Configuración de L2')
plt.ylabel('AMAT (Geometric Mean)')
plt.title('AMAT Geométrico para Diferentes Configuraciones de L2')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

