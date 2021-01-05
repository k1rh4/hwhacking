import glob 
import os
keywords = ["/bin/sh","popen","system","passw","token","secret", "dlopen","setreuid","upload","download","tar ","unzip"]
for file_name in glob.glob("./*"):
    print("[+] %s " %(file_name))
    for keyword in keywords :
        os.system("strings %s | grep %s | awk {'print \"\t\"$0'}" % (file_name, keyword)) 

