#include <gtest.h>

#include <list.h>


TEST(List, can_create_list)
{
	ASSERT_NO_THROW(List<int> list);
}

TEST(List, can_create_list_using_the_copy_constructor)
{
	List<int> list1;

	ASSERT_NO_THROW(List<int> list2(list1));
}

TEST(List, operator_index)
{
	List<int> list1;
	list1.add(10, -1);
	list1.add(20, -1);
	list1.add(30, -1);
	list1.add(40, -1);

	ASSERT_EQ(list1[3], 40);
}

TEST(List, can_get_count)
{
	List<int> list1;
	list1.add(10, -1);
	list1.add(20, -1);
	list1.add(30, -1);
	list1.add(40, -1);

	ASSERT_EQ(list1.getSize(), 4);
}

TEST(List, can_add_value)
{
	List<int> list1;

	ASSERT_NO_THROW(list1.add(10, -1));
}

TEST(List, can_add_from_index__value)
{
	List<int> list1;
	list1.add(10, -1);
	list1.add(20, -1);
	list1.add(30, -1);
	list1.add(40, -1);
	list1.add(200, 2);

	ASSERT_NO_THROW(list1.add(200, 2));
	cout << list1 << endl;
}

TEST(List, can_pop_value)
{
	List<int> list1;
	list1.add(10, -1);
	list1.add(20, -1);
	list1.add(30, -1);
	list1.add(40, -1);
	cout << list1 << endl;
	list1.pop(0);
	list1.pop(1);

	ASSERT_EQ(list1.pop(1), 40);
}

TEST(List, can_pop_last_value)
{
	List<int> list1;
	list1.add(10, -1);
	list1.add(20, -1);
	list1.add(30, -1);
	list1.add(40, -1);

	ASSERT_EQ(list1.pop(), 40);
}

TEST(List, can_find_elem_with_this_elem)
{
	List<int> list1;
	list1.add(10, -1);
	list1.add(20, -1);
	list1.add(30, -1);
	list1.add(40, -1);
	list1.add(20, -1);
	list1.add(50, -1);

	ASSERT_EQ(list1.find(20), 1);
}

TEST(List, can_find_elem_without_this_elem)
{
	List<int> list1;
	list1.add(10, -1);
	list1.add(30, -1);
	list1.add(40, -1);
	list1.add(50, -1);

	ASSERT_EQ(list1.find(20), -1);
}

TEST(List, can_reverse_find_elem_with_this_elem)
{
	List<int> list1;
	list1.add(10, -1);
	list1.add(20, -1);
	list1.add(30, -1);
	list1.add(40, -1);
	list1.add(20, -1);
	list1.add(50, -1);

	ASSERT_EQ(list1.rfind(20), 4);
}

TEST(List, can_reverse_find_elem_without_this_elem)
{
	List<int> list1;
	list1.add(10, -1);
	list1.add(30, -1);
	list1.add(40, -1);
	list1.add(50, -1);

	ASSERT_EQ(list1.rfind(20), -1);
}

TEST(List, can_get_last_elem)
{
	List<int> list1;
	list1.add(10, -1);
	list1.add(30, -1);
	list1.add(40, -1);
	list1.add(50, -1);

	ASSERT_EQ(list1.getLast(), 50);
}

TEST(List, can_clear_list)
{
	List<int> list1;
	list1.add(10, -1);
	list1.add(20, -1);
	list1.add(30, -1);
	list1.add(40, -1);

	ASSERT_NO_THROW(list1.clear());
}

TEST(List, can_print_list)
{
	List<int> list1;
	list1.add(10, -1);
	list1.add(20, -1);
	list1.add(30, -1);
	list1.add(40, -1);

	ASSERT_NO_THROW(cout << list1);
	cout << endl;
}