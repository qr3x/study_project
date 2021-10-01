#include <polynomials.h>

using namespace std;


monom::monom(int _coeff, int x, int y, int z)
{
    if (x >= maxPower || y >= maxPower || z >= maxPower)
        throw logic_error("Power is greater than the maximum power");

    P = x * maxPower * maxPower + y * maxPower + z;
    coeff = _coeff;
}

int monom::getX() const
{
    return P / (maxPower * maxPower);
}

int monom::getY() const
{
    int tmpX = P / (maxPower * maxPower);
    return (P - tmpX * maxPower * maxPower) / maxPower;
}

int monom::getZ() const
{
    int tmpX = P / (maxPower * maxPower);
    int tmpY = (P - tmpX * maxPower * maxPower) / maxPower;
    return P - tmpX * maxPower * maxPower - tmpY * maxPower;
}

int monom::getP() const
{
    return P;
}

int monom::getCoeff() const
{
    return coeff;
}

monom& monom::operator=(const monom& p)
{
    coeff = p.coeff;
    P = p.P;
    return *this;
}

bool monom::operator==(const monom& m) const
{
    return P == m.P;
}

bool monom::operator!=(const monom& m) const
{
    return P != m.P;
}

bool monom::operator>(const monom& m) const
{
    return P > m.P;
}

bool monom::operator>=(const monom& m) const
{
    return P >= m.P;
}

bool monom::operator<(const monom& m) const
{
    return P < m.P;
}

bool monom::operator<=(const monom& m) const
{
    return P <= m.P;
}

monom monom::operator*(const int& val)
{
    monom tmp = *this;
    tmp.coeff *= val;
    return tmp;
}

monom& monom::operator*=(const int& val)
{
    coeff *= val;
    return *this;
}

monom monom::operator+(const monom& m) const
{
    if (P != m.P)
        throw logic_error("Different power of monomials");

    monom tmp = *this;
    tmp.coeff += m.coeff;
    return tmp;
}

monom& monom::operator+=(const monom& m)
{
    if (P != m.P)
        throw logic_error("Different power of monomials");

    coeff += m.coeff;
    return *this;
}

monom monom::operator-(const monom& m) const
{
    if (P != m.P)
        throw logic_error("Different power of monomials");

    monom tmp = *this;
    tmp.coeff -= m.coeff;
    return tmp;
}

monom& monom::operator-=(const monom& m)
{
    if (P != m.P)
        throw logic_error("Different power of monomials");

    coeff -= m.coeff;
    return *this;
}

monom monom::operator*(const monom& m) const
{
    if (getX() + m.getX() >= maxPower)
        throw logic_error("The resulting power exceeds the maximum (for x)");
    if (getY() + m.getY() >= maxPower)
        throw logic_error("The resulting power exceeds the maximum (for y)");
    if (getZ() + m.getZ() >= maxPower)
        throw logic_error("The resulting power exceeds the maximum (for z)");

    monom tmp = *this;
    tmp.coeff *= m.coeff;
    tmp.P += m.P;
    return tmp;
}

monom& monom::operator*=(const monom& m)
{
    if (getX() + m.getX() >= maxPower)
        throw logic_error("The resulting power exceeds the maximum (for x)");
    if (getY() + m.getY() >= maxPower)
        throw logic_error("The resulting power exceeds the maximum (for y)");
    if (getZ() + m.getZ() >= maxPower)
        throw logic_error("The resulting power exceeds the maximum (for z)");

    coeff *= m.coeff;
    P += m.P;
    return *this;
}

monom monom::operator-() const
{
    monom tmp(*this);
    tmp.coeff = -tmp.coeff;
    return tmp;
}

ostream& operator<<(ostream& out, const monom& m) 
{
    out << m.getCoeff();
    if (m.getX() != 0)
        out << " * x^" << m.getX();
    if (m.getY() != 0)
        out << " * y^" << m.getY();
    if (m.getZ() != 0)
        out << " * z^" << m.getZ();

    return out;
}


