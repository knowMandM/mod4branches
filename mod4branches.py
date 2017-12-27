# coding:utf-8

import shutil
import os, codecs
import mod_file, re
import time

u'''\
    这是一个用来在游戏发布外网包时，把trunk上的内网配置改为外网配置的工具
'''

#g_version = u'2.3.20171225'
#g_versioncode = u'8'

OS_ANDOID = 'android'
OS_APPLE = 'ios'

shopconfig_ClientId = {
    OS_APPLE: u'100341',
    OS_ANDOID: u'100117',    
}

recommander_id = {
    OS_ANDOID: '189999236',
    OS_APPLE: '189999259'
}

pay_channel_id = {
    OS_ANDOID: '100066',
    OS_APPLE: '100102'
}

g_toDelFileList = [
    u'./SettingsData.xml',
    u'./UmengConfig.json',
    u'./ct108sdkconfig.json',
    u'./gfsl.xlsx'
]

def getFileInfoForMod(curOS):
    g_fileInfoForMod   = [\
        {
        'fileName'      : ur'./src/config.lua',
        'regex'         : ur'\s*DEBUG\s*=\s(\d+)\s*',
        'replaced_as'   : u'0',
        'codec'         : u'utf-8'
        },
        
        {
        'fileName'      : ur'./src/app/HallConfig/shopconfig/shopconfig.json',
        'regex'         : ur'\s*"ClientId":\s*"(\d*)"',
        'replaced_as'   : shopconfig_ClientId[curOS],
        'codec'         : u'utf-8'
        },
        
        {
        'fileName'      : ur'./src/app/HallConfig/RoomConfig.lua',
        'regex'         : ur'\s*\["areaName"\]\s*=\s*"(.+)"',
        'replaced_as'   : u'一起玩',
        'codec'         : u'utf-8'
        },
        
        {
        'fileName'      : ur'./AppConfig.json',
        'regex'         : ur'\s*"version":\s*"([\d,\.]*)"',
        'replaced_as'   : g_version,
        'codec'         : u'utf-8'
        },
        
        {
        'fileName'      : ur'./AppConfig.json',
        'regex'         : ur'\s*"versionCode":\s*"([\d,\.]*)"',
        'replaced_as'   : g_versioncode,
        'codec'         : u'utf-8'
        },
        
        {
        'fileName'      : ur'./ChannelConfig.json',
        'regex'         : ur'\s*"recommander_id":\s*"(\d*)"',
        'replaced_as'   : recommander_id[curOS],
        'codec'         : u'utf-8'
        },
        
        {
        'fileName'      : ur'./ChannelConfig.json',
        'regex'         : ur'\s*"pay_channel_id":\s*"(\d*)"',
        'replaced_as'   : pay_channel_id[curOS],
        'codec'         : u'utf-8'
        },
    ]
    
    return g_fileInfoForMod

def deleteNeedlessFiles(toDelFileList):
    u'删除不需要的文件'
    for filename in toDelFileList:
        if os.path.exists(filename):
            os.remove(filename)

def modifyBatchFile(listDictFileInfos):
    u'根据正则表达式批量修改文件'
    for node in listDictFileInfos:
        mod_file.modifyFileByRegEx(node['fileName'], node['regex'], node['replaced_as'], coding = node['codec'])

def modifyMain_lua(path):
    u'删除main.lua 中 require "mime" 前的所有内容'
    with codecs.open(path, 'r+', 'utf-8') as f:
        lines = f.readlines()
        regex = re.compile(ur'\s*require\s+')
        for i in range(0, len(lines)):
            if regex.match(lines[i]) == None:
                lines[i] = None
            else:
                break
        
        f.seek(0, 0)
        f.writelines(filter(None, lines))
        f.truncate()

def doModBranch(strScriptPath, OS_type):
    u'''为ios或android的branch进行修改'''
    os.chdir(strScriptPath)
    print(os.getcwd())
    curOS = OS_type
    deleteNeedlessFiles(g_toDelFileList)
    modifyBatchFile(getFileInfoForMod(OS_type))
    modifyMain_lua(ur'./src/main.lua')

def inputScriptPath():
    strPath = raw_input(u'输入脚本的目录:'.encode('gbk'))
    return strPath
    
def inputVersion():
    global g_version
    g_version = raw_input(u'输入脚本客户端要更新成的version:'.encode('gbk'))
    return g_version

def inputVersionCode():
    global g_versioncode
    g_versioncode = raw_input(u'输入脚本客户端要更新成的versionCode:'.encode('gbk'))
    return g_versioncode

def inputOS():
    osChoose = {
        1 : OS_ANDOID,
        2 : OS_APPLE
    }
    for key in osChoose.keys():
        print u'%d: %s' % (key, osChoose[key])
    
    nChoose = 0
    while True:
        try:
            nChoose = int(raw_input(u'输入序号选择操作系统：'.encode('gbk')))
            break
        except ValueError:
            print u'请重输:'
    return osChoose[nChoose]
    
if __name__ == '__main__':
    scriptPath = inputScriptPath()
    version = inputVersion()
    versionCode = inputVersionCode()
    OStype = inputOS()
    doModBranch(scriptPath.replace('\\', '/'), OStype)
    print u'完成,1s后打开目录...'
    time.sleep(1)
    os.system('start ' + scriptPath)
    
    
    