"""
Chapter 11 - Tinh chỉnh Mô hình với OpenAI
Minh hoạ: Tạo file JSONL cho fine-tuning và mô phỏng kết quả
Kỹ thuật: Prepare training data, JSONL format, compare base vs fine-tuned
"""

import json
import os
from typing import Any


# ─── Định dạng JSONL cho fine-tuning ──────────────────────────────────────────

def create_training_example(
    system: str,
    user_input: str,
    assistant_output: str
) -> dict[str, Any]:
    """
    Tạo một ví dụ huấn luyện theo định dạng OpenAI fine-tuning.
    
    Args:
        system: System prompt định nghĩa vai trò mô hình
        user_input: Input từ người dùng
        assistant_output: Output mong muốn (ground truth)
        
    Returns:
        Dictionary theo chuẩn OpenAI JSONL fine-tuning format
    """
    return {
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user_input},
            {"role": "assistant", "content": assistant_output}
        ]
    }


# ─── System prompt cho chuyên môn hoá ──────────────────────────────────────────

CODING_SPECIALIST_SYSTEM = (
    "Bạn là chuyên gia Python. Hoàn thành code theo yêu cầu với: "
    "type hints đầy đủ, docstring Google Style, không thêm comment thừa "
    "bên trong code, không giải thích dài dòng ngoài code."
)


# ─── Dữ liệu huấn luyện mẫu ──────────────────────────────────────────────────

TRAINING_EXAMPLES = [
    create_training_example(
        system=CODING_SPECIALIST_SYSTEM,
        user_input="Viết hàm tính factorial.",
        assistant_output='''def factorial(n: int) -> int:
    """Compute the factorial of a non-negative integer.
    
    Args:
        n: Non-negative integer.
        
    Returns:
        Factorial of n.
        
    Raises:
        ValueError: If n is negative.
    """
    if n < 0:
        raise ValueError(f"n must be non-negative, got {n}.")
    if n == 0:
        return 1
    return n * factorial(n - 1)'''
    ),
    create_training_example(
        system=CODING_SPECIALIST_SYSTEM,
        user_input="Viết hàm tính tổng bình phương của list.",
        assistant_output='''def sum_of_squares(values: list[float]) -> float:
    """Compute the sum of squares of a list of numbers.
    
    Args:
        values: List of numbers.
        
    Returns:
        Sum of squares.
    """
    return sum(v ** 2 for v in values)'''
    ),
    create_training_example(
        system=CODING_SPECIALIST_SYSTEM,
        user_input="Viết hàm kiểm tra palindrome.",
        assistant_output='''def is_palindrome(text: str) -> bool:
    """Check whether a string is a palindrome (case-insensitive).
    
    Args:
        text: Input string to check.
        
    Returns:
        True if text reads the same forwards and backwards.
    """
    normalized = text.lower().replace(" ", "")
    return normalized == normalized[::-1]'''
    ),
    create_training_example(
        system=CODING_SPECIALIST_SYSTEM,
        user_input="Viết hàm đảo ngược từ trong câu.",
        assistant_output='''def reverse_words(sentence: str) -> str:
    """Reverse the order of words in a sentence.
    
    Args:
        sentence: Input sentence.
        
    Returns:
        Sentence with word order reversed.
    """
    return " ".join(sentence.split()[::-1])'''
    ),
    create_training_example(
        system=CODING_SPECIALIST_SYSTEM,
        user_input="Viết hàm flatten một list lồng nhau 2 cấp.",
        assistant_output='''def flatten(nested: list[list[Any]]) -> list[Any]:
    """Flatten a two-level nested list.
    
    Args:
        nested: List of lists.
        
    Returns:
        Single flat list with all elements.
    """
    return [item for sublist in nested for item in sublist]'''
    ),
]


def save_jsonl(examples: list[dict], filepath: str) -> None:
    """
    Lưu danh sách ví dụ ra file JSONL.
    
    Args:
        examples: Danh sách các ví dụ huấn luyện
        filepath: Đường dẫn file output
    """
    with open(filepath, "w", encoding="utf-8") as f:
        for example in examples:
            f.write(json.dumps(example, ensure_ascii=False) + "\n")
    print(f"  Đã lưu {len(examples)} ví dụ → {filepath}")


