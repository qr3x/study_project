#include <gtest.h>

#include <polynomials.h>


TEST(monom, can_create_monom)
{
	ASSERT_NO_THROW(monom mon);
}

TEST(monom, can_create_monom_with_params)
{
	ASSERT_NO_THROW(monom mon(10, 1, 2, 3));
}

TEST(monom, can_create_monom_with_params_with_degree_power_20)
{
	ASSERT_ANY_THROW(monom mon(10, 21, 2, 3));
}

TEST(monom, can_getX)
{
	monom mon(10, 19);
	ASSERT_EQ(mon.getX(), 19);
}

TEST(monom, can_getY)
{
	monom mon(10, 1, 3);
	ASSERT_EQ(mon.getY(), 3);
}

TEST(monom, can_getZ)
{
	monom mon(10, 19, 1, 2);
	ASSERT_EQ(mon.getZ(), 2);
}

TEST(monom, can_getCoeff)
{
	monom mon(10, 19);
	ASSERT_EQ(mon.getCoeff(), 10);
}

TEST(monom, can_appropriation_monom)
{
	monom mon1(10, 1, 2, 3);
	monom mon2(1);
	mon2 = mon1;
	monom* p1 = &mon1;
	monom* p2 = &mon2;

	ASSERT_EQ(mon1.getCoeff(), mon2.getCoeff());
	ASSERT_EQ(mon1.getP(), mon2.getP());
	ASSERT_EQ(mon1.getX(), mon2.getX());
	ASSERT_EQ(mon1.getY(), mon2.getY());
	ASSERT_EQ(mon1.getZ(), mon2.getZ());
	ASSERT_NE(p1, p2);
}






TEST(polynom, can_create_polynom)
{
	ASSERT_NO_THROW(polynom pol);
}

TEST(polynom, can_copy_polynom)
{
	polynom pol1;
	polynom pol2(pol1);
	polynom* p1 = &pol1;
	polynom* p2 = &pol2;
	ASSERT_NE(p1, p2);
}

TEST(polynom, can_appropriation)
{	
	polynom pol1;
	polynom pol2;
	pol2 = pol1;

	polynom* p1 = &pol1;
	polynom* p2 = &pol2;
	ASSERT_NE(p1, p2);
}

TEST(polynom, can_appropriation_polynom)
{
	polynom pol1;
	polynom pol2;
	pol2 = pol1;

	polynom* p1 = &pol1;
	polynom* p2 = &pol2;
	ASSERT_NE(p1, p2);
}
