import re
import sys
import os, glob

metrics = [
    r'CPU [0-9] runs (?P<name>.*\.champsimtrace\.xz)',
    r'(?P<cpu>CPU [0-9]) (?P<prediction>Branch Prediction Accuracy): (?P<prediction_value>([0-9\.]+)|([-]?nan))% (?P<mpki>MPKI): (?P<mpki_value>([0-9\.]+)|([-]?nan)) (?P<rob>Average ROB Occupancy at Mispredict): (?P<rob_value>([0-9\.]+)|([-]?nan))',
    r'(?P<cpu>CPU [0-9]) (?P<ipc>cumulative IPC): (?P<ipc_value>([0-9\.]+)|([-]?nan))',
    r'Simulation complete (?P<cpu>CPU [0-9]+) (?P<instrs>instructions): (?P<instr_value>[0-9]+) (?P<cycles>cycles): (?P<cycle_value>[0-9]+)',
    r'(?P<name>LLC TOTAL)[ \t]+(?P<access>ACCESS):[ \t]+(?P<access_value>[0-9]+)[ \t]+(?P<hit>HIT):[ \t]+(?P<hit_val>[0-9]+)',
    r'(?P<name>cpu[0-9]_DTLB TOTAL)[ \t]+(?P<access>ACCESS):[ \t]+(?P<access_value>[0-9]+)[ \t]+(?P<hit>HIT):[ \t]+(?P<hit_val>[0-9]+)',
    r'(?P<name>cpu[0-9]_ITLB TOTAL)[ \t]+(?P<access>ACCESS):[ \t]+(?P<access_value>[0-9]+)[ \t]+(?P<hit>HIT):[ \t]+(?P<hit_val>[0-9]+)',
    r'(?P<name>cpu[0-9]_L1D TOTAL)[ \t]+(?P<access>ACCESS):[ \t]+(?P<access_value>[0-9]+)[ \t]+(?P<hit>HIT):[ \t]+(?P<hit_val>[0-9]+)',
    r'(?P<name>cpu[0-9]_L1I TOTAL)[ \t]+(?P<access>ACCESS):[ \t]+(?P<access_value>[0-9]+)[ \t]+(?P<hit>HIT):[ \t]+(?P<hit_val>[0-9]+)',
    r'(?P<name>cpu[0-9]_L2C TOTAL)[ \t]+(?P<access>ACCESS):[ \t]+(?P<access_value>[0-9]+)[ \t]+(?P<hit>HIT):[ \t]+(?P<hit_val>[0-9]+)',
    r'(?P<name>cpu[0-9]_STLB TOTAL)[ \t]+(?P<access>ACCESS):[ \t]+(?P<access_value>[0-9]+)[ \t]+(?P<hit>HIT):[ \t]+(?P<hit_val>[0-9]+)',
]

def userError(str):
    print('Error: ', str, '.')
    exit(2)

def abortIfEmpty(list):
    for name, val in list:
        if not name or not val:
            print('Error for entry: ', name, val)
            # exit(1)

def process_entry(idx, regx):
    entries = []
    match idx:
        case 0:
            key = 'traceName'
            val = regx.group('name')
            entries.append((key, val))
            
            abortIfEmpty(entries)
            return entries
        
        case 1:
            key = f"{regx.group('cpu')} {regx.group('prediction')}"
            val = regx.group('prediction_value')
            entries.append((key, val))

            key = f"{regx.group('cpu')} {regx.group('mpki')}"
            val = regx.group('mpki_value')
            entries.append((key, val))

            key = f"{regx.group('cpu')} {regx.group('rob')}"
            val = regx.group('rob_value')
            entries.append((key, val))

            abortIfEmpty(entries)
            return entries
        
        case 2:
            key = f"{regx.group('cpu')} {regx.group('ipc')}"
            val = regx.group('ipc_value')
            entries.append((key, val))

            abortIfEmpty(entries)
            return entries
        
        case 3:
            key = f"{regx.group('cpu')} {regx.group('instrs')}"
            val = regx.group('instr_value')
            entries.append((key, val))

            key = f"{regx.group('cpu')} {regx.group('cycles')}"
            val = regx.group('cycle_value')
            entries.append((key, val))

            abortIfEmpty(entries)
            return entries
        
    if (idx >= 4 and idx <= 10):
        key = f"{regx.group('name')} {regx.group('access')}"
        val = regx.group('access_value')
        entries.append((key, val))

        key = f"{regx.group('name')} {regx.group('hit')}"
        val = regx.group('hit_val')
        entries.append((key, val))

        abortIfEmpty(entries)
        return entries
    
    userError('wrong entry')
    return None

def addInTable(entries : list, table : dict):
    # print(table)
    for key, value in entries:
        if key not in table.keys():
            table[key] = []
            table[key].append(value)
        else:
            table[key].append(value)

def checkTable(table : dict):
    inv = -1
    for key, entries in table.items():
        l = len(entries)
        if inv == -1:
            inv = l
        else:
            if l != inv:
                userError('wrong table size')


def process_and_accumulate(inputDir : str, suffix : str):
    table = dict()
    for filename in glob.glob(f'{inputDir}/{suffix}'):
        with open(os.path.join(os.getcwd(), filename), 'r') as f: # open in readonly mode
            # do your stuff
            # print('==== New trace ====\n')
            lines = f.readlines()
            text = '\n'.join(lines)
            for i, regex in enumerate(metrics):
                resultAll = re.compile(regex).findall(text)
                result = ''
                for line in lines:
                    result = re.compile(regex).search(line)
                    if result:
                        break
                
                if resultAll and result:
                    # print(resultAll)
                    # print(process_entry(i, result))
                    entries = process_entry(i, result)
                    # print(entries)
                    addInTable(entries, table)
                else:
                    userError('unlnown regex pattern')
    checkTable(table)
    # for key, array in table.items():
    #     print(f'{key}:\n{array}')
    # print(table)
    return table


def genCSV(table : dict(), file: str):
    # print(table)
    with open(file, '+w') as f:
        for key in table.keys():
            f.write(f'{key}, ')
        f.write('\n')
        
        size = len(table['traceName'])
        idx = 0
        while(idx != size):
            for key, data in table.items():
                f.write(f'{data[idx]}, ')
            f.write('\n')
            idx += 1






if __name__ == '__main__':
    dir = 'stat'
    outdir = 'stat/results'
    models = ['etalon', 'fifo_cache', 'mru_cache', 'markov_predictor_max', 'markov_predictor_prop']
    for model in models:
        table = process_and_accumulate(f'{dir}/{model}', '*.log')
        # print(table)
        genCSV(table, f'{dir}/{model}/table.csv')


