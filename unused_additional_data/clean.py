
clean = dict()
with open('female.txt') as f:
    lines = f.readlines()
    for l in lines:
        l = l[7:].strip('[ \n ]')
        l = l.replace("'", '').replace('"','').split(', ')
        clean[l[0]] = l[1:]
    print(clean)
    