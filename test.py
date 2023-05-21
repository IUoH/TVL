import random
import matplotlib.pyplot as plt

# Generate assets for 1000 people
num_people = 1000
assets = [random.uniform(0, 100) for _ in range(num_people)]

# Plot the histogram
plt.hist(assets, bins=20, edgecolor='black')
plt.xlabel('Assets')
plt.ylabel('Frequency')
plt.title('Distribution of People\'s Assets')

# Display the plot
plt.show()
