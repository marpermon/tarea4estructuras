from optparse import OptionParser
import gzip
from cache import *

parser = OptionParser()
parser.add_option("-s", dest="cache_capacity")
parser.add_option("-a", dest="cache_assoc")
parser.add_option("-b", dest="block_size")
parser.add_option("-r", dest="repl_policy")
parser.add_option("-t", dest="TRACE_FILE")

(options, args) = parser.parse_args()

cache = cache(options.cache_capacity, options.cache_assoc, options.block_size, options.repl_policy)
cache.print_info()
i = 0 #SOLO PARA DEBUG
with gzip.open(options.TRACE_FILE,'rt') as trace_fh:
    for line in trace_fh:
        line = line.rstrip()
        access_type, hex_str_address  = line.split(" ")
        address = int(hex_str_address, 16)
        cache.access(access_type, address)
        #SOLO PARA DEBUG
        #i+=1
        #if i == 25:
        #    break
cache.print_stats()
