def cocktail_sort(arr):
    n = len(arr)
    if n == 0:
        return

    swapped = True
    start = 0
    end = n - 1

    while swapped:
        swapped = False

        for i in range(start, end):
            if arr[i] > arr[i + 1]:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
                swapped = True

        if not swapped:
            break

        swapped = False
        end -= 1

        for i in range(end - 1, start - 1, -1):
            if arr[i] > arr[i + 1]:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
                swapped = True

        start += 1


def strand_sort(arr):
    def merge_lists(a, b):
        result = []
        i = j = 0
        while i < len(a) and j < len(b):
            if a[i] < b[j]:
                result.append(a[i])
                i += 1
            else:
                result.append(b[j])
                j += 1
        result.extend(a[i:])
        result.extend(b[j:])
        return result

    if len(arr) <= 1:
        return arr.copy()

    strand = [arr[0]]
    remaining = []

    for i in range(1, len(arr)):
        if not (arr[i] < strand[-1]):  # Изменено с >= на not <
            strand.append(arr[i])
        else:
            remaining.append(arr[i])

    return merge_lists(strand, strand_sort(remaining))


class Student:
    def __init__(self, name, score):
        self.name = name
        self.score = score

    def __lt__(self, other):
        return self.score < other.score

    def __le__(self, other):
        return self.score <= other.score

    def __gt__(self, other):
        return self.score > other.score

    def __ge__(self, other):
        return self.score >= other.score

    def __eq__(self, other):
        if not isinstance(other, Student):
            return False
        return self.score == other.score and self.name == other.name

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return f"Student('{self.name}', {self.score})"


def demonstrate_sorting():
    print("=" * 50)
    print("ДЕМОНСТРАЦИЯ РАБОТЫ АЛГОРИТМОВ СОРТИРОВКИ")
    print("=" * 50)

    print("\n1. Сортировка целых чисел (Cocktail Sort):")
    numbers = [64, 34, 25, 12, 22, 11, 90, 5]
    print(f"До сортировки:    {numbers}")
    numbers_copy = numbers.copy()
    cocktail_sort(numbers_copy)
    print(f"После сортировки: {numbers_copy}")

    print("\n2. Сортировка строк (Strand Sort):")
    words = ["banana", "apple", "cherry", "date", "blueberry"]
    print(f"До сортировки:    {words}")
    sorted_words = strand_sort(words)
    print(f"После сортировки: {sorted_words}")

    print("\n3. Сортировка студентов по оценкам:")
    students = [
        Student("Анна", 85),
        Student("Иван", 72),
        Student("Мария", 95),
        Student("Петр", 68),
        Student("Ольга", 91)
    ]

    print("До сортировки:")
    for student in students:
        print(f"  {student}")

    students_copy = students.copy()
    cocktail_sort(students_copy)

    print("\nПосле Cocktail Sort:")
    for student in students_copy:
        print(f"  {student}")

    students_sorted = strand_sort(students)

    print("\nПосле Strand Sort:")
    for student in students_sorted:
        print(f"  {student}")


def test_edge_cases():
    print("\n" + "=" * 50)
    print("ТЕСТИРОВАНИЕ КРАЙНИХ СЛУЧАЕВ")
    print("=" * 50)

    empty_arr = []
    cocktail_sort(empty_arr)
    print(f"Пустой массив: {empty_arr}")

    single_arr = [42]
    cocktail_sort(single_arr)
    print(f"Один элемент: {single_arr}")

    sorted_arr = [1, 2, 3, 4, 5]
    cocktail_sort(sorted_arr)
    print(f"Уже отсортированный: {sorted_arr}")

    reverse_arr = [5, 4, 3, 2, 1]
    cocktail_sort(reverse_arr)
    print(f"Обратный порядок: {reverse_arr}")


if __name__ == "__main__":
    demonstrate_sorting()
    test_edge_cases()
    print("\n" + "=" * 50)
    print("ВСЕ ТЕСТЫ ЗАВЕРШЕНЫ!")
    print("=" * 50)