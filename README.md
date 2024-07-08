# Tarea #4 Estructuras de computadoras digitales 2 - IE 0521
En esta tarea se desarrolló la simulación de las distintas configuraciones del caché, utilizando traces que contienen información de una gran cantidad de accesos a memoria, con el fin de medir su rendimiento, y luego se realizan gráficas para lograr observar mejor los resultados de estas simulaciones, este trabajo se dividió en dos partes:

# 1.Parte 1:
Dentro de la carpeta "base_parte1" se encuentra la simulación de un caché con un solo nivel, para su ejecución se debe ejecutar el siguiente comando: 
python cache_cache.py -s <cache_capacity> -a <cache_assoc> -b <block_size> -r <repl_policy> -t <TRACE_FILE>

Donde la capacidad del caché en kB (-s), asociatividad del caché (-a) y el tamaño del bloque en bytes (-b) será un número entero entre 2, 4, 8,16, 64, 128, etc, siendo únicamente potencias de 2, mientras que, la política de reemplazo (-r) es un char que una “l” (ele) indica LRU y una “r” (erre) indica aleatoria. Por último, los traces(-t) son los indicados anteriomente.

# 2.Parte 2
Dentro de la carpeta "base_parte2" se encuentra la simulación de una caché multinivel con L1, L2 y L3, para su ejecución se debe ejecutar el siguiente comando:

python simulador_cache.py --l1_s <l1_size> --l1_a <l1_assoc> [--l2 --l2_s <l2_size> --l2_a <l2_assoc>] [--l3 --l3_s <l3_size> --l3_a <l3_assoc>] -b <block_size> -t <TRACE_FILE>

Donde --l1_s, --l1_a, son la capacidad de caché y la asociatividad para el nivel L1 tienen un valor de un número entero entre 2, 4, 8,16, 64, 128, etc, siendo únicamente potencias de 2. En caso de necesitar más niveles de caché se tienen las banderas --l2 y --l3, y se agregan las mismas características que para el nivel L1 con las mismas posibilidades de valores. Por último, se tiene el tamaño del bloque en bytes (-b) tiene un valor de un número entero entre 2, 4, 8,16, 64, 128, etc, siendo únicamente potencias de 2 y los traces(-t) son los indicados anteriomente.