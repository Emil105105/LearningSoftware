#!/usr/bin/env python3

# ^^ Linux-executable init

### LEGAL ###

# This is free and unencumbered software released into the public domain.

# Anyone is free to copy, modify, publish, use, compile, sell, or
# distribute this software, either in source code form or as a compiled
# binary, for any purpose, commercial or non-commercial, and by any
# means.

# In jurisdictions that recognize copyright laws, the author or authors
# of this software dedicate any and all copyright interest in the
# software to the public domain. We make this dedication for the benefit
# of the public at large and to the detriment of our heirs and
# successors. We intend this dedication to be an overt act of
# relinquishment in perpetuity of all present and future rights to this
# software under copyright law.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.

# For more information, please refer to <http://unlicense.org/>

### DEPENDENCIES ###

import json
import random
import time
import os
import sys
import math
from hashlib import pbkdf2_hmac
from hashlib import sha512
import platform

### API ###

def setup():
    files = ['Userdata/config.json', 'Userdata/stats.json', 'Languages/EN.json', 'Packages/Test.json']
    contents = ['{\n  "mark_system": "CH",\n  "language": "EN"\n}\n',
        '{\n  "answers": [\n  ],\n  "startup": [\n  ],\n  "answered_question": [\n  ],\n  "info": [\n  ],\n  "quit": [\n  ],\n  "learn": [\n  ],\n  "setup": [\n  ]\n}\n',
        '{\n  "_init1": "LearningSoftware - python terminal edition",\n  "_init2": "made by github.com/Emil105105 | version: ",\n  "_init3": "Useful commands: !help !license !commands",\n  "_commands01": "List of commands:",\n  "_commands02": "    !learn            | start learning",\n  "_commands03": "    !exit             | stop learning",\n  "_commands04": "    !license          | show license",\n  "_commands05": "    !p list           | list all installed packages with status",\n  "_commands06": "    !p list a         | list all installed packages with details",\n  "_commands07": "    !p list e         | list all enabled packages",\n  "_commands08": "    !p enable *       | enable all packages",\n  "_commands09": "    !p enable [name]  | enable specific package",\n  "_commands10": "    !p disable *      | disable all packages",\n  "_commands11": "    !p disable [name] | disable specific package",\n  "_commands12": "    !p reload         | reload all packages from the disk",\n  "_commands13": "    !language [name   | change language (doesn\'t apply for commands yet)",\n  "_commands14": "    !mark             | list avaible mark systems",\n  "_commands15": "    !mark [name]      | change mark system",\n  "_commands16": "    !quit             | quit the software",\n  "unknown command": "unknown command",\n  "name of package": "name of package",\n  "enabled": "enabled",\n  "size": "size",\n  "author": "author",\n  "_license": "This program is in the public domain. Visit <unlicense.org> for more information.",\n  "progress": "progress",\n  "_question": "Enter your answer: ",\n  "estimated mark": "estimated mark",\n  "links": "links",\n  "correct solution": "correct solution",\n  "your answer": "your answer",\n  "_correct": "Your answer was considered correct. Type \'n\' to mark it as wrong: ",\n  "_wrong": "Your answer was considered wrong. Type \'n\' to mark it as correct: ",\n  "copyright": "copyright"\n}\n',
        '{\n  "name": "Test",\n  "id": "__iD__",\n  "enabled": false,\n  "size": 3,\n  "author": "Martin Merkli",\n  "copyright": "Public domain",\n  "content": [\n    {\n      "id": ["__iD__", 0],\n      "includes-image": false,\n      "includes-answer-image": false,\n      "question": "1 + 1 = ?",\n      "links": [],\n      "solution": "2",\n      "solutions": ["2"],\n      "tolerance": 1,\n      "difficulty": 1,\n      "frequency": 1.0\n    },\n    {\n      "id": ["__iD__", 1],\n      "includes-image": false,\n      "includes-answer-image": false,\n      "question": "1 + 2 = ?",\n      "links": [],\n      "solution": "3",\n      "solutions": ["3"],\n      "tolerance": 1,\n      "difficulty": 1,\n      "frequency": 1.0\n    },\n    {\n      "id": ["__iD__", 2],\n      "includes-image": false,\n      "includes-answer-image": false,\n      "question": "2 + 2 = ?",\n      "links": [],\n      "solution": "4",\n      "solutions": ["4"],\n      "tolerance": 1,\n      "difficulty": 1,\n      "frequency": 1.0\n    }\n  ]\n}\n'
        ]
    directories = ['Userdata', 'Languages', 'Packages']
    for i in range(len(directories)):
        try:
            os.mkdir(directories[i])
        except FileExistsError:
            pass
    for i in range(min(len(files), len(contents))):
        with open(relative_file(files[i]), 'w') as f:
            f.write(contents[i])
    monitor_time('setup')
    print('setup done')
    sys.exit()


