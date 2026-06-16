# prox_algorithm
2026 计算复杂性第三次作业：近似算法

探索 MAX-3SAT 和 Metric TSP 两个经典 NP 难组合优化问题。

## 环境要求

- Python 3.11+

## 运行方法

### 生成随机 MAX-3SAT 公式

```bash
python src/max3sat/generate_random_3sat.py
```

使用 `test/max3sat/random_config.txt` 配置文件。自定义配置文件和输出目录：

```bash
python src/max3sat/generate_random_3sat.py -c test/max3sat/random_config.txt -o test/max3sat
```

### 通过随机采样求解 MAX-3SAT 公式

```bash
python src/max3sat/random_solve_max3sat.py -i test/max3sat/random_8_20.txt
```

指定随机种子以保证结果可重现：

```bash
python src/max3sat/random_solve_max3sat.py -i test/max3sat/random_8_20.txt -s 42
```

### 求解 METRIC-TSP（2-近似算法）

```bash
python src/metric_tsp/solve_metric_tsp.py -i test/metric_tsp/sample.txt
```

指定根节点：

```bash
python src/metric_tsp/solve_metric_tsp.py -i test/metric_tsp/sample.txt -r a
```

运行自定义测试用例：

```bash
python src/metric_tsp/solve_metric_tsp.py -i test/metric_tsp/custom.txt
```
