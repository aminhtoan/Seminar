"""
Lab 8 & 9: Prompt Engineering – Few-Shot và Chain of Thought
Chương 8: An Introduction to Prompt Engineering
Chương 9: Advanced Prompt Engineering for Coding-Related Tasks
"""
import numpy as np
from typing import Dict, Optional, List


# ============================================================
# LAB 8: FEW-SHOT LEARNING
# ============================================================

def build_few_shot_prompt(
    task_description: str,
    examples: List[Dict[str, str]],
    new_input: str,
    input_label: str = "INPUT",
    output_label: str = "OUTPUT"
) -> str:
    """
    Xây dựng prompt few-shot theo khung Five S's.
    
    Args:
        task_description: mô tả tác vụ (TASK)
        examples: danh sách {"input": ..., "output": ...}
        new_input: đầu vào mới cần xử lý
        input_label: nhãn cho đầu vào (OLD, INPUT, QUESTION, ...)
        output_label: nhãn cho đầu ra (REFACTORED, OUTPUT, ANSWER, ...)
    Returns:
        Prompt hoàn chỉnh
    """
    prompt_parts = [
        f"CONTEXT: You are a Python expert.",
        f"TASK: {task_description}",
        ""
    ]
    
    # Thêm ví dụ
    for i, ex in enumerate(examples, 1):
        prompt_parts.append(f"{input_label}_{i}: {{{{{ex['input']}}}}}")
        prompt_parts.append(f"{output_label}_{i}: {{{{{ex['output']}}}}}")
        prompt_parts.append("")
    
    # Đầu vào mới
    prompt_parts.append(f"{input_label}: {{{{{new_input}}}}}")
    prompt_parts.append(f"{output_label}:")
    
    return "\n".join(prompt_parts)


def refactor_print_to_logger_fewshot(code: str) -> str:
    """
    Dùng few-shot prompting để refactor print → structured logger.
    Minh họa Lab 8-1 từ sách.
    
    Args:
        code: dòng print() cần refactor
    Returns:
        logger call tương đương
    """
    examples = [
        {
            "input": "print('Process started for config.txt')",
            "output": "logger.info('Processing started', extra={'stage': 'start', 'file': 'config.txt'})"
        },
        {
            "input": "print('Warning! Could not load user data from user_info.csv')",
            "output": "logger.warning('User data failed to load', extra={'module': 'user_loader', 'file': 'user_info.csv'})"
        },
        {
            "input": "print('Error connecting to database!')",
            "output": "logger.error('Database connection failed', extra={'module': 'db_connector'})"
        }
    ]
    
    prompt = build_few_shot_prompt(
        task_description="Refactor print statements into structured logger calls.",
        examples=examples,
        new_input=code,
        input_label="OLD",
        output_label="REFACTORED"
    )
    
    try:
        from openai import OpenAI
        client = OpenAI()
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150,
            temperature=0.1
        )
        return response.choices[0].message.content.strip()
    except Exception:
        # Demo output nếu không có API
        return "logger.error('File not found', extra={'file': 'passwords.txt'})"


# ============================================================
# LAB 9: CHAIN OF THOUGHT (CoT)
# ============================================================

def get_average_return_cot(net_returns: Dict[str, float]) -> float:
    """
    Tính trung bình hình học của portfolio returns với giá trị âm.
    Đây là bài toán minh họa CoT trong chương 9.
    
    Vấn đề với công thức thông thường:
        (-0.2 × 0.4 × -0.35)^(1/3) = 0.32 → SAI! (32% thay vì -10%)
    
    Giải pháp CoT (3 bước):
        Step 1: Chuyển net returns → gross returns (cộng thêm 1)
        Step 2: Tính geometric mean của gross returns
        Step 3: Chuyển về net average (trừ 1)
    
    Args:
        net_returns: dict ánh xạ năm → net return (vd: {"2000": -0.21})
    Returns:
        Net average return dạng float
    Raises:
        ValueError: nếu input rỗng
    """
    if not net_returns:
        raise ValueError("net_returns cannot be empty")
    
    # Step 1: Calculate gross returns
    gross_returns: np.ndarray = np.array(list(net_returns.values())) + 1
    
    # Step 2: Calculate geometric mean of gross returns
    power: float = 1.0 / len(gross_returns)
    gross_average: float = float(np.prod(gross_returns) ** power)
    
    # Step 3: Convert back to net average
    net_average: float = gross_average - 1
    
    return net_average


