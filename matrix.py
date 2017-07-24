import cgi
import copy
import sys
import getopt
import html.parser
import re
import os
import io
import time



_input_dir = None
_stat = None 
_char_dict = []


def PrintUsage():
  print('PrintUsage')

def ParseArgs(args):
  try:
    (opts, filenames) = getopt.getopt(args, '', ['help', 
                                                 'input_dir=',
                                                 'stat'
                                                 ]) 
  except getopt.GetoptError:
    PrintUsage('Invalid arguments.')
    
  for (opt, val) in opts:
    if opt == '--help':
      PrintUsage(None)
    elif opt == '--input_dir':
      global _input_dir
      _input_dir = val
    elif opt == '--stat':
      global _stat
      _stat = True


def WalkFiles(input_dir, file_list):
  for parent,dirnames,filenames in os.walk(input_dir):
    #for dirname in  dirnames:                    
      #print("parent is:" + parent)
      #print("dirname is" + dirname)
 
    for filename in filenames:                        
      #print("parent is:" + parent)
      #print("filename is:" + filename)
      #print("the full name of the file is:" + os.path.join(parent,filename))
      file_list.append(os.path.join(parent,filename))

def StatFilesChars(file_list, output_result_file_path):

  result_file_object = None
  char_dict = {}
  start_num = 0
  file_exist = False
  
  if os.path.exists(output_result_file_path):
    CharDictLoadFromFile(output_result_file_path, char_dict)
    result_file_object = open(output_result_file_path, 'a')
    file_exist = True
    start_num = 1000
    print(output_result_file_path + ' exits')
  else:
    start_num = 100
    file_exist = False 
    result_file_object = open(output_result_file_path, 'w')
    print(output_result_file_path + ' does not exits')

  print(start_num)
  
  for i in range(0, 26):
    s = chr(ord('a')+i)
    if not s in char_dict:
      char_dict[s] = start_num
      result_file_object.write(s + '\t' + str(char_dict[s]) + '\n')
      start_num = start_num +1
 

  if not file_exist:
    start_num = 200
  for i in range(0, 26):
    s = chr(ord('A')+i)
    if not s in char_dict:
      char_dict[s] = start_num
      result_file_object.write(s + '\t' + str(char_dict[s]) + '\n')
      start_num = start_num +1

  if not file_exist:
    start_num = 300
  for i in range(0, 10):
    s = str(i)
    if not s in char_dict:
      char_dict[s] = start_num
      result_file_object.write(s + '\t' + str(char_dict[s]) + '\n')
      start_num = start_num +1
 
  #for k,v in char_dict.items():
  #  print(k)
 

  if not file_exist:
    start_num = 500
  for file_path in file_list:
    file_object = open(file_path, 'r')
    try:
      text = file_object.read( )
      l = list(text)
      for s in l:
        if not s in char_dict:
          char_dict[s] = start_num
          if s == '\n':
            s = '\\n'
          if s == '\t':
            s = '\\t'
          result_file_object.write(s + '\t' + str(start_num) + '\n')
          start_num = start_num + 1
    finally:
      file_object.close( )


  result_file_object.close()


def CharDictLoadFromFile(char_dict_file_path, output_char_dict):
  f = open(char_dict_file_path)
  line = ''
  for line in f:
    line = line.strip('\n')
    kandv = line.split('\t')
    s = kandv[0]

    if s == '\\n':
      s = '\n'
    if s == '\\t':
      s = '\t'
    output_char_dict[s] = kandv[1]

def ToMatrix(file_list, char_dict_file_path, result_file_path):
  result_file_object = open(result_file_path, 'w')
  char_dict = {}
  CharDictLoadFromFile('char.txt', char_dict)
  
  for file_path in file_list:
    print(file_path)
    input_file_object = open(file_path, 'r')


    dir_name = "Output_" + os.path.basename(os.path.dirname(file_path))
    file_name = os.path.basename(file_path)
    if not os.path.exists(dir_name):
      os.mkdir(dir_name)
    output_file_object = open(dir_name + "\\" + file_name + "_matrix", 'w')
    output_matrix = []
    max_line_width = 0
    for line in input_file_object:
      output_matrix_row = []
      if len(line) > max_line_width:
        max_line_width = len(line)
      l = list(line)
      for s in l:
        print(s)
        print(char_dict[s])
        output_matrix_row.append(char_dict[s])
      print(output_matrix_row)
      output_matrix.append(output_matrix_row)

    output_text = ''
    for row in output_matrix:
      count = len(row)
      print(count)
      for i in range(0, max_line_width):
        if i < count:
          if i == 0:
            output_text = output_text + row[i]
          else:
            output_text = output_text + ',' + row[i]
        else:
          output_text = output_text + ',' + '-1'
      output_text = output_text + '\n'
     
    output_file_object.write(output_text)
    output_file_object.close()





def Stat():
  global _input_dir
  rootdir = _input_dir
  file_list = []
  WalkFiles(rootdir, file_list)
  StatFilesChars(file_list, 'char.txt')

def Matrix():
  global _input_dir
  rootdir = _input_dir
  file_list = []
  WalkFiles(rootdir, file_list)
  ToMatrix(file_list, 'char.txt', 'matrix.txt')

if (__name__ == '__main__'):
  print ('start')
  ParseArgs(sys.argv[1:])

  global _stat
  if _stat:
    Stat()
  else:
    Matrix()

