#pragma once
# include <iostream>>

using namespace std;


template <typename T>
class List
{
private:
    class Node
    {
    public:
        T value;    // значение элемента
        Node* next; // следующий элемент
        Node(T value, Node* next)
        {
            this->value = value;
            this->next = next;
        }
    };
    Node* head;       // верхний элемент спиcка
    Node* tail;       // нижний элемент списка
    static int Count; // количество элементов списка

public:
    List();                         // конструктор
    ~List();                        // деструктор
    List(const List& list);         // конструктор копирование

    T& operator[](const int index); // оператор индексации

    int GetCount();                 // количество элементов
    void Add(T value);              // добавление элемента (в конец списка)
    void Delete(int index);         // удаление элемента по индексу
    void Clear();                   // очистка списка

    void Print();                   // вывод элементов на экран
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

//template <typename T>
//void List<T>::Delete(int index)
//{
//    if (index >= this->Count)
//        throw logic_error("Index out of the range");
//    else
//    {
//        Node* temp_node;
//        if (index == 0)
//        {
//            temp_node = this->head;
//            this->head = this->head->next;
//        }
//        else
//        {
//            int counter = 0;
//            Node* node = this->head;
//            while (counter++ != index - 1)
//                node = node->next;
//            temp_node = node->next;
//            if (node->next != NULL)
//                node->next = node->next->next;
//            this->Count--;
//        }
//        delete temp_node;
//    }
//}

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
        //if (index == Count - 1)
        //    return this->tail->value;

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