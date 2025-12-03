#Title- DAILY CALORIE TRACKER
#Name- Vaishali Doonga
#Date- 06-11-2025


import datetime
print("Welcome to the Daily Calorie Tracker!")
print("This tool helps you track your daily meals and calories, calculate totals and averages, and compare against your daily limit.")

meals = []
calories = []

num_meals = int(input("How many meals do you want to enter? "))

for i in range(num_meals):
    meal_name = input(f"Enter meal name for meal {i+1}: ")
    meal_calories = float(input(f"Enter calorie amount for {meal_name}: "))
    meals.append(meal_name)
    calories.append(meal_calories)

total_calories = sum(calories)
average_calories = total_calories / num_meals if num_meals > 0 else 0

daily_limit = float(input("Enter your daily calorie limit: "))


if total_calories > daily_limit:
    status_message = f"Warning: You have exceeded your daily calorie limit by {total_calories - daily_limit:.2f} calories."
else:
    status_message = "Great! You are within your daily calorie limit."

print(status_message)


print("\nMeal Name\t\tCalories")
print("--------------------------------")
for meal, cal in zip(meals, calories):
    print(f"{meal}\t\t\t{cal}")
print(f"Total:\t\t\t{total_calories}")
print(f"Average:\t\t\t{average_calories}")


save_option = input("Do you want to save this session to a file? (yes/no): ").lower()
if save_option == "yes":
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    filename = "calorie_session_log.txt"
    with open(filename, "w") as file:
        file.write(f"Session Timestamp: {timestamp}\n")
        file.write("Meal Details:\n")
        for meal, cal in zip(meals, calories):
            file.write(f"- {meal}: {cal} calories\n")
        file.write(f"Total Calories: {total_calories}\n")
        file.write(f"Average Calories per Meal: {average_calories}\n")
        file.write(f"Daily Limit: {daily_limit}\n")
        file.write(f"Status: {status_message}\n")
    print(f"Session saved to {filename}")
else:
    print("Session not saved.")
