with open('/Users/joshs/Desktop/geniza_stuff/Chapter_1.md') as f:
    doc = f.read()

for x in range(100,0,-1):
    footnote_num = ("." + str(x))
    doc = doc.replace(footnote_num, ".")
with open("/Users/joshs/Desktop/geniza_stuff/Chapter_1_edited.txt", "w") as text_file:
    text_file.write(doc)