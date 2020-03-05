import random


class Stats:
    def __init__(self, company):
        self.reporting_company = company

    def show_design_results(self):
        print('Design Dept')
        self.reporting_company.__design.get_test_results()
        print()
    
    def show_front_results(self):
        print('Front Dept')
        self.reporting_company.__front.get_test_results()
        print()

    def show_back_results(self):
        print('Back Dept')
        self.reporting_company.__back.get_test_results()
        print()

    def show_design_totals(self):
        print('Design Dept')
        self.reporting_company.__design.get_totals()
        print()
    
    def show_front_totals(self):
        print('Front Dept')
        self.reporting_company.__front.get_totals()
        print()

    def show_back_totals(self):
        print('Back Dept')
        self.reporting_company.__back.get_totals()
        print()


class Repository:
    def create_person(self):
        Male_names = ['Alexander', 'Alexey', 'Andrey', 'Boris', 'Petr', 'Vladimir', 'Kirill']
        Male_last_names = ['Ivanov', 'Gozman', 'Kuznetsov', 'Petrov', 'Yakovlev', 'Belokon']
        Female_names = ['Alyona', 'Maria', 'Inna', 'Anastasiya', 'Uliyana']
        Female_last_names = ['Petrova', 'Shulman', 'Vasilyeva', 'Valentinova', 'Rozhkina']
        male_or_female = random.randint(0,1)
        if male_or_female == 1:
            first_name = Male_names[random.randint(0, len(Male_names)-1)]
            last_name = Male_last_names[random.randint(0, len(Male_last_names)-1)]
        else:
            first_name = Female_names[random.randint(0, len(Female_names)- 1)]
            last_name = Female_last_names[random.randint(0, len(Female_last_names)- 1)]
        
        return Employee(first_name, last_name, 0)

    def create_department(self, name, policy, dept):
        department = Department(name, policy, dept)
        for _ in range(5):
            department.add_employee(self.create_person())
        department.set_boss(self.create_person())
        return department
    
    def create_company(self):
        back = self.create_department('Back Dept', LoyalPolicy, dept=None)
        front = self.create_department('Front Dept', StrictPolicy, back)
        design = self.create_department('Design Dept', ModeratePolicy, front)
        company = Company(design, front, back)

        return company


class Company:
    def __init__(self, design, front, back):
        self.__design = design
        self.__front = front
        self.__back = back

    def add_task(self, task):
        self.__design.add_task(task)
    
    def work_at_task(self):
        self.__design.work_at_task()
        self.__front.work_at_task()
        self.__back.work_at_task()
    
    def has_tasks(self):
        return (self.__design.has_tasks() or self.__front.has_tasks() or self.__back.has_tasks())
    

class Department:
    def __init__(self, name, policy, dept):
        self.name = name
        self.policy = policy
        self.__next = dept
        self.boss = 'boss'  # экземпляр класса Employee
        self.__team = {}    # Состав отдела и количество задач у каждого сотрудника
        self.__tasks_in_time = 0
        self.__overdue_tasks = 0
    
    def add_employee(self, employee):
        self.__team[employee] = 0
        employee.add_observer(self)

    def set_boss(self, boss):
        self.__team[boss] = 0
        self.boss = boss

    def has_tasks(self):
        for i in self.__team:
            print(i.tasks, '-', len(i.tasks),  i.first_name, i.last_name)
            if len(i.tasks) > 0:
                return True
        return False

    def add_task(self, task):
        min_employee = None
        for employee in self.__team:
            if min_employee == None:
                min_employee = employee
            elif self.__team[employee] < self.__team[min_employee]:
                min_employee = employee
        min_employee.add_task(task)
        print(min_employee.tasks)
        self.__team[min_employee] += 1
  
    def work_at_task(self):
        if self.has_tasks():
            for employee in self.__team:
                employee.work_at_task()

    def update(self, task):
        if task.act_time > task.plan_time:
            self.policy.fine()
        else:
            self.policy.reward()

        if self.__next:
            self.__next.add_task(task)   

    def get_test_results(self):
        for i in self.__team:
            print(i.first_name, i.last_name, '-', i.kpi, ': Total', self.__team[i])
    
    def get_totals(self):
        print('Всего задач, переданных в отдел: ', self.__tasks_in_time + self.__overdue_tasks)
        print('Задачи, выполненные в срок: ', self.__tasks_in_time)
        print('Просроченные задачи: ', self.__overdue_tasks)
    

class LoyalPolicy:
    @staticmethod
    def reward(dept, employee, task):
        if task.act_time <= task.plan_time:
            employee.kpi += 2
            dept.__tasks_in_time += 2
            if employee != dept.boss:
                dept.boss.kpi += 2

    @staticmethod
    def fine(dept, employee, task):
        if task.act_time > (task.plan_time * 1.5):
            employee.kpi -= 1
            dept.__overdue_tasks += 1
            if employee != dept.boss:
                dept.boss.kpi -= 1


class ModeratePolicy:
    @staticmethod
    def reward(dept, employee, task):
        if task.act_time <= task.plan_time:
            employee.kpi += 1
            dept.__tasks_in_time += 1
            if employee != dept.boss:
                dept.boss.kpi += 1

    @staticmethod
    def fine(dept, employee, task):
        if task.act_time > task.plan_time:
            employee.kpi -= 1
            dept.__overdue_tasks += 1
            if employee != dept.boss:
                dept.boss.kpi -= 1


class StrictPolicy:
    @staticmethod
    def reward(dept, employee, task):
        if task.act_time <= task.plan_time:
            employee.kpi += 1
            dept.__tasks_in_time += 1
            if employee != dept.boss:
                dept.boss.kpi += 1

    @staticmethod
    def fine(dept, employee, task):
        if task.act_time > task.plan_time:
            employee.kpi -= 2
            dept.__overdue_tasks += 1
            if employee != dept.boss:
                dept.boss.kpi -= 2


class Employee:
    def __init__(self, first_name, last_name, kpi):
        self.first_name = first_name
        self.last_name = last_name
        self.kpi = kpi
        self.tasks = []
        self.__observers = []

    def add_task(self, task):
        self.tasks.append(task)

    def work_at_task(self):
        if len(self.tasks) != 0:
            task = self.tasks[0]
            x = random.randint(0, 100)
            task.act_time += 1
            if x < 100 - task.complexity:
                del self.tasks[0]
                for observer in self.__observers:
                    observer.update(self, task)
    
    def add_observer(self, observer):
        self.__observers.append(observer)

    def remove_observer(self, observer):
        self.__observers.remove(observer)


class Task:
    def __init__(self, plan_time,complexity):
        self.plan_time = plan_time
        self.act_time = 0
        self.complexity = complexity

    def show_act_time(self):
        return self.act_time
    
    def show_plan_time(self):
        return self.plan_time
    
    def show_complexity(self):
        return self.complexity

