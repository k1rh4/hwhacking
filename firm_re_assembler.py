#!/bin/python
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-s", "--startAddr", dest="start_addr" , type=int,
                  help="start address")

parser.add_option("-e", "--endAddr", dest="end_addr", type=int, 
                  help="end address")

parser.add_option("-i", "--input_file", dest="in_file",
                  help="input_file")

parser.add_option("-o", "--output_file", dest="out_file",
                  help="output_file")

parser.add_option("-m", "--inject_file", dest="inject_file",
                  help="inject_flag ")

(options, args) = parser.parse_args()

def carving(file_in, file_out, start_addr, end_addr):
	print ("[+] carving start ")
	print ("[+] Open file %s" %(file_in))
	f1 = open(file_in,"r") 
	file_data = f1.read()
	f1.close()
	print("[+] Carving: start address: [0x%x], end address: [0x%x] "%(start_addr, end_addr ))
	file_data= file_data[start_addr: end_addr]
	print("[+] Save file: %s " %(file_out))
	with open(file_out,"w") as f:
		f.write(file_data)

def inject(file_in, file_out, start_addr, end_addr):
	print ("[+] injection start ")
	print ("[+] Open file %s" %(file_in))
	f1 = open(file_in,"r") 
	file_data = f1.read()
	f1.close()
	print("[+] Injection: start address: [0x%x], end address: [0x%x] "%(start_addr, end_addr ))
	size_1 = end_addr - start_addr
	print("[+] inject size : [%d] " %(size_1))
	head_data = file_data[0:start_addr]
	tail_data = file_data[start_addr+size_1::]
	print ("[+] inject file open and ljust with zero")
	f2 = open(options.inject_file,"r") 
	inject_data = f2.read()
	inject_data = inject_data.ljust(size_1,'\xff')
	f2.close()
	print("[+] inject file size : [%d] " % len(inject_data))
	print("[+] Success inject to [%s] file. " %(file_out) )
	f3 = open(file_out,"w") 
	data = head_data + inject_data + tail_data
	f3.write(data)
	f3.close()


def main():
	if not options or not options.in_file or not options.out_file: 
		parser.print_help()
		exit(0)
	
	if( options.inject_file ):
		inject(options.in_file, options.out_file, options.start_addr, options.end_addr )

	else:
		carving(options.in_file, options.out_file, options.start_addr, options.end_addr )




if __name__ == "__main__":
	main()

