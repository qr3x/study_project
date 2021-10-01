#pragma once

#include<iostream>

using namespace std;


template<class T>
class Node
{
public:
	T value;
	Node<T>* next;
	Node<T>* prev;
	Node(T value = (T)0, Node<T>* next = nullptr, Node<T>* prev = nullptr) : value(value), next(next), prev(prev) {};
};


template<class T>
class List
{
private:
	Node<T>* head;
	Node<T>* tail;
	int count;
public:
	List();
	List(const List& list);
	~List();

	List& operator=(const List& p);
	T& operator[](const int index);
	T& getValue(const int index);

	int getSize() { return count; };                 // get list's count
	void add(const T& value, int index);             // add elem in tail to position
	T pop(int index);                                // del elem by index (and return him)
	T pop();                                         // del last elem (and return him)
	int find(const T& t);                            // find elem in list
	int rfind(const T& t);                           // reverse find elem in list
	const T getLast();

	bool isEmpty() { return (head == nullptr); };    // check if it is empty

	void clear();

	friend ostream& operator<<(ostream& out, const List& list)
	{
		if (list.count == 0)
		{
			out << "List()" << endl;
			return out;
		}

		Node<T>* node = list.head;
		out << "List(";
		while (node != nullptr)
		{
			if (node->next == list.tail)
			{
				out << node->value << ")";
				return out;
			}
			out << node->value << ", ";
			node = node->next;
		}
	}
};

template<class T>
List<T>::List()
{
	this->head = nullptr;
	this->tail = nullptr;
	this->count = 0;
}

template<class T>
List<T>::List(const List& list)
{
	Node<T>* node = list.head;
	if (node == nullptr)
	{
		this->head = nullptr;
		this->tail = nullptr;
		this->count = 0;
		return;
	}

	while (node != nullptr)
	{
		this->add(node->value, -1);
		node = node->next;
		if (node == nullptr)
			this->tail = node;
	}
	this->count = list.count;
}

template <typename T>
List<T>::~List()
{
	this->clear();
}

template <typename T>
void List<T>::add(const T& value, int index)
{
	/*
		add element to end to position
	*/
	if (index == -1)
	{
		Node<T>* node = new Node<T>(value);
		if (this->isEmpty())
		{
			this->head = node;
			this->tail = node;

			this->head->next = this->tail;
			this->head->prev = this->tail;

			this->tail->next = this->head;
			this->tail->prev = this->head;
		}
		else
		{
			Node<T>* temp = this->tail;

			this->tail->next = node;
			this->tail = node;

			this->tail->prev = temp;
			this->tail->next = this->head;
			this->head->prev = this->tail;
		}
	}
	else
	{
		if (index >= this->count)
			throw logic_error("index >= list's size");

		Node<T>* node = new Node<T>(value);
		if (index == 0)
		{
			Node<T>* oldHead = this->head;
			this->head = node;
			this->head->next = oldHead;
			this->head->prev = this->tail;
			oldHead->prev = this->head;
			this->tail->next = this->head;

			this->count++;

			return;
		}

		int counter = 0;
		Node<T>* temp_node = this->head;
		Node<T>* prev;
		while (counter != index)
		{
			prev = temp_node;
			temp_node = temp_node->next;
			counter++;
		}

		prev->next = node;
		node->prev = prev;
		node->next = temp_node;
		temp_node->prev = node;
	}

	this->count++;
}

template <typename T>
T List<T>::pop(int index)
{
	/*
		return deleted element
		begin with 0 (as operator[])
	*/
	if (index >= this->count)
		throw logic_error("List: Index out of the range");
	else
	{
		T val;
		if (index == 0)
		{
			val = this->head->value;
			this->head = this->head->next;
			this->head->prev = this->tail;
			this->tail->next = this->head;

			this->count--;

			return val;
		}
		int counter = 0;
		Node<T>* node = this->head;
		Node<T>* prev;
		while (counter != index)
		{
			prev = node;
			node = node->next;
			counter++;
		}

		val = node->value;
		Node<T>* temp = node->next;
		delete node;
		node = temp;
		prev->next = node;
		node->prev = prev;

		this->count--;

		return val;
	}
}

template <typename T>
T List<T>::pop()
{
	/*
		return deleted last element
	*/

	return (this->pop(this->count - 1));
}

template<class T>
int List<T>::find(const T& t)
{
	/*
		find elem in list
	*/
	Node<T>* node = this->head;

	for (int i = 0; i < count; i++)
	{
		if (t == node->value)
			return i;

		node = node->next;
	}

	return -1;
}

template<class T>
int List<T>::rfind(const T& t)
{
	/*
		reverse find elem in list
	*/
	Node<T>* node = this->head;
	int index = -1;
	for (int i = 0; i < count; i++)
	{
		if (t == node->value)
			index = i;

		node = node->next;
	}

	return index;
}

template<class T>
const T List<T>::getLast()
{
	/*
		get last value
	*/
	return (this->tail->value);
}

template <typename T>
void List<T>::clear()
{
	/*
		delete all elements
	*/
	if (this->head != nullptr)
	{
		Node<T>* node = this->head;
		Node<T>* next;
		this->tail = nullptr;
		for (int i = 0; i < this->count; i++)
		{
			next = node->next;
			delete node;
			node = next;
		}
		this->head = nullptr;
	}
	this->count = 0;
}

template<class T>
List<T>& List<T>::operator=(const List<T>& p)
{
	Node<T>* node = list.head;
	if (node == nullptr)
	{
		this->head = nullptr;
		this->tail = nullptr;
		this->count = 0;
		return;
	}

	while (node != nullptr)
	{
		this->add(node->value);
		node = node->next;
		if (node == nullptr)
			this->tail = node;
	}
	this->count = list.count;
	return *this;
}

template <typename T>
T& List<T>::operator[](const int index)
{
	if (index >= this->count)
		throw logic_error("List: Index out of the range");
	else
	{
		int counter = 0;
		Node<T>* node = this->head;
		while (counter != index)
		{
			node = node->next;
			counter++;
		}

		return node->value;
	}
}

template<class T>
inline T& List<T>::getValue(const int index)
{
	if (index >= this->count)
		throw logic_error("List: Index out of the range");
	else
	{
		int counter = 0;
		Node<T>* node = this->head;
		while (counter != index)
		{
			node = node->next;
			counter++;
		}

		return node->value;
	}
}
