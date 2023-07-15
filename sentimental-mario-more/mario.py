import cs50

h = -1

while True:
    h = cs50.get_int("Height: ")
    if 0<h<9:
        break


for y in range(0, h):
    for x in range(0, h - y - 1):
        print(" ", end="")
    for x2 in range(0, y + 1):
        print("#", end="")
    print("  ", end="")
    for x3 in range(0, y + 1):
        print("#", end="")
    print("")
