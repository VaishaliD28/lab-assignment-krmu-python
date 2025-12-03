import pandas as pd
print("Pandas working!")
import numpy as np


# Task 1: Load Data
df = pd.read_csv("weather.csv")
print(df.head())
print(df.info())
print(df.describe())

# Task 2: Cleaning
df['Date'] = pd.to_datetime(df['Date'])
df = df[['Date', 'Temperature', 'Rainfall', 'Humidity']]
df = df.dropna()

# Task 3: NumPy Statistics
print("Mean Temperature:", np.mean(df['Temperature']))
print("Min Temperature:",  np.min(df['Temperature']))
print("Max Temperature:",  np.max(df['Temperature']))
print("Std Temperature:",  np.std(df['Temperature']))

# Task 4: Simple Plots
plt.plot(df['Date'], df['Temperature'])
plt.title("Daily Temperature Trend")
plt.savefig("temp_line.png")
plt.show()

df.groupby(df['Date'].dt.month)['Rainfall'].sum().plot(kind='bar', title="Monthly Rainfall")
plt.savefig("rainfall_bar.png")
plt.show()

plt.scatter(df['Temperature'], df['Humidity'])
plt.title("Humidity vs Temperature")
plt.savefig("scatter.png")
plt.show()

# Task 5: Grouping
monthly = df.groupby(df['Date'].dt.month).mean()
print("Monthly Averages:\n", monthly)

# Task 6: Export
df.to_csv("cleaned_weather.csv", index=False)
print("Assignment Complete!")
