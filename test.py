from datetime import datetime
print(datetime.today().date())
print(datetime.today().date())
print(datetime.today().date())
print(datetime.today().date())


a = '20.10.2020'
b = datetime.strptime(a, "%d.%m.%Y")
print(b)