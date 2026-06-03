import random
import argparse
import os


def parse_config(config_path):
    config = {}
    with open(config_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            parts = line.split()
            if len(parts) < 2:
                continue
            key, value = parts[0], parts[1]
            config[key] = value
    return config


def generate_3sat(num_vars, num_clauses, seed):
    rng = random.Random(seed)
    clauses = []
    for _ in range(num_clauses):
        vars_in_clause = rng.sample(range(1, num_vars + 1), 3)
        clause = []
        for v in vars_in_clause:
            if rng.random() < 0.5:
                clause.append(f"x{v}")
            else:
                clause.append(f"-x{v}")
        clauses.append(clause)
    return clauses


def main():
    parser = argparse.ArgumentParser(description="Generate random MAX-3SAT formula")
    parser.add_argument("--config", "-c",
                        default=os.path.join("test", "max3sat", "random_config.txt"),
                        help="Path to config file")
    parser.add_argument("--output-dir", "-o", default=None,
                        help="Output directory (overrides config output_file's base)")
    args = parser.parse_args()

    config = parse_config(args.config)
    num_vars = int(config.get("number_of_variables", 8))
    num_clauses = int(config.get("number_of_clauses", 20))
    seed = int(config.get("seed", 2026))
    output_file = config.get("output_file", f"random_{num_vars}_{num_clauses}.txt")

    clauses = generate_3sat(num_vars, num_clauses, seed)

    if args.output_dir:
        output_path = os.path.join(args.output_dir, output_file)
    else:
        config_dir = os.path.dirname(args.config)
        output_path = os.path.join(config_dir, output_file)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, 'w') as f:
        for clause in clauses:
            f.write(' '.join(clause) + '\n')


if __name__ == "__main__":
    main()
