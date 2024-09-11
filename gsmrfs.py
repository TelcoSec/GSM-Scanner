#!/usr/bin/python3
#!coding=utf-8


import argparse
import subprocess
import sys
#import pyshark
from argparse import ArgumentParser


gain='34'
interface='rtl-0' # rtl-0
speed='5'
seconds='10'



class GSMScan():

    #cfile=arfcn+'.cfile'
    gain='34'
    interface='hackrf' # rtl-0
    speed='5'
    seconds='10'
    def detect_bts(self,interface,gain,speed):
        print('Scanning BTSs Around..')
        scan_BTS = subprocess.run(["/usr/local/bin/grgsm_scanner", "--band=GSM900",'--gain='+gain,'--args='+interface,'--speed='+speed])
        return scan_BTS



class GSMSniff():
    def sniffarfcn(self,arfcn,seconds,cfile):
        print('Scanning ARFCN', arfcn,'for', seconds,'Seconds')
        sniff_ARFCN = subprocess.run(["/usr/local/bin/grgsm_capture", "--arfcn="+arfcn,'--rec-length='+seconds,arfcn+'.cfile'],capture_output=True)
        return arfcn,cfile

class GSMDecode():
    def BCCH(self,arfcn,b_timeslot,cfile):
        decode_BCCH = subprocess.run(["/usr/local/bin/grgsm_decode", "--arfcn="+arfcn,'--mode=BCCH','--timeslot='+b_timeslot,'--cfile=test'])

    def SDCCH8(self,arfcn,d_timeslot,cfile):
        print("The Corrrect TimeSlot is inside the Immediate Assignment \n Channel description packet")
        decode_SDCCH8 = subprocess.run(["/usr/local/bin/grgsm_decode", "--arfcn="+arfcn,'--mode=SDCCH8','--timeslot='+d_timeslot,'--print-bursts','--cfile='+cfile],capture_output=True)

    def SMS(d_timeslot,cfile):
        decode_SMS = subprocess.run(["/usr/local/bin/grgsm_decode", '--arfcn='+scanner.arfcn,'-s 1e6','--timeslot='+d_timeslot,'--mode=SDCCH8','-e 3','-k SIMKEY','--cfile='+cfile],capture_output=True)
    def VOICE(codec):
        pass


scanner=GSMScan()
sniff=GSMSniff()
decode=GSMDecode()

def learn():
    print("\n\n\n")
    print("ARFCN 45Mhz difference \nbetween Downlink and Uplink")
    print("Modulation: GMSK")
    print("Access: FDMA or TDMA")
    print("TDMA deals with Physical Channels")
    print("TDMA Frames =  8 Timeslots (Physical Channels)")
    print("TDMA Frame = 4.62 ms")
    print("TDMA Channel = 0.557 ms = burst period")
    print("TDMA Signalling Channel = 0")
    print("TDMA Traffic Channel = 1-7")
    print("TDMA Frames = Multiframe, SuperFrame, hyperFrame")
    print("\n\n\n")





def decode():
    print("Running decode function")
    decode.BCCH(arfcn,timeslot,cfile)
    decode.SDCCH8(arfcn,timeslot,cfile)
    arfcn=input('Sniff what ARFCN: ')
    cfile=arfcn+'.cfile'
    #timeslot='0'
   # sniff.arfcn(arfcn,scan.seconds,cfile)
    for timeslot in range(5):
        print('Decoding BCCH Timeslot:'+str(timeslot))
        decode.BCCH(arfcn,str(timeslot),cfile)
    for timeslot in range(5):
        print('Decoding SDCCH8 Timeslot:'+str(timeslot))
        decode.SDCCH8(arfcn,str(timeslot),cfile)

def main():
    parser = argparse.ArgumentParser(
                        prog='GSMTesting',
                        description='GSM Sniffing, Decoding, Cracking',
                        epilog='Join the COmmunity: ')
    subparsers = parser.add_subparsers(dest="command")
    #Scan
    parser_scan = subparsers.add_parser("scan", help="Scan BTSs Around!")
    scan = parser.add_argument_group('scan', 'Scan BTSs around...')
#    scan.add_argument('foo', help='foo help')
    #Sniff
    parser_sniff = subparsers.add_parser("sniff", help="Sniff ARFCN frequencies")
    parser_sniff.add_argument("--arfcn", dest='sniff',help="ARFCN to sniff. Run a scan first.")
    parser_sniff.add_argument("--file", dest='sniff',type=str, help="Save CFILE.")

    sniff = parser.add_argument_group('sniff', 'Sniff ARFC')
    sniff.add_argument('--arfcn', dest='sniff',help="ARFCN to sniff. Run a scan first.")
    sniff.add_argument('--cfile', dest='sniff',type=str, help="Save CFILE.")



    decode = parser.add_argument_group('decode', 'decode description')
    decode.add_argument('--dec', help='bar help')
    decode.add_argument("--file", dest='decode', type=argparse.FileType('r'), help="Cfile to decode.")

    parser.add_argument("--install", action="store_true", help="Install Dependencies")
    parser.add_argument("--learn", action="store_true", help="Learn some stuff")
    args = parser.parse_args()


    if args.command == "scan":
        scanner.detect_bts(scanner.interface,scanner.gain,scanner.speed)
        arfcn=input('Sniff what ARFCN: ')
    elif args.command == "sniff":
        sniff.sniffarfcn(args.arfcn,seconds,'dev.cfile')
    elif args.command == "decode":
        decode()



if __name__ == '__main__':
    main()
