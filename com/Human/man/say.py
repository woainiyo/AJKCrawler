import re
s = "abcabccccaaa"
sum = re.findall("(a(b))", s)
print(sum)