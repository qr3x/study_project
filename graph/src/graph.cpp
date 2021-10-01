#include "graph.h"


void GraphNode::insertArc(GraphArc* garc) {
	arcs.insert(garc);
	arcsCount++;
}

void GraphNode::deleteArc(GraphArc* garc) {
	arcs.erase(garc);
	arcsCount--;
}


void Graph::insertNode(GraphNode* gnode) {
	nodes.insert(gnode);
	nodeCount++;
}

void Graph::insertArc(GraphArc* garc) {
	arcs.insert(garc);
	arcsCount++;
}

void Graph::deleteNode(GraphNode* gnode) {
	nodes.erase(gnode);
	nodeCount--;
}

void Graph::deleteArc(GraphArc* garc) {
	arcs.erase(garc);
	arcsCount--;
}

Graph Graph::PrimsAlgorithm()
{
	Graph graph;

	set<GraphNode*>::iterator iterNodesThis = this->nodes.begin();
	graph.insertNode(*iterNodesThis);

	int len = this->getNodeCount();
	GraphArc* minArc;
	// walk exactly <len> times
	for (int count = 0; count < len - 1; count++) {
		set<GraphNode*>::iterator iterNodesGraph = graph.nodes.begin();
		int minWight = -1;
		GraphNode* minNode;
		GraphNode* minNodeWithOurNode;
		GraphNode* nowNode;
		// walking through our vertex
		for (int node = 0; node < graph.getNodeCount(); node++, iterNodesGraph++) {
			nowNode = *iterNodesGraph;
			set<GraphArc*>::iterator iterArcsGraph = nowNode->arcs.begin();
			// walking all arcs of the current vertex
			for (int arc = 0; arc < nowNode->getArcCount(); arc++, iterArcsGraph++) {
				// if the same arc, then skip
				set<GraphArc*>::iterator iterArcsTmp = graph.arcs.begin();
				bool next = false;
				for (int i = 0; i < graph.getArcCount(); i++, iterArcsTmp++) {
					// there is already this arc
					if (*iterArcsTmp == *iterArcsGraph) {
						next = true;
						break;
					}
					// there are already these vertex
					set<GraphNode*>::iterator iterNodesTmp = graph.nodes.begin();
					bool next_first = false;
					bool next_second = false;
					for (int j = 0; j < graph.getNodeCount(); j++, iterNodesTmp++) {
						if ((*iterArcsGraph)->getFirst() == *iterNodesTmp)
							next_first = true;
						if ((*iterArcsGraph)->getSecond() == *iterNodesTmp)
							next_second = true;

						if (next_first && next_second) {
							next = true;
							break;
						}
					}
					
					// to exit after checking the vertices
					if (next)
						continue;
				}
				if (next)
					continue;

				// check minWight
				if (((*iterArcsGraph)->getWeight() < minWight) || (minWight == -1)) {
					minWight = (*iterArcsGraph)->getWeight();
					minNode = nowNode;
					minArc = (*iterArcsGraph);
					minNodeWithOurNode = minArc->getFirst();
					if (minNodeWithOurNode == minNode)
						minNodeWithOurNode = minArc->getSecond();
				}
			}
		}
		graph.insertNode(minNodeWithOurNode);
		graph.insertArc(minArc);
	}

	return graph;
}

ostream& operator<<(ostream& out, Graph& g) {
	set<GraphNode*>::iterator iterNodes = g.nodes.begin();
	set<GraphArc*>::iterator iterArcs = g.arcs.begin();

	out << "Nodes: ";
	int lenNodes = g.getNodeCount();
	for (int i = 0; i < lenNodes; i++, iterNodes++) {
		if (i == lenNodes - 1)
			out << (*iterNodes)->getName() << "\n";
		else
			out << (*iterNodes)->getName() << ", ";
	}

	out << "Arcs(weight): ";
	int lenArcs = g.getArcCount();
	for (int i = 0; i < lenArcs; i++, iterArcs++) {
		if (i == lenArcs - 1)
			out << (*iterArcs)->getName() << "(" << (*iterArcs)->getWeight() << ")" << "\n";
		else
			out << (*iterArcs)->getName() << "(" << (*iterArcs)->getWeight() << ")" << ", ";
	}

    return out;
}