def load_config():
    with open(relative_file('Userdata/config.json')) as f:
        config = json.loads(f.read())
        mark_system = config["mark_system"]
        txt = load_language(config["language"])
    return mark_system, txt

def relative_file(relative_path: str):
    script_dir = os.getcwd()
    absulute_path = os.path.join(script_dir, relative_path)
    return absulute_path

# def load_packages():
#     global packages
#     packages = []
#     package_file_names = os.listdir(relative_file('Packages/'))
#     for package_file_name in package_file_names:
#         if '.lep' in package_file_name:
#             cur_package = ['', []]
#             zip = zipfile.ZipFile(relative_file('Packages/' + package_file_name), 'r')
#             for name in zip.namelist():
#                 if 'init.json' in name:
#                     cur_package[0] = zip.read(name).decode().replace('"__iD__"', str(len(packages)))
#                 elif '.json' in name:
#                     cur_package[1].append(zip.read(name).decode().replace('"__iD__"', str(len(packages))))
#                     packages.append([json.loads(cur_package[0]), []])
#                     for i in cur_package[1]:
#                         packages[-1][1].append(json.loads(i))

def load_packages():
    packages2 = []
    package_file_names = os.listdir(relative_file('Packages/'))
    for package_file_name in package_file_names:
        if '.json' in package_file_name:
            with open(relative_file('Packages/' + package_file_name), 'r') as f:
                p = f.read()
                q = p.replace('"__iD__"', str(len(packages2)))
                r = json.loads(q)
                packages2.append(r)
    return packages2

def list_packages(packages):
    r = []
    for i in range(len(packages)):
        r.append(packages[i]["name"])
    return r

def list_status_packages(packages):
    r = []
    for i in range(len(packages)):
        r.append(packages[i]["enabled"])
    return r

def list_property_packages(property: str, packages):
    r = []
    for i in range(len(packages)):
        r.append(packages[i][property])
    return r

def list_enabled_packages(packages):
    r = []
    for i in range(len(packages)):
        if packages[i]["enabled"]:
            r.append(packages[i]["name"])
    return r

def total_frequency_enabled(packages):
    r = 0.0
    for i in range(len(packages)):
        if packages[i]["enabled"]:
            for j in range(len(packages[i]["content"])):
                r += packages[i]["content"][j]["frequency"]
    return r

def total_frequency_index(n: float, packages):
    s = 0.0
    for i in range(len(packages)):
        if packages[i]["enabled"]:
            for j in range(len(packages[i]["content"])):
                s += packages[i]["content"][j]["frequency"]
                if s >= n:
                    return [i, j]

def randfloat(a: float, b: float):
    return random.random() * (b - a) + a

def fround(n: float, precision: int):
    return round(n * pow(10, precision)) / pow(10, precision)

def get_exercise(packages):
    if len(list_enabled_packages(packages)) > 0:
        total_frequency = total_frequency_enabled(packages)
        coords = total_frequency_index(randfloat(0, total_frequency), packages)
        return packages[coords[0]]["content"][coords[1]]
    else:
        return None

def save_packages(packages):
    for i in range(len(packages)):
        with open(relative_file('Packages/' + packages[i]["name"]) + '.json', 'w') as f:
            f.write(json.dumps(packages[i], indent=4))

def disable_all_packages(packages):
    for i in range(len(packages)):
        packages[i]["enabled"] = False
    save_packages(packages)
    return packages

def enable_all_packages(packages):
    for i in range(len(packages)):
        packages[i]["enabled"] = True
    save_packages(packages)
    return packages

def total_enabled_exercises(packages):
    r = 0
    for i in range(len(packages)):
        if packages[i]["enabled"]:
            for j in range(len(packages[i]["content"])):
                r += 1
    return r

def calculate_mark(mark_system, total_answered_exercises, total_correct_exercises):
    if total_answered_exercises == 0:
        return 0
    elif mark_system == 'CH':
        return fround(((total_correct_exercises / total_answered_exercises) * 5) + 1, 1)
    elif mark_system == 'float':
        return fround(total_correct_exercises / total_answered_exercises, 2)
    elif mark_system == 'percent':
        return fround(total_correct_exercises / total_answered_exercises, 2) * 100
    else:
        return fround(total_correct_exercises / total_answered_exercises, 2)

