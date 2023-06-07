import PyPDF2
import os
from os import listdir
from os.path import isfile, join
import time

watchdir = "."
outputdir = "../consume/"
pollingTime = 10

ocrlanguages = "deu"


def doStuff(files: list):
    print(files)
    for file in files:
        print("Starting OCR on " + file)
        os.system("ocrmypdf -l " + ocrlanguages + " --deskew --rotate-pages --skip-text " + file + " 'ocr_" + file + "'")
        reader = PyPDF2.PdfReader("ocr_" + file)
        current = 1
        start = 1
        end = 1
        letters = []

        for page in reader.pages:
            text = page.extract_text()
            if text == "":
                end = current - 1
                letters.append([start, end])
                start = current + 1
            current = current + 1

        if(end != current):
            letters.append([start, current - 1])

        anzahl = 1
        for brief in letters:
            print("Creating letter nr. " + str(anzahl))
            pdf = PyPDF2.PdfWriter()
            for page in range(brief[0] - 1, brief[1]):
                pdf.add_page(reader.pages[page])
            output = outputdir + file.split(".")[0] + "_" + str(anzahl) + ".pdf"
            with open(output, "wb") as output_pdf:
                pdf.write(output_pdf)
            anzahl = anzahl + 1
        os.remove("./ocr_" + file)


#doStuff(["input.pdf", "inputcopy.pdf"])

def fileInDirectory(my_dir: str):
    onlyfiles = [f for f in listdir(my_dir) if isfile(join(my_dir, f))]
    return onlyfiles

def listComparison(OriginalList: list, NewList: list):
    differencesList = [x for x in NewList if x not in OriginalList]
    return differencesList


def fileWatcher(my_dir: str, pollTime: int):
    while True:
        if 'watching' not in locals():
            previousFileList = fileInDirectory(my_dir)
            watching = 1
            print("First Time")
            print(previousFileList)
        
        time.sleep(pollTime)
        print("checking for files")
        newFileList = fileInDirectory(my_dir)

        fileDiff = listComparison(previousFileList, newFileList)

        previousFileList = newFileList
        if len(fileDiff) == 0: continue
        doStuff(fileDiff)

fileWatcher(watchdir, pollingTime)
