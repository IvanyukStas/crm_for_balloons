from datetime import datetime


a = '20.10.2020'
b = datetime.strptime(a, "%d.%m.%Y")
print(b)