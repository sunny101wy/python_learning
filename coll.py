
import matplotlib.pyplot as plt

# 定义 Collatz 轨迹函数
def collatz_sequence(n):
    seq = [n]
    while n != 1:
        if n % 2 == 0:
            n //= 2
        else:
            n = 3 * n + 1
        seq.append(n)
    return seq

# 定义绘图函数
def plot_collatz_trajectories(start=1, end=1000):
    plt.figure(figsize=(18, 10))
    for n in range(start, end + 1):
        seq = collatz_sequence(n)
        plt.plot(range(len(seq)), seq, linewidth=0.5)

    plt.title(f"Collatz 序列轨迹图（起始值 {start} 到 {end}）", fontsize=16)
    plt.xlabel("步数 Step", fontsize=14)
    plt.ylabel("当前值", fontsize=14)
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# 执行函数，画出 1 到 1000 的图像
plot_collatz_trajectories(1, 1000)
