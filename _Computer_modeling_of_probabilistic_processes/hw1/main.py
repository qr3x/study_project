import random

"""
Homework №0: print first name, last name and group number
"""
print('----------Task №0----------')

print('Hello python')
print('I\'m Vlad Kishkin, group number №381903-3\n')

"""
Task №1_1: print 10 fibonacci numbers
"""
print('----------Task №1----------')

print('output from array:')
fib = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
for i, element in enumerate(fib):
    print(f'{i}: {element}')

print('\ngenerating fibonacci numbers and displaying them:')
fib1 = 0
fib2 = 1

# catch the error
while True:
    try:
        numbers = int(input('how many numbers to output(min = 2): '))

        if numbers < 2:
            print('you entered a number less than 2. Try again')
        else:
            break
    except ValueError:
        print('you entered not a number. Try again')

print(f'0: {fib1}')
print(f'1: {fib2}')
for i in range(2, numbers):
    fib1, fib2 = fib2, fib1 + fib2
    print(f'{i}: {fib2}')

"""
Task №1_2: work with random
!not explained yet
"""
print('----------Task №2----------')

print('\nrandom.seed(10) and random.random():')
random.seed(10)
print(random.random())

print('\nrandom.uniform(10, 20):')
print(random.uniform(10, 20))

print('\nrandom.randint(10, 20):')
print(random.randint(10, 20))

print('\nrandom.choice([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]):')
print(random.choice([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]))

print('\ngeneration password:')
name = input('Enter your name: ').lower()
surname = input('Enter your surname: ').lower()
numbers = '0123456789'.lower()
password = ''
for i in range(10):
    upper_or_lower = random.randint(0, 1)
    char = random.choice([random.choice(name), random.choice(surname), random.choice(numbers)])
    password += char.lower() if upper_or_lower else char.upper()

print(password)
