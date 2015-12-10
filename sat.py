#!/bin/python

import argparse
from shlex import split
from os import getpid, remove, devnull
from sys import argv
from subprocess import Popen, PIPE, call, STDOUT

def start_tune(args):
    
    tmpFile = "/tmp/"+str(argv[0]).split("/")[-1]+"."+str(getpid())
    scanLine = "S "+args.frequency+"000 "+args.polarization+" "+args.symbolRate+"000 "+args.fec
    
    with open(tmpFile, "w") as f:
        f.write(scanLine+"\n")
        
    scan_cmd = "scandvb -a "+args.N+" "+tmpFile
    channels = list()

    scan = Popen(scan_cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    for i in scan.stdout:
        channels.append(i.split(":"))
    
    remove(tmpFile)
    
    vlc_cmd = "/usr/bin/vlc -v --color --ttl 12  --ts-es-id-pid "
    # if args.daemon == "yes":
    #     vlc_cmd = vlc_cmd + " -d "
        
    if len(channels) > 0:
        
        vlc_cmd = vlc_cmd + "dvb-s:// --dvb-budget-mode --dvb-frequency={0}000 --dvb-srate={1}000 --dvb-polarization={2} --sout-standard-access=http --sout-mux-caching=5000 --sout-standard-mux=ts --sout '#duplicate".format(args.frequency, args.symbolRate, args.polarization) + "{"
        streams = list()
        info = list()
        streams = list()
        d_port = args.port - 1
        for i in channels:
            d_port += 1
            streams.append("dst=std{dst="+args.addr+":"+str(d_port)+"},select=\"program="+i[-1].replace("\n", "")+"\", ")
            info.append("{0:<20} - http://{1}:{2}".format(i[0],args.addr, d_port))
        
        streams[-1] = streams[-1][0:(len(streams[-1]) - 2)]
        
        for i in streams:
            vlc_cmd = vlc_cmd + i + " "
        vlc_cmd = vlc_cmd + "}'"
        
        print(vlc_cmd)
        for i in info:
            print(i)
            
        FNULL = open(devnull, 'w')
        retcode = call(split(vlc_cmd), stdout=FNULL, stderr=STDOUT)
    
def parse_args():
    parser = argparse.ArgumentParser(description='Process argumants')
    parser.add_argument("-f", "--frequency", type=str, dest = "frequency", help = "Transponders frequency, MHz, e. g.: 11766, 12380")
    parser.add_argument("-s", "--symbolrate", type=str, dest = "symbolRate", help = "The symbol rate of the modulated signal, in Ksymbols/s, e. g.: 27500, 30000")
    parser.add_argument("-p", "--polarization", type=str, dest = "polarization", help = "\"H\"/\"V\"/\"R\"/\"L\"")
    parser.add_argument("-F", "--FEC", type=str, dest = "fec", default = "3/4", help = "specifies the code-rate to use for Forward Error Correction, like 2/3, 3/4, 5/6")
    parser.add_argument("-a", "--adapter", type=str, dest = "N", default = "0", help = "use DVB /dev/dvb/adapterN/")
    parser.add_argument("-H", "--adddress", type=str, dest = "addr", default = "0.0.0.0", help = "IP-address for listening sockets, by default = 0.0.0.0")
    # parser.add_argument("-D", "--daemon", type=str, dest = "daemon", default = "yes", help = "Run vlc as daemon")
    parser.add_argument("-P", "--start-port", type=int, dest = "port", default = 8000, help = "Start port for sockets")
    parser.set_defaults(func=start_tune)
    
    return parser.parse_args()

def main():
	args = parse_args()
	args.func(args)

if __name__ == '__main__':
	main()