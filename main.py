import random
import matplotlib.pyplot as plt
import numpy as np

map_size = 201
num_points = 1000
num_of_events = 250


class Person:
    def __init__(self, talent, loc):
        self.talent = max(min(talent, 1.0), 0.0)
        self.assets = 10.0
        self.record = []
        self.loc = loc

    def __str__(self):
        return f"Talent: {self.talent}, Assets: {self.assets}"

    def update_assets(self, event_occurred):
        if event_occurred:
            self.assets *= 2
        else:
            self.assets /= 2


def move_points_randomly(points):
    for i in range(len(points)):
        x, y = points[i]
        dx, dy = random.choice([(0, 1), (0, -1), (-1, 0), (1, 0)])
        new_x = (x + dx) % map_size
        new_y = (y + dy) % map_size
        points[i] = (new_x, new_y)


def generate_points(num_points):
    return [(random.randint(0, map_size - 1), random.randint(0, map_size - 1)) for _ in range(num_points)]


def event_occurred(talent):
    probability = talent * 100
    return random.uniform(0, 100) <= probability


good_things = generate_points(num_of_events)
bad_things = generate_points(num_of_events)

people_list = [Person(random.gauss(0.6, 0.1), loc)
               for loc in generate_points(num_points)]

for _ in range(80):
    for person in people_list:
        for event in good_things:
            if person.loc == event:
                person.update_assets(event_occurred(person.talent))
        for event in bad_things:
            if person.loc == event:
                person.update_assets(False)
    move_points_randomly(good_things)
    move_points_randomly(bad_things)

assets = [person.assets for person in people_list]
total_assets = sum(assets)
top20_assets = sum(sorted(assets, reverse=True)[:200])
ratio = top20_assets / total_assets

print(f"Minimum Assets: {min(people_list, key=lambda p: p.assets)}")
print(f"Maximum Assets: {max(people_list, key=lambda p: p.assets)}")
print(f"Top 20 Assets Ratio: {ratio}")

fig, (ax1, ax2) = plt.subplots(nrows=2, figsize=(10, 8))
fig.suptitle('Distribution of People\'s Assets', fontsize=16)

# Histogram plot
ax1.hist(assets, bins='auto', edgecolor='black')
# ax1.set_xscale('log')
ax1.set_yscale('log')
ax1.set_xlabel('Assets')
ax1.set_ylabel('Frequency')

# Scatter plot of people's locations
x_coords, y_coords = zip(*[person.loc for person in people_list])
ax2.scatter(x_coords, y_coords, marker='.', color='black')
ax2.set_xlim(0, map_size - 1)
ax2.set_ylim(0, map_size - 1)
ax2.set_aspect('equal')
ax2.set_xlabel('X Coordinate')
ax2.set_ylabel('Y Coordinate')

plt.tight_layout()
plt.show()
