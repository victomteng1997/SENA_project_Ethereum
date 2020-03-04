f = open('test.html','r')
content = f.readlines()

f.close()
print(content)
final = content[0].split('\\n')
f = open('new_test.html','w')
f.writelines(final)
f.close()

