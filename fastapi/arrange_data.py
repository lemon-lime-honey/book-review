original = open("./raw_names.txt", "r", encoding="utf-8")
output = open("./names.txt", "w", encoding="utf-8")

name_set = set()

while True:
    ipt = original.readline()
    if not ipt: break
    name_set.add(ipt.strip().lower())

output.write('\n'.join(name_set))

original.close()
output.close()

original = open("./raw_books.txt", "r", encoding="utf-8")
output = open("./book.txt", "w", encoding="utf-8")

ipt = original.readline().split()
name_set = set(ipt)

output.write('\n'.join(name_set))

original.close()
output.close()

original = open("./raw_title.txt", "r", encoding="utf-8")
output = open("./title.txt", "w", encoding="utf-8")

ipt = original.readline().split()
name_set = set(ipt)

output.write('\n'.join(name_set))

output.truncate()

original.close()
output.close()