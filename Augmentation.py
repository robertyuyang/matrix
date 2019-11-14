import os
import re
import random
import string


def geneRandomName():
    ret = ''
    len = random.randint(1, 20)
    for i in range(len):
        if i == 0:
            ret = ret + random.choice(string.ascii_letters)
        else:
            ret = ret + random.choice(string.ascii_letters + string.digits)
    return ret

path = '/Users/robertyu/Documents/src/robert/py/matrix/data/Readability Data/Java Code/Training Set/Unreadable/original_test'



for root, dirs, files in os.walk(path):
    for f in files:
        file_path = os.path.join(root, f)
        if not file_path.endswith(".java"):
            continue
        print(file_path)
        f = open(file_path, encoding='utf-8')
        file_name = os.path.split(file_path)[1]

        shotname, extension = os.path.splitext(file_name)
        of = open('data/output/' + shotname + '.m' + extension, encoding='utf-8', mode='w')
        content = f.read()
        m_content = content
        # regexp = r'(\w(\w|::|\*|\&|\s)*)\(.*)( )*{'  # decls * & space::name( ...
        regexp = r'(\s*(private|public)\s+\w+\s+)(\w+)(\(.*\)\s+{)'
        func_dec_re = re.compile(regexp)
        #var_dec_re = re.compile(r'\s+(\w+)\s*=')

        #function
        match_result = func_dec_re.match(content)
        if match_result:
            function_name = match_result.group(3)  # .split()[-1]
            print(function_name)
            m_content = func_dec_re.sub(lambda x: x.group(1) + geneRandomName() + x.group(4), content)

        var_dict = {}

        var_re_list = [re.compile(r'\s+(\w+)\s*='), re.compile(r'\s+(\w+)\.'), re.compile(r'(\s+|\()(\w+)\,'), re.compile(r'(\s+|\()(\w+)\)'),
                       re.compile(r'\+\s*(\w+)[^\w\(]'), re.compile(r'[^\w]+\s*(\w+)\s*\+')]
        for rep in var_re_list:
            var_list = rep.findall(m_content)
            for var_name in var_list:
                if isinstance(var_name, tuple):
                    var_name = var_name[1]
                if not var_name[0].isdigit():
                    var_dict[var_name] = 1;
        var_list = list(var_dict)
        print(var_list)
        for (var_name,v) in var_dict.items():
            rdname = geneRandomName()
            m_content = m_content.replace(var_name + '.', rdname + '.').replace(var_name + ',', rdname + ',').replace(var_name + ')', rdname + ')')
            m_content = re.sub(r'(\s+)(\w+)(\s*=)', lambda x : x.group(1) + rdname + x.group(3), m_content)
            m_content = re.sub(r'(\+\s*)(\w+)([^\w\(])', lambda x : x.group(1) + rdname + x.group(3), m_content)
            m_content = re.sub(r'([^\w]+\s*)(\w+)(\s*\+)', lambda x : x.group(1) + rdname + x.group(3), m_content)



        of.write(m_content)

        f.close()
        of.close()
