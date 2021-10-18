filename = input('file name: ')
with open(filename, 'r') as f:
    file = f.readlines()
def switch(x):
    n = ''
    for i in range(len(x)):
        if not x[i] == '\n':
            n += x[i]
    y = n.split(';')
    if y[0][0] == ' ':
        y[0] = y[0][1:]
    z = y[1] + ';' + y[0]
    m = ''
    return z
output = [''] * len(file)
for i in range(len(file)):
    output[i] = switch(file[i])
for i in range(len(output)):
    print(output[i])
