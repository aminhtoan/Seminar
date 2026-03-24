"""
Chapter 7 - Đọc và Hiểu Cơ sở Mã với GenAI
Minh hoạ Manhattan distance và Euclidean distance giữa hai ma trận
Đây là code base ví dụ trong cuốn sách (ch7/)
"""

from typing import Union
import math


# ─── Kiểu dữ liệu ────────────────────────────────────────────────────────────

Matrix = list[list[float]]


# ─── Hàm tiện ích ─────────────────────────────────────────────────────────────

def validate_matrices(matrix_a: Matrix, matrix_b: Matrix) -> None:
    """
    Xác nhận hai ma trận có cùng kích thước.
    
    Args:
        matrix_a: Ma trận thứ nhất
        matrix_b: Ma trận thứ hai
        
    Raises:
        ValueError: Nếu kích thước không khớp
    """
    if len(matrix_a) != len(matrix_b):
        raise ValueError(
            f"Số hàng không khớp: {len(matrix_a)} vs {len(matrix_b)}"
        )
    for i, (row_a, row_b) in enumerate(zip(matrix_a, matrix_b)):
        if len(row_a) != len(row_b):
            raise ValueError(
                f"Số cột hàng {i} không khớp: {len(row_a)} vs {len(row_b)}"
            )


# ─── Manhattan Distance (L1 Norm) ─────────────────────────────────────────────

def manhattan_distance(matrix_a: Matrix, matrix_b: Matrix) -> float:
    """
    Tính khoảng cách Manhattan (L1 Norm) giữa hai ma trận.
    
    Định nghĩa: sum(|a_ij - b_ij|) cho tất cả i, j
    
    Args:
        matrix_a: Ma trận đầu vào thứ nhất
        matrix_b: Ma trận đầu vào thứ hai
        
    Returns:
        Khoảng cách Manhattan (float)
        
    Example:
        >>> a = [[1, 2], [3, 4]]
        >>> b = [[2, 2], [1, 4]]
        >>> manhattan_distance(a, b)
        3.0
    """
    validate_matrices(matrix_a, matrix_b)
    total = 0.0
    for row_a, row_b in zip(matrix_a, matrix_b):
        for a, b in zip(row_a, row_b):
            total += abs(a - b)
    return total


# ─── Euclidean Distance (L2 Norm) ─────────────────────────────────────────────

def euclidean_distance(matrix_a: Matrix, matrix_b: Matrix) -> float:
    """
    Tính khoảng cách Euclidean (L2 Norm) giữa hai ma trận.
    
    Định nghĩa: sqrt(sum((a_ij - b_ij)^2)) cho tất cả i, j
    
    Args:
        matrix_a: Ma trận đầu vào thứ nhất
        matrix_b: Ma trận đầu vào thứ hai
        
    Returns:
        Khoảng cách Euclidean (float)
        
    Example:
        >>> a = [[1, 0], [0, 1]]
        >>> b = [[0, 0], [0, 0]]
        >>> euclidean_distance(a, b)
        1.4142135623730951
    """
    validate_matrices(matrix_a, matrix_b)
    sum_sq = 0.0
    for row_a, row_b in zip(matrix_a, matrix_b):
        for a, b in zip(row_a, row_b):
            sum_sq += (a - b) ** 2
    return math.sqrt(sum_sq)


# ─── Tiện ích hiển thị ──────────────────────────────────────────────────────

def print_matrix(matrix: Matrix, name: str) -> None:
    """In ma trận với định dạng đẹp."""
    print(f"  {name}:")
    for row in matrix:
        print("    " + "  ".join(f"{v:6.2f}" for v in row))


# ─── DEMO ───────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 60)
    print("CHAPTER 7: Đọc và Hiểu Codebase - Manhattan & Euclidean Distance")
    print("=" * 60)
    
    # Test case 1: Ma trận đơn giản
    a1: Matrix = [[1, 2, 3], [4, 5, 6]]
    b1: Matrix = [[1, 2, 3], [4, 5, 6]]
    print("\nTest 1 - Ma trận giống hệt nhau:")
    print_matrix(a1, "A")
    print_matrix(b1, "B")
    print(f"  Manhattan: {manhattan_distance(a1, b1)}")
    print(f"  Euclidean: {euclidean_distance(a1, b1)}")
    
    # Test case 2: Ví dụ Pacman từ sách
    a2: Matrix = [[1, 1]]   # Pacman tại (1,1)
    b2: Matrix = [[3, 2]]   # Ghost tại (3,2)
    print("\nTest 2 - Pacman vs Ghost (từ sách):")
    print_matrix(a2, "Pacman (1,1)")
    print_matrix(b2, "Ghost  (3,2)")
    print(f"  Manhattan (bước đi): {manhattan_distance(a2, b2)}")
    print(f"  Euclidean (đường thẳng): {euclidean_distance(a2, b2):.4f}")
    
    # Test case 3: Ma trận lớn hơn
    import random
    random.seed(42)
    a3 = [[random.randint(0, 10) for _ in range(4)] for _ in range(3)]
    b3 = [[random.randint(0, 10) for _ in range(4)] for _ in range(3)]
    print("\nTest 3 - Ma trận ngẫu nhiên 3x4:")
    print_matrix(a3, "A")
    print_matrix(b3, "B")
    print(f"  Manhattan: {manhattan_distance(a3, b3)}")
    print(f"  Euclidean: {euclidean_distance(a3, b3):.4f}")
    
    # Test case 4: Validation error
    print("\nTest 4 - Kiểm tra lỗi kích thước không khớp:")
    try:
        manhattan_distance([[1, 2]], [[1, 2, 3]])
    except ValueError as e:
        print(f"  ValueError caught: {e}")
    
    print("\nHoàn thành demo Chapter 7!")
