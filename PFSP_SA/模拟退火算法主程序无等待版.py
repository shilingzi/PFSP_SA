import random
import math
import time
#构造计算函数
def calculate_total_time(num_jobs, num_machines, schedule, processing_times):
    machine_time = [0 for _ in range(num_machines)]
    for j in range(num_machines):
        if j == 0:
            machine_time[j] = processing_times[schedule[0]][j]
        else:
            machine_time[j] = machine_time[j - 1] + processing_times[schedule[0]][j]

    for i in range(1, num_jobs):
        compared_time = [0 for _ in range(num_machines)]  # 对每一个工件，构造无间断加工在各机器上的完成时间
        for j in range(num_machines):
            if j == 0:  # 如果经过第一个机器直接算
                compared_time[j] = processing_times[schedule[i]][j]
            else:  # 如果不是，需要用经过上一个机器结束的时间再加上本机器所用时间
                compared_time[j] = compared_time[j - 1] + processing_times[schedule[i]][j]

        the_most_influenced_cost = 0  # 记录需要最多增加多少时间
        for j in range(num_machines):
            if j == 0:
                time_interval = machine_time[j] - 0  # 因为是从0开始的
            else:
                time_interval = machine_time[j] - compared_time[j - 1]  # 上一个工件在本环节加工结束的时间 - 本工件在本环节开始的时间
            if time_interval > the_most_influenced_cost:
                the_most_influenced_cost = time_interval

        for j in range(num_machines):  # 生成新的时间序列
            machine_time[j] = compared_time[j] + the_most_influenced_cost

    # 输出总的时间
    total_time = machine_time[-1]
    return total_time



def simulated_annealing(num_jobs, num_machines, processing_times, initial_temperature=10000, cooling_rate=0.95):
    current_schedule = list(range(num_jobs))  # 初始化解
    current_cost = calculate_total_time(num_jobs, num_machines, current_schedule, processing_times)
    best_schedule = current_schedule
    best_cost = current_cost
    temperature = initial_temperature  # 初始温度

    start_time = time.time()  # 计时开始

    while temperature > 0.1:  # 当温度大于0.1时
        new_schedule = current_schedule.copy()  # 生成新解
        j1, j2 = random.randint(0, num_jobs-1), random.randint(0, num_jobs-1)  # 随机选择两个工作交换
        new_schedule[j1], new_schedule[j2] = new_schedule[j2], new_schedule[j1]
        new_cost = calculate_total_time(num_jobs, num_machines, new_schedule, processing_times)  # 计算新解的成本
        if new_cost < current_cost or random.random() < math.exp((current_cost - new_cost) / temperature):  # 决定是否接受新解
            current_schedule = new_schedule
            current_cost = new_cost
        if current_cost < best_cost:  # 更新最优解
            best_cost = current_cost
            best_schedule = current_schedule
        temperature *= cooling_rate  # 更新温度

    end_time = time.time()  # 计时结束
    consumed_time = end_time - start_time  # 计算运行时间

    return best_cost, best_schedule, consumed_time

def sa_multiple_runs(num_runs, num_jobs, num_machines, processing_times):
    results = []
    for _ in range(num_runs):
        best_cost, best_schedule, consumed_time = simulated_annealing(num_jobs, num_machines, processing_times)
        results.append((best_cost, best_schedule, consumed_time))
    return results
# 设置工作数量、机器数量、处理时间和运行次数
num_jobs = 8
num_machines = 8
processing_times = [[456, 789, 654, 321, 456, 789, 654, 789], [654, 123, 123, 456, 789, 654, 321, 147], [852, 369, 632, 581, 472, 586, 320, 120], [145, 678, 965, 421, 365, 824, 758, 639], [632, 581, 475, 32, 536, 325, 863, 21], [425, 396, 325, 147, 852, 12, 452, 863], [214, 123, 456, 789, 654, 321, 456, 789], [654, 789, 654, 123, 123, 456, 789, 654]]
num_runs = 30
results = sa_multiple_runs(num_runs, num_jobs, num_machines, processing_times)
# 打印结果
for i, result in enumerate(results):
    print(f"Run {i + 1}:")
    print("instance")
    print("We have {} jobs".format(num_jobs))
    print("We have {} machines".format(num_machines))
    print(f"Minimum time required: {result[0]}")
    print(f"Best schedule: {result[1]}")
    print(f"Consumed time: {result[2]} seconds\n")
