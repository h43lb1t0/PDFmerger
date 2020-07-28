from PyPDF2 import PdfFileReader, PdfFileWriter
import tkinter as tk
from tkinter import filedialog
from tkinter import font
import time
import os

root_main = tk.Tk()
root_merge = None
root_encrypt = None
root_both = None

mergecollor = 'yellow'
encryptcollor = 'green'
bothcollor = 'light green'

script_dir = os.path.dirname(__file__)

rel_merge = 'img/merge.png'
abs_merge = os.path.join(script_dir, rel_merge)

rel_encrypt = 'img/encrypt.png'
abs_encrypt = os.path.join(script_dir, rel_encrypt)

rel_both = 'img/both.png'
abs_both = os.path.join(script_dir, rel_both)

img_merge = tk.PhotoImage(file = abs_merge)
img_encrypt = tk.PhotoImage(file = abs_encrypt)
img_both = tk.PhotoImage(file = abs_both)

def mainGUI():
    x = 166
    y = 250
    root_main.title('PDFer')
    root_main.geometry("500x250")
    root_main.resizable(False, False)
    description = tk.Label(root_main, text='Choose an Option')
    description.config(font=("Arial", 15))
    description.pack()
    creator = tk.Label(root_main, text='by h43lb1t0')
    creator.config(font=("Arial", 10))
    creator.pack(side=tk.BOTTOM)
    buttton_merge = tk.Button(root_main, command=lambda: mergeGUI(), height=y, width=x,image = img_merge, bg=mergecollor, activebackground="#DB6200")
    buttton_merge.pack(side=tk.LEFT)
    button_encrypt = tk.Button(root_main, command=lambda: encryptGUI(), height=y, width=x,image = img_encrypt, bg=encryptcollor, activebackground="#DB6200")
    button_encrypt.pack(side=tk.LEFT)
    button_both = tk.Button(root_main, command=lambda: bothGUI(), height=y, width=x,image = img_both, bg=bothcollor, activebackground="#DB6200")
    button_both.pack(side=tk.LEFT)
    root_main.mainloop()

def mergeGUI():
    global root_merge
    global infotext
    root_merge = tk.Toplevel()
    #root_merge.title('Merge PDFs')
    root_merge.geometry("250x250")
    root_merge.configure(bg=mergecollor)
    root_merge.resizable(False, False)
    infotext = tk.Label(root_merge, text='Name the Outputfile*', bg=mergecollor)
    infotext.config(font=('Arial', 11))
    infotext.pack()
    outputfilename = tk.Entry(root_merge, bd=3)
    outputfilename.pack(side=tk.TOP)
    merge = tk.Button(root_merge, command=lambda : mergePDF(outputfilename.get() + '.pdf', both=False), height=180, width=166, bg=mergecollor, activebackground="#3d9dc2", image = img_merge)
    merge.pack(side=tk.BOTTOM)
    root_merge.mainloop()


def encryptGUI():
    global root_encrypt
    global infotext
    root_encrypt = tk.Toplevel()
    root_encrypt.geometry('250x265')
    root_encrypt.configure(bg=encryptcollor)
    root_encrypt.resizable(False, False)
    root_encrypt.title=('Encypt PDFs')
    infotext = tk.Label(root_encrypt, text='Enter a password*', bg=encryptcollor)
    infotext.config(font=('Arial', 11))
    infotext.pack(side=tk.TOP)
    password = tk.Entry(root_encrypt, bd=3)
    password.pack(side=tk.TOP)
    infotext2 = tk.Label(root_encrypt, text='Name the outputfile', bg=encryptcollor)
    infotext2.config(font=('Arial', 11))
    infotext2.pack(side=tk.TOP)
    namefile = tk.Entry(root_encrypt, bd=3)
    namefile.pack(side=tk.TOP)
    encrypt = tk.Button(root_encrypt, command=lambda : encryptPDF(password.get(), namefile.get()), height=180, width=166, bg=encryptcollor, activebackground="#3d9dc2", image = img_encrypt)
    encrypt.pack(side=tk.BOTTOM)
    root_encrypt.mainloop()

