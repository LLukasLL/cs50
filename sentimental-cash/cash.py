import cs50

while True:
    change_owed = cs50.get_float("Change owed: ")
    if 0 <= change_owed:
        break

coins = 0

while change_owed > 0.245:
    change_owed -= 0.2500
    coins += 1
while change_owed > 0.095:
    change_owed -= 0.1000
    coins += 1
while change_owed > 0.045:
    change_owed -= 0.0500
    coins += 1
while change_owed > 0.005:
    change_owed -= 0.0100
    coins += 1

print(coins)