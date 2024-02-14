from ruamel.yaml import YAML
import re


with open('txt.txt', encoding='utf-8') as file:
    a = YAML(typ='safe').load(re.sub('<[^>]*>', '', file.read()))
    print(a)
    print(type(a))
    if type(a) == dict:
        print(2342)
