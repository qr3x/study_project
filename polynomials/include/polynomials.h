#pragma once
#include <iostream>
#include <cmath>
#include <list.h>


const int maxPower = 21;

struct monom
{
private:
	int coeff;
	int P;
public:
	monom(int _coeff = 0, int x = 0, int y = 0, int z = 0);

	int getX() const;
	int getY() const;
	int getZ() const;
	int getP() const;
	int getCoeff() const;

	monom& operator=(const monom& p);

	bool operator==(const monom& m) const;
	bool operator!=(const monom& m) const;
	bool operator>(const monom& m) const;
	bool operator>=(const monom& m) const;
	bool operator<(const monom& m) const;
	bool operator<=(const monom& m) const;

	monom operator*(const int& val);
	monom& operator*=(const int& val);

	monom operator+(const monom& m) const;
	monom& operator+=(const monom& m);
	monom operator-(const monom& m) const;
	monom& operator-=(const monom& m);
	monom operator*(const monom& m) const;
	monom& operator*=(const monom& m);

	monom operator-() const;

	friend ostream& operator<<(ostream& ostr, const monom& m);
};


class polynom {
private:
	List<monom>* listMonom;
public:
	polynom();
	polynom(const polynom& p);
	~polynom();

	polynom& operator=(const polynom& p);

	polynom operator*(const int& val);
	polynom& operator*=(const int& val);

	polynom operator+(const monom& m);
	polynom& operator+=(const monom& m);
	polynom operator-(const monom& m);
	polynom& operator-=(const monom& m);
	polynom operator*(const monom& m);
	polynom& operator*=(const monom& m);

	polynom operator+(const polynom& m);
	polynom& operator+=(const polynom& m);
	polynom operator-(const polynom& m);
	polynom& operator-=(const polynom& m);
	polynom operator*(const polynom& m);
	polynom& operator*=(const polynom& m);

	friend ostream& operator<<(ostream& ostr, const polynom& m);
};