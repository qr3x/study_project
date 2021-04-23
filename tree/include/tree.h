#pragma once 
#include <iostream>
#include <string>

using namespace std;


template <class T>
struct Node{
	T value;
	Node<T>* right;
	Node<T>* left;
	int count;

	Node(T value, Node<T>* right = nullptr, Node<T>* left = nullptr) : value(value), right(right), left(left), count(1) {};
	void addCount()
	{
		count++;
	}
};


class Tree 
{
private:
	Node<string>* head;
public:
	Tree();
	Tree(string str);

	void addWord(string str);
	int getCount(string str);
};