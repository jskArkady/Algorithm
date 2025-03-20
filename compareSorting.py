import time
import random
import threading


# 🔹 버블 정렬
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]


# 🔹 삽입 정렬
def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key


# 🔹 선택 정렬
def selection_sort(arr):
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]


# 🔹 퀵 정렬
def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)


# 🔹 병합 정렬
def merge_sort(arr):
    if len(arr) > 1:
        mid = len(arr) // 2
        left_half = arr[:mid]
        right_half = arr[mid:]

        merge_sort(left_half)
        merge_sort(right_half)

        i = j = k = 0
        while i < len(left_half) and j < len(right_half):
            if left_half[i] < right_half[j]:
                arr[k] = left_half[i]
                i += 1
            else:
                arr[k] = right_half[j]
                j += 1
            k += 1

        while i < len(left_half):
            arr[k] = left_half[i]
            i += 1
            k += 1

        while j < len(right_half):
            arr[k] = right_half[j]
            j += 1
            k += 1


# 🔹 힙 정렬
def heapify(arr, n, i):
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2

    if left < n and arr[left] > arr[largest]:
        largest = left
    if right < n and arr[right] > arr[largest]:
        largest = right
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, largest)


def heap_sort(arr):
    n = len(arr)
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)
    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        heapify(arr, i, 0)


# 🔹 Tim Sort (파이썬 기본 정렬)
def tim_sort(arr):
    arr.sort()


# 🔹 정렬 실행 및 시간 측정 함수
def timed_sorting(sort_function, data, results, name):
    arr_copy = data[:]  # 원본 데이터 유지
    start_time = time.time()

    if sort_function == quick_sort:
        sorted_arr = sort_function(arr_copy)  # 퀵 정렬은 리스트를 반환
        arr_copy[:] = sorted_arr  # 원본 리스트를 정렬된 리스트로 갱신
    else:
        sort_function(arr_copy)

    end_time = time.time()
    results[name] = end_time - start_time


# 🔹 n 입력값 조정 가능
def compare_sorting_algorithms(n=1000):
    data = [random.randint(1, n) for _ in range(n)]
    sorting_algorithms = {
        "Bubble Sort": bubble_sort,
        "Insertion Sort": insertion_sort,
        "Selection Sort": selection_sort,
        "Quick Sort": quick_sort,
        "Merge Sort": merge_sort,
        "Heap Sort": heap_sort,
        "Tim Sort(default)": tim_sort,
    }

    threads = []
    results = {}

    for name, func in sorting_algorithms.items():
        thread = threading.Thread(
            target=timed_sorting, args=(func, data, results, name)
        )
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    # 🔹 결과 정렬 및 출력
    sorted_results = sorted(results.items(), key=lambda x: x[1])

    # 📌 표 출력 (정렬 속도 비교)
    print("\n📌 정렬 알고리즘 성능 비교")
    print("=" * 40)
    print(f"{'Sorting Algorithm':<20} {'Execution Time (s)':>15}")
    print("=" * 40)
    for name, time_taken in sorted_results:
        print(f"{name:<20} {time_taken:>15.6f}")
    print("=" * 40)
    print("n =", n, "\n")


# 실행 (입력 크기 조정 가능)
compare_sorting_algorithms(n=10000)
