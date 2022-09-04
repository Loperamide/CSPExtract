import sys
import sqlite3
import os
from os.path import isfile, join

def control_args():
    if (len(sys.argv) < 2):
        print("Error : need arguments")
    if (len(sys.argv) > 2):
        print("Error : too much arguments")
    if (len(sys.argv) < 2 or len(sys.argv) > 2):
        print("extract.py Directory_name")

def get_last_pos(str, source):
    str_find = bytearray(str,'ascii')
    last_pos = 0
    pos = 0
    while True:
        pos = source.find(str_find, last_pos)
        if pos == -1:
            break
        last_pos = pos + 1
    return (last_pos -1)

def extract_png_from_layer(working_file):
    try:
        with open(working_file, "rb") as inputFile:
            content = inputFile.read()
            if content != "":
                s = 'PNG'
                begin_pos = get_last_pos(s, content)
                begin_pos -= 1

                s = 'IEND'                
                end_pos = get_last_pos(s, content)
                end_pos += 4

                with open(working_file+".png", 'wb') as outputFile:
                    outputFile.write(content[begin_pos:end_pos])
    except FileNotFoundError:
        print("File not found")

def extract_sqlite_layers(working_file):
    con = sqlite3.connect(working_file)
    cur = con.cursor()
    cur.execute("select _PW_ID, FileData from MaterialFile")
    row = cur.fetchone()
    while row != None:
        #extract images
        file_name = working_file+"."+str(row[0])+".layer"
        with open(file_name, 'wb') as outputFile:
            outputFile.write(row[1])
            extract_png_from_layer(file_name)
        os.remove(file_name)
        row = cur.fetchone()
    cur.close()

def main():
    # Control args
    control_args()

    if isfile(sys.argv[1]):
        print("A file provided as an argument, extracting textures from the file...")
        filedir=''
        files = [sys.argv[1]]
    else:
        filedir = sys.argv[1]
        files = [join(filedir,x) for x in os.listdir(filedir)]
        files = [x for x in files if isfile(x)]

    for m_file in files:
        print(m_file)
        extract_sqlite_layers(m_file)

if __name__ == "__main__":
   main()
