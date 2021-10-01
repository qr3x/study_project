#pragma once

#include <iostream>

using namespace std;


class Node
{
public:
	int value;
	Node* next;

	Node(int _value = 0, Node* _next = nullptr) {
		value = _value;
		next = _next;
	}

	Node operator = (const Node& N) {
		value = N.value;
		next = N.next;
	}
};


class List {
private:
	int count;

	Node* head;
	Node* tail;
public:
	List(Node* head_ = nullptr, Node* tail_ = nullptr) :head(head_), tail(tail_) {
		count = 2;

		if (tail == nullptr) 
			count--;
		if (head == nullptr) 
			count--;
	}
	~List() { this->clear(); }
	List(const List& p);

	void addVal(int val);
	void add(Node* n);

	bool isLoop1();
	bool isLoop2();
	bool isLoop3();

	void clear();

	void print();
};