import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

def draw_gantt_chart(num_jobs, num_machines, schedule, processing_times):
    start_times = []

    machine_time = [0 for _ in range(num_machines)]
    start_tmp = []

    for j in range(num_machines):  # 先将第一个工件加工完成
        if j == 0:
            machine_time[j] = processing_times[schedule[0]][j]
        else:
            machine_time[j] = machine_time[j - 1] + processing_times[schedule[0]][j]

        start_tmp.append(machine_time[j] - processing_times[schedule[0]][j])
    start_times.append(start_tmp)

    for i in range(1, num_jobs):  # 考虑剩下的工件
        start = []
        compared_time = [0 for _ in range(num_machines)]  # 对每一个工件，构造无间断加工在各机器上的完成时间
        for j in range(num_machines):
            if j == 0:  # 如果经过的第一个机器直接算
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
            start.append(machine_time[j] - processing_times[schedule[i]][j])
        start_times.append(start)

    m = range(num_jobs)  # 工件数
    n = range(num_machines)  # 机器个数
    # 创建绘图实例
    fig, ax = plt.subplots()

    for i in n:  # 以机器（工序）为行
        for j in m:  # 每一个颜色代表一个工件
            ax.barh(n[i], processing_times[schedule[j]][i], left=start_times[j][i], color=f"C{j % 10}")

    labels = [''] * len(processing_times)

    for f in m:
        labels[f] = f"Job {schedule[f]}"
    patches = [mpatches.Patch(color=f"C{i % 10}", label="{:s}".format(labels[i])) for i in range(len(processing_times))]
    ax.legend(handles=patches)
    ax.set_yticks(range(num_machines))
    ax.set_title("Gantt Chart")
    ax.set_xlabel("Time")
    ax.set_ylabel("Machine")

    plt.show()


# 设置参数
num_jobs = 8
num_machines = 8
processing_times = [[456, 789, 654, 321, 456, 789, 654, 789], [654, 123, 123, 456, 789, 654, 321, 147], [852, 369, 632, 581, 472, 586, 320, 120], [145, 678, 965, 421, 365, 824, 758, 639], [632, 581, 475, 32, 536, 325, 863, 21], [425, 396, 325, 147, 852, 12, 452, 863], [214, 123, 456, 789, 654, 321, 456, 789], [654, 789, 654, 123, 123, 456, 789, 654]]
schedule = [5, 7, 4, 1, 6, 3, 0, 2]
#绘制甘特图
draw_gantt_chart(num_jobs, num_machines, schedule, processing_times)
