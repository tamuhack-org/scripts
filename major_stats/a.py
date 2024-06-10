
sum = 0

with open("majors.txt") as f:
    for line in f:
        num = int(line.strip().split()[-1])
        sum += num

print(sum)

