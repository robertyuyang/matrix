import cgi
import copy
import sys
import getopt
import re
import os
import io
import time



_input_dir = None
_stat = None
_xmlword = None
_xmlelement = None
_char_dict = []


def PrintUsage():
  print('PrintUsage')

def ParseArgs(args):
  try:
    (opts, filenames) = getopt.getopt(args, '', ['help',
                                                 'input_dir=',
                                                 'stat',
                                                 'xmlword',
                                                 'xmlelement'
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
    elif opt == '--xmlword':
      global _xmlword
      _xmlword = True
    elif opt == '--xmlelement':
      global _xmlelement
      _xmlelement = True


def WalkFiles(input_dir, file_list):
  print(input_dir)
  for parent,dirnames,filenames in os.walk(input_dir):
    for dirname in  dirnames:
      #print("the full name of the dir is:" + os.path.join(parent,dirname))
      WalkFiles(os.path.join(parent, dirname), file_list)
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
    print s
    output_char_dict[s] = kandv[1]

def Extra(count):
  result = ''
  for i in range(0, count):
    result += '-1,'
  return result

def XmlTransfer(file_list, char_dict_file_path, result_file_path):
  char_dict = {}
  CharDictLoadFromFile(char_dict_file_path, char_dict)


  for k, v in char_dict.items():
    char_dict[k] = char_dict[k] + ','

  format_char_dict = {}
  format_char_dict[' '] = char_dict.pop(' ')
  format_char_dict['\n'] = char_dict.pop('\n')
  format_char_dict['\t'] = char_dict.pop('\t')

  speical_char_dict = {}
  speical_char_dict[','] = char_dict.pop(',')

  max_line_width = 0
  max_line_count = 0

  dir_name = "xmlencode_" + os.path.basename(os.path.dirname(file_list[0]))
  matrix_dir_name = "wordmatrix_" + os.path.basename(os.path.dirname(file_list[0]))
  if not os.path.exists(dir_name):
    os.mkdir(dir_name)
  if not os.path.exists(matrix_dir_name):
    os.mkdir(matrix_dir_name)
  encode_file_list = []

  for file_path in file_list:
    if not file_path.endswith('.xml'):
      continue;
    input_file_object = open(file_path, 'r')
    content = input_file_object.read()
    input_file_object.close()

    #remove \n in the end (dont know why there is a \n
    if content.endswith('\n'):
      content = content[0: len(content) - 1]
    content = re.sub(r'<\?xml([^<>]*)?>\n', '', content)#remove xml head





    content = content.replace(',', speical_char_dict[','])

    content = re.sub(r'<name>([^<>]*)</name>', '<name>'+char_dict["Identifier"]+'</name>', content)

    #replace gerenic type
    content = re.sub(r'<type><name>((?!<type>).)*<argument_list((?!<type>).)*</name></type>(\s+)<name>([^d][^<>]*)</name>',
                     lambda m:'<type><name>'+char_dict["Identifier"]+'</name></type>'+m.group(3) +'<name>'+char_dict["Identifier"]+'</name>', content)

    content = re.sub(r'<argument_list>\(\)</argument_list>', '<argument_list>'+char_dict["("] + char_dict[")"] + '</argument_list>', content)
    content = re.sub(r'<parameter_list>\(\)</parameter_list>', '<parameter_list>'+char_dict["("] + char_dict[")"] + '</parameter_list>', content)
    '''
    #replace function name
    content = re.sub(r'<name>([^<>]*)</name><parameter_list>', '<name>'+char_dict["FunctionName"]+'</name><parameter_list>', content)
    #replace type and varible name(varible declaration)
    content = re.sub(r'<type>(<specifier>[^<>]*</specifier>\s+)*<name>([^d][^<>]*)</name></type>(\s+)<name>([^d][^<>]*)</name>',
                     lambda m:'<type>'+ m.group(1) if(m.group(1) is not None) else '' +'<name>'+char_dict["TypeName"]+'</name></type>'+m.group(3) +'<name>'+char_dict["VariableName"]+'</name>', content)

    #replace gerenic type
    content = re.sub(r'<type><name>((?!<type>).)*<argument_list((?!<type>).)*</name></type>(\s+)<name>([^d][^<>]*)</name>',
                     lambda m:'<type><name>'+char_dict["TypeName"]+'</name></type>'+m.group(3) +'<name>'+char_dict["VariableName"]+'</name>', content)

    #replace member function call
    content = re.sub(r'<call><name><name>([^<>]*)</name><operator>.</operator><name>([^<>]*)</name></name>',
                     '<call><name><name>'+char_dict["VariableName"]+'</name><operator>.</operator><name>'+char_dict["FunctionName"]+'</name></name>',
              content);
    #replace member variable
    content = re.sub(r'<expr><name><name>([^<>]*)</name><operator>.</operator><name>([^<>]*)</name></name></expr>',
                     '<expr><name><name>'+char_dict["VariableName"]+'</name><operator>.</operator><name>'+char_dict["VariableName"]+'</name></name></expr>',
                     content);
    # replace global function call (include new xxx())
    content = re.sub(r'<call><name>([^<>]*)</name>', '<call><name>' + char_dict["FunctionName"] + '</name>', content)

    # replace varible in expr (i = 0)
    content = re.sub(r'<expr><name>([^<>]*)</name>', '<expr><name>' + char_dict['VariableName'] + '</name>', content)
    '''


    #replace literal
    content =re.sub(r'<literal type="string">([^<>]*)</literal>', '<literal type="string">'+char_dict["String"]+'</literal>', content)
    content =re.sub(r'<literal type="number">([^<>]*)</literal>', '<literal type="number">'+char_dict["Number"]+'</literal>', content)
    # replace throws type
    content = re.sub(r'<expr><name>([^<>]*)</name></expr>', '<expr><name>' + char_dict["TypeName"] + '</name></expr>',
                     content)

    #replace =
    content = re.sub(r'<init>=', '<init>'+char_dict['='], content)
    #replace comment
    content = re.sub(r'<comment([^<>]*)>([^<>]*)</comment>', lambda m:'<comment'+m.group(1)+'>'+char_dict["Comment"]+'</comment>', content)
    #replace throws
    content = re.sub(r'<throws>throws', '<throws>'+ char_dict['throws'], content)

    for k in ['if', 'else', 'for', 'while', 'throw']:
      content = content.replace(r'<'+k+'>' + k , r'<'+k+'>'+ char_dict[k])
    content = re.sub(r'<block>{', '<block>' + char_dict["{"], content)
    content = re.sub(r'}</block>', char_dict["}"] + '<block>', content)

    for k,v in char_dict.items():
      content = content.replace(r'>' + k +'<', '>' + v +'<')
      '''
      if k == '(' or k == '[' or k == ')':
        k = '\\' + k
      if k == '++':
        k = r'\+\+'
      print k
      content = re.sub(r'>' + k +r'(\s+)<', lambda m:'>' + v + (m.group(1) if (m.group(1) is not None) else '') +'<', content)
      '''
    #replace sapce \n \t
    for k,v in format_char_dict.items():
      content = content.replace(r'>' + k +'<', '>' + v +'<')

    midcontent = content;


    content = re.sub(r'<([^<>]*)>', '', content)

    for k in [' ', '\t']:
      content = content.replace(k, format_char_dict[k])
    content = content.replace('\n', format_char_dict['\n'] + '\n')

    lines = content.split('\n')
    if len(lines) > max_line_count:
      max_line_count = len(lines)
    for line in lines:
      if len(line.split(',')) > max_line_width:
        max_line_width = len(line.split(','))

    file_name = os.path.basename(file_path)
    output_file_path = os.path.join(dir_name , file_name + ".txt")
    output_file_object = open(output_file_path, 'w')
    output_file_object.write(content)
    output_file_object.close()

    encode_file_list.append(output_file_path)

    #output_file_object_mid = open(os.path.join(dir_name , file_name + "_wordmatrix_mid.java"), 'w')
    #output_file_object_mid.write(midcontent)

    print file_path + 'encoded.'

  for file_path in encode_file_list:

    input_file_object = open(file_path)
    content = input_file_object.read()
    input_file_object.close()

    output_content = ''

    lines = content.split('\n')
    for line in lines:
      extra_count = max_line_width - len(line.split(','))
      output_content += line + Extra(extra_count)
      output_content += '\n'

    extra_row_count = max_line_count - len(lines)
    for i in range(0, extra_row_count):
      output_content += Extra(max_line_width) + '\n'

    file_name = os.path.basename(file_path)
    output_file_path = os.path.join(matrix_dir_name , file_name + "_wordmatrix.txt")
    output_file_object = open(output_file_path, 'w')
    output_file_object.write(output_content)
    output_file_object.close()


  print('max line width: %d' % max_line_width)
  print('max line count: %d' % max_line_count)



def ToMatrix(file_list, char_dict_file_path, result_file_path):

  print('ToMaritx %d files' % len(file_list))
  result_file_object = open(result_file_path, 'w')
  char_dict = {}
  CharDictLoadFromFile(char_dict_file_path, char_dict)



  max_line_width = 0
  max_line_count = 0

  '''
  for file_path in file_list:
    input_file_object = open(file_path, 'r')


    lines = input_file_object.readlines()
    if len(lines) > max_line_count:
      max_line_count = len(lines)

    for line in lines:
      if len(line) > max_line_width:
        max_line_width = len(line)
    input_file_object.close()


  print('max line width: %d' % max_line_width)
  print('max line count: %d' % max_line_count)
  '''
  for file_path in file_list:
    print(file_path)
    if not file_path.endswith('.xml'):
      continue;
    input_file_object = open(file_path, 'r')


    dir_name = "Output_" + os.path.basename(os.path.dirname(file_path))
    file_name = os.path.basename(file_path)
    if not os.path.exists(dir_name):
      os.mkdir(dir_name)
    output_file_object = open(dir_name + "\\" + file_name + "_matrix", 'w')

    output_matrix = []
    for line in input_file_object:
      output_matrix_row = []
      l = list(line)
      for s in l:
        output_matrix_row.append(char_dict[s])
      output_matrix.append(output_matrix_row)

    output_text = ''

    row_count = len(output_matrix)
    for row_index in range(0, max_line_count):
      if row_index >= row_count:
        for i in range(0, max_line_width):
          if i == 0:
            output_text = output_text + '-1'
          else:
            output_text = output_text + ',' + '-1'
        output_text = output_text + '\n'
        continue

      row = output_matrix[row_index]
      row_width = len(row)
      for i in range(0, max_line_width):
        if i < row_width:
          if i == 0:
            output_text = output_text + row[i]
          else:
            output_text = output_text + ',' + row[i]
        else:
          output_text = output_text + ',' + '1'
      output_text = output_text + '\n'

    output_file_object.write(output_text)
    output_file_object.close()
    input_file_object.close()





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
  XmlTransfer(file_list, 'word.txt', 'word_matrix.txt')

if (__name__ == '__main__'):
  print ('start')
  ParseArgs(sys.argv[1:])

  #global _stat
  if _stat:
    Stat()
  else:
    Matrix()

    #re.sub(r'<([^<>]*)>', '', content)

