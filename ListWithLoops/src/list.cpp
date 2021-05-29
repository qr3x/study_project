#include "List.h"


List::List(const List& p) {
	Node* node = new Node(p.head->value, p.head->next);
	head = tail = new Node(p.head->value, p.head->next);
	count = 1;

	node = node->next;
	while (node != nullptr) {
		this->add(node);
		node = node->next;
		count++;
	}
}

void List::addVal(int val) {
	Node* node = new Node(val, nullptr);

	if (this->head == nullptr)
		this->head = node;
	else
		this->tail->next = node;
	this->tail = node;
	count++;
}

void List::add(Node* n) {
	if (this->head == nullptr)
		this->head = n;
	else
		this->tail->next = n;
	this->tail = n;
	count++;
}

void List::clear() {
	this->head != nullptr;
}

void List::print() {
	if (this->count == 0)
	{
		cout << "List is empty" << endl;
		return;
	}
	int i = count;
	Node* node = this->head;
	cout << "[ ";
	while ((node != nullptr) && (i > 0)) {
		if (node->next == nullptr) {
			cout << node->value << " ]";
			return;
		}
		cout << node->value << ", ";
		node = node->next;
		i--;
	}
	return;
}

// the first one takes one step, the second two
bool List::isLoop1() {
	if (this->count == 0)
		throw logic_error("List is empty");

	Node* node1 = this->head;
	Node* node2 = this->head->next;
	while (node1 != nullptr) {
		if ((node1->next == nullptr) || (node2->next == nullptr))
			return false;
		if (node2->next->next == nullptr)
			return false;
		if (node1 == node2)
			return true;
		node1 = node1->next;
		node2 = node2->next->next;
	}
}

// the first steps on 1, 2, 3 and etc
bool List::isLoop2() {
	if (this->count == 0)
		throw logic_error("List is empty");

	int step = 1;

	Node* first = head;
	while (true) {
		Node* second = first;
		for (int i = 0; i < step; i++) {
			second = second->next;
			if (second->next == nullptr)
				return false;
		}

		if (first == second)
			return true;

		first = second;

		step++;
	}
}

// changing pointers
bool List::isLoop3() {
	if (head == nullptr)
		return false;
	if (head->next == nullptr)
		return false;

	Node* node = nullptr;
	Node* curr = head;
	Node* next = head->next;
	bool isloop = false;
	while (true) { 
		curr->next = node;
		if (next == nullptr) {
			if (curr == head)
				isloop = true;
			Node* tmp = next;
			next = node;
			node = tmp;
			break;
		}
		node = curr;
		curr = next;
		next = next->next;
	}
	return isloop;
}