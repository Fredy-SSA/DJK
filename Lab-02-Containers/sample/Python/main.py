# Initialize the list
weekdays = ["Sunday", "Monday", "Tuesday","Wednesday", "Thursday","Friday", "Saturday"]
print("Seven Weekdays are:\n")
print("--------------------------------")
print(" ")
# Iterate the list using for loop
for day in range(len(weekdays)):
    print(weekdays[day])

print("--------------------------------")

from datetime import date

today = date.today()
print("Today's date:", today)