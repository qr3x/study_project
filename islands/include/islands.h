#include <iostream>

using namespace std;


const int MAX_SIZE_VECTOR = 100;


template <class ValType>
class Vector {
private:
	ValType* pVector;
	int size;
public:
	Vector(int s = 10);
	Vector(const Vector& v);
	~Vector();

	int getSize() { return size; };
	ValType& operator[](int index);

	friend ostream& operator<<(ostream& out, const Vector& v)
	{
		out << "[";
		for (int i = 0; i < v.size; i++)
			if (i != v.size - 1)
				out << v.pVector[i] << ", ";
		out << "]";
		return out;
	}
};


template <class ValType>
Vector<ValType>::Vector(int s)
{
	if (s < 0 || s > MAX_SIZE_VECTOR)
		throw logic_error("vector size <= 0 or > MAX_SIZE");

	size = s;
	pVector = new ValType[size];
	for (int i = 0; i < size; i++)
		pVector[i] = (ValType)0;
}

template <class ValType>
Vector<ValType>::Vector(const Vector& v)
{
	size = v.size;
	pVector = new ValType[size];
	for (int i = 0; i < size; i++)
		pVector[i] = v.pVector[i];
}

template <class ValType>
Vector<ValType>::~Vector()
{
	delete[] pVector;
	size = 0;
}

template <class ValType>
ValType& Vector<ValType>::operator[](int index)
{
	if (index < 0 || index >= MAX_SIZE_VECTOR)
		throw logic_error("vector index < 0 or >= MAX_SIZE");

	return pVector[index];
}

template <class ValType>
class Matrix : public Vector<Vector<ValType> > {
public:
	Matrix(int s);

	void addPointIsland(int row, int col)
	{
		pVector[row][col] = -1;
	}

	int getCountIslands();

	friend ostream& operator<<(ostream& out, Matrix& mt)
	{
		out << "[ ";
		for (int i = 0; i < mt.getSize(); i++)
			if (i != mt.getSize() - 1)
				out << mt[i] << "," << endl;
			else
				out << mt[i] << endl;
		out << " ]";

		return out;
	}
};


template <class ValType>
Matrix<ValType>::Matrix(int s) : Vector<Vector<ValType> >(s)
{
	if (s <= 0 || s > MAX_SIZE_VECTOR)
		throw logic_error("matrix size <=0 or > MAX_SIZE");

	for (int i = 0; i < s; i++)
	{
		Vector<ValType> temp(s);
		this->operator[](i) = temp;
	}
		
}

template<class ValType>
inline int Matrix<ValType>::getCountIslands()
{
	
}