def bothGUI():
    global root_both
    global infotext
    root_both = tk.Toplevel()
    root_both.geometry('250x260')
    root_both.configure(bg=bothcollor)
    root_both.resizable(False,False)
    root_both.title('Merge & encrypt')
    infotext = tk.Label(root_both, text='Enter a password', bg=bothcollor)
    infotext.config(font=('Arial', 11))
    infotext.pack(side=tk.TOP)
    password = tk.Entry(root_both, bd=3)
    password.pack(side=tk.TOP)
    infotext2 = tk.Label(root_both, text='Name the outputfile', bg=bothcollor)
    infotext2.config(font=('Arial', 11))
    infotext2.pack(side=tk.TOP)
    namefile = tk.Entry(root_both, bd=3)
    namefile.pack(side=tk.TOP)
    doboth = tk.Button(root_both, command=lambda : mergeGUI(), height=180, width=166, bg=bothcollor, activebackground="#3d9dc2", image = img_both)
    doboth.pack(side=tk.TOP)
    root_both.mainloop()

def mergePDF(outputfilename, both):
    if outputfilename == ".pdf":
        change_pwHint('No Name entered', 'red')
        return
    pdf_writer = PdfFileWriter()
    files = filedialog.askopenfilenames(parent=root_merge, title='Choose PDF-files', filetypes=[('PDF Files', '*.pdf')])

    savedic = filedialog.askdirectory(parent=root_merge, title='Select the Save Directory')

    for file in root_merge.tk.splitlist(files):
        pdf_reader = PdfFileReader(file)
        for page in range(pdf_reader.getNumPages()):
            pdf_writer.addPage(pdf_reader.getPage(page))
        
    with open(savedic + '/' + outputfilename, 'wb') as out:
        if pdf_reader.getNumPages() != 0:
            if both == False:
                change_pwHint('Sucsess', 'blue')
                pdf_writer.write(out)
            else:
                doBoth(out)
        else:
            change_pwHint('failed', 'red')
    time.sleep(5)
    root_merge.destroy()

def encryptPDF(password, namefile):
    if password == "":
        change_pwHint('You need to Enter a Password', 'red')
        return
    else:
        filename = filedialog.askopenfilename(parent=root_encrypt, title='Choose PDF-file', filetypes=[('PDF Files', '*.pdf')])
        red_filename = filename
        savedic = filedialog.askdirectory(parent=root_encrypt, title='Select the Save Directory')

        pdf_reader = PdfFileReader(red_filename)
        pdf_writer = PdfFileWriter()

        for page in range(pdf_reader.getNumPages()):
            pdf_writer.addPage(pdf_reader.getPage(page))

        pdf_writer.encrypt(user_pwd=password, use_128bit=True)

        if namefile != '':
            openName = savedic + '/' + namefile + '.pdf'
        else:
            while filename.find('/') > 0:
                print('Filename: ' + filename)
                head, sep, filename = filename.partition('/')
                print('Filename after partition: ' + filename)
            else:
                outputfilename = filename[:-4] + '.encrypted.pdf'
                openName = savedic + '/' + outputfilename

        print(openName)

        with open(openName, 'wb') as out:
            print('OPENED')
            if pdf_reader.getNumPages() != 0:
                print('> 0')
                change_pwHint('Succses', 'blue')
                pdf_writer.write(out)
                print('Done')
            else:
                change_pwHint('failed', 'red')
        time.sleep(5)
        root_encrypt.destroy()

def doBoth(out):
    pass


def change_pwHint(output_text, color):
    infotext['text'] = output_text
    infotext['fg'] = color
    infotext.pack(side=tk.TOP)


mainGUI()