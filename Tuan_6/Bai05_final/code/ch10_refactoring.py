"""
Chapter 10 - Tái cấu trúc Mã với GenAI
Minh hoạ: Refactor từ nested loop → vectorized operation
Bài toán: Tính khoảng cách giữa hai ma trận (Manhattan & Euclidean)
"""

import math
import time
import random


# ─── TRƯỚC refactoring: Code "smelly" ─────────────────────────────────────────

def compute_distances_v1(mat_a, mat_b):
    """
    TRƯỚC: Code "code smell" - nested loops, tên biến kém, không type hints.
    Đây là ví dụ về code CẦN được refactor.
    """
    # BAD: tên biến không mô tả
    r1 = len(mat_a)
    c1 = len(mat_a[0])
    t1 = 0
    t2 = 0
    
    # BAD: nested loops thủ công
    for i in range(r1):
        for j in range(c1):
            # BAD: logic tính toán lẫn lộn không tách biệt
            d = mat_a[i][j] - mat_b[i][j]
            if d < 0:
                d = -d
            t1 += d
            t2 += (mat_a[i][j] - mat_b[i][j]) ** 2
    
    # BAD: trả về tuple không có tên
    return t1, t2 ** 0.5


# ─── SAU refactoring: Clean Code ─────────────────────────────────────────────

Matrix = list[list[float]]


def _validate_shape(matrix_a: Matrix, matrix_b: Matrix) -> None:
    """Kiểm tra hai ma trận có cùng kích thước.
    
    Args:
        matrix_a: Ma trận thứ nhất.
        matrix_b: Ma trận thứ hai.
        
    Raises:
        ValueError: Nếu kích thước không khớp.
    """
    if len(matrix_a) != len(matrix_b) or len(matrix_a[0]) != len(matrix_b[0]):
        raise ValueError(
            f"Kích thước không khớp: "
            f"({len(matrix_a)}×{len(matrix_a[0])}) vs "
            f"({len(matrix_b)}×{len(matrix_b[0])})"
        )


def compute_manhattan_distance(matrix_a: Matrix, matrix_b: Matrix) -> float:
    """
    Tính khoảng cách Manhattan (L1) giữa hai ma trận.
    
    Refactored: Tách biệt rõ ràng từng loại khoảng cách.
    
    Args:
        matrix_a: Ma trận đầu vào thứ nhất.
        matrix_b: Ma trận đầu vào thứ hai (cùng kích thước).
        
    Returns:
        Khoảng cách Manhattan (tổng sai số tuyệt đối).
    """
    _validate_shape(matrix_a, matrix_b)
    return sum(
        abs(a - b)
        for row_a, row_b in zip(matrix_a, matrix_b)
        for a, b in zip(row_a, row_b)
    )


def compute_euclidean_distance(matrix_a: Matrix, matrix_b: Matrix) -> float:
    """
    Tính khoảng cách Euclidean (L2) giữa hai ma trận.
    
    Refactored: Dùng generator expression thay nested loops.
    
    Args:
        matrix_a: Ma trận đầu vào thứ nhất.
        matrix_b: Ma trận đầu vào thứ hai (cùng kích thước).
        
    Returns:
        Khoảng cách Euclidean (căn bậc hai tổng bình phương sai số).
    """
    _validate_shape(matrix_a, matrix_b)
    sum_sq = sum(
        (a - b) ** 2
        for row_a, row_b in zip(matrix_a, matrix_b)
        for a, b in zip(row_a, row_b)
    )
    return math.sqrt(sum_sq)


# ─── Vectorized version (numpy-style, without numpy) ──────────────────────────

def flatten_matrix(matrix: Matrix) -> list[float]:
    """Chuyển ma trận 2D thành danh sách 1D."""
    return [val for row in matrix for val in row]


def compute_manhattan_vectorized(matrix_a: Matrix, matrix_b: Matrix) -> float:
    """
    Phiên bản vector hoá của Manhattan distance.
    Tương đương numpy: np.sum(np.abs(np.array(a) - np.array(b)))
    """
    _validate_shape(matrix_a, matrix_b)
    flat_a = flatten_matrix(matrix_a)
    flat_b = flatten_matrix(matrix_b)
    return sum(abs(a - b) for a, b in zip(flat_a, flat_b))


# ─── Benchmark: So sánh hiệu năng ─────────────────────────────────────────────

def benchmark_versions(size: int = 50, iterations: int = 1000) -> None:
    """So sánh tốc độ giữa v1 (nested loop) và v2 (generator)."""
    random.seed(42)
    mat_a = [[random.random() for _ in range(size)] for _ in range(size)]
    mat_b = [[random.random() for _ in range(size)] for _ in range(size)]
    
    # V1: Nested loops
    t0 = time.perf_counter()
    for _ in range(iterations):
        compute_distances_v1(mat_a, mat_b)
    t1 = time.perf_counter()
    v1_time = (t1 - t0) / iterations * 1000
    
    # V2: Generator expressions
    t0 = time.perf_counter()
    for _ in range(iterations):
        compute_manhattan_distance(mat_a, mat_b)
        compute_euclidean_distance(mat_a, mat_b)
    t1 = time.perf_counter()
    v2_time = (t1 - t0) / iterations * 1000
    
    print(f"  Ma trận {size}×{size}, {iterations} lần lặp:")
    print(f"  V1 (nested loop): {v1_time:.3f} ms/lần")
    print(f"  V2 (generator):   {v2_time:.3f} ms/lần")
    ratio = v1_time / v2_time if v2_time > 0 else float('inf')
    print(f"  Tỷ lệ cải thiện:  {ratio:.2f}x")


# ─── DEMO ───────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 60)
    print("CHAPTER 10: Refactoring Code với GenAI")
    print("=" * 60)
    
    a = [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]]
    b = [[1.5, 2.5, 2.0], [4.0, 6.0, 5.0]]
    
    print("\n1. So sánh TRƯỚC và SAU refactoring:")
    print("   V1 (code smelly):")
    m1, e1 = compute_distances_v1(a, b)
    print(f"     Manhattan={m1}, Euclidean={e1:.4f}")
    
    print("   V2 (clean code):")
    m2 = compute_manhattan_distance(a, b)
    e2 = compute_euclidean_distance(a, b)
    print(f"     Manhattan={m2}, Euclidean={e2:.4f}")
    print(f"     Kết quả khớp: {abs(m1-m2) < 1e-9 and abs(e1-e2) < 1e-9}")
    
    print("\n2. Code Smells đã được sửa:")
    smells = [
        ("Tên biến kém (t1, t2, r1)",   "Tên mô tả (manhattan_distance, euclidean_distance)"),
        ("Nested loops thủ công",         "Generator expressions pythonic"),
        ("Logic trộn lẫn",               "Mỗi hàm một nhiệm vụ (SRP)"),
        ("Không có type hints",          "Type hints đầy đủ"),
        ("Không có validation",          "Validate kích thước ma trận"),
        ("Trả tuple không tên",          "Hàm riêng biệt có tên rõ ràng"),
    ]
    for before, after in smells:
        print(f"   ✗ {before}")
        print(f"   ✓ {after}")
        print()
    
    print("3. Benchmark hiệu năng:")
    benchmark_versions(size=30, iterations=500)
    
    print("\nHoàn thành demo Chapter 10!")
