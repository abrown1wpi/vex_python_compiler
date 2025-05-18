import os

#################################################################################################
#                                                                                               #
#  ██████   ██████      ███    ██  ██████  ████████      █████  ██   ████████ ████████ ██████   #
#  ██   ██ ██    ██     ████   ██ ██    ██    ██        ██   ██ ██      ██    ██       ██   ██  #
#  ██   ██ ██    ██     ██ ██  ██ ██    ██    ██        ██   ██ ██      ██    ██████   ██████   #
#  ██   ██ ██    ██     ██  ██ ██ ██    ██    ██        ███████ ██      ██    ██       ██   ██  #
#  ██   ██ ██    ██     ██   ████ ██    ██    ██        ██   ██ ██      ██    ██       ██   ██  #
#  ██████   ██████      ██    ███  ██████     ██        ██   ██ ███████ ██    ████████ ██   ██  #
#                                                                                               #
#################################################################################################



dirs = [dir for dir in os.listdir("src")] #find all of the files in the src directory

main_orig = open("src/main.py", "r") #open the main file
main_orig_text = main_orig.read()
main_comp = open("compiled/main.py", "w")

def get_contents_after_last_import(text):
    lines = text.splitlines()
    last_import_index = -1
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith('import ') or stripped.startswith('from '):
            last_import_index = i
    if last_import_index == -1:
        return text  
    if last_import_index + 1 >= len(lines):
        return ""  
    return "\n".join(lines[last_import_index + 1:])


def parse_named_block(text, name):
    lines = text.splitlines()
    result = []
    capture = False
    indent_prefix = None
    
    for i, line in enumerate(lines):
        stripped = line.strip()
        
        if not capture:
            if stripped.startswith(f"class {name}") and (
                len(stripped) == len(f"class {name}") or 
                stripped[len(f"class {name}")].isspace() or 
                stripped[len(f"class {name}")] in ":("
            ):
                result.append(line)
                capture = True
                indent_prefix = len(line) - len(line.lstrip())
                continue
            
            if stripped.startswith(f"def {name}") and (
                len(stripped) == len(f"def {name}") or 
                stripped[len(f"def {name}")].isspace() or 
                stripped[len(f"def {name}")] in ":("
            ):
                result.append(line)
                capture = True
                indent_prefix = len(line) - len(line.lstrip())
                continue
        
        if capture:
            current_indent = len(line) - len(line.lstrip())
            if line.strip() == "":
                result.append(line)  
            elif current_indent > indent_prefix: # type: ignore
                result.append(line)
            else:
                break 
    
    return "\n".join(result)



def tokenize_file(file_name,contents,priority):
    contents.replace("\nimport math","\n")
    file_org = open("src/{}.py".format(file_name),"r")
    file_text = file_org.read()
    file_by_line = file_text.split("\n")
    file_import = [l for l in file_by_line if "import" in l]
    file_import = [l[5:].split(" import ") for l in file_import if "from" in l]
    token = {}

    text = get_contents_after_last_import(file_text)
    token = {"priority":priority,"contents":text,"children":file_import,"parent_file":None}
    return token



def generate_main_token(contents):
    contents.replace("\nimport math","\n")
    main_orig_by_line = contents.split("\n")
    main_orig_import = [l for l in main_orig_by_line if "import" in l]
    main_orig_import = [l[5:].split(" import ") for l in main_orig_import if "from" in l]
    text = get_contents_after_last_import(contents)
    token = {"priority":0,"contents":text,"children":main_orig_import,"parent_file":None}
    return token




if len(dirs) == 1:
    # just main.py
    main_comp.write(main_orig_text)
else:
    library_imports = ["vex","math"]

    token_tree = {"main":generate_main_token(main_orig_text)}
    tokens_to_search = ["main",]
    while len(tokens_to_search) > 0:
        
        parent_name = tokens_to_search.pop(0)
        parent_token = token_tree[parent_name]

        for name,contents in parent_token["children"]:
            if name in library_imports:
                continue
            keys = token_tree.keys()
            if name in keys:
                token = token_tree[name]
                if token["priority"] < parent_token["priority"]+1:
                    token["priority"] = parent_token["priority"]+1
                    tokens_to_search.append(name)
                
            else:
                new_token = tokenize_file(name,contents,parent_token["priority"]+1)
                token_tree[name] = new_token
                tokens_to_search.append(name)


    max_priority = max(v.get("priority", 0) for v in token_tree.values())

    text = "from vex import *\nimport math\n"
    for i in range(max_priority,-1,-1):
        tokens_with_priority = {k: v for k, v in token_tree.items() if v.get('priority') == i}
        for item in tokens_with_priority:

            text +="\n"+token_tree[item]["contents"]
    main_comp.write(text)
        

    

print("done")