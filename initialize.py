import os
import shutil
import platform

def get_personal_path():
    os_type = platform.system()
    personal_path = 'None'
    try:
        if os_type == 'Darwin':

            path = os.path.expanduser('~/Library/Application Support/Code/User/globalStorage/vexrobotics.vexcode/sdk/python/V5/V5_1_0_1_25/vexv5/stubs')
            if os.path.exists(path):
                personal_path = '"' + path + '"'
            else:
                raise(Exception('CANT FIND SDK'))
            
        elif os_type == 'Windows':

            path = os.path.expanduser('~').replace('\\', '\\\\') + '\\\\Appdata\\\\Roaming\\\\Code\\\\User\\\\globalStorage\\\\vexrobotics.vexcode\\\\sdk\\\\python\\\\V5\\\\V5_1_0_1_25\\\\vexv5\\\\stubs'
            if os.path.exists(path):
                personal_path = '"' + path + '"'
            else:
                raise(Exception('CANT FIND SDK'))
            
        elif os_type == 'Linux':

            path = os.path.expanduser('~/.config/Code/User/globalStorage/vexrobotics.vexcode/sdk/python/V5/V5_1_0_1_25/vexv5/stubs')
            if os.path.exists(path):
                personal_path = '"' + path + '"'
            else:
                raise(Exception('CANT FIND SDK'))
            
    except Exception as e:
        print(e)

    settings_json = '{\n\t"python.analysis.stubPath": ' + personal_path + ',\n\t"python.analysis.diagnosticMode": "workspace",\n\t"python.analysis.typeCheckingMode": "basic"\n}'
    return settings_json

def write_jsons():
    # Make .vscode folder
    vscode_path = ".vscode"
    if not os.path.isdir(vscode_path) : os.mkdir(vscode_path)

    # Make settings.json
    settings_json_path = vscode_path + "/settings.json"
    sj = open(settings_json_path, "w")
    settings_json = get_personal_path()
    sj.write(settings_json)

    # Make vex_project_settings.json
    vex_project_settings_path = vscode_path + "/vex_project_settings.json"
    vps = open(vex_project_settings_path, "w")
    vex_project_settings_json = '{\n\t"extension": {\n\t\t"version": "0.6.0",\n\t\t"json": 2\n\t},\n\t"project": {\n\t\t"name": "' + '",\n\t\t"description": "",\n\t\t"creationDate": "",\n\t\t"platform": "V5",\n\t\t"language": "python",\n\t\t"slot": 1,\n\t\t"sdkVersion": "V5_1_0_1_25",\n\t\t"python": {\n\t\t\t"main": "compiled/main.py"\n\t\t}\n\t}\n}'
    vps.write(vex_project_settings_json)

write_jsons()

