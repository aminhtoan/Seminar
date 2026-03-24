"""
Chapter 9 - Kỹ thuật Gợi ý Nâng cao cho Tác vụ Lập trình
Minh hoạ: Chain-of-Thought (CoT) Prompting và Prompt Chaining
Bài toán: Geometric Mean với giá trị âm (Net Portfolio Returns)
"""

import math
from typing import Union


# ─── Bài toán: Geometric Mean với giá trị âm ──────────────────────────────────

IBM_YEARLY_RETURNS: dict[str, float] = {
    "2000": -0.2084,   # -20.84%
    "2001":  0.4300,   # +43.00%
    "2002": -0.3547,   # -35.47%
}


def geometric_mean_naive(returns: list[float]) -> float:
    """
    Tính geometric mean theo công thức đơn giản.
    LỖI: Không xử lý được giá trị âm đúng cách!
    
    Args:
        returns: Danh sách lợi nhuận (có thể âm)
        
    Returns:
        Geometric mean (SAI khi có giá trị âm)
    """
    product = 1.0
    for r in returns:
        product *= r
    n = len(returns)
    # Vấn đề: tích của số âm lẻ là âm, không thể lấy căn thực
    if product < 0:
        return float("nan")  # Không xác định!
    return product ** (1.0 / n)


def geometric_mean_gross_returns(net_returns: list[float]) -> float:
    """
    Tính geometric mean ĐÚNG bằng cách chuyển đổi sang gross returns.
    
    Phương pháp:
      1. Chuyển net return → gross return: gross = 1 + net
      2. Tính tích của tất cả gross returns
      3. Lấy căn bậc n của tích
      4. Chuyển ngược lại: result = gross_mean - 1
    
    Args:
        net_returns: Danh sách lợi nhuận thuần (có thể âm)
        
    Returns:
        Trung bình lợi nhuận hàng năm (geometric mean)
        
    Raises:
        ValueError: Nếu gross return bằng 0 hoặc âm
        
    Example:
        >>> ibm = [-0.2084, 0.4300, -0.3547]
        >>> result = geometric_mean_gross_returns(ibm)
        >>> print(f"Trung bình: {result:.2%}")
        Trung bình: -9.93%
    """
    if not net_returns:
        raise ValueError("Danh sách lợi nhuận không được rỗng.")
    
    n = len(net_returns)
    gross_product = 1.0
    
    for net_return in net_returns:
        gross_return = 1.0 + net_return
        if gross_return <= 0:
            raise ValueError(
                f"Gross return không hợp lệ ({gross_return:.4f}). "
                f"Net return phải > -1 (không mất hơn 100%)."
            )
        gross_product *= gross_return
    
    gross_mean = gross_product ** (1.0 / n)
    return gross_mean - 1.0


# ─── Chain-of-Thought: hướng dẫn từng bước ────────────────────────────────────

def cot_geometric_mean_explanation(net_returns: list[float]) -> None:
    """Hiển thị Chain-of-Thought step-by-step reasoning."""
    print("  [CoT] Bước 1: Chuyển net returns → gross returns")
    gross = [1 + r for r in net_returns]
    for i, (net, gr) in enumerate(zip(net_returns, gross)):
        print(f"    Năm {i+1}: {net:+.4f} → {gr:.4f}")
    
    print("\n  [CoT] Bước 2: Tính tích của gross returns")
    product = 1.0
    for g in gross:
        product *= g
    print(f"    Tích = {' × '.join(f'{g:.4f}' for g in gross)} = {product:.6f}")
    
    print(f"\n  [CoT] Bước 3: Lấy căn bậc {len(net_returns)}")
    n = len(net_returns)
    gross_mean = product ** (1.0 / n)
    print(f"    {product:.6f}^(1/{n}) = {gross_mean:.6f}")
    
    print(f"\n  [CoT] Bước 4: Chuyển ngược → net return")
    net_mean = gross_mean - 1.0
    print(f"    {gross_mean:.6f} - 1 = {net_mean:+.4f} = {net_mean:+.2%}")


# ─── Prompt Chaining: chuỗi tác vụ liên tiếp ──────────────────────────────────

def demonstrate_prompt_chaining() -> None:
    """
    Minh hoạ Prompt Chaining - cải thiện code qua nhiều bước.
    Mỗi bước dùng output của bước trước làm input.
    """
    print("\n  Prompt Chain:")
    
    steps = [
        ("Bước 1", "Implement geometric_mean_gross_returns", 
         "→ Hàm cơ bản hoạt động đúng"),
        ("Bước 2", "Thêm type hints đầy đủ", 
         "→ net_returns: list[float]) -> float"),
        ("Bước 3", "Thêm docstring Google Style + ví dụ", 
         "→ Tài liệu hoàn chỉnh"),
        ("Bước 4", "Thêm input validation",
         "→ Xử lý edge cases (rỗng, gross ≤ 0)"),
        ("Bước 5", "Viết unit tests",
         "→ test_happy_path, test_negative, test_error"),
    ]
    
    for step, task, result in steps:
        print(f"    [{step}] {task}")
        print(f"            {result}")


# ─── DEMO ───────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 60)
    print("CHAPTER 9: Chain-of-Thought & Prompt Chaining")
    print("=" * 60)
    
    returns_list = list(IBM_YEARLY_RETURNS.values())
    years = list(IBM_YEARLY_RETURNS.keys())
    
    print(f"\nDữ liệu IBM Stock Returns:")
    for year, ret in IBM_YEARLY_RETURNS.items():
        print(f"  {year}: {ret:+.2%}")
    
    print(f"\n1. Geometric Mean NAIVE (sai với giá trị âm):")
    naive = geometric_mean_naive(returns_list)
    print(f"   Kết quả: {naive} (NaN = không xác định!)")
    
    print(f"\n2. Chain-of-Thought Reasoning - từng bước:")
    cot_geometric_mean_explanation(returns_list)
    
    print(f"\n3. Kết quả cuối cùng (đúng):")
    result = geometric_mean_gross_returns(returns_list)
    print(f"   Geometric Mean = {result:+.4f} = {result:+.2%}")
    print(f"   Kiểm chứng: $1000 × (1{result:+.4f})^3 = "
          f"${1000 * (1 + result)**3:.2f}")
    
    print(f"\n4. Prompt Chaining - cải thiện code qua nhiều bước:")
    demonstrate_prompt_chaining()
    
    print("\nHoàn thành demo Chapter 9!")
