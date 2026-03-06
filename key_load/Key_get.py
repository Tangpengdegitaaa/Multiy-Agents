import os
import json
import getpass  

def load_key(keyname:str) -> str: 
    file_name = os.path.dirname(__file__)+"/Keys.json"  
                                                       
    if os.path.exists(file_name):
        with open(file_name,"r") as file:   #以只读模式打开文件       
            Key = json.load(file)  #json.load()：将JSON内容解析为Python字典
        if keyname in Key and Key[keyname]:
            return str(Key[keyname])
        else:
            keyval=getpass.getpass("配置文件中没有相应就，请输入对应配置信息:").strip()
            Key[keyname] = keyval
            with open(file_name,"w") as file:
                json.dump(Key,file,indent=4)
            return str(keyval)
    else:
        keyval=getpass.getpass("没有配置文件，建立配置文件，输入对应配置信息:").strip()
        Key ={
            keyname:keyval
        }
        with open(file_name,"w") as file:
            json.dump(Key,file,indent=4)
        return str(keyval)
