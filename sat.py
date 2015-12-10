#!/bin/python

import os
import argparse

def start_tune(args):
    print(os.getpid())
    
    
def parse_args():
    parser = argparse.ArgumentParser(description='Process argumants')
    parser.add_argument("-f", "--frequency", dest = "frequency", help = "Transponders frequency, MHz, e. g.: 11766, 12380.")
    parser.add_argument("-s", "--symbolrate", dest = "symbolRate", help = "The symbol rate of the modulated signal, in Ksymbols/s, e. g.: 27500, 30000.")
    parser.add_argument("-p", "--polarization", dest = "polarization", help = "\"H\"/\"V\"/\"R\"/\"L\"")
    parser.add_argument("-F", "--FEC", dest = "fec", help = "specifies the code-rate to use for Forward Error Correction; type in the first number of the code-rate, for 2/3 use --dvb-rate=2, etc. (default is 9, meaning automatic detection).")
    parser.set_defaults(func=start_tune)
    
    return parser.parse_args()

def main():
	args = parse_args()
	args.func(args)

if __name__ == '__main__':
	main()