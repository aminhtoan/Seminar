"""
Chapter 8 - Giới thiệu Kỹ thuật Gợi ý (Prompt Engineering)
Minh hoạ Few-Shot Learning / In-Context Learning qua OpenAI API
Kỹ thuật: Zero-shot, One-shot, Few-shot
"""

import os
import json


# ─── Cấu trúc prompt engineering ──────────────────────────────────────────────

SYSTEM_PROMPT = """Bạn là một chuyên gia Python. Khi tôi cung cấp một hàm,
hãy hoàn thành nó tuân thủ đúng style guide sau:
- Sử dụng type hints đầy đủ
- Thêm docstring theo format Google Style
- Sử dụng tên biến mô tả rõ ràng
- Không thêm comment thừa bên trong code
"""


def build_zero_shot_prompt(task: str) -> list[dict]:
    """Xây dựng prompt zero-shot (không có ví dụ)."""
    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": task}
    ]


def build_few_shot_prompt(task: str, examples: list[dict]) -> list[dict]:
    """
    Xây dựng prompt few-shot với các ví dụ minh hoạ.
    
    Args:
        task: Nhiệm vụ cần thực hiện
        examples: Danh sách các cặp (input, output) mẫu
        
    Returns:
        Danh sách các tin nhắn theo định dạng OpenAI Chat API
    """
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    
    # Thêm các ví dụ few-shot
    for example in examples:
        messages.append({"role": "user", "content": example["input"]})
        messages.append({"role": "assistant", "content": example["output"]})
    
    # Thêm task thực sự
    messages.append({"role": "user", "content": task})
    return messages


# ─── Ví dụ few-shot cho code style ────────────────────────────────────────────

FEW_SHOT_EXAMPLES = [
    {
        "input": "def add(x, y):\n    return x + y",
        "output": '''def add(x: float, y: float) -> float:
    """Add two numbers together.
    
    Args:
        x: First number.
        y: Second number.
        
    Returns:
        Sum of x and y.
    """
    return x + y'''
    },
    {
        "input": "def get_max(lst):\n    m = lst[0]\n    for i in lst:\n        if i > m:\n            m = i\n    return m",
        "output": '''def get_max(values: list[float]) -> float:
    """Return the maximum value in a list.
    
    Args:
        values: Non-empty list of numbers.
        
    Returns:
        Maximum value found in the list.
        
    Raises:
        ValueError: If values is empty.
    """
    if not values:
        raise ValueError("List must not be empty.")
    return max(values)'''
    }
]


# ─── Mô phỏng phân tích prompt (không gọi API thật) ──────────────────────────

def analyze_prompt_quality(messages: list[dict]) -> dict:
    """
    Phân tích chất lượng của prompt (mô phỏng, không cần API).
    
    Returns:
        Dictionary với các chỉ số chất lượng
    """
    num_examples = sum(1 for m in messages if m["role"] == "assistant")
    system_length = len([m for m in messages if m["role"] == "system"][0]["content"])
    user_messages = [m for m in messages if m["role"] == "user"]
    
    return {
        "so_vi_du_few_shot": num_examples,
        "do_dai_system_prompt": system_length,
        "so_luot_trao_doi": len(messages),
        "loai_prompt": "few-shot" if num_examples > 0 else "zero-shot",
        "uoc_tinh_tokens": sum(len(m["content"].split()) * 1.3 
                               for m in messages)
    }


# ─── Minh hoạ các kỹ thuật prompt engineering ─────────────────────────────────

PROMPT_TECHNIQUES = {
    "Zero-Shot": {
        "mo_ta": "Không có ví dụ, chỉ có hướng dẫn.",
        "khi_dung": "Tác vụ đơn giản, rõ ràng",
        "uu_diem": "Ngắn gọn, tiết kiệm token",
        "nhuoc_diem": "Output không nhất quán về style"
    },
    "One-Shot": {
        "mo_ta": "Một ví dụ minh hoạ kết quả mong muốn.",
        "khi_dung": "Cần định hướng format",
        "uu_diem": "Cân bằng tốt giữa chi phí và chất lượng",
        "nhuoc_diem": "Có thể chưa đủ cho tác vụ phức tạp"
    },
    "Few-Shot": {
        "mo_ta": "2-5 ví dụ để hướng dẫn mô hình.",
        "khi_dung": "Cần tuân thủ coding style cụ thể",
        "uu_diem": "Output nhất quán và chất lượng cao",
        "nhuoc_diem": "Tốn token hơn, cần chọn ví dụ tốt"
    },
    "Chain-of-Thought": {
        "mo_ta": "Hướng dẫn mô hình suy luận từng bước.",
        "khi_dung": "Tác vụ đa bước, logic phức tạp",
        "uu_diem": "Độ chính xác cao cho bài toán phức tạp",
        "nhuoc_diem": "Response dài hơn nhiều"
    }
}


# ─── DEMO ───────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 60)
    print("CHAPTER 8: Prompt Engineering - Few-Shot Learning")
    print("=" * 60)
    
    task = "def calc_average(numbers):\n    return sum(numbers) / len(numbers)"
    
    # Zero-shot
    print("\n1. Zero-Shot Prompt:")
    zero_shot = build_zero_shot_prompt(task)
    z_analysis = analyze_prompt_quality(zero_shot)
    print(f"   Số tin nhắn: {z_analysis['so_luot_trao_doi']}")
    print(f"   Loại: {z_analysis['loai_prompt']}")
    print(f"   Ước tính tokens: {z_analysis['uoc_tinh_tokens']:.0f}")
    
    # Few-shot
    print("\n2. Few-Shot Prompt (với 2 ví dụ):")
    few_shot = build_few_shot_prompt(task, FEW_SHOT_EXAMPLES)
    f_analysis = analyze_prompt_quality(few_shot)
    print(f"   Số ví dụ: {f_analysis['so_vi_du_few_shot']}")
    print(f"   Loại: {f_analysis['loai_prompt']}")
    print(f"   Ước tính tokens: {f_analysis['uoc_tinh_tokens']:.0f}")
    
    # So sánh kỹ thuật
    print("\n3. So sánh các kỹ thuật Prompt Engineering:")
    print(f"  {'Kỹ thuật':<20} {'Khi dùng':<35} {'Ưu điểm'}")
    print(f"  {'-'*20} {'-'*35} {'-'*30}")
    for name, info in PROMPT_TECHNIQUES.items():
        print(f"  {name:<20} {info['khi_dung']:<35} {info['uu_diem']}")
    
    # In prompt mẫu
    print("\n4. Cấu trúc Few-Shot Prompt (JSON):")
    print(json.dumps(few_shot[:3], ensure_ascii=False, indent=2))
    
    print("\nHoàn thành demo Chapter 8!")
