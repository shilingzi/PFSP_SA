def process_file(file_path):
    instances = {}

    # 打开文件并读取所有行
    with open(file_path, 'r') as file:
        lines = file.read().splitlines() # 按行分割

    # 解析单个示例
    def parse_instance(lines):
        processing_times = []
        for line in lines:
            values = line.split()
            # 获取任务处理时间，从索引1开始，步长为2（只获取数字，忽略文字）
            job_times = [int(values[i]) for i in range(1, len(values), 2)]
            # 只有在任务处理时间列表不为空时才追加
            if job_times:
                processing_times.append(job_times)
        return processing_times

    i = 0
    while i < len(lines):
        # 查找以"instance"开头的行
        if lines[i].startswith("instance"):
            instance_name = lines[i]
            i += 2  # 跳过 "instance"行及其后的空行
            instance_lines = []
            while i < len(lines) and not lines[i].startswith("instance"):
                # 忽略空行
                if lines[i].strip():
                    instance_lines.append(lines[i])
                i += 1
            # 解析示例并保存结果
            instances[instance_name] = parse_instance(instance_lines)
        else:
            i += 1

    return instances


# 需要处理的文件路径
file_path = "最优化方法大作业-2023-无等待置换流水车间调度-4道题目.txt"
instances = process_file(file_path)

# 以写入模式打开输出文件
with open("output.txt", "w") as output_file:
    for instance_name, instance_data in instances.items():
        # 将示例数据写入文件
        output_file.write(f"{instance_name}:\n")
        output_file.write(f"{instance_data}\n\n")