def calculate_progress(packages, list_answered_exercises, total_answered_exercises):
    if total_enabled_exercises(packages) != 0:
        p1 = len(list_answered_exercises) / total_enabled_exercises(packages) * 100
        p2 = total_answered_exercises / total_enabled_exercises(packages) * 100
        return str(round(p1)) + '%  |  '+ str(round(p2)) + '%'
    else:
        return 0

def increase_frequency(id: list, constant: float, packages):
    packages[id[0]]["content"][id[1]]["frequency"] *= constant
    save_packages(packages)
    return packages

def decrease_frequency(id: list, constant: float, packages):
    packages[id[0]]["content"][id[1]]["frequency"] /= constant
    save_packages(packages)
    return packages

def monitor_answered_exercises(exercise_to_add: list, list_answered_exercises):
    if exercise_to_add in list_answered_exercises:
        pass
    else:
        list_answered_exercises.append(exercise_to_add)
    return list_answered_exercises

def monitor_answers(id: list, answer: str, is_correct: bool, packages):
    to_append = {"package_name": '', "exercise_id": 0, "entered_answer": '', "is_correct": False}
    to_append["package_name"] = packages[id[0]]["name"]
    to_append["exercise_id"] = id[1]
    to_append["entered_answer"] = answer
    to_append["is_correct"] = is_correct
    with open(relative_file('Userdata/stats.json'), 'r') as f:
        answers = json.loads(f.read())
    answers["answers"].append(to_append)
    with open(relative_file('Userdata/stats.json'), 'w') as f:
        f.write(json.dumps(answers, indent=4))

def load_language(language_name: str):
    if os.path.exists(relative_file('Languages/' + language_name + '.json')):
        with open(relative_file('Languages/' + language_name + '.json'), 'r') as f:
            txt = json.loads(f.read())
    else:
        raise Exception('Language file for ' + language_name + ' does not exist.')
    return txt

def enable_package(name: str, packages):
    for i in range(len(packages)):
        if packages[i]["name"] == name:
            packages[i]["enabled"] = True
            save_packages(packages)
    return packages

def disable_package(name: str, packages):
    for i in range(len(packages)):
        if packages[i]["name"] == name:
            packages[i]["enabled"] = False
            save_packages(packages)
    return packages

def monitor_time(action: str):
    with open(relative_file('Userdata/stats.json'), 'r') as f:
        stats = json.loads(f.read())
    stats[action].append(time.time())
    with open(relative_file('Userdata/stats.json'), 'w') as f:
        f.write(json.dumps(stats, indent=4))

def log_system_info():
    info = {}
    info['platform']=platform.system()
    info['platform-release']=platform.release()
    info['platform-version']=platform.version()
    info['architecture']=platform.machine()
    info['processor']=platform.processor()
    info['uname'] = str(os.uname())
    info['learning_software_version'] = '1.0'
    info['python_version'] = str(sys.version_info)
    with open(relative_file('Userdata/config.json'), 'r') as f:
        info['config'] = json.loads(f.read())
    with open(relative_file('Userdata/stats.json'), 'r') as f:
        stats = json.loads(f.read())
    stats['info'] = info
    with open(relative_file('Userdata/stats.json'), 'w') as f:
        f.write(json.dumps(stats, indent=4))
    encrypt_stats()

def set_mark(new: str):
    with open(relative_file('Userdata/config.json'), 'r') as f:
        config = json.loads(f.read())
    config['mark_system'] = new
    mark_system = new
    with open(relative_file('Userdata/config.json'), 'r') as f:
        f.write(json.dumps(stats, indent=4))
    return mark_system

## STAT ENCRYPTION ##

def encrypt_stats():
    with open(relative_file('Userdata/stats.json'), 'rb') as f:
        stats = f.read()
    with open(relative_file('Userdata/stats.json.enc'), 'wb') as f:
        f.write(rsaencrypt(stats))

def xor(x: bytes, y: bytes):
    return bytes([_a ^ _b for _a, _b in zip(x, y)])


def secure_hash(data: bytes, mode: int = 1, length: int = 64):
    hashed = pbkdf2_hmac('sha512', data, sha512(data).digest(), (mode + 10) * 1000, length)
    return hashed


