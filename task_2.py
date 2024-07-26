def binary_search(arr, target):
    """
    Виконує двійковий пошук в відсортованому масиві.
    
    Параметри:
    arr (list of float): Відсортований масив з дробовими числами.
    target (float): Значення, для якого потрібно знайти верхню межу.
    
    Повертає:
    tuple: (кількість ітерацій, верхня межа).
    """
    left, right = 0, len(arr) - 1
    iterations = 0
    upper_bound = None
    
    while left <= right:
        iterations += 1
        mid = left + (right - left) // 2
        
        if arr[mid] == target:
            return (iterations, arr[mid])
        elif arr[mid] < target:
            left = mid + 1
        else:
            upper_bound = arr[mid]
            right = mid - 1
    
    # Якщо ми не знайшли точного значення, повертаємо верхню межу
    if upper_bound is None and left < len(arr):
        upper_bound = arr[left]
        
    return (iterations, upper_bound)

# Приклад використання
sorted_array = [1.2, 2.5, 3.7, 4.8, 6.0, 7.3]
target_value = 5.0
result = binary_search(sorted_array, target_value)
print("Кількість ітерацій:", result[0])
print("Верхня межа:", result[1])
