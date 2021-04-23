#include "tree.h"


Tree::Tree()
{
	this->head = nullptr;
}

Tree::Tree(string str)
{
	this->head = nullptr;

	string temp("");
	string ch;
	int len = str.length();
	for (int i = 0; i < len; i++)
	{
		ch = str[i];
		if (i != len - 1)
			if (ch == " ")
			{
				this->addWord(temp);
				temp = "";
			}
			else
				temp += ch;
		else
		{
			temp += ch;
			this->addWord(temp);
		}
	}
}

void Tree::addWord(string str)
{
	if (this->head == nullptr)
	{
		this->head = new Node<string>(str);
		return;
	}
	Node<string>* node = this->head;
	Node<string>* node_child;
	while (true)
	{
		if (node->value < str)
		{
			node_child = node->right;
			if (node_child == nullptr)
			{
				node->right = new Node<string>(str);
				break;
			}
			node = node_child;
		}
		else if (node->value > str)
		{
			node_child = node->left;
			if (node_child == nullptr)
			{
				node->left = new Node<string>(str);
				break;
			}
			node = node_child;
		}
		else
		{
			node->addCount();
			break;
		}
	}
}

int Tree::getCount(string str)
{
	Node<string>* node = this->head;
	while (node->value != str)
		if (node->value < str)
		{
			node = node->right;
			if (node == nullptr)
				return 0;
		}
		else
		{
			node = node->left;
			if (node == nullptr)
				return 0;
		}

	return node->count;
}