def build_cot_prompt(function_signature: str, steps: List[str]) -> str:
    """
    Xây dựng prompt Chain of Thought với các bước suy luận tường minh.
    
    Args:
        function_signature: chữ ký hàm cần implement
        steps: danh sách các bước suy luận
    Returns:
        CoT prompt hoàn chỉnh
    """
    steps_text = "\n".join(f"  Step {i+1}: {s}" for i, s in enumerate(steps))
    
    return f"""CONTEXT: You are a Python expert implementing a financial function.
TASK: Implement the following Python function by following the exact steps below.

FUNCTION: {{{{ {function_signature} }}}}

STEPS TO FOLLOW:
{steps_text}

Important: Return ONLY the Python code implementation. No explanations, no comments.

CODE:"""


def prompt_chaining_demo(initial_code: str) -> Dict[str, str]:
    """
    Minh họa Prompt Chaining: chuỗi 3 prompt cải thiện code từng bước.
    
    Chain:
        1. Tạo code cơ bản
        2. Cải thiện type hints
        3. Chuẩn hóa docstring
    
    Args:
        initial_code: code ban đầu cần cải thiện
    Returns:
        dict với kết quả ở mỗi bước
    """
    results = {"step_0_original": initial_code}
    
    try:
        from openai import OpenAI
        client = OpenAI()
        
        def call_api(prompt: str) -> str:
            r = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=400,
                temperature=0.1
            )
            return r.choices[0].message.content.strip()
        
        # Step 1: Thêm type hints
        prompt1 = f"""
CONTEXT: You are a Python expert.
TASK: Add proper type hints to all function parameters and return values.
      Return ONLY the code, no explanations.
CODE: {{{{{initial_code}}}}}
IMPROVED_CODE:"""
        results["step_1_type_hints"] = call_api(prompt1)
        
        # Step 2: Thêm docstring chuẩn Google style
        prompt2 = f"""
CONTEXT: You are a Python documentation expert.  
TASK: Add a Google-style docstring to the function. Keep existing type hints.
      Return ONLY the code, no explanations.
CODE: {{{{{results["step_1_type_hints"]}}}}}
DOCUMENTED_CODE:"""
        results["step_2_docstring"] = call_api(prompt2)
        
        # Step 3: Thêm error handling
        prompt3 = f"""
CONTEXT: You are a Python expert focused on robustness.
TASK: Add input validation and appropriate error handling. 
      Return ONLY the code, no explanations.
CODE: {{{{{results["step_2_docstring"]}}}}}
ROBUST_CODE:"""
        results["step_3_error_handling"] = call_api(prompt3)
        
    except Exception as e:
        results["error"] = str(e)
    
    return results


# ============================================================
# DEMO
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("LAB 8: Few-Shot Learning")
    print("=" * 60)
    
    # Demo few-shot prompt structure
    print("\n--- Cấu trúc Few-Shot Prompt ---")
    demo_prompt = build_few_shot_prompt(
        task_description="Convert net returns to gross returns.",
        examples=[
            {"input": "-0.20", "output": "0.80"},
            {"input": "0.43", "output": "1.43"},
        ],
        new_input="-0.35",
        input_label="NET",
        output_label="GROSS"
    )
    print(demo_prompt)
    
    print("\n--- Refactor print → logger (Few-Shot) ---")
    result = refactor_print_to_logger_fewshot("print('Error! File not found: passwords.txt')")
    print(f"Input:  print('Error! File not found: passwords.txt')")
    print(f"Output: {result}")
    
    print("\n" + "=" * 60)
    print("LAB 9: Chain of Thought (CoT)")
    print("=" * 60)
    
    # IBM portfolio returns từ sách
    IBM_YEARLY_RETURNS: Dict[str, float] = {
        "2000": -0.2084,
        "2001": 0.4300,
        "2002": -0.3547
    }
    
    print("\n--- Geometric Mean cho Portfolio Returns ---")
    avg = get_average_return_cot(IBM_YEARLY_RETURNS)
    print(f"IBM Returns (2000-2002): {IBM_YEARLY_RETURNS}")
    print(f"Net Average Return: {avg:.1%}")  # -9.9%
    print(f"Giải thích: $1000 → ${1000 * (1 + avg)**3:.0f} sau 3 năm")
    
    # Minh họa tại sao công thức thông thường sai
    naive = ((-0.2084) * 0.43 * (-0.3547)) ** (1/3)
    print(f"\nCông thức sai (naive): {naive:.1%}")  # 32% - SAI!
    print(f"CoT đúng: {avg:.1%}")  # -9.9% - ĐÚNG!
    
    # CoT prompt structure
    print("\n--- CoT Prompt Structure ---")
    cot_prompt = build_cot_prompt(
        "get_average_return(net_returns: Dict[str, float]) -> float",
        [
            "Convert net returns to gross returns by adding 1 to each value",
            "Calculate the geometric mean of the gross returns",
            "Subtract 1 to convert back to net average return",
            "Return the result as float"
        ]
    )
    print(cot_prompt)
