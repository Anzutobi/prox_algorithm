import random
import time
import argparse
import os


def parse_literal(lit):
    if lit.startswith('-x'):
        return int(lit[2:]), False
    else:
        return int(lit[1:]), True


def parse_formula(filepath):
    clauses = []
    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            clause = [parse_literal(lit) for lit in line.split()]
            clauses.append(clause)
    return clauses


def count_satisfied(assignment, clauses):
    count = 0
    satisfied_indices = []
    for idx, clause in enumerate(clauses):
        satisfied = False
        for var, is_positive in clause:
            if assignment[var] == is_positive:
                satisfied = True
                break
        if satisfied:
            count += 1
            satisfied_indices.append(idx + 1)
    return count, satisfied_indices


def solve(filepath, seed=None):
    clauses = parse_formula(filepath)

    num_vars = max(abs(var) for clause in clauses for var, _ in clause)
    num_clauses = len(clauses)
    target = (num_clauses * 7 + 7) // 8

    if seed is not None:
        rng = random.Random(seed)
    else:
        rng = random.Random()

    start = time.perf_counter()
    loop_count = 0
    best_assignment = None
    best_count = 0
    best_indices = []

    while True:
        loop_count += 1
        assignment = {v: rng.choice([True, False]) for v in range(1, num_vars + 1)}
        satisfied_count, satisfied_indices = count_satisfied(assignment, clauses)

        if satisfied_count > best_count:
            best_count = satisfied_count
            best_assignment = assignment
            best_indices = satisfied_indices

        if satisfied_count >= target:
            break

    elapsed = time.perf_counter() - start

    return best_assignment, best_count, best_indices, target, num_vars, num_clauses, clauses, loop_count, elapsed


def format_clause(clause):
    return '(' + ' v '.join(
        f"x{var}" if is_pos else f"~x{var}"
        for var, is_pos in clause
    ) + ')'


def output_result(assignment, satisfied_count, satisfied_indices, target,
                  num_vars, num_clauses, clauses, loop_count, elapsed, filepath):
    formula_str = ' ∧ '.join(format_clause(c) for c in clauses)

    print("输入公式：")
    print(formula_str)
    print(f"变量数量：{num_vars}")
    print(f"子句数量：{num_clauses}")
    print(f"目标满足子句数量：{target}")
    print("找到的变量赋值：")
    for v in range(1, num_vars + 1):
        print(f"x{v} = {'True' if assignment[v] else 'False'}")
    print(f"满足的子句数量：{satisfied_count} / {num_clauses}")
    print("满足的子句编号：" + ', '.join(f"C{i}" for i in satisfied_indices))
    print(f"随机循环次数：{loop_count}")
    print(f"运行时间：{elapsed:.4f} 秒")


def main():
    parser = argparse.ArgumentParser(description="Solve MAX-3SAT via random sampling")
    parser.add_argument("--input", "-i", required=True,
                        help="Input formula file")
    parser.add_argument("--seed", "-s", type=int, default=None,
                        help="Random seed")
    args = parser.parse_args()

    assignment, satisfied_count, satisfied_indices, target, \
        num_vars, num_clauses, clauses, loop_count, elapsed = solve(args.input, args.seed)

    output_result(assignment, satisfied_count, satisfied_indices, target,
                  num_vars, num_clauses, clauses, loop_count, elapsed, args.input)


if __name__ == "__main__":
    main()