polynom::polynom() 
{
    listMonom = new List<monom>;
    listMonom->add(monom(), -1);
}

polynom::polynom(const polynom& p) 
{
    listMonom = new List<monom>;
    List<monom>* temp = p.listMonom;
    for (int i = 0; i < p.listMonom->getSize(); i++)
    { 
        listMonom->add(p.listMonom->getValue(i), -1);
    }
}

polynom::~polynom() 
{
    delete listMonom;
}

polynom& polynom::operator=(const polynom& p)
{
    listMonom = new List<monom>;
    List<monom>* temp = p.listMonom;
    for (int i = 0; i < p.listMonom->getSize(); i++)
    {
        listMonom->add(p.listMonom->getValue(i), -1);
    }

    return *this;
}

polynom polynom::operator*(const int& val)
{
    if (val != 0)
    {
        polynom tmp(*this);
        for (int i = 0; i < tmp.listMonom->getSize(); i++)
            tmp.listMonom->getValue(i) *= val;

        return tmp;
    }
    else
        return polynom();
}

polynom& polynom::operator*=(const int& val) 
{
    if (val != 0)
    {
        for (int i = 0; i < this->listMonom->getSize(); i++)
            this->listMonom->getValue(i) *= val;

        return *this;
    }
    else
        return polynom();
}

polynom polynom::operator+(const monom& m)
{
    polynom tmp(*this);
    if (m.getCoeff() != 0)
    {
        for (int i = 0; i < tmp.listMonom->getSize(); i++)
        {
            monom mon = tmp.listMonom->getValue(i);
            if (m > mon || i == tmp.listMonom->getSize() - 1)
            {
                tmp.listMonom->add(m, i);
                break;
            }
            else
            {
                tmp.listMonom->getValue(i) += m;
                break;
            }
        }
    }

    return tmp;
}

polynom& polynom::operator+=(const monom& m) 
{
    if (m.getCoeff() != 0)
    {
        for (int i = 0; i < this->listMonom->getSize(); i++)
        {
            monom mon = this->listMonom->getValue(i);
            if (m > mon || i == this->listMonom->getSize() - 1)
            {
                this->listMonom->add(m, i);
                break;
            }
            else
            {
                this->listMonom->getValue(i) += m;
                break;
            }
        }
    }

    return *this;
}

polynom polynom::operator-(const monom& m)
{
    polynom tmp(*this);
    if (m.getCoeff() != 0)
    {
        for (int i = 0; i < tmp.listMonom->getSize(); i++)
        {
            monom mon = tmp.listMonom->getValue(i);
            if (m > mon || i == tmp.listMonom->getSize() - 1)
            {
                tmp.listMonom->add(-m, i);
                break;
            }
            else
            {
                tmp.listMonom->getValue(i) -= m;
                break;
            }
        }
    }

    return tmp;
}

polynom& polynom::operator-=(const monom& m)
{
    if (m.getCoeff() != 0)
    {
        for (int i = 0; i < this->listMonom->getSize(); i++)
        {
            monom mon = this->listMonom->getValue(i);
            if (m > mon || i == this->listMonom->getSize() - 1)
            {
                this->listMonom->add(-m, i);
                break;
            }
            else
            {
                this->listMonom->getValue(i) -= m;
                break;
            }
        }
    }

    return *this;
}

polynom polynom::operator*(const monom& m)
{
    if (m.getCoeff() != 0)
    {
        polynom tmp(*this);
        for (int i = 0; i < tmp.listMonom->getSize(); i++)
            tmp.listMonom->getValue(i) *= m;

        return tmp;
    }
    else
        return polynom();
}

polynom& polynom::operator*=(const monom& m) 
{
    if (m.getCoeff() != 0)
    {
        for (int i = 0; i < this->listMonom->getSize(); i++)
            this->listMonom->getValue(i) *= m;

        return *this;
    }
    else
        return polynom();
}

