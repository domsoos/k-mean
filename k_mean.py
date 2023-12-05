import math
import random
import matplotlib.pyplot as plt


# Structure to hold each point's coordinates
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

# Calculate the Euclidean distance between two points
def euclidean(p1, p2):
    return math.sqrt((p2.x - p1.x)**2 + (p2.y - p1.y)**2)

# Read the points from the data file
def read_points_from_file(file_path):
    points = []
    with open(file_path, 'r') as file:
        for line in file:
            point = line.split()
            x = float(point[0])
            y = float(point[1])
            points.append(Point(x, y))
    return points

# Function to implement the K-means algorithm
def k_means(points, k=3, max_iterations=10, tolerance=0.001):
    centroids = random.sample(points, k) # random points to initialize
    sse_per_iteration = []
    cluster_history = []

    for iteration in range(max_iterations):
        clusters = [[] for _ in range(k)]
        for point in points:
            distances = [euclidean(point, centroid) for centroid in centroids]
            closest_centroid_index = distances.index(min(distances))
            clusters[closest_centroid_index].append(point)

        # calculate sum of squares
        sse = sum(sum(euclidean(point, centroids[i])**2 for point in cluster) for i, cluster in enumerate(clusters))
        sse_per_iteration.append(sse)
        cluster_history.append(clusters)

        # calculate new centroids
        new_centroids = []
        for i, cluster in enumerate(clusters):
            if len(cluster) == 0:  # If a cluster is empty, re-initialize its centroid
                new_centroids.append(random.choice(points))
                continue
            x_coords = [p.x for p in cluster]
            y_coords = [p.y for p in cluster]
            new_centroids.append(Point(sum(x_coords) / len(cluster), sum(y_coords) / len(cluster)))

        # check for convergence
        if all(euclidean(new_centroids[i], centroids[i]) < tolerance for i in range(k)):
            break

        centroids = new_centroids

    return cluster_history, centroids, sse_per_iteration


# Merged functions to handle multiple runs and plotting
def run_k_means_multiple_times(points, k, num_runs=10):
    best_sse = float('inf')
    best_clusters = None
    best_centroids = None
    
    for run in range(num_runs):
        cluster_history, centroids, sse_per_iteration = k_means(points, k)
        if sse_per_iteration[-1] < best_sse:
            best_sse = sse_per_iteration[-1]
            best_clusters = cluster_history
            best_centroids = centroids
    
    return best_clusters, best_centroids, best_sse

# Function to plot each SSE for each k
def plot_each_k(all_sse_histories, k_values):
    average_sses = [sum(all_sse_histories[k]) / len(all_sse_histories[k]) for k in k_values]
    
    plt.figure(figsize=(10, 6))
    plt.plot(k_values, average_sses, marker='o')
    plt.title("K-Means for each K")
    plt.xlabel("Number of Clusters, k")
    plt.ylabel("Average Sum of Squared Errors (SSE)")
    plt.show()

# Function to plot clusters for each k at each iteration
def plot_all_clusters(all_cluster_histories, k_values, attempt):
    if len(k_values) < 2:
        for iteration in range(len(all_cluster_histories)):
            plt.figure(figsize=(6, 4))
            for cluster in all_cluster_histories[iteration]:
                plt.scatter([p.x for p in cluster], [p.y for p in cluster])
            plt.title(f"{attempt} attempt clusters for k={k_values[0]} at Iteration {iteration + 1}/{len(all_cluster_histories)}")
            plt.xlabel("X-coordinate")
            plt.ylabel("Y-coordinate")
            plt.show()
        return
    else:
        for k in k_values:
            for iteration in range(len(all_cluster_histories[k])):
                plt.figure(figsize=(6, 4))
                for cluster in all_cluster_histories[k][iteration]:
                    plt.scatter([p.x for p in cluster], [p.y for p in cluster])
                plt.title(f"Clusters for k={k} at Iteration {iteration + 1}")
                plt.xlabel("X-coordinate")
                plt.ylabel("Y-coordinate")
                plt.show()

def plot_sse_for_k(sse_per_iteration, k, attempt):
    plt.figure()
    plt.plot(sse_per_iteration, marker='o')
    plt.title(f"{attempt} attempt Convergence Curve for k={k}")
    plt.xlabel("Number of iterations")
    plt.ylabel("Sum of Squared Errors (SSE)")
    plt.grid(True)
    plt.show()

# Main execution
if __name__ == '__main__':
	points = read_points_from_file('A.txt')
	k_values = range(2, 11)  # K values from 2 to 10
	all_sse_histories = {k: [] for k in k_values}
	all_cluster_histories = {}

	for k in k_values:
		cluster_history, _, best_sse = run_k_means_multiple_times(points, k, num_runs=2)
		all_sse_histories[k].append(best_sse)
		all_cluster_histories[k] = cluster_history

	attempts = ["1st", "2nd", "3rd"]
	k=3
	for attempt in attempts:	
		cluster_history_k3, centroids_k3, sse_per_iteration_k3 = k_means(points, k)
		plot_sse_for_k(sse_per_iteration_k3, k, attempt)
		plot_all_clusters(cluster_history_k3, [3], attempt)
	plot_each_k(all_sse_histories, k_values)
	# The user can also choose to plot all cluster histories
	#plot_all_clusters(all_cluster_histories, k_values)
