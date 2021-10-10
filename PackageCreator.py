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

### API ###

def create_package(name, content, author):
    package = {}
    package['name'] = name
    package['id'] = "__iD__"
    package['enabled'] = False
    pacakge['author'] = author
    package['copyright'] = "Public domain"
    package['content'] = []
    for i in range(len(content)):
        exercise = {}
        exercise['id'] = ["__iD__", int(i)]
        exercise['includes-image'] = False
        exercise['includes-answer-image'] = False
        exercise['question'] = content[i]['question']
        exercise['links'] = []
        exercise['solution'] = content[i]['solution']
        exercise['solutions'] = [str(content[i]['solutions'])]
        exercise['tolerance'] = 2
        exercise['difficulty'] = 1
        exercise['frequency'] = 1.0
        package['content'].append(exercise)
    return package

def load_from_file(name):
    content = []
    with open(name + '.txt', 'r') as f:
        lines = f.readlines()
        for i in range(len(lines)):
            if lines[i] in ['', ' ']:
                pass
            else:
                exercise = {}
                exercise['question'] = lines[i].spit(';')[0]
                exercise['solution'] = lines[i].spit(';')[1]
                content.append(exercise)
    return content

### INTERFACE ###

def file_to_package():
    name = input('name: ')
    author = 'Martin Merkli'
    package = create_package(name, load_from_file(name), author)
    with open(name + '.json', 'w') as f:
        f.write(json.dumps(package))

if __name__ == '__main__':
    file_to_package()
