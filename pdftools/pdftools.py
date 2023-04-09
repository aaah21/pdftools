import PyPDF2 as pdf
import re
import os
import sys


def check_args(args):
    # Returns
    #           [0] Boolean.    True        : Arguments are right.
	#							False		: Missing or wrong  arguments.
	#
	#			[1] String. 	File name.
    #           [2] integer.    # of copies

    ar_file = ''
    arg_sw = False
    for i in range(0, len(args)):
        y = args[i].lower()
        if '-f:' in y:
            ar_file = (y[y.find("-f:") + 3:])
        if '-n:' in y:
            ar_copies = (y[y.find("-n:") + 3:])

    if len(ar_file) == 0 :
        arg_sw = False
    else:
        arg_sw = True

    return [arg_sw, ar_file, ar_copies]


def print_arg():

    print()
    print('Saves 20 copies for page on the pdf file amex.pdf')
    print()
    print("pdftool -f:'amex.pdf -n:20'")
    print()
    print('-f:pdf-file-name')
    print('-n:#-of-copies')
    print()

def copy(filename,copies):
    filepdf=filename
    file = open(filepdf,"rb")
    reader = pdf.PdfReader(file)
    page = reader.pages[0]
    try:
        os.mkdir(filepdf+"_dir")
    except:
        print("Directory alreday Exists")
    for page_number in range(0, len(reader.pages)):
        writer = pdf.PdfWriter()
        selected_page = reader.pages[page_number]
        #find_currency = re.findall('\$\d[.,]+\d+',selected_page.extract_text())
        #find_currency = re.findall('?\$\d[.,]+\d+',selected_page.extract_text())
        #print("Page {} found {}".format(page_number+1,find_currency))
        #if (page_number == 2):
        #    print(selected_page.extract_text())

        writer.add_page(selected_page)
        for copy in range(copies):
            filename_output = f"{filepdf}_dir\{filepdf}-page-{page_number+1}-copy-{copy}.pdf"
            out = open(filename_output,"wb")
            writer.write(out)
            print("Created  a pdf:{}".format(filename_output))

def main(argvs):
    chk_arg = check_args(argvs)
    if not chk_arg[0]:
        print_arg()
        exit()

    main_pdf_file = chk_arg[1]
    main_copies =  chk_arg[2]
    #try:
    #    copy(main_pdf_file,20)
    #except:
    #    print("Some problems copying files...")


    copy(main_pdf_file,20)
    print("Some problems copying files...")









if __name__ == "__main__":
    main(sys.argv)




