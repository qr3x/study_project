#pragma once
#include <iostream>

using namespace std;


template <typename T>
class List
{
private:
    class Node
    {
    public:
        T value;    // çíà÷åíèå ýëåìåíòà
        Node* next; // ñëåäóþùèé ýëåìåíò
        Node(T value, Node* next)
        {
            this->value = value;
            this->next = next;
        }
    };
    Node* head;       // âåðõíèé ýëåìåíò ñïècêà
    Node* tail;       // íèæíèé ýëåìåíò ñïèñêà
    static int Count; // êîëè÷åñòâî ýëåìåíòîâ ñïèñêà

public:
    List();                         // êîíñòðóêòîð
    ~List();                        // äåñòðóêòîð
    List(const List& list);         // êîíñòðóêòîð êîïèðîâàíèå

    T& operator[](const int index); // îïåðàòîð èíäåêñàöèè

    int GetCount();                 // êîëè÷åñòâî ýëåìåíòîâ
    void Add(T value);              // äîáàâëåíèå ýëåìåíòà (â êîíåö ñïèñêà)
    void Delete(int index);         // óäàëåíèå ýëåìåíòà ïî èíäåêñó
    void Clear();                   // î÷èñòêà ñïèñêà

    void Print();                   // âûâîä ýëåìåíòîâ íà ýêðàí
};

template <typename T>
int List<T>::Count = 0;


template<typename T>
List<T>::List()
{
    this->head = NULL;
    this->tail = NULL;
}

template <typename T>
List<T>::~List()
{
    this->Clear();
}

template <typename T>
List<T>::List(const List& list)
{
    Node* node = list.head;
    while (node != NULL) {
        this->Add(node->value);
        node = node->next;
    }
}

template <typename T>
void List<T>::Add(T value)
{
    Node* node = new Node(value, NULL);
    if (this->head == NULL)
        this->head = node;
    else
        this->tail->next = node;
    this->tail = node;
    this->Count++;
}

template <typename T>
void List<T>::Delete(int index)
{
    if (index >= this->Count)
        throw logic_error("Index out of the range");
    else
    {
        if (index == 0)
        {
            this->head = this->head->next;
        }
        else
        {
            int counter = 0;
            Node* node = this->head;
            while (counter++ != index - 1)
                node = node->next;

            if (node->next != NULL)
                node->next = node->next->next;

            this->Count--;
        }
    }
}

template <typename T>
void List<T>::Clear()
{
    if (this->head != NULL)
    {
        Node* node = this->head;
        Node* next;
        while (node != NULL)
        {
            next = node->next;
            delete node;
            node = next;
        }
        this->head = NULL;
    }
    Count = 0;
}

template <typename T>
T& List<T>::operator[](const int index)
{
    if (index >= this->Count)
        throw logic_error("Index out of the range");
    else
    {
        int counter = 0;
        Node* node = this->head;
        while (counter++ != index)
            node = node->next;

        return node->value;
    }
}

template <typename T>
void List<T>::Print()
{
    if (this->Count == 0)
    {
        cout << "List is empty" << endl;
        return;
    }

    Node* node = this->head;
    cout << "[";
    while (node != NULL)
    {
        if (node->next == NULL)
        {
            cout << node->value << "]" << endl;
            return;
        }
        cout << node->value << ", ";
        node = node->next;
    }
}

template <typename T>
int List<T>::GetCount()
{
    return this->Count;
}
