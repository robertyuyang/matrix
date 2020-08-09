# -*- coding: utf-8 -*-
import sys
import getopt
import re
import os
import errno


_input_dir = None
_stat = None
_javachar = None
_xmlword = None
_xmlelement = None
_xmlwordascii = None
_xmlword1line = None
_validate = None
_char_dict = []

_invalidreg = re.compile(r'[^\,\-\d\n]')
_invalidwordreg = re.compile(r'[^\,\-\d\n]+')

def printf(fmt, *args):
  print(fmt % args)

def PrintUsage():
  print('PrintUsage')

def ParseArgs(args):
  try:
    (opts, filenames) = getopt.getopt(args, '', ['help',
                                                 'input_dir=',
                                                 'stat',
                                                 'javachar',
                                                 'xmlword',
                                                 'xmlwordascii',
                                                 'xmlword1line',
                                                 'xmlelement',
                                                 'validate'
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
    elif opt == '--xmlword1line':
      global _xmlword1line
      _xmlword1line = True
    elif opt == '--javachar':
      global _javachar
      _javachar = True
    elif opt == '--xmlwordascii':
      global _xmlwordascii
      _xmlwordascii = True
    elif opt == '--xmlelement':
      global _xmlelement
      _xmlelement = True
    elif opt == '--validate':
      global  _validate
      _validate = True


def WalkFiles(input_dir, file_list):
  print(input_dir)
  for parent,dirnames,filenames in os.walk(input_dir):
    #for dirname in  dirnames:
      #print("the full name of the dir is:" + os.path.join(parent,dirname))

      #WalkFiles(os.path.join(parent, dirname), file_list)
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
    #print s
    output_char_dict[s] = kandv[1]

def Extra(count):
  result = ''
  for i in range(0, count):
    result += '-1,'
  return result

def Ascii(content):
  result = ''
  for c in content:
    if c == '\n':
      result += '\n'
    else:
      result += str(ord(c)) + ','
  return result

def ItemCount(line):
  ar = line.split(',')
  count = len(ar)
  if ar[count - 1] == '':
    count = count - 1
  return count

def XmlAscii(content):
  content = re.sub(r'<([^<>]*)>', '', content)
  content = re.sub(r'&lt;', '<', content)
  content = re.sub(r'&gt;', '>', content)
  result = ''
  for c in content:
    result += str(ord(c)) + ','
  return result

def XmlWordOnelineTransfer(file_list, char_dict_file_path):
  char_dict = {}
  CharDictLoadFromFile(char_dict_file_path, char_dict)

  for k, v in char_dict.items():
    char_dict[k] = '{${'+ v + '}$}'

  format_char_dict = {}
  format_char_dict[' '] = char_dict.pop(' ')
  format_char_dict['\n'] = char_dict.pop('\n')
  format_char_dict['\t'] = char_dict.pop('\t')


  max_words_count = 0
  '''
  dir_name = "xmlencode_" + os.path.basename(os.path.dirname(file_list[0]))
  matrix_dir_name_prefix = "output_xmlword" + ("ascii_" if to_ascii else "_")
  matrix_dir_name = matrix_dir_name_prefix + os.path.basename(os.path.dirname(file_list[0]))
  if not os.path.exists(dir_name):
    os.mkdir(dir_name)
  if not os.path.exists(matrix_dir_name):
    os.mkdir(matrix_dir_name)
  '''
  encode_file_list = []

  for file_path in file_list:
    if not file_path.endswith('.xml'):
      print '%s not a xml' % file_path
      continue;
    input_file_object = open(file_path, 'r')
    content = input_file_object.read()
    input_file_object.close()

    #remove \n in the end (dont know why there is a \n
    if content.endswith('\n'):
      content = content[0: len(content) - 1]
    content = re.sub(r'<\?xml([^<>]*)?>\n', '', content)#remove xml head
    content = content.replace('\n</unit>','')#remove unit tail
    content = re.sub(r'<unit([^<>]*)>','', content)#remove unit tail

    #replace package
    packagelines = re.findall(r'<package>package .*</package>', content)
    if(len(packagelines) == 1):
      packageline = packagelines[0]
      newpackageline = re.sub(r'<name>([^<$>]*)</name>','<name>'+char_dict["TypeName"]+'</name>',packageline)
      newpackageline = re.sub(r'<package>package', '<package>'+char_dict['package'],newpackageline)
      content = content.replace(packageline, newpackageline)
    importlines = re.findall(r'<import>import .+</import>', content)
    if(len(importlines) >= 1):
      for importline in importlines:
        newimportline = re.sub(r'<name>([^<$>]*)</name>','<name>'+char_dict["TypeName"]+'</name>',importline)
        newimportline = re.sub(r'<import>import', '<import>'+char_dict['import'],newimportline)
        content = content.replace(importline, newimportline)

    # replace literal
    content = content.replace(r'<literal type="null">null</literal>',
                              '<literal type="null">' + char_dict["null"] + '</literal>')
    content = content.replace(r'<literal type="boolean">true</literal>',
                              '<literal type="boolean">' + char_dict["true"] + '</literal>')
    content = content.replace(r'<literal type="boolean">false</literal>',
                                '<literal type="boolean">' + char_dict["false"] + '</literal>')
    content = re.sub(r'<literal type="string">([^<>]*)</literal>',
                       '<literal type="string">' + char_dict["String"] + '</literal>', content)
    content = re.sub(r'<literal type="number">([^<$>]*)</literal>',
                     '<literal type="number">' + char_dict["Number"] + '</literal>', content)
    content = re.sub(r'<literal type="char">([^<$>]*)</literal>',
                     lambda m: '<literal type="char">' + char_dict["String"] + '</literal>', content)
    # replace comment
    content = re.sub(r'<comment([^<$>]*)>([^<$>]*)</comment>',
                     lambda m: '<comment' + m.group(1) + '>' + char_dict["Comment"] + '</comment>', content)


    #replace class
    content = re.sub(r'>(\s*)(class)(\s*)<name>([^<$>]+)</name>',
                     lambda  m:'>'+ m.group(1) + char_dict['class']+ m.group(3) + '<name>'+char_dict["TypeName"]+'</name>', content)
    content = content.replace('<implements>implements', '<implements>'+char_dict['implements'])
    content = re.sub('<super><name>([^<$>]+)</name></super>', '<super><name>'+char_dict['TypeName']+'<super><name>',content)


    #transfer list varible
    content = re.sub(r'<name><name>([^<$>]*)</name><index>\[(.+)\]</index></name>',
                     lambda m:'<name>'+char_dict['VariableName']+'</name><index>['+m.group(2)+']</index></name>', content)
    #transfer list type to type
    content = re.sub(r'<name><name>([^<$>]*)</name><index>\[\]</index></name>',
                     lambda m:'<name>'+m.group(1)+'</name>', content) #does not replace with typename, cos it'll be used later
    #transfer generic type to type
    content = re.sub(r'<name><name>([^<$>]*)</name><argument_list type="generic">&lt;((?!argument_list).)*&gt;</argument_list></name>',
                     lambda m:'<name>'+m.group(1)+'</name>', content) #does not replace with typename, cos it'll be used later


    #replace function name
    #re.sub(r'<name>([^<$>]*)</name><parameter_list>', lambda m:printf('func:'+m.group(1)), content)
    content = re.sub(r'<name>([^<$>]*)</name></type>(\s+)<name>([^<$>]*)</name><parameter_list>',
                     lambda m: '<name>'+(char_dict['TypeName'] if m.group(1) not in char_dict else char_dict[m.group(1)])+'</name></type>' +m.group(2)+ '<name>'+char_dict["FunctionName"]+'</name><parameter_list>', content)
    #content = re.sub(r'<name>([^<$>]*)</name><parameter_list>', lambda m: '<name>'+char_dict["FunctionName"]+'</name><parameter_list>', content)

    #replace type and varible name(varible declaration)
    content = re.sub(r'<name>([^\d][^<$>]*)</name></type>(\s+)<name>([^\d][^<$>]*)</name>',
                     lambda m:'<name>'+char_dict["TypeName"]+'</name></type>'+m.group(2) +'<name>'+char_dict["VariableName"]+'</name>', content)
    content = re.sub('<type><name>([^ ]*)</name></type>(\s+)<name>([^<$>]*)</name>',
           lambda m: '<type><name>' + re.sub('<name>([^<$>]*)</name>', '<name>' + char_dict['TypeName'] + '</name>',
                                             m.group(1)) + '</name></type>' + m.group(2) + '<name>' + char_dict['VariableName'] + '</name>', content)

    '''
    # replace gerenic type
    content = re.sub(
      r'<type><name>((?!<type>).)*<argument_list((?!<type>).)*</name></type>(\s+)<name>([^d][^<$>]*)</name>',
      lambda m: '<type><name>' + char_dict["TypeName"] + '</name></type>' + m.group(3) + '<name>' + char_dict[
        "VariableName"] + '</name>', content)

    # replace gerenic type
    content = re.sub(
    r'<call><name><name>([^<$>]*)</name><argument_list type="generic">&lt;<argument><name>([^<$>]*)</name></argument>&gt;</argument_list></name>',
      lambda m: '<call><name><name>'+char_dict["TypeName"]+'</name><argument_list type="generic">&lt;<argument><name>'+char_dict["TypeName"]+'</name></argument>&gt;</argument_list></name>', content)
    '''
    # replace member function call
    content = re.sub(r'<call><name><name>([^<$>]*)</name><operator>.</operator><name>([^<$>]*)</name></name>',
                     '<call><name><name>' + char_dict["VariableName"] + '</name><operator>.</operator><name>' +
                     char_dict["FunctionName"] + '</name></name>',
                     content);
    # replace member variable
    content = re.sub(r'<name><name>([^<$>]*)</name><operator>.</operator><name>([^<$>]*)</name></name>',
                     '<name><name>' + char_dict["VariableName"] + '</name><operator>.</operator><name>' +
                     char_dict["VariableName"] + '</name></name>',
                     content);
    # replace global function call (include new xxx())
    content = re.sub(r'<call><name>([^<$>]*)</name>', '<call><name>' + char_dict["FunctionName"] + '</name>', content)

    # replace varible in expr (i = 0)
    content = re.sub(r'<expr><name>([^<$>]*)</name>', '<expr><name>' + char_dict['VariableName'] + '</name>', content)
    content = re.sub(r'<name>([^<$>]*)</name></expr>', '<name>' + char_dict['VariableName'] + '</name></expr>', content)
    content = re.sub(r'<operator>\(</operator><name>([^<$>]*)</name><operator>\)</operator>', '<operator>(</operator><name>'+char_dict['TypeName'] +'</name><operator>)</operator>', content)
    # replace varible in  < x
    content = re.sub(r'</operator>(\s+)<name>([^<$>]*)</name>', '</operator><name>' + char_dict['VariableName'] + '</name>', content)
    # replace throws type
    #content = re.sub(r'<expr><name>([^<$>]*)</name></expr>', '<expr><name>' + char_dict["TypeName"] + '</name></expr>',                 content)

    content = content.replace('<name>void</name>', '<name>' + char_dict['void'] + '</name>')
    content = content.replace('<index>[', '<index>' + char_dict['['])
    content = content.replace(']</index>', char_dict[']'] + '</index>')

    for(k,v) in char_dict.items():
      content = content.replace('<specifier>'+k+'</specifier>', '<specifier>'+v+'</specifier>')
      content = content.replace('<operator>'+k+'</operator>', '<operator>'+v+'</operator>')
    #replace ()
    content = re.sub(r'<argument_list>\(',
                     '<argument_list>' + char_dict["("], content)
    content = re.sub(r'<parameter_list>\(',
                     '<parameter_list>' + char_dict["("], content)
    content = re.sub(r'\)</argument_list>',
                     char_dict[")"] + '</argument_list>', content)
    content = re.sub(r'\)</parameter_list>',
                     char_dict[")"] + '</parameter_list>', content)
    #replace =
    content = re.sub(r'<init>=', '<init>'+char_dict['='], content)
    #replace throws
    content = re.sub(r'<throws>throws', '<throws>'+ char_dict['throws'], content)

    for k in ['if', 'else', 'for', 'while', 'throw']:
      content = content.replace(r'<'+k+'>' + k , r'<'+k+'>'+ char_dict[k])
    for k in ['switch', 'case', 'default', 'continue', 'break']:
      content = content.replace('<' + k + '>' + k, '<' + k + '>'+ char_dict[k])
    for k in ['try', 'catch', 'finally', 'return']:
      content = re.sub('>' + k + r'(\s*)<', lambda m:'>' + char_dict[k] + m.group(1) + '<', content)
    content = re.sub(r'<block>{', '<block>' + char_dict["{"], content)
    content = re.sub(r'}</block>', char_dict["}"] + '<block>', content)
    content = re.sub(r'<import>import', '<import>'+char_dict['import'], content)
    content = re.sub(r'<condition>\(', '<condition>'+char_dict['('], content)
    content = re.sub(r'\)</condition>', char_dict[')']+ '</condition>', content)
    content = re.sub(r'<elseif>else', '<elseif>'+char_dict['else'], content)
    content = re.sub(r'<annotation>@((?!<annotation>).)*</annotation>', char_dict['Annotation'], content, flags=re.M|re.S)
    #顺序很重要，先替换泛型类型，避免泛型类型中的原始类型先被替换，再替换所有非空格\t的关键字，这样会先过滤掉所有自定义类型，,再转所有name里的(包括自定义类型），最后把空格\t转掉

    '''
    if not to_ascii:
      # replace gerenic type
      content = re.sub(
        r'<type><name>((?!<type>).)*<argument_list((?!<type>).)*</name></type>(\s+)<name>([^d][^<$>]*)</name>',
        lambda m: '<type><name>' + char_dict["Identifier"] + '</name></type>' + m.group(3) + '<name>' + char_dict[
          "Identifier"] + '</name>', content)

      for k,v in char_dict.items():
        content = content.replace(r'>' + k +'<', '>' + v +'<')

      # replace idenfifer
      content = re.sub(r'<name>([^<$>,]*)</name>', '<name>' + char_dict["Identifier"] + '</name>', content)


      #gerenic_type_reg = re.compile(r'<type><name>((?!<type>).*<argument_list(?!<type>).*)</name></type>(\s+)<name>([^d][^<$>]*)</name>')
      #if gerenic_type_reg.search(content):

      #  content = gerenic_type_reg.sub(
      #   lambda m: '<type><name>' + XmlAscii(m.group(1)) + '</name></type>' + m.group(2) + '<name>' + Ascii(m.group(3)) + '</name>', content)

      for k,v in char_dict.items():
        content = content.replace(r'>' + k +'<', '>' + v +'<')

      #replace idenfifer
      content = re.sub(r'<name>([^<$>,]*)</name>', lambda m:'<name>'+Ascii(m.group(1))+'</name>', content)

    '''




    #replace sapce \n \t
    #for k,v in format_char_dict.items():
    #  if k != '\n':
    #    content = content.replace(r'>' + k +'<', '>' + v +'<')

    content = re.sub(r'<([^<$>]*)>', '', content)
    content = content.replace(' ', format_char_dict[' '])
    content = content.replace('\n', format_char_dict['\n'])
    content = content.replace('\t', format_char_dict['\t'])
    content = content.replace('(', char_dict['('])
    content = content.replace(')', char_dict[')'])
    content = content.replace(';', char_dict[';'])
    content = content.replace(':', char_dict[':'])
    content = content.replace(',', char_dict[','])


    #sorted_char_keys = sorted(char_dict, key=lambda d: len(d), reverse=True)
    #for k in sorted_char_keys:
    #  content = content.replace(k, char_dict[k])
    #for k in [' ', '\t', '\n']:
    #  content = content.replace(k, format_char_dict[k])





    content = content.replace('}$}',',')
    content = content.replace('{${','')

    global _invalidwordreg
    invalidwords = _invalidwordreg.findall(content)
    if len(invalidwords) > 0:
      print '>>>>>>>>>>>> some invalid words: ' + str(invalidwords) + 'in file ' + file_path
    #content = _invalidwordreg.sub(char_dict['Unknown'], content)


    #replace END!!!



    wordscnt = ItemCount(content)
    if wordscnt > max_words_count:
      print '%s max word count %d' % (file_path, wordscnt)
      max_words_count = wordscnt


    output_file_path = ReplaceRootDir(file_path, 'output_word1line_encoded' )
    output_file_object = open(output_file_path, 'w')
    output_file_object.write(content)
    output_file_object.close()

    encode_file_list.append(output_file_path)

    #output_file_object_mid = open(os.path.join(dir_name , file_name + "_wordmatrix_mid.java"), 'w')
    #output_file_object_mid.write(midcontent)

    #print output_file_path + '   encoded.'

  print('max words count: %d' % max_words_count)

  print(len(encode_file_list))
  i = 0
  for file_path in encode_file_list:
    i = i +1
    print(i)
    print(file_path)
    input_file_object = open(file_path)
    content = input_file_object.read()
    input_file_object.close()

    output_content = ''

    if content.find('120,') != -1:
      print 'find 120:========='+file_path
    extra_count = max_words_count - ItemCount(content)
    output_content = content + Extra(extra_count)

    output_file_path = ReplaceRootDir(file_path, 'WordOneLine')
    output_file_path = ReplaceExt(output_file_path, 'matrix')
    output_file_object = open(output_file_path, 'w')
    #output_file_object = open(output_file_path, 'w')
    output_file_object.write(output_content)
    output_file_object.close()
    print output_file_path +' written.'
    Validate([output_file_path])


  print('max words count: %d' % max_words_count)


def XmlTransfer(file_list, char_dict_file_path, to_ascii, oneline=False):
  char_dict = {}
  CharDictLoadFromFile(char_dict_file_path, char_dict)


  for k, v in char_dict.items():
    char_dict[k] = char_dict[k] + '$$$'

  format_char_dict = {}
  format_char_dict[' '] = char_dict.pop(' ')
  format_char_dict['\n'] = char_dict.pop('\n')
  format_char_dict['\t'] = char_dict.pop('\t')

  speical_char_dict = {}
  speical_char_dict[','] = char_dict.pop(',')

  max_line_width = 0
  max_line_count = 0
  max_words_count = 0
  '''
  dir_name = "xmlencode_" + os.path.basename(os.path.dirname(file_list[0]))
  matrix_dir_name_prefix = "output_xmlword" + ("ascii_" if to_ascii else "_")
  matrix_dir_name = matrix_dir_name_prefix + os.path.basename(os.path.dirname(file_list[0]))
  if not os.path.exists(dir_name):
    os.mkdir(dir_name)
  if not os.path.exists(matrix_dir_name):
    os.mkdir(matrix_dir_name)
  '''
  encode_file_list = []

  for file_path in file_list:
    if not file_path.endswith('.xml'):
      print '%s not a xml' % file_path
      continue;
    input_file_object = open(file_path, 'r')
    content = input_file_object.read()
    input_file_object.close()

    #remove \n in the end (dont know why there is a \n
    if content.endswith('\n'):
      content = content[0: len(content) - 1]
    content = re.sub(r'<\?xml([^<>]*)?>\n', '', content)#remove xml head
    content = content.replace('\n</unit>','')#remove unit tail
    content = re.sub(r'<unit([^<>]*)>','', content)#remove unit tail


    if not to_ascii:
      # replace literal
      content = re.sub(r'<literal type="string">([^<>]*)</literal>',
                       '<literal type="string">' + char_dict["String"] + '</literal>', content)
      content = re.sub(r'<literal type="number">([^<>]*)</literal>',
                       '<literal type="number">' + char_dict["Number"] + '</literal>', content)
      content = re.sub(r'<literal type="char">([^<>]*)</literal>',
                       lambda m: '<literal type="char">' + char_dict["String"] + '</literal>', content)
      # replace comment
      content = re.sub(r'<comment([^<>]*)>([^<>]*)</comment>',
                       lambda m: '<comment' + m.group(1) + '>' + char_dict["Comment"] + '</comment>', content)
    else :
      # replace gerenic type
      gerenic_type_reg = re.compile(
        r'<type><name>((?!<type>).*<argument_list(?!<type>).*)</name></type>(\s+)<name>([^d][^<>]*)</name>')
      if gerenic_type_reg.search(content):
        content = gerenic_type_reg.sub(
          lambda m: '<type><name>' + XmlAscii(m.group(1)) + '</name></type>' + m.group(2) + '<name>' + Ascii(
            m.group(3)) + '</name>', content)

        # replace literal
      content = re.sub(r'<literal type="string">([^<>]*)</literal>',
                         lambda m: '<literal type="string">' + Ascii(m.group(1)) + '</literal>', content)
      content = re.sub(r'<literal type="number">([^<>]*)</literal>',
                         lambda m: '<literal type="number">' + Ascii(m.group(1)) + '</literal>', content)
      content = re.sub(r'<literal type="char">([^<>]*)</literal>',
                         lambda m: '<literal type="char">' + Ascii(m.group(1)) + '</literal>', content)
      # replace comment
      # replace comment
      content = re.sub(r'<comment([^<>]*)>([^<>]*)</comment>',
                         lambda m: '<comment' + m.group(1) + '>' + Ascii(m.group(2)) + '</comment>', content)

    content = content.replace(',', speical_char_dict[','])


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
    # replace throws type
    content = re.sub(r'<expr><name>([^<>]*)</name></expr>', '<expr><name>' + char_dict["TypeName"] + '</name></expr>',
                     content)

    '''

    #replace ()
    content = re.sub(r'<argument_list>\(\)</argument_list>',
                     '<argument_list>' + char_dict["("] + char_dict[")"] + '</argument_list>', content)
    content = re.sub(r'<parameter_list>\(\)</parameter_list>',
                     '<parameter_list>' + char_dict["("] + char_dict[")"] + '</parameter_list>', content)
    #replace =
    content = re.sub(r'<init>=', '<init>'+char_dict['='], content)
    #replace throws
    content = re.sub(r'<throws>throws', '<throws>'+ char_dict['throws'], content)

    for k in ['if', 'else', 'for', 'while', 'throw']:
      content = content.replace(r'<'+k+'>' + k , r'<'+k+'>'+ char_dict[k])
    for k in ['try', 'catch', 'finally', 'return']:
      content = re.sub('>' + k + r'(\s+)<', lambda m:'>' + char_dict[k] + m.group(1) + '<', content)
    content = re.sub(r'<block>{', '<block>' + char_dict["{"], content)
    content = re.sub(r'}</block>', char_dict["}"] + '<block>', content)
    content = re.sub(r'<import>import', '<import>'+char_dict['import'], content)
    content = re.sub(r'<condition>\(', '<condition>'+char_dict['('], content)
    content = re.sub(r'\)</condition>', char_dict[')']+ '</condition>', content)
    content = re.sub(r'<elseif>else', '<elseif>'+char_dict['else'], content)
    content = re.sub(r'<annotation>@((?!<annotation>).)*</annotation>', char_dict['Annotation'], content, flags=re.M|re.S)
    #顺序很重要，先替换泛型类型，避免泛型类型中的原始类型先被替换，再替换所有非空格\t的关键字，这样会先过滤掉所有自定义类型，,再转所有name里的(包括自定义类型），最后把空格\t转掉

    if not to_ascii:
      # replace gerenic type
      content = re.sub(
        r'<type><name>((?!<type>).)*<argument_list((?!<type>).)*</name></type>(\s+)<name>([^d][^<>]*)</name>',
        lambda m: '<type><name>' + char_dict["Identifier"] + '</name></type>' + m.group(3) + '<name>' + char_dict[
          "Identifier"] + '</name>', content)

      for k,v in char_dict.items():
        content = content.replace(r'>' + k +'<', '>' + v +'<')

      # replace idenfifer
      content = re.sub(r'<name>([^<>,]*)</name>', '<name>' + char_dict["Identifier"] + '</name>', content)


    else:
      # replace gerenic type
      '''
      gerenic_type_reg = re.compile(r'<type><name>((?!<type>).*<argument_list(?!<type>).*)</name></type>(\s+)<name>([^d][^<>]*)</name>')
      if gerenic_type_reg.search(content):

        content = gerenic_type_reg.sub(
         lambda m: '<type><name>' + XmlAscii(m.group(1)) + '</name></type>' + m.group(2) + '<name>' + Ascii(m.group(3)) + '</name>', content)
      '''

      for k,v in char_dict.items():
        content = content.replace(r'>' + k +'<', '>' + v +'<')

      #replace idenfifer
      content = re.sub(r'<name>([^<>,]*)</name>', lambda m:'<name>'+Ascii(m.group(1))+'</name>', content)






    #replace sapce \n \t
    for k,v in format_char_dict.items():
      if k != '\n':
        content = content.replace(r'>' + k +'<', '>' + v +'<')


    content = re.sub(r'<([^<>]*)>', '', content)


    sorted_char_keys = sorted(char_dict, key=lambda d: len(d), reverse=True)
    for k in sorted_char_keys:
      content = content.replace(k, char_dict[k])
    for k in [' ', '\t']:
      content = content.replace(k, format_char_dict[k])



    if not oneline:
      content = content.replace('\n', format_char_dict['\n'] + '\n')
    else:
      content = content.replace('\n', format_char_dict['\n'])



    content = content.replace('$$$',',')

    global _invalidwordreg
    invalidwords = _invalidwordreg.findall(content)
    if len(invalidwords) > 0:
      print
      '>>>>>>>>>>>> some invalid words: ' + str(invalidwords) + 'in file ' + file_path
    content = _invalidwordreg.sub(char_dict['Unknown'], content)
    content = content.replace('$$$',',')


    #replace END!!!


    #stat matrix size
    if not oneline:
      lines = content.split('\n')
      if len(lines) > max_line_count:
        max_line_count = len(lines)

        print file_path + ' ' + str(max_line_count)
      for line in lines:
        if ItemCount(line) > max_line_width:
          max_line_width = ItemCount(line)
          print '%s max line %d' % (file_path, max_line_width)
    else:

      wordscnt = ItemCount(content)
      if wordscnt > max_words_count:
        print '%s max word count %d' % (file_path, wordscnt)
        max_words_count = wordscnt


    output_file_path = ReplaceRootDir(file_path, 'mitoutput_word_encoded_%s' % ('ascii' if to_ascii else ''))
    #output_file_object = open(output_file_path, 'w')
    #output_file_object.write(content)
    #output_file_object.close()

    encode_file_list.append(output_file_path)

    #output_file_object_mid = open(os.path.join(dir_name , file_name + "_wordmatrix_mid.java"), 'w')
    #output_file_object_mid.write(midcontent)

    #print output_file_path + '   encoded.'

  print('final max words count: %d' % max_words_count)

  print(len(encode_file_list))
  i = 0
  for file_path in encode_file_list:
    i = i +1
    print(i)
    print(file_path)
    input_file_object = open(file_path)
    content = input_file_object.read()
    input_file_object.close()

    output_content = ''

    if not oneline:
      lines = content.split('\n')
      for line in lines:
        extra_count = max_line_width - ItemCount(line)
        output_content += line + Extra(extra_count)
        output_content += '\n'

      extra_row_count = max_line_count - len(lines)
      for i in range(0, extra_row_count):
        output_content += Extra(max_line_width) + '\n'
    else:
      if content.find('120,') != -1:
        print 'id:========='+file_path
      extra_count = max_words_count - ItemCount(content)
      output_content = content + Extra(extra_count)


    #file_name = os.path.basename(file_path)
    #output_file_path = os.path.join(matrix_dir_name , file_name + ".matrix")

    output_file_path = ReplaceRootDir(file_path, 'Word%s' % ('Char' if to_ascii else ''))
    output_file_path = ReplaceExt(output_file_path, 'matrix')
    output_file_object = open(output_file_path, 'w')
    #output_file_object = open(output_file_path, 'w')
    output_file_object.write(output_content)
    output_file_object.close()
    print output_file_path +' written.'
    Validate([output_file_path])


  print('max line width: %d' % max_line_width)
  print('max line count: %d' % max_line_count)
  print('max words count: %d' % max_words_count)


def XmlElementTransfer(file_list, char_dict_file_path):

  char_dict = {}
  CharDictLoadFromFile(char_dict_file_path, char_dict)


  for k, v in char_dict.items():
    char_dict[k] = char_dict[k] + ','



  max_line_width = 0
  max_line_count = 0



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

    content = re.sub(r'>([^<>]*)<', lambda m: '>' + re.sub(r'[^\n]', '', m.group(1)) + '<', content)#remove text without removing \n
    #for k in [',',' ','\t','{','}','(',')','&gt;','&lt;',';','[', ']', '?']:
    #  content = content.replace(k, '')

    for k in char_dict:
      #content = re.sub(r'<'+k+r'([^<>]*)>([^<>\n]*)<', '<'+k+'><', content)#remove text and attr
      content = re.sub(r'<'+k+r'([^<>]*)>', '<'+k+'>', content)#remove text and attr

    open('test.java','w').write(content)

    for k in char_dict:
      content = re.sub(r'</' +k +'>', '', content)#remove xml tail

    for k in char_dict:
      content = re.sub(r'<' +k +'>', char_dict[k], content)


    content = content.replace('\n</unit>','')#remove unit tail
    content = content.replace('\n', str(ord('\n')) +','+ '\n')

    content = re.sub(r'<([^<>]*)>', '', content)

    lines = content.split('\n')
    if len(lines) > max_line_count:
      max_line_count = len(lines)
    for line in lines:
      if ItemCount(line)  > max_line_width:
        max_line_width =ItemCount(line)

    #file_name = os.path.basename(file_path)
    #output_file_path = os.path.join(dir_name , file_name)
    output_file_path = ReplaceRootDir(file_path, 'midoutput_element_encoded')
    output_file_object = open(output_file_path, 'w')
    output_file_object.write(content)
    output_file_object.close()

    encode_file_list.append(output_file_path)

    #output_file_object_mid = open(os.path.join(dir_name , file_name + "_wordmatrix_mid.java"), 'w')
    #output_file_object_mid.write(midcontent)

    print file_path + ' encoded.'

  for file_path in encode_file_list:

    input_file_object = open(file_path)
    content = input_file_object.read()
    input_file_object.close()

    output_content = ''

    lines = content.split('\n')
    for line in lines:
      extra_count = max_line_width - ItemCount(line)
      output_content += line + Extra(extra_count)
      output_content += '\n'

    extra_row_count = max_line_count - len(lines)
    for i in range(0, extra_row_count):
      output_content += Extra(max_line_width) + '\n'


    output_file_path = ReplaceRootDir(file_path, 'Node')
    output_file_path = ReplaceExt(output_file_path, 'matrix')
    output_file_object = open(output_file_path, 'w')
    output_file_object.write(output_content)
    output_file_object.close()
    print output_file_path + ' written.'
    Validate([output_file_path])

  print('max line width: %d' % max_line_width)
  print('max line count: %d' % max_line_count)





def ToMatrix(file_list, char_dict_file_path):

  print('ToMaritx %d files' % len(file_list))
  char_dict = {}
  CharDictLoadFromFile(char_dict_file_path, char_dict)



  max_line_width = 305
  max_line_count = 50


  for file_path in file_list:
    if not file_path.endswith('.java'):
      continue;

    input_file_object = open(file_path, 'r')


    lines = input_file_object.readlines()
    if len(lines) > max_line_count:
      max_line_count = len(lines)
      print '%s max line count %d' % (file_path, max_line_count)

    for line in lines:
      if len(line) > max_line_width:
        max_line_width = len(line)
        print '%s max line width %d' % (file_path, max_line_width)
    input_file_object.close()


  print('max line width: %d' % max_line_width)
  print('max line count: %d' % max_line_count)
  return

  for file_path in file_list:
    print(file_path)
    if not file_path.endswith('.java'):
      continue;
    input_file_object = open(file_path, 'r')

    output_file_path = ReplaceRootDir(file_path, 'Character') + '.matrix'
    print(output_file_path)
    output_file_object = open(output_file_path, 'w')

    '''
    if not os.path.exists("output_javachar"):
      os.mkdir("output_javachar")
    dir_name = os.path.join("output_javachar" , os.path.basename(os.path.dirname(file_path)))
    file_name = os.path.basename(file_path)
    if not os.path.exists(dir_name):
      os.mkdir(dir_name)
    output_file_object = open(os.path.join(dir_name ,  file_name + ".matrix" ),'w')
    '''
    output_matrix = []
    for line in input_file_object:
      output_matrix_row = []
      l = list(line)
      for s in l:
        if s == '\r':
          continue
        if char_dict.has_key(s):
          output_matrix_row.append(char_dict[s])
        else:
          output_matrix_row.append(char_dict['unknown'])

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
        output_text = output_text + ',\n'
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
          output_text = output_text + ',' + '-1'
      output_text = output_text + ',\n'

    output_file_object.write(output_text)
    output_file_object.close()
    input_file_object.close()
    #print output_file_path + ' written.'

def mkdir_p(path):
  try:
    os.makedirs(path)
  except OSError as exc:  # Python >2.5 (except OSError, exc: for Python <2.5)
    if exc.errno == errno.EEXIST and os.path.isdir(path):
      pass
    else:
      raise

def ReplaceRootDir(file_path, dir_name):
  rootdir = _input_dir.split(os.sep)[-1]
  new_file_path = file_path.replace(_input_dir, os.path.join('./'+dir_name, rootdir))
  '''
  ar = file_path.split(os.sep)
  if ar[0] == '.':
    ar = ar[1:]
  ar[0] = dir_name
  new_file_path = '.'
  for p in ar:
    new_file_path = os.path.join(new_file_path, p)

  1/2/3/4/5
  5/6/7/8.java
  1/2/3/4/char/5/6/7/8.java
  '''
  if not os.path.exists(os.path.dirname(new_file_path)):
    mkdir_p(os.path.dirname(new_file_path))
  return new_file_path
  #return os.path.splitext(new_file_path)[0]

def ReplaceExt(file_path, ex):
  return os.path.splitext(file_path)[0] + '.' + ex

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



def Validate(file_list):
  for file_path in file_list:
    if not file_path.endswith('.matrix'):
      continue;
    f = open(file_path)
    content = f.read();
    global  _invalidwordreg
    ret = _invalidwordreg.findall(content)
    if len(ret) > 0:
      print '>>>>>>>>>>>>>>>>>>>>'+file_path + ' is invalid with ' + str(ret)
      exit()

if (__name__ == '__main__'):
  print ('start')
  ParseArgs(sys.argv[1:])

  #global _stat

  rootdir = _input_dir
  file_list = []
  WalkFiles(rootdir, file_list)

  if _stat:
    Stat()
  elif _javachar:
    ToMatrix(file_list, 'char.txt')
  elif _xmlword1line:
    XmlWordOnelineTransfer(file_list, 'word2.txt')
  elif _xmlword:
    XmlTransfer(file_list, 'word.txt', False)
  elif _xmlwordascii:
    XmlTransfer(file_list, 'word.txt',  True)
  elif _xmlelement:
    XmlElementTransfer(file_list, 'element.txt')
  elif _validate:
    print "---------VALIDATE-------------"
    Validate(file_list)
    #re.sub(r'<([^<>]*)>', '', content)

'''

def ToMatrix0(file_list, char_dict_file_path):

  print('ToMaritx %d files' % len(file_list))
  char_dict = {}
  CharDictLoadFromFile(char_dict_file_path, char_dict)



  max_line_width = 0
  max_line_count = 0

  
  for file_path in file_list:
    print(file_path)
    if not file_path.endswith('.xml'):
      continue;
    input_file_object = open(file_path, 'r')


    dir_name = "Output_" + os.path.basename(os.path.dirname(file_path))
    file_name = os.path.basename(file_path)
    if not os.path.exists(dir_name):
      os.mkdir(dir_name)
    output_file_object = open(dir_name + "\\" + file_name + ".matrix", 'w')

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

  rootdir = _input_dir
  file_list = []
  WalkFiles(rootdir, file_list)
  if _stat:
    Stat()
  elif _javachar:
    ToMatrix(file_list, 'char.txt')
  elif _xmlword:
    XmlTransfer(file_list, 'word.txt', False)
  elif _xmlwordascii:
    XmlTransfer(file_list, 'word.txt',  True)
  #elif _xmlelement:

    #re.sub(r'<([^<>]*)>', '', content)

'''