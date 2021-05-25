import networkx as nx
import matplotlib.pyplot as plt

from bin.input import input_graph
import bin.branching as br


def main():
	graph, no_nodes = input_graph()

	G = nx.DiGraph()
	for i in graph:
		G.add_edge(i[0], i[1], weight=i[2])

	# Plotting
	plt.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.01, wspace=0.05, hspace=0)
	plt.tight_layout()
	options = {
		'node_color': 'cyan',
		'node_size': 150,
		'width': 2,
		'arrowstyle': '-|>',
		'arrowsize': 12,
		#"connectionstyle":'arc3, rad = 0.1'
	}
	pos = nx.spring_layout(G)

	plt.subplot(1, 2, 1)
	nx.draw_networkx(G, pos, arrows=True, **options)
	labels = nx.get_edge_attributes(G, 'weight')
	nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
	plt.plot()	

	B = br.minimum_branching(G)

	plt.subplot(1, 2, 2)
	nx.draw_networkx(B, pos, arrows=True, **options)
	labels = nx.get_edge_attributes(B, 'weight')
	nx.draw_networkx_edge_labels(BlockingIOError, pos, edge_labels=labels)
	plt.plot()	

	plt.show()

if __name__ == '__main__':
	main()