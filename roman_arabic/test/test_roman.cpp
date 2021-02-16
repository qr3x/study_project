#include <gtest.h>
#include "roman.h"


// init тесты
TEST(test_roman, init_without_param)
{
    ASSERT_NO_THROW(roman rom);
}

TEST(test_roman, init_with_char_param)
{
    ASSERT_NO_THROW(roman rom('V'));
    roman rom('V');
    EXPECT_EQ("V", rom.value);
}

TEST(test_roman, init_with_string_param)
{
    ASSERT_NO_THROW(roman rom("IV"));
}

TEST(test_arabic, init_without_param)
{
    ASSERT_NO_THROW(arabic arab);
}

TEST(test_arabic, init_with_param)
{
    ASSERT_NO_THROW(arabic arab(5));
}

// “есты на правильность перевода из арабских чисел в римские 
TEST(test_converter__arabic_to_roman, test_1)
{
    Convertor con;
    arabic arab(1);
    roman rom = con.toRoman(arab);
    EXPECT_EQ("I", rom.value);
}

TEST(test_converter__arabic_to_roman, test_4)
{
    Convertor con;
    arabic arab(4);
    roman rom = con.toRoman(arab);
    EXPECT_EQ("IV", rom.value);
}

TEST(test_converter__arabic_to_roman, test_5)
{
    Convertor con;
    arabic arab(5);
    roman rom = con.toRoman(arab);
    EXPECT_EQ("V", rom.value);
}

TEST(test_converter__arabic_to_roman, test_9)
{
    Convertor con;
    arabic arab(9);
    roman rom = con.toRoman(arab);
    EXPECT_EQ("IX", rom.value);
}

TEST(test_converter__arabic_to_roman, test_10)
{
    Convertor con;
    arabic arab(10);
    roman rom = con.toRoman(arab);
    EXPECT_EQ("X", rom.value);
}

TEST(test_converter__arabic_to_roman, test_87)
{
    Convertor con;
    arabic arab(87);
    roman rom = con.toRoman(arab);
    EXPECT_EQ("LXXXVII", rom.value);
}

TEST(test_converter__arabic_to_roman, test_249)
{
    Convertor con;
    arabic arab(249);
    roman rom = con.toRoman(arab);
    EXPECT_EQ("CCXLIX", rom.value);
}

TEST(test_converter__arabic_to_roman, test_500)
{
    Convertor con;
    arabic arab(500);
    roman rom = con.toRoman(arab);
    EXPECT_EQ("D", rom.value);
}

TEST(test_converter__arabic_to_roman, test_783)
{
    Convertor con;
    arabic arab(783);
    roman rom = con.toRoman(arab);
    EXPECT_EQ("DCCLXXXIII", rom.value);
}

TEST(test_convertor__roman_to_arabic, test_1_to_3999)
{
    /* ѕроверка дл€ чисел от 1 до 3999 (Ќа все доступные числа с I, V, X, L, C, D, M):
    ѕереводим арабское число в римское (уже проверили работу этого перевода)
    «атем это римское число переводим обратно в арабское и свер€ем их */

    Convertor con;
    arabic arab;
    roman rom;

    for (int i = 1; i <= 3999; i++)
    {
        rom.value = con.toRoman(i).value;
        arab.value = con.toArabic(rom).value;
        EXPECT_EQ(i, arab.value);
    }
}
