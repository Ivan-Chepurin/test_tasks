'''
Task 1:
Дан массив чисел, состоящий из некоторого количества подряд идущих единиц, за которыми следует какое-то количество подряд идущих нулей: 111111111111111111111111100000000.
Найти индекс первого нуля (то есть найти такое место, где заканчиваются единицы, и начинаются нули)

Какова сложность вашего алгоритма?

def task(array):
  pass

print(task("111111111111111111111111100000000"))
# >> OUT: 25...
'''


def task(array):
    """O(log n)"""
    left, right = 0, len(array) - 1
    while right - left > 1:
        middle = (left + right) // 2
        if array[middle] == '1':
            left = middle
        else:
            right = middle

    if array[left] == '0':
        return left
    elif array[right] == '0':
        return right
    else:
        return None


print(task("1111111100000000000"))
