from optparse import OptionParser
import gzip
from cache import Cache

parser = OptionParser()
parser.add_option("--l1_s", dest="l1_s")
parser.add_option("--l1_a", dest="l1_a")
parser.add_option("--l2", action="store_true", dest="has_l2")
parser.add_option("--l2_s", dest="l2_s")
parser.add_option("--l2_a", dest="l2_a")
parser.add_option("--l3", action="store_true", dest="has_l3")
parser.add_option("--l3_s", dest="l3_s")
parser.add_option("--l3_a", dest="l3_a")
parser.add_option("-b", dest="block_size", default="64")
parser.add_option("-t", dest="TRACE_FILE")

(options, args) = parser.parse_args()

# Crear caché L1
l1_cache = Cache(options.l1_s, options.l1_a, options.block_size, "l")

# Crear caché L2 si está presente
l2_cache = None
if options.has_l2:
    l2_cache = Cache(options.l2_s, options.l2_a, options.block_size, "l")

# Crear caché L3 si está presente
l3_cache = None
if options.has_l3:
    l3_cache = Cache(options.l3_s, options.l3_a, options.block_size, "l")

with gzip.open(options.TRACE_FILE, 'rt') as trace_fh:
    for line in trace_fh:
        line = line.rstrip()
        access_type, hex_str_address = line.split(" ")
        address = int(hex_str_address, 16)
        
        # Acceso a L1
        is_l1_miss = l1_cache.access(access_type, address)
        
        if is_l1_miss:
            # Acceso a L2 si L1 falla
            if l2_cache:
                is_l2_miss = l2_cache.access(access_type, address)
                if is_l2_miss:
                    # Acceso a L3 si L2 falla
                    if l3_cache:
                        is_l3_miss = l3_cache.access(access_type, address)
                        if is_l3_miss:
                            l3_cache.access(access_type, address)  # Traer a L3
                        l2_cache.access(access_type, address)  # Traer a L2
                    l1_cache.access(access_type, address)  # Traer a L1
                else:
                    l1_cache.access(access_type, address)  # Traer a L1
            else:
                # Si no hay L2, traemos directamente a L1 (simulamos traer desde memoria)
                l1_cache.access(access_type, address)

# Imprimir estadísticas
print("Estadísticas y parámetros de la caché L1:")
l1_cache.print_stats()
l1_cache.print_info()
if l2_cache:
    print("\nEstadísticas y parámetros de la caché L2:")
    l2_cache.print_stats()
    l2_cache.print_info()    
if l3_cache:
    print("\nEstadísticas y parámetros de la caché L3:")
    l3_cache.print_stats()
    l3_cache.print_info()
