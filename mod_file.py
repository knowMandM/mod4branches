# coding: utf-8

import re, codecs

def modifyFileByRegEx(uniFilePath, uniRegEx, uniReplaceStr, iReplaceIndex = 1, coding='utf-8'):
    u'''根据 uniRegEx 在 uniFilePath 中查找到符合条件的行，用uniReplaceStr替换该行iReplaceIndex的内容'''
    with codecs.open(uniFilePath, 'r+', coding) as f:
        listLine = f.readlines()
        regex = re.compile(uniRegEx)
        for i in range(0, len(listLine)):
            match = regex.match(listLine[i])
            if match != None:
                listLine[i] = listLine[i].replace(match.group(iReplaceIndex), uniReplaceStr)
                break
        f.seek(0,0)
        f.writelines(listLine)
        f.truncate()