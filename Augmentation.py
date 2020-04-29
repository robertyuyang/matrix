import os
import re
import random
import string

mfunc = 1
mvar = 0
mvar_rate = .35
mspace =1
suffix = '.fs'

def geneRandomName(maxLen):
    ret = ''
    len = random.randint(3, maxLen)
    for i in range(len):
        if i == 0:
            ret = ret + random.choice(string.ascii_letters)
        else:
            ret = ret + random.choice(string.ascii_letters + string.digits)
    return ret

path = '/Users/robertyu/Documents/src/robert/py/matrix/data/Readability Data/Java Code/Training Set/Unreadable/original'
keywords_list = ['null', 'true', 'false', 'java', 'com', 'org', 'File', 'continue', 'int', 'float', 'break', 'return', 'class', 'this', 'super', 'Thread', 'Arrays','Collections', 'log']

def iskeyword(str):
    for k in keywords_list:
       if str == k:
           return True

    return False
def myfindall(regex, seq):

    return regex.findall(seq)
    resultlist=[]
    pos=0

    while True:
       result = regex.search(seq, pos)
       if result is None:
          break
       group_count = len(result.groups())
       if group_count > 0:
            resultlist.append(result.groups()[0])
       else:
            resultlist.append(seq[result.start():result.end()])
       pos = result.start()+1
    return resultlist

'''
s = 'import org.gudy.azureus2.platform.PlatformManager;'
print(re.findall(r'\.(\w+)[^\w]', s))
print(myfindall( re.compile(r'\.(\w+)[^\w]'), s))
'''
for root, dirs, files in os.walk(path):
    for f in files:
        file_path = os.path.join(root, f)
        if not file_path.endswith(".java"):
            continue
        print(file_path)
        f = open(file_path, encoding='utf-8')
        file_name = os.path.split(file_path)[1]

        shotname, extension = os.path.splitext(file_name)
        of = open('data/output/' + shotname + suffix + extension, encoding='utf-8', mode='w')
        content = f.read()
        m_content = content
        #regexp = r'(\s*(private|public)\s+\w+\s+)(\w+)(\(.*\)\s+{)'
        regexp = r'(\s*(private|public|protected)\s+\w+\s+)(\w+)(\()'
        func_dec_re = re.compile(regexp)
        #var_dec_re = re.compile(r'\s+(\w+)\s*=')

        #function
        if mfunc :
            match_result = func_dec_re.search(content)
            if match_result:
                function_name = match_result.group(3)  # .split()[-1]
                print(function_name)
                m_content = func_dec_re.sub(lambda x: x.group(1) + geneRandomName(8) + x.group(4), content)

        if mvar:
            #variable
            var_dict = {}

            var_re_list = [re.compile(r'\s+(\w+)\s*='), #String var =
                           re.compile(r'[^\w](\w+)\.'), # var.invoke
                           re.compile(r'[^\w](\w+);'), # var;
                           re.compile(r'\.(\w+)[^\w\(]'), # obj.var
                           re.compile(r'(\s+|\()(\w+)\,'), #func(String var, Int i)
                           re.compile(r'(\s+|\()(\w+)\s*\)'), #func(Int var)
                            re.compile(r'\+\s*(\w+)[^\w\(]'),
                           re.compile(r'[^\w]+\s*(\w+)\s*\+')]
            for rep in var_re_list:
                var_list = myfindall(rep, m_content)
                for var_name in var_list:
                    if isinstance(var_name, tuple):
                        var_name = var_name[1]
                    if not var_name[0].isdigit() and not iskeyword(var_name) and var_name != 'self' and len(var_name.strip()) > 0:
                        var_dict[var_name] = 1;
            #var_list = list(var_dict)
            print(list(var_dict))

            if mvar_rate < 1:
                var_list = random.sample(list(var_dict), (int)(len(var_dict) * mvar_rate))
                var_dict = {}
                for var_name in var_list:
                    var_dict[var_name] = 1;


            print(list(var_dict))
            for (var_name,v) in var_dict.items():
                rdname = geneRandomName(5)
                m_content = re.sub(r'([^\w\"])('+var_name + r')([^\w\"])', lambda x: x.group(1) + rdname + x.group(3), m_content)
                '''
                if len(var_name) > 3:
                    m_content = m_content.replace(var_name, rdname)
                else:
                    m_content = m_content.replace(var_name + '.', rdname + '.').replace(var_name + ',', rdname + ',').replace(var_name + ')', rdname + ')')
                    m_content = re.sub(r'(\s+)(\w+)(\s*=)', lambda x: x.group(1) + rdname + x.group(3), m_content)
                    m_content = re.sub(r'(\+\s*)(\w+)([^\w\(])', lambda x: x.group(1) + rdname + x.group(3), m_content)
                    m_content = re.sub(r'([^\w]+\s*)(\w+)(\s*\+)', lambda x: x.group(1) + rdname + x.group(3), m_content)
                    m_content = re.sub(r'([^\w])(\s*\+)', lambda x: x.group(1) + rdname + x.group(3), m_content)
                '''

        if mspace:
            d = "\n"
            m_lines = [e + d for e in m_content.split(d) if e]
            lines_count = len(m_lines)

            line_index_dict = {}
            m_line_index_dict = {}
            line_index_list = []
            for i in range(lines_count):
                line_index_dict[i]= m_lines[i]
                line_index_list.append(i)

           # merge_line_count = 3
            merge_count = (int)(lines_count * .3)
            strip_count = (int)(lines_count * .3)

            m_index_list = random.sample(line_index_list, merge_count)

            for index in m_index_list:
                m_lines[index]  = m_lines[index].replace('\n', '')

            m_index_list = random.sample(line_index_list, strip_count)
            for index in m_index_list:
                m_lines[index] = m_lines[index].lstrip()

            m_content = ''.join(m_lines)

            '''
            for i in range(merge_count):
                cur_lines_count = len(line_index_dict)
                index_index =  random.randint(0, cur_lines_count - merge_line_count + 1)
                start =
                for j in range(merge_line_count):
                    if j != merge_line_count - 1:
                        m_line_index_dict[start + j] = line_index_dict.pop(start + j).replace('\n', '')
                    else:
                        m_line_index_dict[start + j] = line_index_dict.pop(start + j)


            m_line_index_dict = dict(m_line_index_dict.items(), line_index_dict.items())

            m_content = ""
            for i in range(lines_count):
                m_content = m_content + m_line_index_dict[i]

            '''

        of.write(m_content)

        f.close()
        of.close()
