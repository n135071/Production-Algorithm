# قراءة الملف tasks.txt
with open("tasks.txt", "r") as file:
    tasks_data = file.readlines()

# قراءة الملف tasks_links.txt
with open("tasks_links.txt", "r") as file:
    links_data = file.readlines()

# قوائم لتخزين البيانات
tasks = []
links = []

# معالجة بيانات المهام
for line in tasks_data:
    task_id, task_time = line.strip().split(",")
    tasks.append((int(task_id), int(task_time)))

# معالجة بيانات الروابط بين المهام
for line in links_data:
    source, target = line.strip().split(",")
    links.append((int(source), int(target)))


def generate_permutations(tasks, steps):
    if steps == 1:
        return [[task] for task in tasks]
    else:
        permutations = []
        for task in tasks:
            remaining_tasks = [t for t in tasks if t != task]
            sub_permutations = generate_permutations(remaining_tasks, steps - 1)
            for sub_permutation in sub_permutations:
                permutations.append([task] + sub_permutation)
        return permutations


def check_conditions(perm):
    for link in links:
        source, target = link
        if source in perm and target in perm:
            if perm.index(source) > perm.index(target):
                return False
    return True


def calculate_total_time(perm):
    total_time = 0
    for task in perm:
        total_time += task[1]
    return total_time


def calculate_differences(perm, avg_time):
    total_diff = 0
    for task in perm:
        diff = abs(task[1] - avg_time)
        total_diff += diff
    return total_diff


def solve_problem(steps):
    all_permutations = generate_permutations(tasks, steps)
    all_results = []

    for perm in all_permutations:
        if check_conditions(perm):
            total_time = calculate_total_time(perm)
            avg_time = total_time / steps
            total_diff = calculate_differences(perm, avg_time)
            all_results.append((perm, total_time, avg_time, total_diff))

    return all_results


steps = 3
results = solve_problem(steps)
# كتابة النتائج إلى ملف
with open("all_results_steps.txt", "w") as file:
    for i, result in enumerate(results, start=1):
        perm, total_time, avg_time, total_diff = result
        file.write(f"\nSolution {i}:\n")
        for j, task in enumerate(perm, start=1):
            file.write(
                f"{j} : {task[0]} Total Time=({task[1]}), dif={abs(task[1]-avg_time):.2f}\n"
            )
        file.write(f"Total Time= {total_time}\n")

    file.write(f"\nTotal Time= {results[0][1]}\n")
    file.write(f"Total_time/Steps = {results[0][1] / steps:.2f}\n")
    file.write(f"Total differences = {results[0][3]:.2f}\n")
    file.write(f"Average differences = {results[0][3] / steps:.2f}\n")
    file.write(f"Max Time = {max(results, key=lambda x: x[1])[1]}\n")
    file.write(f"Min Time = {min(results, key=lambda x: x[1])[1]}\n")

    for i, result in enumerate(results, start=1):
        perm, total_time, _, _ = result
        file.write(f"\nSolution {i}:\n")
        for j, task in enumerate(perm, start=1):
            file.write(f"{j} : {task[0]} {task[1]}\n")
        file.write(f"Total Time = {total_time}\n")
