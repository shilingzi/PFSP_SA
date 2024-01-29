import random
import math
import time
import matplotlib.pyplot as plt


def pfsp_sa(num_jobs, num_machines, processing_times, temperature, cooling_rate):
    start_time = time.time()

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

    best_energy = calculate_total_time(best_solution)

    while temperature > 0.1:
        new_solution = best_solution.copy()
        i = random.randint(0, num_jobs-1)
        j = random.randint(0, num_jobs-1)
        new_solution[i], new_solution[j] = new_solution[j], new_solution[i]

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

        temperature *= cooling_rate

    end_time = time.time()
    consumed_time = end_time - start_time# 计算运行时间

    return best_energy, best_solution, consumed_time


def pfsp_sa_runs(num_runs, num_jobs, num_machines, processing_times, temperature, cooling_rate):
    results = []
    for _ in range(num_runs):
        min_time, best_schedule, consumed_time = pfsp_sa(num_jobs, num_machines, processing_times, temperature, cooling_rate)
        results.append((min_time, best_schedule, consumed_time))
    return results


def run_experiment(num_runs, num_jobs, num_machines, processing_times):
    temperatures = [10000, 5000, 1000]
    cooling_rates = [0.95, 0.8, 0.7,0.6,0.5]

    results = {}

    for temp in temperatures:
        for rate in cooling_rates:
            results[(temp, rate)] = pfsp_sa_runs(num_runs, num_jobs, num_machines, processing_times, temp, rate)

    return results

#可视化实验结果
def visualize_results(results):
    temperatures = [key[0] for key in results.keys()]
    cooling_rates = [key[1] for key in results.keys()]
    avg_times = [sum(run[0] for run in results[key])/len(results[key]) for key in results.keys()]

    plt.figure(figsize=(10, 4))

    plt.subplot(121)  # 创建一个1行2列的子图，并开始绘制第一个子图
    plt.scatter(temperatures, avg_times)
    for i in range(len(temperatures)):
        plt.annotate(f'CR: {cooling_rates[i]}, AT: {avg_times[i]:.2f}',
                     (temperatures[i], avg_times[i]),
                     textcoords="offset points",
                     xytext=(-10,-10),
                     ha='center')
    plt.xlabel('Temperature')
    plt.ylabel('Average Time')
    plt.title('Temperature vs Average Time')

    plt.subplot(122)  # 开始绘制第二个子图
    plt.scatter(cooling_rates, avg_times)
    for i in range(len(cooling_rates)):
        plt.annotate(f'T: {temperatures[i]}, AT: {avg_times[i]:.2f}',
                     (cooling_rates[i], avg_times[i]),
                     textcoords="offset points",
                     xytext=(-10,-10),
                     ha='center')
    plt.xlabel('Cooling Rate')
    plt.ylabel('Average Time')
    plt.title('Cooling Rate vs Average Time')

    plt.tight_layout()  # 自动调整子图间的间距
    plt.show()



# 设置工作数量、机器数量、处理时间和运行次数
num_jobs = 11
num_machines = 5
processing_times = [[375, 12, 142, 245, 412], [632, 452, 758, 278, 398], [12, 876, 124, 534, 765], [460, 542, 523, 120, 499], [528, 101, 789, 124, 999], [796, 245, 632, 375, 123], [532, 230, 543, 896, 452], [14, 124, 214, 543, 785], [257, 527, 753, 210, 463], [896, 896, 214, 258, 259], [532, 302, 501, 765, 988]]
num_runs = 30

results = run_experiment(num_runs, num_jobs, num_machines, processing_times)
visualize_results(results)







