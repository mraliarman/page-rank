import matplotlib.pyplot as plt
import networkx
graph = {}
damping_factor = 0.85
max_iterations = 100
convergence_threshold = 1e-6

with open('input_graph.txt', 'r') as file:
    for line in file:
        source, target = line.split('->')
        source = source.strip()
        target = target.strip()
        if source not in graph:
            graph[source] = []
        graph[source].append(target)

graph_len = len(graph)
page_rank = {node: 1 / graph_len for node in graph}

for i in range(max_iterations):
    new_page_rank = {node: (1 - damping_factor) / graph_len for node in graph}
    two_node_different = 0
    for node, neighbors in graph.items():
        num_neighbors = len(neighbors)
        if num_neighbors > 0:
            for neighbor in neighbors:
                new_page_rank[neighbor] += damping_factor * page_rank[node] / num_neighbors
                two_node_different += abs(new_page_rank[neighbor] - page_rank[neighbor])
    page_rank = new_page_rank
    if two_node_different < convergence_threshold:
        break

for node in graph:
    print(f"{node}:{page_rank[node]:.3f}")

plt.figure(figsize=(10, 7))
pos = networkx.spring_layout(graph) # type: ignore
networkx.draw_networkx_nodes(graph, pos, node_color='lightgreen', node_size=1900) # type: ignore
networkx.draw_networkx_labels(graph, pos, labels={node: f"{node}\n{page_rank[node]:.3f}" for node in graph}) # type: ignore

for source, targets in graph.items():
    for target in targets:
        plt.annotate("", xy=pos[target], xytext=pos[source], arrowprops=dict(arrowstyle="-|>", alpha=0.5))
plt.show()