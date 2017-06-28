import re, sys, os                                                   
import time
   
    
def transferFiles():

    batchFile = "cd C:\CK\E2E_Scanning\Zipped_Files\zipped_files_20170609_111338.zip"

    print (batchFile)

    fopen = open('C:\CK\E2E_Scanning\Zipped_Files\batch_ftp.txt', 'w')
    fopen.write(batchFile)
    fopen.close()

    cmd = "C:\Program Files\PuTTY" psftp host -l username-pw password-P port_number -v -b \"d:\\_ftp.txt\" > \"G:\\ch\\shared03\\cms\\WORK REQUESTS\\WR1500-DNB Account Copies\\ftp_results.txt\"\""
    print cmd

    ret = os.system(cmd)

    sys.exit(ret)     
