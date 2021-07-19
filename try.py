import sys
ordernumber=sys.argv[1]
tempsb=f"./done/{ordernumber}.done"
print(tempsb)
open(f"./done/{ordernumber}.done", 'w').close()
# print(ordernumber,type(ordernumber))