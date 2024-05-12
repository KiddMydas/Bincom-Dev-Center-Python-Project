#!/usr/bin/python3
import psycopg2
from collections import Counter
import random

# Data representing colors worn by staff each day of the week
staff_colors_data = {
    "Monday": "GREEN, YELLOW, GREEN, BROWN, BLUE, PINK, BLUE, YELLOW, ORANGE, CREAM, ORANGE, RED, WHITE, BLUE, WHITE, BLUE, BLUE, BLUE, GREEN",
    "Tuesday": "ARSH, BROWN, GREEN, BROWN, BLUE, BLUE, BLEW, PINK, PINK, ORANGE, ORANGE, RED, WHITE, BLUE, WHITE, WHITE, BLUE, BLUE, BLUE",
    "Wednesday": "GREEN, YELLOW, GREEN, BROWN, BLUE, PINK, RED, YELLOW, ORANGE, RED, ORANGE, RED, BLUE, BLUE, WHITE, BLUE, BLUE, WHITE, WHITE",
    "Thursday": "BLUE, BLUE, GREEN, WHITE, BLUE, BROWN, PINK, YELLOW, ORANGE, CREAM, ORANGE, RED, WHITE, BLUE, WHITE, BLUE, BLUE, BLUE, GREEN",
    "Friday": "GREEN, WHITE, GREEN, BROWN, BLUE, BLUE, BLACK, WHITE, ORANGE, RED, RED, RED, WHITE, BLUE, WHITE, BLUE, BLUE, BLUE, WHITE"
}


# Modify the generated number based on specified patterns
def modify_binary_number(binary_number):
    if "111" in binary_number:
        return binary_number.replace("111", "001")
    else:
        return "0000"


# Extracting all colors into a single list
all_colors = []


for day_colors in staff_colors_data.values():
    colors_list = day_colors.split(",")
    for color in colors_list:
        all_colors.append(color.strip().upper())

# Counting the occurrences of each color
color_counts = Counter(all_colors)

# Connecting to the PostgreSQL database
conn = psycopg2.connect(
    dbname = input("Database Name: "),
    user = input("Username: "),
    password = input("Password: "),
    host = input("Host: "),
    port = input("Port: ")
)

# Creating a cursor object
cur = conn.cursor()

# 6. Creating a table to store colors and their frequencies if it doesn't exist
cur.execute("""
    CREATE TABLE IF NOT EXISTS color_frequencies (
        color TEXT PRIMARY KEY,
        frequency INTEGER
    )
""")

# Inserting color frequencies in the table
for color, frequency in color_counts.items():
    cur.execute("INSERT INTO color_frequencies (color, frequency) VALUES (%s, %s) ON CONFLICT (color) DO UPDATE SET frequency = EXCLUDED.frequency", (color, frequency))

conn.commit()

# 1. Calculating the mean color
mean_color = max(color_counts, key=color_counts.get)

# 2. Finding the most common color
most_common_color = color_counts.most_common(1)[0][0]

# 3. Finding the median color
sorted_colors = sorted(color_counts)
n = len(sorted_colors)
median_color = sorted_colors[n // 2] if n % 2 != 0 else sorted_colors[n // 2 - 1]

# 4. Calculating the variance of the colors
mean_frequency = sum(color_counts.values()) / len(color_counts)
variance = sum((count - mean_frequency) ** 2 for count in color_counts.values()) / len(color_counts)

# 5. Calculating the probability of choosing red at random
red_frequency = color_counts.get("RED", 0)
total_colors = sum(color_counts.values())
red_probability = red_frequency / total_colors

#######
colors_and_frequencies = dict(color_counts)

# 8. Generating a random 4-digit binary number and converting it to base 10
random_number = "".join(str(random.randint(0, 1)) for _ in range(4))
base_10_number = int(random_number, 2)
modified_number = modify_binary_number(random_number)
base_10_number_mod = int(modified_number, 2)
# 9. Summing the first 50 Fibonacci numbers
fib_sequence = [0, 1]
while len(fib_sequence) < 50:
    fib_sequence.append(fib_sequence[-1] + fib_sequence[-2])
fib_sum = sum(fib_sequence)

# Printing the results
print("1. The average color of shirts worn:", mean_color)
print("2. The color mostly worn throughout the week:", most_common_color)
print("3. The median color worn:", median_color)
print("4. The variation in the colors worn:", variance)
print("5. The likelihood of randomly choosing a red color:", red_probability)
print("6. The colors worn and their frequencies:", colors_and_frequencies)
print("8. A randomly generated 4-digit binary number is:", random_number, ".")
print("   When converted to base 10, it becomes:", base_10_number, ".")
print("   However when adjusted to the pattern it becomes:", modified_number, ".")
print("   Which when converted to base 10, becomes:", base_10_number_mod, ".")
print("9. The sum of the first 50 Fibonacci numbers is:", fib_sum, ".")
print(color_counts)

# Closing the cursor and connection
cur.close()
conn.close()
