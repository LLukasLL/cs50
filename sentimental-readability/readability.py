import cs50

text = cs50.get_string("Text: ")


letters = 0
for i in text:
    if i.isalpha():
        letters += 1

words = 1
for j in text:
    if j == ' ':
        words += 1

sentences = 0
for k in text:
    if k == '.' or k == '!' or k == '?':
        sentences += 1


L = float(100 * letters / words)
S = float(100 * sentences / words)

# 0.0588 * L - 0.296 * S - 15.8

index = float(0.0588 * L - 0.296 * S - 15.8)

grade = round(index)

if grade < 1:
    print("Before Grade 1")
elif grade > 16:
    print("Grade 16+")
else:
    print("Grade: ", grade)