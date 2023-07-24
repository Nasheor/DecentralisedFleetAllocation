import math

def divide_and_compute_neighbors(n, k, connections):
    def divide_grid():
        cells_per_community = (n * n) // k
        community_width = math.isqrt(cells_per_community)
        community_height = cells_per_community // community_width

        num_communities_row_col = int(math.sqrt(k))

        communities = []
        for i in range(num_communities_row_col):
            for j in range(num_communities_row_col):
                top_left_x = i * community_width
                top_left_y = j * community_height
                communities.append(((top_left_x, top_left_y), (top_left_x + community_width - 1, top_left_y + community_height - 1)))

        return communities, num_communities_row_col

    def get_neighbors_with_diagonal(communities, num_communities_row_col):
        neighbors = {}

        for i in range(num_communities_row_col):
            for j in range(num_communities_row_col):
                community_index = i * num_communities_row_col + j
                community_neighbors = []

                directions = [
                    (-1, 0),  # North
                    (1, 0),   # South
                    (0, -1),  # West
                    (0, 1),   # East
                    (-1, -1), # North-West
                    (-1, 1),  # North-East
                    (1, -1),  # South-West
                    (1, 1),   # South-East
                ]

                for direction in directions:
                    neighbor_i = i + direction[0]
                    neighbor_j = j + direction[1]

                    if 0 <= neighbor_i < num_communities_row_col and 0 <= neighbor_j < num_communities_row_col:
                        neighbor_index = neighbor_i * num_communities_row_col + neighbor_j
                        community_neighbors.append(neighbor_index+1)

                neighbors[community_index+1] = community_neighbors

        return neighbors

    communities, num_communities_row_col = divide_grid()
    neighbors_diagnol = get_neighbors_with_diagonal(communities, num_communities_row_col)
    total_connections = 0
    computed_neighbors = {}
    if connections <= 500:
        for key in neighbors_diagnol.keys():
            computed_neighbors[key] = []
            neighbors_diagnol[key] = [item for item in neighbors_diagnol[key] if item > key or len(neighbors_diagnol[key]) == 1]
            for item in neighbors_diagnol[key]:
                total_connections += 1
    else:
        for key in neighbors_diagnol.keys():
            for item in neighbors_diagnol[key]:
                total_connections += 1

    connection_count = 0
    sec_id = 1
    while connection_count <= connections:
        if len(neighbors_diagnol[sec_id]) > 1:
            if sec_id not in computed_neighbors.keys():
                computed_neighbors[sec_id] = []
            computed_neighbors[sec_id].append(neighbors_diagnol[sec_id].pop(0))
            connection_count += 1
        if sec_id != len(neighbors_diagnol.keys()):
            sec_id += 1
        else:
            sec_id = 1
    # print(total_connections)
    # print(connection_count)
    return communities, computed_neighbors


if __name__ == '__main__':
    # Testing with a grid size 1000 grid and 256 communities
    grid_size = 1000
    num_communities = 256
    connections = 1600
    communities, neighbors = divide_and_compute_neighbors(grid_size, num_communities, connections)
    print(communities)
    print(neighbors)

