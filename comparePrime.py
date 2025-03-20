import threading
import time
import random

def is_prime_basic(number):
    """기본 소수 판별 함수"""
    if number < 2:
        return False
    if number == 2:
        return True
    if number % 2 == 0:
        return False
    
    i = 3
    while i * i <= number:
        if number % i == 0:
            return False
        i += 2
    
    return True

def is_prime_optimized(number):
    """6k ± 1 최적화를 사용한 소수 판별 함수"""
    if number <= 1:
        return False
    if number <= 3:
        return True
    if number % 2 == 0 or number % 3 == 0:
        return False
    
    i = 5
    while i * i <= number:
        if number % i == 0 or number % (i + 2) == 0:
            return False
        i += 6
    
    return True

def is_prime_miller_rabin(n, k=5):
    """밀러-라빈 소수 판별법"""
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0:
        return False
    
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2
    
    for _ in range(k):
        a = random.randint(2, n - 2)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    
    return True

def benchmark_algorithm(algo_func, test_numbers, algo_name, results):
    """알고리즘 벤치마크 함수"""
    start_time = time.time()
    
    # 소수 개수 카운트 초기화
    prime_count = 0
    
    # 각 숫자마다 소수 여부 확인
    for num in test_numbers:
        if algo_func(num):
            prime_count += 1
    
    end_time = time.time()
    execution_time = end_time - start_time
    
    # 결과 저장
    results[algo_name] = {
        'time': execution_time,
        'prime_count': prime_count
    }
    
    print(f"{algo_name} 완료: {execution_time:.4f}초, 소수 개수: {prime_count}")

def run_benchmark(test_range=None, num_tests=10000):
    """벤치마크 실행 함수"""
    if test_range is None:
        # 기본 테스트 범위: 작은 수, 중간 수, 큰 수
        test_numbers = (
            [random.randint(2, 1000) for _ in range(num_tests // 3)] +
            [random.randint(1000, 100000) for _ in range(num_tests // 3)] +
            [random.randint(100000, 10000000) for _ in range(num_tests // 3)]
        )
    else:
        # 사용자 지정 범위
        min_val, max_val = test_range
        test_numbers = [random.randint(min_val, max_val) for _ in range(num_tests)]
    
    print(f"테스트 수: {len(test_numbers)}개")
    print(f"범위: {min(test_numbers)}에서 {max(test_numbers)}까지")
    
    # 결과를 저장할 딕셔너리
    results = {}
    
    # 쓰레드 생성
    threads = [
        threading.Thread(
            target=benchmark_algorithm, 
            args=(is_prime_basic, test_numbers, "Basic Algorithm", results)
        ),
        threading.Thread(
            target=benchmark_algorithm, 
            args=(is_prime_optimized, test_numbers, "6k±1 Optimized", results)
        ),
        threading.Thread(
            target=benchmark_algorithm, 
            args=(is_prime_miller_rabin, test_numbers, "Miller-Rabin", results)
        )
    ]
    
    print("벤치마크 시작...")
    
    # 쓰레드 시작
    for thread in threads:
        thread.start()
    
    # 모든 쓰레드가 완료될 때까지 대기
    for thread in threads:
        thread.join()
    
    # 가장 빠른 알고리즘 찾기
    fastest = min(results, key=lambda x: results[x]['time'])
    print(f"\n가장 빠른 알고리즘: {fastest} ({results[fastest]['time']:.4f}초)")
    
    # 소수 개수 일치 여부 확인
    prime_counts = [data['prime_count'] for data in results.values()]
    if all(count == prime_counts[0] for count in prime_counts):
        print(f"모든 알고리즘이 동일한 소수 개수를 반환했습니다: {prime_counts[0]}")
    else:
        print("경고: 알고리즘 간 소수 개수가 일치하지 않습니다!")
        for algo, data in results.items():
            print(f"  - {algo}: {data['prime_count']}")
    
    return results

if __name__ == "__main__":
    # 임의의 테스트 세트 생성을 위한 시드 설정 (결과 재현 가능)
    # random.seed(42)
    
    # 작은 수부터 큰 수까지 다양한 범위의 숫자로 테스트
    print("==== 다양한 크기의 숫자 테스트 ====")
    run_benchmark()
    
    # 작은 숫자만 테스트
    print("\n\n==== 작은 숫자 테스트 (2-100,000) ====")
    run_benchmark(test_range=(2, 100000), num_tests=100000)
    
    # 큰 숫자만 테스트
    print("\n\n==== 큰 숫자 테스트 (1,000,000,000-10,000,000,000) ====")
    run_benchmark(test_range=(1000000000, 10000000000), num_tests=100000)