#include <iostream>
#include "graph.h"


using namespace std;


int main()
{
    // creating the vertices of the graph
    GraphNode* a = new GraphNode("A");
    GraphNode* b = new GraphNode("B");
    GraphNode* c = new GraphNode("C");
    GraphNode* d = new GraphNode("D");
    GraphNode* e = new GraphNode("E");
    GraphNode* f = new GraphNode("F");
    GraphNode* g = new GraphNode("G");

    // create graph arcs
    // for A node
    GraphArc* ab = new GraphArc(7, a, b);
    GraphArc* ad = new GraphArc(5, a, d);

    // for B node
    GraphArc* bc = new GraphArc(8, b, c);
    GraphArc* bd = new GraphArc(9, b, d);
    GraphArc* be = new GraphArc(7, b, e);

    // for C node
    GraphArc* ce = new GraphArc(5, c, e);

    // for D node
    GraphArc* de = new GraphArc(15, d, e);
    GraphArc* df = new GraphArc(6, d, f);

    // for E node
    GraphArc* ef = new GraphArc(8, e, f);
    GraphArc* eg = new GraphArc(9, e, g);

    // for F node
    GraphArc* fg = new GraphArc(11, f, g);

    Graph graph;
    // add all vertices and arcs to our graph
    graph.insertNode(a);
    graph.insertNode(b);
    graph.insertNode(c);
    graph.insertNode(d);
    graph.insertNode(e);
    graph.insertNode(f);
    graph.insertNode(g);

    graph.insertArc(ab);
    graph.insertArc(ad);
    graph.insertArc(bc);
    graph.insertArc(bd);
    graph.insertArc(be);
    graph.insertArc(ce);
    graph.insertArc(de);
    graph.insertArc(df);
    graph.insertArc(ef);
    graph.insertArc(eg);
    graph.insertArc(fg);


    cout << "Our graph:\n" << graph << endl << endl;
    cout << "Minimal spanning tree as a graph(Prim's algorithm):\n" << graph.PrimsAlgorithm() << endl;


    return 0;
}
