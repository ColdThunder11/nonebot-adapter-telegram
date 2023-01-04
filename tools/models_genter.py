from lxml import etree
from typing import Dict, List, Optional, Text, Union, Tuple

type_defs = {
    "Integer" : "int",
    "Boolean" : "bool",
    "String" : "str",
    "True" : "bool",
    "Intege": "int",
    "Float" : "float",
    "Float number" : "float",
    "Integer or String": "Union[int, str]",
    "InputFile or String" : "str",
    "MessageEntit" : "MessageEntity",
    "Message" : "MessageBody"
}


def get_field_py_type(type_name:str, optional:bool) -> str:
    return_str = ""
    if optional:
        return_str += "Optional["
    if type_name.startswith("Array of "):
        type_name_s = type_name.strip("Array of ")
        if type_name_s in type_defs.keys():
            return_str += f'List["{type_defs[type_name_s]}"]'
        else:
            return_str += f'List["{type_name_s}"]'
    else:
        if type_name in type_defs.keys():
            return_str += f'"{type_defs[type_name]}"'
        else:
            return_str += f'"{type_name}"'
    if optional:
        return_str += "]"
    return return_str

def method_name_text_builder(html_text : str) -> str:
    html_text = html_text.strip("\n")
    plain_text = ""
    left_count = 0
    pointer = 0
    while(pointer < len(html_text)):
        char = html_text[pointer]
        if char == "<" :
            left_count += 1
            pointer += 1
            continue
        elif char == ">":
            left_count -= 1
            pointer += 1
            continue
        else:
            if left_count == 0:
                plain_text += char
            pointer += 1
            continue
    return plain_text

def method_name_annotation_builder(html_text : str) -> str:
    html_text = html_text.strip("\n")
    plain_text = ""
    left_count = 0
    pointer = 0
    while(pointer < len(html_text)):
        char = html_text[pointer]
        if char == "<" :
            left_count += 1
            pointer += 1
            continue
        elif char == ">":
            left_count -= 1
            pointer += 1
            continue
        else:
            if left_count == 0:
                plain_text += char
            pointer += 1
            continue
    return plain_text

def type_define_builder(html_text : str) -> Tuple[str,str]:
    html_text = html_text.strip("\n")
    thread_start = html_text.find("<thead>")
    thread_end = html_text.find("</thead>")
    thread_content = html_text[thread_start:thread_end]
    thread_th_count = thread_content.count("<th>")
    tbody_start = html_text.find("<tbody>")
    tbody_end = html_text.find("</tbody>")
    tbody_content = html_text[tbody_start:tbody_end]
    type_class_text  =""
    type_class_annotation = "    Arguments:\n"
    if thread_th_count == 3:
        pointer = 0
        while((filed_start := tbody_content.find("<td>",pointer)) != -1):
            field_end = tbody_content.find("</td>",pointer)
            field_name = method_name_text_builder(tbody_content[filed_start:field_end+5])
            pointer = field_end +5
            if field_name == "from":
                type_class_text = '''
    @root_validator(pre=True)
    def gen_message(cls, values: dict):
        if "from" in values:
            values["from_"] = values["from"]
            del values["from"]
        return values
''' + type_class_text
                field_name = "from_"

            field_type_start = tbody_content.find("<td>",pointer)
            field_type_end = tbody_content.find("</td>",pointer)
            field_type = method_name_text_builder(tbody_content[field_type_start:field_type_end+5])
            pointer = field_type_end +5
            
            field_description_start = tbody_content.find("<td>",pointer)
            field_description_end = tbody_content.find("</td>",pointer)
            field_description = method_name_text_builder(tbody_content[field_description_start:field_description_end+5])
            pointer = field_description_end +5
            field_optional = True if field_description.startswith("Optional") else False
            field_type = get_field_py_type(field_type, field_optional)
            type_class_text += f"    {field_name}: {field_type}\n"
            type_class_annotation += f"        {field_name}: {field_description}\n"

    if thread_th_count == 4:
        pass
    return (type_class_text,type_class_annotation)


f = open("Telegram Bot API.html","r",encoding="utf-8")
html=etree.HTML(f.read())
f.close()
#print(etree.tostring(html))
#Types Genter  //*[@id="dev_page_content"]/h4[179]
type_pos_list : List[int] = []
type_pos_list.append(9)
for i in range(15,97):
    type_pos_list.append(i)
for i in range(179,182):
    type_pos_list.append(i)
type_pos_list.append(191)
for i in range(193,223):
    type_pos_list.append(i)
for i in range(227,239):
    type_pos_list.append(i)
for i in range(240,250):
    type_pos_list.append(i)
for i in range(251,256):
    type_pos_list.append(i)
#type_pos_list.append(232)
types_text = '''
from typing import Dict, List, Optional, Text, Union
from typing_extensions import Literal

from pydantic import BaseModel, root_validator
from enum import Enum
'''
#for i in range(13,79)://*[@id="dev_page_content"]/h4[146]//*[@id="dev_page_content"]/h4[149]//*[@id="dev_page_content"]/h4[157]
for i in type_pos_list:
    result = html.xpath(f'//*[@id="dev_page_content"]/h4[{i}]')[0]
    type_str = method_name_text_builder(str(etree.tostring(result), encoding = "utf8"))
    if type_str.strip()[0].islower():
        continue
    class_define = f"\nclass {type_str}(BaseModel):"
    #print(etree.tostring(result.getnext()))
    annotation_text = method_name_annotation_builder(str(etree.tostring(result.getnext()), encoding = "utf8"))
    define_table = result.getnext().getnext()
    type_info = type_define_builder(str(etree.tostring(define_table)))
    if type_info[0] == "":
        types_text += f"{class_define}\n    '''\n    {annotation_text}\n\n{type_info[1]}    '''\npass\n".replace("\\\'","'")
    else:
        types_text += f"{class_define}\n    '''\n    {annotation_text}\n\n{type_info[1]}    '''\n{type_info[0]}\n".replace("\\\'","'")
    #print(type_str)
    #print(annotation_text)
    #print(type_info)
types_text += '''
Update.update_forward_refs()
Chat.update_forward_refs()
MessageBody.update_forward_refs()
InlineKeyboardButton.update_forward_refs()
'''.strip()
print(types_text)
with open("tg_types.py","w",encoding="utf-8") as wf:
    wf.write(types_text)