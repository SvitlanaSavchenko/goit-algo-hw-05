import timeit
from collections import defaultdict

# Реалізація алгоритмів пошуку підрядка

# Алгоритм Боєра-Мура
def boyer_moore(text, pattern):
    def preprocess(pattern):
        bad_char = defaultdict(lambda: -1)
        for i, char in enumerate(pattern):
            bad_char[char] = i
        return bad_char
    
    m, n = len(pattern), len(text)
    bad_char = preprocess(pattern)
    
    s = 0
    while s <= n - m:
        j = m - 1
        while j >= 0 and pattern[j] == text[s + j]:
            j -= 1
        if j < 0:
            return s
        s += max(1, j - bad_char[text[s + j]])
    return -1

# Алгоритм Кнута-Морріса-Пратта
def kmp_search(text, pattern):
    def compute_lps(pattern):
        lps = [0] * len(pattern)
        length = 0
        i = 1
        while i < len(pattern):
            if pattern[i] == pattern[length]:
                length += 1
                lps[i] = length
                i += 1
            else:
                if length != 0:
                    length = lps[length - 1]
                else:
                    lps[i] = 0
                    i += 1
        return lps
    
    lps = compute_lps(pattern)
    i = j = 0
    while i < len(text):
        if pattern[j] == text[i]:
            i += 1
            j += 1
        
        if j == len(pattern):
            return i - j
        elif i < len(text) and pattern[j] != text[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    return -1

# Алгоритм Рабіна-Карпа
def rabin_karp(text, pattern):
    def hash_value(s, end):
        h = 0
        for i in range(end):
            h = (h * base + ord(s[i])) % prime
        return h
    
    def rehash(old_hash, old_char, new_char, pattern_len):
        new_hash = (old_hash - ord(old_char) * base**(pattern_len - 1)) * base
        new_hash = (new_hash + ord(new_char)) % prime
        return new_hash
    
    if len(pattern) > len(text):
        return -1
    
    base = 256
    prime = 101
    
    pattern_hash = hash_value(pattern, len(pattern))
    text_hash = hash_value(text, len(pattern))
    
    for i in range(len(text) - len(pattern) + 1):
        if pattern_hash == text_hash and text[i:i + len(pattern)] == pattern:
            return i
        
        if i < len(text) - len(pattern):
            text_hash = rehash(text_hash, text[i], text[i + len(pattern)], len(pattern))
    
    return -1

# Функції для тестування і вимірювання часу

def test_algorithms(text, pattern_existing, pattern_nonexisting):
    # Підрядок, що існує
    def run_boyer_moore_existing():
        return boyer_moore(text, pattern_existing)
    
    def run_kmp_existing():
        return kmp_search(text, pattern_existing)
    
    def run_rabin_karp_existing():
        return rabin_karp(text, pattern_existing)
    
    # Підрядок, що не існує
    def run_boyer_moore_nonexisting():
        return boyer_moore(text, pattern_nonexisting)
    
    def run_kmp_nonexisting():
        return kmp_search(text, pattern_nonexisting)
    
    def run_rabin_karp_nonexisting():
        return rabin_karp(text, pattern_nonexisting)
    
    # Вимірювання часу
    time_boyer_moore_existing = timeit.timeit(run_boyer_moore_existing, number=100)
    time_kmp_existing = timeit.timeit(run_kmp_existing, number=100)
    time_rabin_karp_existing = timeit.timeit(run_rabin_karp_existing, number=100)
    
    time_boyer_moore_nonexisting = timeit.timeit(run_boyer_moore_nonexisting, number=100)
    time_kmp_nonexisting = timeit.timeit(run_kmp_nonexisting, number=100)
    time_rabin_karp_nonexisting = timeit.timeit(run_rabin_karp_nonexisting, number=100)
    
    return {
        'existing': {
            'Boyer-Moore': time_boyer_moore_existing,
            'KMP': time_kmp_existing,
            'Rabin-Karp': time_rabin_karp_existing
        },
        'nonexisting': {
            'Boyer-Moore': time_boyer_moore_nonexisting,
            'KMP': time_kmp_nonexisting,
            'Rabin-Karp': time_rabin_karp_nonexisting
        }
    }

# Основна частина програми

if __name__ == "__main__":
    # Читання текстів
    with open("article1.txt", "r", encoding="utf-8") as f1:
        text_1 = f1.read()
    
    with open("article2.txt", "r", encoding="utf-8") as f2:
        text_2 = f2.read()

    # Підрядки для тестування
    pattern_existing = "example"  # замініть на підрядок, який дійсно існує в текстах
    pattern_nonexisting = "nonexistentpattern"  # замініть на вигаданий підрядок

    # Тестування для статті 1
    results_1 = test_algorithms(text_1, pattern_existing, pattern_nonexisting)
    
    # Тестування для статті 2
    results_2 = test_algorithms(text_2, pattern_existing, pattern_nonexisting)
    
    # Виведення результатів
    print("Результати для статті 1:")
    print("Підрядок, що існує:")
    for algo, time in results_1['existing'].items():
        print(f"{algo}: {time:.6f} секунд")
    print("Підрядок, що не існує:")
    for algo, time in results_1['nonexisting'].items():
        print(f"{algo}: {time:.6f} секунд")
    
    print("\nРезультати для статті 2:")
    print("Підрядок, що існує:")
    for algo, time in results_2['existing'].items():
        print(f"{algo}: {time:.6f} секунд")
    print("Підрядок, що не існує:")
    for algo, time in results_2['nonexisting'].items():
        print(f"{algo}: {time:.6f} секунд")
