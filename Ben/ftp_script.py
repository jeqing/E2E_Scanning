

#==========================================================================================================#
# Python FTP scripts

import re, sys, os                                                   
import time
   
    

## Call main class
if __name__ == "__main__":

    batchFile = "cd To_D&B\nls\nput \"D:\Statements\Retrieved\\account_copies_28MAR2017.zip\"\nls"

    print (batchFile)

    fopen = open('d:\batch_ftp.txt', 'w')
    fopen.write(batchFile)
    fopen.close()

    cmd = "\"\"C:\Program Files (x86)\PuTTY\ps_ftp.exe\" host -l username-pw password-P port_number -v -b \"d:\\_ftp.txt\" > \"G:\\ch\\shared03\\cms\\WORK REQUESTS\\WR1500-DNB Account Copies\\ftp_results.txt\"\""
    print cmd

    ret = os.system(cmd)

    sys.exit(ret)     
