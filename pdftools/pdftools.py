import PyPDF2 as pdf
import re
import os
import sys
import fitz
from io import BytesIO



def check_args(args):
    # Returns
    #           [0] Boolean.    True        : Arguments are right.
	#							False		: Missing or wrong  arguments.
	#
	#			[1] String. 	File name.
    #           [2] integer.    # of copies
    #


    ar_file = ''
    ar_copies = 0
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

def copy(filename,copies_arg):
    filepdf=filename
    currency_regex = "-?\d+[,.]\d+"
    file = open(filepdf,"rb")
    reader = pdf.PdfReader(file)

    try:
        os.mkdir(filepdf+"_dir")
    except:
        print("Directory alreday Exists")
    for page_number in range(0, len(reader.pages)):
        writer = pdf.PdfWriter()
        selected_page = reader.pages[page_number]
        page_text = selected_page.extract_text()
        page_lines = page_text.split('\n')
        currency_found = re.findall(currency_regex,page_text)
        if copies_arg == 0:
            copies = len(currency_found)
        else:
            copies = copies_arg
        if page_number == 2:
            for i in page_lines:
                print(i)

        #if page_number == 2:
        #    print(page_text)
        #    print(currency_found)
        writer.add_page(selected_page)
        for copy in range(copies):
            filename_output = f"{filepdf}_dir\p{page_number+1}-c{copy+1}.pdf"
            out = open(filename_output,"wb")
            
            writer.write(out)
            print("Created a pdf:{}".format(filename_output))

def copy2(filename,copies_arg):
    currency_regex = "-?\d+[,.]\d+"
    reader = fitz.open(filename)
    output_buffer = BytesIO()
    pages = reader.page_count

    try:
        os.mkdir(filename+"_dir")
    except:
        print("Directory alreday Exists")
    for page_number in range(pages):
        #print("{} {}".format(page_number,pages))
        writer = fitz.open(filename)
        copy  = 0
        writer.select(list(range(page_number,page_number+1)))
        selected_page = writer[0]
        page_text = selected_page.get_text()
        page_lines = page_text.split('\n')
        for line in selected_page.get_text("blocks"):
            currency_found = re.findall(currency_regex,line[4])
            if currency_found:
                #print("{} {}".format(line,currency_found))
                x1 = 30
                y1 = line[1]-4
                x2 = line[2]+20
                y2 = line[3]+4
                r1 = fitz.Rect(x1,y1,x2,y2)
                copy = copy +1
                writer = fitz.open(filename)
                writer.select(list(range(page_number,page_number+1)))
                selected_page = writer[0]
                highlight = selected_page.add_highlight_annot(r1)
                highlight.update()
                filename_output = f"{filename}_dir\p{page_number+1}-c{copy} {currency_found[0]}.pdf"
                writer.save(filename_output)
                
                print("Created a pdf:{}".format(filename_output))




def main(argvs):
    chk_arg = check_args(argvs)
    if not chk_arg[0]:
        print_arg()
        exit()

    main_pdf_file = chk_arg[1]
    main_copies =  int(chk_arg[2])

    try:
        copy2(main_pdf_file,main_copies)
    except Exception as e:
        print("Some problems copying files..."+str(e))

if __name__ == "__main__":
    main(sys.argv)