def hashpassword(password: str, minlength: int):
    pbkdf2_hmac_hashed = secure_hash(password.encode(), 4, 1024)
    hashed = pbkdf2_hmac_hashed
    while len(hashed) < minlength:
        hashed += hashed
    return hashed

def rsaencrypt(file: bytes):
    filekey = int(os.urandom(500).hex(), 16)
    key = pow(filekey, int('72a4f9d44a5b5fbd649086ee0e854dcbfb6c7c06939cd9ffa96a50193eb44ea6485af97791a8202e8c03a2b2c1ee2d86ef1946af3f844a8dfb3ce41b8e3fca1a825a3', 16), int('4992948087876777730e30306668e1e0ce27a3c5ae353aa126cd539271ea9638e3a6f00a28bc3aadcbad59b509fa55224dc1af8c5c24bd76f1cf0f9ca7a9572626ddd458d1d85c195f6def32a9c98c39d1bb6ca4dbf119d9e4144c048ac720168f847084a4348b6f0f653a721ca88b2773a0eda37b6fb5888360904367e3db1b42ef12bdd7', 16))
    hashed = hashpassword(str(filekey), len(file))
    normalcipher = xor(file, hashed)
    cipher = b'\x02RSA'
    cipher += bytes([len(str(key).encode()) // 256])
    cipher += bytes([len(str(key).encode()) % 256])
    cipher += str(key).encode()
    cipher += normalcipher
    return cipher

### INTERFACE ###

def print_package_list(packages, txt):
    output = txt["name of package"]
    for i in range(24 - len(output)):
        output += ' '
    output += ' | ' + txt["enabled"] + '\n'
    a = list_packages(packages)
    b = list_status_packages(packages)
    for i in range(len(a)):
        output += a[i]
        for j in range(24 - len(a[i])):
            output += ' '
        output += ' | '
        output += str(b[i])
        output += '\n'
    print(output)

def print_packages_details(packages, txt):
    output = txt["name of package"]
    for i in range(24 - len(output)):
        output += ' '
    output += ' | ' + txt["enabled"]
    for i in range(36 - len(output)):
        output += ' '
    output += ' | ' + txt["size"]
    for i in range(46 - len(output)):
        output += ' '
    output += ' | ' + txt["author"]
    for i in range(64 - len(output)):
        output += ' '
    output += ' | ' + txt["copyright"]
    for i in range(96 - len(output)):
        output += ' '
    output += '\n'
    a = list_packages(packages)
    b = list_status_packages(packages)
    c = list_property_packages('size', packages)
    d = list_property_packages('author', packages)
    e = list_property_packages('copyright', packages)
    for i in range(min(len(a), len(b), len(c), len(d), len(e))):
        print(i)
        tmp_a = a[i]
        tmp_b = b[i]
        tmp_c = c[i]
        tmp_d = d[i]
        tmp_e = e[i]
        output += tmp_a
        for i in range(24 - len(tmp_a)):
            output += ' '
        output += ' | ' + str(tmp_b)
        for i in range(9 - len(str(tmp_b))):
            output += ' '
        output += ' | ' + str(tmp_c)
        for i in range(7 - len(str(tmp_c))):
            output += ' '
        output += ' | ' + tmp_d
        for i in range(15 - len(tmp_d)):
            output += ' '
        output += ' | ' + tmp_e
        for i in range(29 - len(tmp_e)):
            output += ' '
        output += '\n'
    print(output)

def print_enabled_packages(packages, txt):
    output = txt["name of package"] + '\n'
    a = list_enabled_packages(packages)
    for i in range(len(a)):
        tmp_a = a[i]
        output += str(tmp_a) + '\n'
    print(output)

def interpreter(current_input, txt, mark_system, packages):
    if len(current_input) == 0:
        return 'continue', txt, mark_system, packages
    elif current_input[0] == '!':
        command = current_input[1:].split(' ')
        while '' in command:
            del command[command.index('')]
        if command[0].lower() in ['help', 'commands']:
            print(txt["_commands01"])
            print(txt["_commands02"])
            print(txt["_commands03"])
            print(txt["_commands04"])
            print(txt["_commands05"])
            print(txt["_commands06"])
            print(txt["_commands07"])
            print(txt["_commands08"])
            print(txt["_commands09"])
            print(txt["_commands10"])
            print(txt["_commands11"])
            print(txt["_commands12"])
            print(txt["_commands13"])
            print(txt["_commands14"])
            print(txt["_commands15"])
            print(txt["_commands16"])
            return 'stay'
        elif command[0].lower() in ['p']:
            if len(command) < 2:
                print(txt["unknown command"] + ': ' + current_input)
                return 'stay', txt, mark_system, packages
            elif command[1].lower() in ['list']:
                if len(command) < 3:
                    print_package_list(packages, txt)
                    return 'stay', txt, mark_system, packages
                elif command[2] in ['a']:
                    print_packages_details(packages, txt)
                    return 'stay', txt, mark_system, packages
                elif command[2] in ['e']:
                    print_enabled_packages(packages, txt)
                    return 'stay', txt, mark_system, packages
                else:
                    print(txt["unknown command"] + ': ' + current_input)
                    return 'stay', txt, mark_system, packages
            elif command[1].lower() in ['reload']:
                packages = load_packages()
                return 'reload', txt, mark_system, packages
            elif command[1].lower() in ['enable']:
                if len(command) > 2:
                    if command[2] in ['*']:
                        packages = enable_all_packages(packages)
                        return 'reload', txt, mark_system, packages
                    elif command[2] in list_packages(packages):
                        packages = enable_package(command[2], packages)
                        return 'reload', txt, mark_system, packages
                    else:
                        print(txt["unknown command"] + ': ' + current_input)
                        return 'stay', txt, mark_system, packages
                else:
                    print(txt["unknown command"] + ': ' + current_input)
                    return 'stay', txt, mark_system, packages
            elif command[1].lower() in ['disable']:
                if len(command) > 2:
                    if command[2] in ['*']:
                        packages = disable_all_packages(packages)
                        return 'reload', txt, mark_system, packages
                    elif command[2] in list_packages(packages):
                        packages = disable_package(command[2], packages)
                        return 'reload', txt, mark_system, packages
                    else:
                        print(txt["unknown command"] + ': ' + current_input)
                        return 'stay', txt, mark_system, packages
                else:
                    print(txt["unknown command"] + ': ' + current_input)
                    return 'stay', txt, mark_system, packages
            else:
                print(txt["unknown command"] + ': ' + current_input)
                return 'stay', txt, mark_system, packages
        elif command[0].lower() in ['license']:
            print(txt["_license"])
            return 'stay', txt, mark_system, packages
        elif command[0].lower() in ['language']:
            if len(command) > 1:
                if os.path.exists(relative_file('Languages/' + command[1] + '.json')):
                    txt = load_language(command[1])
                    return 'stay', txt, mark_system, packages
                else:
                    print(txt["unknown command"] + ': ' + current_input)
                    return 'stay', txt, mark_system, packages
            else:
                print(txt["unknown command"] + ': ' + current_input)
                return 'stay', txt, mark_system, packages
        elif command[0].lower() in ['quit', 'exit']:
            monitor_time('quit')
            sys.exit(0)
        elif command[0].lower() in ['learn']:
            monitor_time('learn')
            return 'learn', txt, mark_system, packages
        elif command[0].lower() in ['mark']:
            if len(command) > 1:
                if command[1] in ['CH', 'float', 'percentage']:
                    mark_system = set_mark(command[1])
                    return 'stay', txt, mark_system, packages
                else:
                    print(txt["unknown command"] + ': ' + current_input)
                    return 'stay', txt, mark_system, packages
            else:
                print('Avaible: CH, float, percentage; In use: ' + mark_system)
                return 'stay', txt, mark_system, packages
        else:
            print(txt["unknown command"] + ': ' + current_input)
            return 'stay', txt, mark_system, packages
    else:
        return 'continue', txt, mark_system, packages

def check_answer(current_exercise, current_input):
    if current_exercise['tolerance'] in [0, 1]:
        if current_input in current_exercise["solutions"]:
            return True
        else:
            return False
    elif current_exercise['tolerance'] in [2]:
        if current_input in current_exercise["solutions"]:
            return True
        else:
            for i in range(len(current_exercise['solutions'])):
                if current_input.lower().replace(' ', '') == current_exercise['solutions'][i].lower().replace(' ', ''):
                    return True
    elif current_exercise['tolerance'] in [3]:
        return True
    else:
        if current_input in current_exercise["solutions"]:
            return True
        else:
            return False

def set_correct(packages, current_exercise, total_answered_exercises, current_input, total_correct_exercises, list_answered_exercises):
    total_answered_exercises += 1
    total_correct_exercises += 1
    packages = decrease_frequency(current_exercise["id"], 2.0, packages)
    monitor_answers(current_exercise["id"], current_input, True, packages)
    list_answered_exercises = monitor_answered_exercises(current_exercise, list_answered_exercises)
    return packages, total_answered_exercises, list_answered_exercises, total_correct_exercises

def set_wrong(packages, current_exercise, total_answered_exercises, current_input, list_answered_exercises):
    total_answered_exercises += 1
    packages = increase_frequency(current_exercise["id"], 2.0, packages)
    monitor_answers(current_exercise["id"], current_input, False, packages)
    list_answered_exercises = monitor_answered_exercises(current_exercise, list_answered_exercises)
    return packages, total_answered_exercises, list_answered_exercises

def ask_exercise(current_exercise, txt, packages, total_answered_exercises, total_correct_exercises, list_answered_exercises, mark_system):
    current_exercise = get_exercise(packages)
    if current_exercise == None:
        print(txt['_no enabled'])
        return 'goto_menu', packages, total_answered_exercises, total_correct_exercises, list_answered_exercises
    print(txt["progress"] + ': ' + calculate_progress(packages, list_answered_exercises, total_answered_exercises))
    print(txt["estimated mark"] + ': ' +  str(calculate_mark(mark_system, total_answered_exercises, total_correct_exercises)))
    print()
    print(current_exercise["question"])
    if len(current_exercise["links"]) > 0:
        print(txt["links"] + str(current_exercise["links"]))
    print()
    current_input = input(txt["_question"])
    monitor_time('answered_question')
    if current_input in ['!exit']:
        return 'goto_menu', packages, total_answered_exercises, total_correct_exercises, list_answered_exercises
    elif current_input in ['!quit']:
        monitor_time('quit')
        sys.exit(0)
    else:
        print(txt["correct solution"] + ': ' + current_exercise["solution"])
        print()
        print(txt["your answer"] + ': ' + current_input)
        print()
        if check_answer(current_exercise, current_input):
            if input(txt["_correct"]).replace(' ', '').lower() in ['n', 'no', 'w', 'wrong']:
                packages, total_answered_exercises, list_answered_exercises = set_wrong(packages, current_exercise, total_answered_exercises, current_input, list_answered_exercises)
            else:
                packages, total_answered_exercises, list_answered_exercises, total_correct_exercises = set_correct(packages, current_exercise, total_answered_exercises, current_input, total_correct_exercises, list_answered_exercises)
        else:
            if input(txt["_wrong"]).replace(' ', '').lower() in ['n', 'no', 'w', 'wrong', 'c', 'correct']:
                packages, total_answered_exercises, list_answered_exercises, total_correct_exercises = set_correct(packages, current_exercise, total_answered_exercises, current_input, total_correct_exercises, list_answered_exercises)
            else:
                packages, total_answered_exercises, list_answered_exercises = set_wrong(packages, current_exercise, total_answered_exercises, current_input, list_answered_exercises)
    return 'stay', packages, total_answered_exercises, total_correct_exercises, list_answered_exercises

def main():
    if not os.path.exists(relative_file('Userdata/config.json')):
        setup()
    elif not os.path.exists(relative_file('Userdata/stats.json')):
        setup()
    current_exercise = None
    total_answered_exercises = 0
    list_answered_exercises = []
    total_correct_exercises = 0
    current_input = ''
    packages = []
    mark_system = ''
    txt = {}
    packages = load_packages()
    mark_system, txt = load_config()
    monitor_time('startup')
    log_system_info()
    print(txt["_init1"])
    print(txt["_init2"] + '1.0')
    print(txt["_init3"])
    loop = True
    while loop:
        current_input = input(' > ')
        respond, txt, mark_system, packages = interpreter(current_input, txt, mark_system, packages)
        if respond in ['learn']:
            loop2 = True
            while loop2:
                respond2, packages, total_answered_exercises, total_correct_exercises, list_answered_exercises = ask_exercise(current_exercise, txt, packages, total_answered_exercises, total_correct_exercises, list_answered_exercises, mark_system)
                if respond2 in ['goto_menu']:
                    loop2 = False
        elif respond in ['reload']:
            current_exercise = None
            total_answered_exercises = 0
            list_answered_exercises = []
            total_correct_exercises = 0
            current_input = ''
            packages = []
            mark_system = ''
            txt = {}
            packages = load_packages()
            mark_system, txt = load_config()

if __name__ == '__main__':
    main()
