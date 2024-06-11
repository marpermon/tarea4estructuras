from math import log2 ,floor #line:1
class cache :#line:3
    def __init__ (OOOOO0OO000OOOOOO ,O0O0OOO0O0O000OO0 ,O0OOOO0OOOOO00OOO ,OOOOOO00O0OO00OOO ,OOO000O0O0O0OO00O ):#line:4
        OOOOO0OO000OOOOOO .total_access =0 #line:6
        OOOOO0OO000OOOOOO .total_misses =0 #line:7
        OOOOO0OO000OOOOOO .total_reads =0 #line:8
        OOOOO0OO000OOOOOO .total_read_misses =0 #line:9
        OOOOO0OO000OOOOOO .total_writes =0 #line:10
        OOOOO0OO000OOOOOO .total_write_misses =0 #line:11
        OOOOO0OO000OOOOOO .cache_capacity =int (O0O0OOO0O0O000OO0 )#line:13
        OOOOO0OO000OOOOOO .cache_assoc =int (O0OOOO0OOOOO00OOO )#line:14
        OOOOO0OO000OOOOOO .block_size =int (OOOOOO00O0OO00OOO )#line:15
        OOOOO0OO000OOOOOO .repl_policy =OOO000O0O0O0OO00O #line:16
        OOOOO0OO000OOOOOO .byte_offset_size =log2 (OOOOO0OO000OOOOOO .block_size )#line:18
        OOOOO0OO000OOOOOO .num_sets =int ((OOOOO0OO000OOOOOO .cache_capacity *1024 )/(OOOOO0OO000OOOOOO .block_size *OOOOO0OO000OOOOOO .cache_assoc ))#line:19
        OOOOO0OO000OOOOOO .index_size =int (log2 (OOOOO0OO000OOOOOO .num_sets ))#line:20
        OOOOO0OO000OOOOOO .valid_table =[[False for OOO0OO0OOOOO00OOO in range (OOOOO0OO000OOOOOO .cache_assoc )]for O00O00O0000OO00O0 in range (OOOOO0OO000OOOOOO .num_sets )]#line:22
        OOOOO0OO000OOOOOO .tag_table =[[0 for OOOOOO0000O00OOOO in range (OOOOO0OO000OOOOOO .cache_assoc )]for O00OOO00O00OOOOO0 in range (OOOOO0OO000OOOOOO .num_sets )]#line:23
        OOOOO0OO000OOOOOO .repl_table =[[0 for OO0000O0O00OOO0O0 in range (OOOOO0OO000OOOOOO .cache_assoc )]for OOOOOO00OO0OOOOO0 in range (OOOOO0OO000OOOOOO .num_sets )]#line:24
    def print_info (O0000OO0OOOO0OOOO ):#line:26
        print ("Parámetros del caché:")#line:27
        print ("\tCapacidad:\t\t\t"+str (O0000OO0OOOO0OOOO .cache_capacity )+"kB")#line:28
        print ("\tAssociatividad:\t\t\t"+str (O0000OO0OOOO0OOOO .cache_assoc ))#line:29
        print ("\tTamaño de Bloque:\t\t\t"+str (O0000OO0OOOO0OOOO .block_size )+"B")#line:30
        print ("\tPolítica de Reemplazo:\t\t\t"+str (O0000OO0OOOO0OOOO .repl_policy ))#line:31
    def print_stats (O0O00O000O0OO0O0O ):#line:33
        print ("Resultados de la simulación")#line:34
        O0OO0OOO00OOOO0O0 =(100.0 *O0O00O000O0OO0O0O .total_misses )/O0O00O000O0OO0O0O .total_access #line:35
        O0OO0OOO00OOOO0O0 ="{:.3f}".format (O0OO0OOO00OOOO0O0 )#line:36
        O00OOOOOO0O0000OO =(100.0 *O0O00O000O0OO0O0O .total_read_misses )/O0O00O000O0OO0O0O .total_reads #line:37
        O00OOOOOO0O0000OO ="{:.3f}".format (O00OOOOOO0O0000OO )#line:38
        OOO0OO0OOO00O0OO0 =(100.0 *O0O00O000O0OO0O0O .total_write_misses )/O0O00O000O0OO0O0O .total_writes #line:39
        OOO0OO0OOO00O0OO0 ="{:.3f}".format (OOO0OO0OOO00O0OO0 )#line:40
        OOOO0OO000O00OO0O =str (O0O00O000O0OO0O0O .total_misses )+","+O0OO0OOO00OOOO0O0 +"%,"+str (O0O00O000O0OO0O0O .total_read_misses )+","#line:41
        OOOO0OO000O00OO0O +=O00OOOOOO0O0000OO +"%,"+str (O0O00O000O0OO0O0O .total_write_misses )+","+OOO0OO0OOO00O0OO0 +"%"#line:42
        print (OOOO0OO000O00OO0O )#line:43
    def access (O0OOO0O0OOOO0OO00 ,O0O0O0O0O0OOO0O0O ,OOOO0O00OOO00OOO0 ):#line:45
        O0OOOO0OOO0OO0O0O =int (OOOO0O00OOO00OOO0 %(2 **O0OOO0O0OOOO0OO00 .byte_offset_size ))#line:46
        OOO0OO000OO0O0000 =int (floor (OOOO0O00OOO00OOO0 /(2 **O0OOO0O0OOOO0OO00 .byte_offset_size ))%(2 **O0OOO0O0OOOO0OO00 .index_size ))#line:47
        O0OOOOO000OO0O000 =int (floor (OOOO0O00OOO00OOO0 /(2 **(O0OOO0O0OOOO0OO00 .byte_offset_size +O0OOO0O0OOOO0OO00 .index_size ))))#line:48
        OOO0OO0000O00O0O0 =O0OOO0O0OOOO0OO00 .find (OOO0OO000OO0O0000 ,O0OOOOO000OO0O000 )#line:50
        OO0OO0O0O00OO0O0O =False #line:51
        if OOO0OO0000O00O0O0 ==-1 :#line:53
            O0OOO0O0OOOO0OO00 .bring_to_cache (OOO0OO000OO0O0000 ,O0OOOOO000OO0O000 )#line:54
            O0OOO0O0OOOO0OO00 .total_misses +=1 #line:55
            if O0O0O0O0O0OOO0O0O =="r":#line:56
                O0OOO0O0OOOO0OO00 .total_read_misses +=1 #line:57
            else :#line:58
                O0OOO0O0OOOO0OO00 .total_write_misses +=1 #line:59
            OO0OO0O0O00OO0O0O =True #line:60
        O0OOO0O0OOOO0OO00 .total_access +=1 #line:62
        if O0O0O0O0O0OOO0O0O =="r":#line:63
            O0OOO0O0OOOO0OO00 .total_reads +=1 #line:64
        else :#line:65
            O0OOO0O0OOOO0OO00 .total_writes +=1 #line:66
        return OO0OO0O0O00OO0O0O #line:68
    def find (OOO00OOOOOOOOOOOO ,O0O00000O0OOOO0O0 ,OOO0O000OO0O0O0OO ):#line:70
        for O0OOO00OO0O0000O0 in range (OOO00OOOOOOOOOOOO .cache_assoc ):#line:71
            if OOO00OOOOOOOOOOOO .valid_table [O0O00000O0OOOO0O0 ][O0OOO00OO0O0000O0 ]and (OOO00OOOOOOOOOOOO .tag_table [O0O00000O0OOOO0O0 ][O0OOO00OO0O0000O0 ]==OOO0O000OO0O0O0OO ):#line:72
                return O0OOO00OO0O0000O0 #line:73
        return -1 #line:74
    def bring_to_cache (OOOO0000OO0OOO0OO ,O00OO0000OO0O00O0 ,OO00O0OOOO0O00O0O ):#line:76
        OO000OO0OOOO0O00O =-1 #line:78
        for OO000O00OO0000O0O in range (OOOO0000OO0OOO0OO .cache_assoc ):#line:79
            if not OOOO0000OO0OOO0OO .valid_table [O00OO0000OO0O00O0 ][OO000O00OO0000O0O ]:#line:80
                OOOO0000OO0OOO0OO .valid_table [O00OO0000OO0O00O0 ][OO000O00OO0000O0O ]=True #line:81
                OOOO0000OO0OOO0OO .tag_table [O00OO0000OO0O00O0 ][OO000O00OO0000O0O ]=OO00O0OOOO0O00O0O #line:82
                OOOO0000OO0OOO0OO .repl_table [O00OO0000OO0O00O0 ][OO000O00OO0000O0O ]=OOOO0000OO0OOO0OO .cache_assoc -1 #line:83
                OO000OO0OOOO0O00O =OO000O00OO0000O0O #line:84
                break #line:85
        if OOOO0000OO0OOO0OO .repl_policy =="l":#line:88
            OO00000OOO000O00O =999999 #line:89
            for OO000O00OO0000O0O in range (OOOO0000OO0OOO0OO .cache_assoc ):#line:92
                OOO0OO00O0O0000OO =OOOO0000OO0OOO0OO .repl_table [O00OO0000OO0O00O0 ][OO000O00OO0000O0O ]#line:93
                if OOO0OO00O0O0000OO <OO00000OOO000O00O :#line:94
                    OO00000OOO000O00O =OO000O00OO0000O0O #line:95
            OOOO0000OO0OOO0OO .valid_table [O00OO0000OO0O00O0 ][OO00000OOO000O00O ]=True #line:97
            OOOO0000OO0OOO0OO .tag_table [O00OO0000OO0O00O0 ][OO00000OOO000O00O ]=OO00O0OOOO0O00O0O #line:98
            OOOO0000OO0OOO0OO .repl_table [O00OO0000OO0O00O0 ][OO00000OOO000O00O ]=OOOO0000OO0OOO0OO .cache_assoc -1 #line:99
            OO000OO0OOOO0O00O =OO00000OOO000O00O #line:100
            for OO000O00OO0000O0O in range (OOOO0000OO0OOO0OO .cache_assoc ):#line:103
                if OO000O00OO0000O0O ==OO000OO0OOOO0O00O :#line:104
                    continue #line:105
                else :#line:106
                    OOOO0000OO0OOO0OO .repl_table [O00OO0000OO0O00O0 ][OO000O00OO0000O0O ]-=1 
