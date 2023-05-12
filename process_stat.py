import re
import sys
import os, glob

# PredictionRegex = r'(?P<name>Branch Prediction Accuracy): (?P<value>[0-9\.]+)%'
# IPCMetricRegex = r'(?P<name>cumulative IPC): (?P<value>[0-9\.]+)'
# InstructionsRegex = r'(?P<name>instructions):(?P<value>[0-9]+)'
# CyclesRegex = r'(?P<name>cycles):(?P<value>[0-9]+)'
# MKPIRegex = r'(?P<name>MPKI):(?P<value>[0-9]+)'
# ROBMissRegex = r'(?P<name>Average ROB Occupancy at Mispredict):(?P<value>[0-9]+)'
# traceRegex = r'CPU [0-9] runs (?P<trace>.*\.champsimtrace\.xz)'

rrr = re.compile(r'CPU')

metrics = [
    r'CPU [0-9] runs (?P<name>.*\.champsimtrace\.xz)',
    r'(?P<cpu>CPU [0-9]) (?P<prediction>Branch Prediction Accuracy): (?P<prediction_value>[0-9\.]+)% (?P<mpki>MPKI): (?P<mpki_value>[0-9\.]+) (?P<rob>Average ROB Occupancy at Mispredict): (?P<rob_value>[0-9\.]+)',
    r'(?P<cpu>CPU [0-9]) (?P<ipc>cumulative IPC): (?P<ipc_value>[0-9\.]+)',
    r'Simulation complete (?P<cpu>CPU [0-9]+) (?P<instrs>instructions): (?P<instr_value>[0-9]+) (?P<cycles>cycles): (?P<cycle_value>[0-9]+)',
    r'(?P<name>LLC TOTAL)[ \t]+(?P<access>ACCESS):[ \t]+(?P<access_value>[0-9]+)[ \t]+(?P<hit>HIT):[ \t]+(?P<hit_val>[0-9]+)',
    r'(?P<name>cpu[0-9]_DTLB) TOTAL[ \t]+(?P<access>ACCESS):[ \t]+(?P<access_value>[0-9]+)[ \t]+(?P<hit>HIT):[ \t]+(?P<hit_val>[0-9]+)',
    r'(?P<name>cpu[0-9]_ITLB) TOTAL[ \t]+(?P<access>ACCESS):[ \t]+(?P<access_value>[0-9]+)[ \t]+(?P<hit>HIT):[ \t]+(?P<hit_val>[0-9]+)',
    r'(?P<name>cpu[0-9]_L1D) TOTAL[ \t]+(?P<access>ACCESS):[ \t]+(?P<access_value>[0-9]+)[ \t]+(?P<hit>HIT):[ \t]+(?P<hit_val>[0-9]+)',
    r'(?P<name>cpu[0-9]_L1I) TOTAL[ \t]+(?P<access>ACCESS):[ \t]+(?P<access_value>[0-9]+)[ \t]+(?P<hit>HIT):[ \t]+(?P<hit_val>[0-9]+)',
    r'(?P<name>cpu[0-9]_L2C) TOTAL[ \t]+(?P<access>ACCESS):[ \t]+(?P<access_value>[0-9]+)[ \t]+(?P<hit>HIT):[ \t]+(?P<hit_val>[0-9]+)',
    r'(?P<name>cpu[0-9]_STLB) TOTAL[ \t]+(?P<access>ACCESS):[ \t]+(?P<access_value>[0-9]+)[ \t]+(?P<hit>HIT):[ \t]+(?P<hit_val>[0-9]+)',
]


def process_and_accumulate(inputDir : str, suffix : str, outputFile : str):
    for filename in glob.glob(f'{inputDir}/{suffix}'):
        with open(os.path.join(os.getcwd(), filename), 'r') as f: # open in readonly mode
            # do your stuff
            lines = f.readlines()
            print(lines[24])
            text = '\n'.join(lines)
            for i, regex in enumerate(metrics):
                result = re.compile(regex).findall(text)
                if result:
                    print(result)
                else:
                    print('no')


            
            



if __name__ == '__main__':
    dir = 'stat'
    outdir = 'stat/results'
    process_and_accumulate(f'{dir}/fifo_cache', '*.log', 'output')

