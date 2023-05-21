import random
import matplotlib.pyplot as plt


class People:
    def __init__(self, talent, assets, record, loc):
        self.talent = float(talent)
        self.assets = float(assets)
        self.record = record
        self.loc = loc


def model():
    # Define parameters
    map_size = 201
    num_points = 1000
    num_of_events = 250

    def move_points_randomly(points):
        # Move points randomly in four directions
        for i in range(len(points)):
            x, y = points[i]
            direction = random.randint(0, 3)
            if direction == 0:
                x, y = x, y + 1
            elif direction == 1:
                x, y = x, y - 1
            elif direction == 2:
                x, y = x - 1, y
            else:
                x, y = x + 1, y
            x = x % map_size  # Wrap around if coordinates go beyond map size
            y = y % map_size
            points[i] = (x, y)

    def generate_coordinates(num_points, map_size):
        # Generate random coordinates within the map size
        return [(random.randint(0, map_size), random.randint(0, map_size))
                for _ in range(num_points)]

    def event_occurred(talent):
        # Determine if an event occurs based on talent level
        probability = talent * 100
        return random.uniform(0, 100) <= probability

    # Generate good and bad things coordinates
    good_things = generate_coordinates(num_of_events, map_size)
    bad_things = generate_coordinates(num_of_events, map_size)

    # Generate all possible coordinates on the map
    all_coordinates = [(x, y) for x in range(map_size)
                       for y in range(map_size)]
    random.shuffle(all_coordinates)
    random_points = all_coordinates[:num_points]

    # Generate talents for each person
    talents = [max(min(random.normalvariate(0.6, 0.1), 1.0), 0.0)
               for _ in range(num_points)]

    # Create a list of people with their attributes
    people_list = [People(talent, 10, [], coord)
                   for talent, coord in zip(talents, random_points)]

    # Simulate events and movements
    for _ in range(80):
        for person in people_list:
            for point in good_things:
                # Check if a person is at a good thing location and event occurs
                if person.loc == point and event_occurred(person.talent):
                    person.assets *= 2
                    person.record.append(True)
            for point in bad_things:
                # Check if a person is at a bad thing location and decrease assets
                if person.loc == point:
                    person.assets /= 2
                    person.record.append(False)
        move_points_randomly(good_things)
        move_points_randomly(bad_things)

    return people_list


def main():
    rich_talent = []
    poor_talent = []
    bias = []
    run_times = 100

    for _ in range(run_times):
        people_list = model()
        max_key = max(range(len(people_list)),
                      key=lambda i: people_list[i].assets)
        min_key = min(range(len(people_list)),
                      key=lambda i: people_list[i].assets)
        aver = sum([person.talent for person in people_list])/1000
        bias.append(people_list[max_key].talent - aver)
        rich_talent.append(people_list[max_key].talent)
        poor_talent.append(people_list[min_key].talent)

    num_bins = 20
    plt.hist(rich_talent, bins=num_bins, alpha=0.5, label='Rich')
    plt.hist(poor_talent, bins=num_bins, alpha=0.5, label='Poor')
    plt.xlabel('Value')
    plt.ylabel('Frequency')
    plt.title('Data Distribution')
    plt.legend()
    plt.show()

    # Print results
    print("rich talent: ", rich_talent)
    print("poor talent: ", poor_talent)
    for i in bias:
        print(i)
    print("average rich talent: ", sum(rich_talent) / run_times)
    print("average poor talent: ", sum(poor_talent) / run_times)


if __name__ == "__main__":
    main()
