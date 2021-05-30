#include <iostream>
#include <set>

using namespace std;


class GraphArc;


class GraphNode {
private:
	string name;
	int arcsCount;
public:
	set<GraphArc*> arcs;

	GraphNode() : name(""), arcsCount(0) {};
	GraphNode(string name_) : name(name_), arcsCount(0) {};

	void insertArc(GraphArc* garc);
	void deleteArc(GraphArc* garc);

	string getName() { return name; };
	int getArcCount() { return arcsCount; };
};


class GraphArc {
private:
	string name;
	int weight;
	GraphNode* first,* second;
public:
	GraphArc() : name(""), weight(-1), first(nullptr), second(nullptr) {};
	GraphArc(int weight_, GraphNode* first_, GraphNode* second_) : name(first_->getName() + second_->getName()), weight(weight_), first(first_), second(second_) {
		first_->insertArc(this);
		second_->insertArc(this);
	};

	string getName() { return name; };
	int getWeight() { return weight; };

	GraphNode* getFirst() { return first; };
	GraphNode* getSecond() { return second; };
};


class Graph {
private:
	int nodeCount;
	int arcsCount;
public:
	set<GraphNode*> nodes;
	set<GraphArc*> arcs;

	Graph() {
		nodeCount = 0;
		arcsCount = 0;
	}

	int getNodeCount() { return nodeCount; };
	int getArcCount() { return arcsCount; };

	void insertNode(GraphNode* gnode);
	void insertArc(GraphArc* garc);

	void deleteNode(GraphNode* gnode);
	void deleteArc(GraphArc* garc);

	Graph PrimsAlgorithm();  // Minimum spanning tree

	friend ostream& operator<<(ostream& ostr, Graph& g);
};
