import random
import numpy as np
import matplotlib.pyplot as plt


class People:
    def __init__(self, talent, assets, record, loc):
        self.talent = np.float64(talent)
        self.assets = np.float64(assets)
        self.record = record
        self.loc = loc


def model():
    # Define parameters
    map_size = 201
    num_points = 1000
    num_of_events = 250

    def move_points_randomly(points):
        # Move points randomly in four directions
        directions = np.random.randint(0, 4, size=len(points))
        x_moves = np.where(directions == 2, -1,
                           np.where(directions == 3, 1, 0))
        y_moves = np.where(directions == 0, 1,
                           np.where(directions == 1, -1, 0))
        points[:, 0] = (points[:, 0] + x_moves) % map_size
        points[:, 1] = (points[:, 1] + y_moves) % map_size

    def generate_coordinates(num_points, map_size):
        # Generate random coordinates within the map size
        return np.random.randint(0, map_size, size=(num_points, 2))

    # Generate good and bad things coordinates
    good_things = generate_coordinates(num_of_events, map_size)
    bad_things = generate_coordinates(num_of_events, map_size)

    # Generate talents for each person
    talents = np.clip(np.random.normal(0.6, 0.1, size=num_points), 0.0, 1.0)

    # Create a list of people with their attributes
    people_list = [People(talent, 10, [], coord) for talent, coord in zip(
        talents, generate_coordinates(num_points, map_size))]

    # Simulate events and movements
    for _ in range(80):
        for person in people_list:
            # Check if a person is at a good thing location and event occurs
            good_event_indices = np.where((person.loc == good_things).all(axis=1) & (
                np.random.uniform(0, 100, size=num_of_events) <= person.talent * 100))
            person.assets *= np.power(2, len(good_event_indices[0]))
            person.record.extend([True] * len(good_event_indices[0]))

            # Check if a person is at a bad thing location and decrease assets
            bad_event_indices = np.where(
                (person.loc == bad_things).all(axis=1))
            person.assets /= np.power(2, len(bad_event_indices[0]))
            person.record.extend([False] * len(bad_event_indices[0]))

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
        talents = np.array([person.talent for person in people_list])
        assets = np.array([person.assets for person in people_list])

        max_key = np.argmax(assets)
        min_key = np.argmin(assets)
        aver = np.mean(talents)
        bias.append(talents[max_key] - aver)
        rich_talent.append(talents[max_key])
        poor_talent.append(talents[min_key])

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
    print("bias: ", bias)
    print("average rich talent: ", np.mean(rich_talent))
    print("average poor talent: ", np.mean(poor_talent))


if __name__ == "__main__":
    main()