polynom polynom::operator+(const polynom& m) {
    polynom tmp(*this);

    for (int j = 0; j < m.listMonom->getSize(); j++)
    {
        monom mon2 = m.listMonom->getValue(j);
        if (mon2.getCoeff() != 0)
        {
            for (int i = 0; i < tmp.listMonom->getSize(); i++)
            {
                monom mon1 = tmp.listMonom->getValue(i);
                if (mon2 > mon1 || i == tmp.listMonom->getSize() - 1)
                {
                    tmp.listMonom->add(mon2, i);
                    break;
                }
                else
                {
                    tmp.listMonom->getValue(i) += mon2;
                    break;
                }
            }
        }
    }

    return tmp;
}

polynom& polynom::operator+=(const polynom& m) {
    for (int j = 0; j < m.listMonom->getSize(); j++)
    {
        monom mon2 = m.listMonom->getValue(j);
        if (mon2.getCoeff() != 0)
        {
            for (int i = 0; i < this->listMonom->getSize(); i++)
            {
                monom mon1 = this->listMonom->getValue(i);
                if (mon2 > mon1 || i == this->listMonom->getSize() - 1)
                {
                    this->listMonom->add(mon2, i);
                    break;
                }
                else
                {
                    this->listMonom->getValue(i) += mon2;
                    break;
                }
            }
        }
    }

    return *this;
}

polynom polynom::operator-(const polynom& m) {
    polynom tmp(*this);

    for (int j = 0; j < m.listMonom->getSize(); j++)
    {
        monom mon2 = m.listMonom->getValue(j);
        if (mon2.getCoeff() != 0)
        {
            for (int i = 0; i < tmp.listMonom->getSize(); i++)
            {
                monom mon1 = tmp.listMonom->getValue(i);
                if (mon2 > mon1 || i == tmp.listMonom->getSize() - 1)
                {
                    tmp.listMonom->add(-mon2, i);
                    break;
                }
                else
                {
                    tmp.listMonom->getValue(i) -= mon2;
                    break;
                }
            }
        }
    }

    return tmp;
}

polynom& polynom::operator-=(const polynom& m) {
    for (int j = 0; j < m.listMonom->getSize(); j++)
    {
        monom mon2 = m.listMonom->getValue(j);
        if (mon2.getCoeff() != 0)
        {
            for (int i = 0; i < this->listMonom->getSize(); i++)
            {
                monom mon1 = this->listMonom->getValue(i);
                if (mon2 > mon1 || i == this->listMonom->getSize() - 1)
                {
                    this->listMonom->add(-mon2, i);
                    break;
                }
                else
                {
                    this->listMonom->getValue(i) -= mon2;
                    break;
                }
            }
        }
    }

    return *this;
}

polynom polynom::operator*(const polynom& m) {
    polynom tmp(*this);
    for (int j = 0; j < m.listMonom->getSize(); j++)
    {
        monom mon2 = m.listMonom->getValue(j);

        if (mon2.getCoeff() != 0)
        {
            for (int i = 0; i < tmp.listMonom->getSize(); i++)
                tmp.listMonom->getValue(i) *= mon2;
        }
    }

    return tmp;
}

polynom& polynom::operator*=(const polynom& m) {
    for (int j = 0; j < m.listMonom->getSize(); j++)
    {
        monom mon2 = m.listMonom->getValue(j);

        if (mon2.getCoeff() != 0)
        {
            for (int i = 0; i < this->listMonom->getSize(); i++)
                this->listMonom->getValue(i) *= mon2;
        }
    }

    return *this;
}

ostream& operator<<(ostream& out, const polynom& m) {
    for (int i = 0; i < m.listMonom->getSize(); i++)
    {
        monom mon = m.listMonom->getValue(i);
        if (mon.getCoeff() > 0)
            if (i == 0)
                cout << mon;
            else
                cout << " + " << mon;
        else if (mon.getCoeff() < 0)
            cout << " - " << -mon;
    }

    return out;
}