import csv
from pathlib import Path
import os

E_correct = [0] * 9
E_total = [0] * 9

path = Path(os.getcwd())
path = path.parent.absolute()
path = str(path) + "\\assets\\recognition_logs\\recognition_log.csv"
log = open(path, "r")
log = csv.reader(log)
print("Log file opened, parsing...")

for row in log:
    if row.__len__() < 9:
        continue
    if not row[0].isnumeric():
        continue
    if int(row[0]) not in range(1,7):
        continue

    E_level = int(row[3])
    Is_correct = int(row[8])
    if Is_correct == 1:
        E_correct[E_level-1] += 1
    E_total[E_level-1] += 1

print("Results:")
for i in range(9):
    print("\tE = " + str(i) + " \tRaw correct =" + str(E_correct[i]) + " \tRaw total =" + str(E_total[i]) + " \tPercent Correct = " + str(100 * E_correct[i] / E_total[i])[:5] + "%) correct")
    