def validate_jsonl(filepath: str) -> dict[str, Any]:
    """
    Kiểm tra file JSONL trước khi upload fine-tuning.
    
    Returns:
        Dict với các thống kê: total, valid, errors, avg_tokens
    """
    stats = {"total": 0, "valid": 0, "errors": [], "avg_tokens": 0}
    total_tokens = 0
    
    with open(filepath, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            stats["total"] += 1
            try:
                example = json.loads(line.strip())
                
                # Kiểm tra cấu trúc
                assert "messages" in example, "Missing 'messages' key"
                messages = example["messages"]
                assert len(messages) >= 2, "Need at least 2 messages"
                
                roles = [m["role"] for m in messages]
                assert "user" in roles, "Missing 'user' role"
                assert "assistant" in roles, "Missing 'assistant' role"
                
                # Ước tính tokens (4 chars ≈ 1 token)
                text_len = sum(len(m["content"]) for m in messages)
                total_tokens += text_len // 4
                
                stats["valid"] += 1
            except (json.JSONDecodeError, AssertionError, KeyError) as e:
                stats["errors"].append(f"Dòng {line_num}: {e}")
    
    if stats["valid"] > 0:
        stats["avg_tokens"] = total_tokens // stats["valid"]
    
    return stats


# ─── Mô phỏng so sánh base model vs fine-tuned ────────────────────────────────

BASE_MODEL_OUTPUT = '''# Tính factorial
def factorial(n):
    # Kiểm tra điều kiện đầu vào
    if n < 0:
        # Không chấp nhận số âm
        raise ValueError("n phải là số không âm")
    # Trường hợp cơ bản
    if n == 0:
        return 1
    # Đệ quy
    return n * factorial(n - 1)
# Ví dụ sử dụng: factorial(5) = 120
'''

FINE_TUNED_OUTPUT = '''def factorial(n: int) -> int:
    """Compute the factorial of a non-negative integer.
    
    Args:
        n: Non-negative integer.
        
    Returns:
        Factorial of n.
        
    Raises:
        ValueError: If n is negative.
    """
    if n < 0:
        raise ValueError(f"n must be non-negative, got {n}.")
    if n == 0:
        return 1
    return n * factorial(n - 1)
'''


# ─── DEMO ───────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 60)
    print("CHAPTER 11: Fine-Tuning với OpenAI")
    print("=" * 60)
    
    # Tạo file JSONL
    jsonl_path = "ch11_fine_tuning_data.jsonl"
    print(f"\n1. Tạo file JSONL huấn luyện:")
    save_jsonl(TRAINING_EXAMPLES, jsonl_path)
    
    # Validate
    print(f"\n2. Kiểm tra file JSONL:")
    stats = validate_jsonl(jsonl_path)
    print(f"   Tổng ví dụ:    {stats['total']}")
    print(f"   Hợp lệ:        {stats['valid']}")
    print(f"   Lỗi:           {len(stats['errors'])}")
    print(f"   Ước tính tokens/ví dụ: ~{stats['avg_tokens']}")
    
    # So sánh base vs fine-tuned
    print(f"\n3. So sánh Base Model vs Fine-Tuned Model:")
    print(f"\n   [Base GPT-4o-mini] output (có comment thừa, không có type hints):")
    for line in BASE_MODEL_OUTPUT.strip().split('\n'):
        print(f"     {line}")
    
    print(f"\n   [Fine-Tuned Model] output (tuân thủ style guide):")
    for line in FINE_TUNED_OUTPUT.strip().split('\n'):
        print(f"     {line}")
    
    # So sánh chỉ số
    print(f"\n4. Chỉ số so sánh:")
    base_lines = len(BASE_MODEL_OUTPUT.strip().split('\n'))
    ft_lines = len(FINE_TUNED_OUTPUT.strip().split('\n'))
    base_comments = BASE_MODEL_OUTPUT.count('#')
    ft_comments = FINE_TUNED_OUTPUT.count('#')
    
    metrics = [
        ("Số dòng code", base_lines, ft_lines),
        ("Inline comments (#)", base_comments, ft_comments),
        ("Có type hints", "Không", "Có"),
        ("Có docstring", "Không", "Có (Google Style)"),
        ("Có input validation", "Có", "Có"),
    ]
    
    print(f"   {'Chỉ số':<25} {'Base':>10} {'Fine-Tuned':>12}")
    print(f"   {'-'*25} {'-'*10} {'-'*12}")
    for metric, base_val, ft_val in metrics:
        print(f"   {metric:<25} {str(base_val):>10} {str(ft_val):>12}")
    
    # Dọn dẹp
    if os.path.exists(jsonl_path):
        os.remove(jsonl_path)
    
    print("\nHoàn thành demo Chapter 11!")
