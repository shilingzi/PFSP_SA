import matplotlib.pyplot as plt

def draw_gantt_chart(num_jobs, num_machines, processing_times, schedule):
    # 计算每台机器上每个作业的开始和结束时间
    start_times = [[0] * num_machines for _ in range(num_jobs)]
    end_times = [[0] * num_machines for _ in range(num_jobs)]

    for i in range(num_jobs):
        for j in range(num_machines):
            job = schedule[i]  # 获取当前工作序列中的工作
            if i == 0 and j == 0:
                start_times[job][j] = 0
            elif i == 0:
                start_times[job][j] = end_times[job][j - 1]
            elif j == 0:
                start_times[job][j] = end_times[schedule[i - 1]][j]
            else:
                start_times[job][j] = max(end_times[job][j - 1], end_times[schedule[i - 1]][j])

            end_times[job][j] = start_times[job][j] + processing_times[job][j]

    # 创建甘特图
    fig, ax = plt.subplots()

    for j in range(num_machines):
        for i in range(num_jobs):
            job = schedule[i]
            ax.barh(j, processing_times[job][j], left=start_times[job][j], color=f"C{job % 10}")

    ax.set_xlabel("Time")
    ax.set_ylabel("Machine")
    ax.set_title("Gantt Chart")
    ax.set_yticks(range(num_machines))
    ax.legend([f"Job {schedule[i]}" for i in range(num_jobs)])

    plt.show()

# 样例数据
num_jobs = 11
num_machines = 5
processing_times =[[375, 12, 142, 245, 412], [632, 452, 758, 278, 398], [12, 876, 124, 534, 765], [460, 542, 523, 120, 499], [528, 101, 789, 124, 999], [796, 245, 632, 375, 123], [532, 230, 543, 896, 452], [14, 124, 214, 543, 785], [257, 527, 753, 210, 463], [896, 896, 214, 258, 259], [532, 302, 501, 765, 988]]
schedule =[7, 4, 8, 0, 2, 6, 3, 10, 9, 5, 1]#作业顺序
#绘制甘特图
draw_gantt_chart(num_jobs, num_machines, processing_times, schedule)
