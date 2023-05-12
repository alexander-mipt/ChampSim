import re
import sys
import os, glob

PredictionRegex = r'(?P<name>Branch Prediction Accuracy): (?P<value>[0-9\.]+)%'
IPCMetricRegex = r'(?P<name>cumulative IPC): (?P<value>[0-9\.]+)'
InstructionsRegex = r'(?P<name>instructions):(?P<value>[0-9]+)'
CyclesRegex = r'(?P<name>cycles):(?P<value>[0-9]+)'
MKPIRegex = r'(?P<name>MPKI):(?P<value>[0-9]+)'
ROBMissRegex = r'(?P<name>Average ROB Occupancy at Mispredict):(?P<value>[0-9]+)'

cache_Regex = [
    r'(?P<name>LLC) TOTAL[ \t]+(?P<access>ACCESS):[ \t]+(?P<access_value>[0-9]+)[ \t]+(?P<hit>HIT):[ \t]+(?P<hit_val>[0-9]+)',
    r'(?P<name>cpu[0-9]_DTLB) TOTAL[ \t]+(?P<access>ACCESS):[ \t]+(?P<access_value>[0-9]+)[ \t]+(?P<hit>HIT):[ \t]+(?P<hit_val>[0-9]+)',
    r'(?P<name>cpu[0-9]_ITLB) TOTAL[ \t]+(?P<access>ACCESS):[ \t]+(?P<access_value>[0-9]+)[ \t]+(?P<hit>HIT):[ \t]+(?P<hit_val>[0-9]+)',
    r'(?P<name>cpu[0-9]_L1D) TOTAL[ \t]+(?P<access>ACCESS):[ \t]+(?P<access_value>[0-9]+)[ \t]+(?P<hit>HIT):[ \t]+(?P<hit_val>[0-9]+)',
    r'(?P<name>cpu[0-9]_L1I) TOTAL[ \t]+(?P<access>ACCESS):[ \t]+(?P<access_value>[0-9]+)[ \t]+(?P<hit>HIT):[ \t]+(?P<hit_val>[0-9]+)',
    r'(?P<name>cpu[0-9]_L2C) TOTAL[ \t]+(?P<access>ACCESS):[ \t]+(?P<access_value>[0-9]+)[ \t]+(?P<hit>HIT):[ \t]+(?P<hit_val>[0-9]+)',
    r'(?P<name>cpu[0-9]_STLB) TOTAL[ \t]+(?P<access>ACCESS):[ \t]+(?P<access_value>[0-9]+)[ \t]+(?P<hit>HIT):[ \t]+(?P<hit_val>[0-9]+)',
]


def process_and_accumulate(inputDir : str, suffix : str, outputFile : str, *metrics):
    for filename in glob.glob(suffix):
        with open(os.path.join(os.getcwd(), filename), 'r') as f: # open in readonly mode
            # do your stuff
            line = f.readline()
            while(line):

                line = f.readline()
            



if __name__ == '__main__':
    dir = 'stat/'
    outdir = 'stat/results'
