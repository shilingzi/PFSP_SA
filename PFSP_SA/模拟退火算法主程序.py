import random
import math
import time

def pfsp_sa(num_jobs, num_machines, processing_times):
    # 开始计时
    start_time = time.time()

    # 通过调用随机函数来初始化
    initial_solution = list(range(num_jobs))
    random.shuffle(initial_solution)
    best_solution = initial_solution.copy()

    # 定义计算函数
    def calculate_total_time(sequence):
        completion_times = [[0] * num_machines for _ in range(num_jobs)]
        for i in range(num_jobs):
            for j in range(num_machines):
                if i == 0 and j == 0:
                    completion_times[i][j] = processing_times[sequence[i]][j]
                elif i == 0:
                    completion_times[i][j] = completion_times[i][j-1] + processing_times[sequence[i]][j]
                elif j == 0:
                    completion_times[i][j] = completion_times[i-1][j] + processing_times[sequence[i]][j]
                else:
                    completion_times[i][j] = max(completion_times[i][j-1], completion_times[i-1][j]) + processing_times[sequence[i]][j]
        return completion_times[-1][-1]

    # 设置初始温度和退火比率
    temperature = 10000
    cooling_rate = 0.95

    # 初始化最优解
    best_energy = calculate_total_time(best_solution)

    # 持续模拟退火，直到温度小于0.1
    while temperature > 0.1:
        # 生成一个新解
        new_solution = best_solution.copy()
        i = random.randint(0, num_jobs-1)
        j = random.randint(0, num_jobs-1)
        new_solution[i], new_solution[j] = new_solution[j], new_solution[i]

        # 计算当前解和新解所需的步数
        current_energy = calculate_total_time(best_solution)
        new_energy = calculate_total_time(new_solution)

        # 决定是否接受新的解决方案
        if new_energy < current_energy:
            best_solution = new_solution.copy()
            best_energy = new_energy
        else:
            probability = math.exp((current_energy - new_energy) / temperature)
            if random.random() < probability:
                best_solution = new_solution.copy()

        # 更新温度
        temperature *= cooling_rate

    # 停止计时
    end_time = time.time()
    # 计算运行时间
    consumed_time = end_time - start_time

    return best_energy, best_solution, consumed_time

def pfsp_sa_runs(num_runs, num_jobs, num_machines, processing_times):
    results = []
    for _ in range(num_runs):
        min_time, best_schedule, consumed_time = pfsp_sa(num_jobs, num_machines, processing_times)
        results.append((min_time, best_schedule, consumed_time))
    return results
# 设置工作数量、机器数量、处理时间和运行次数
num_jobs = 11
num_machines = 5
processing_times =[[375, 12, 142, 245, 412], [632, 452, 758, 278, 398], [12, 876, 124, 534, 765], [460, 542, 523, 120, 499], [528, 101, 789, 124, 999], [796, 245, 632, 375, 123], [532, 230, 543, 896, 452], [14, 124, 214, 543, 785], [257, 527, 753, 210, 463], [896, 896, 214, 258, 259], [532, 302, 501, 765, 988]]
num_runs = 30
results = pfsp_sa_runs(num_runs, num_jobs, num_machines, processing_times)
# 打印结果
for i, (min_time, best_schedule, consumed_time) in enumerate(results):
    print(f"Run {i+1}:")
    print("instance")
    print("We have {} jobs".format(num_jobs))
    print("We have {} machines".format(num_machines))
    print("Minimum time required:", min_time)
    print("Best schedule:", best_schedule)
    print("Consumed time:", consumed_time, "seconds")
