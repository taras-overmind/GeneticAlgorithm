import random
from dataclasses import dataclass

POPULATION_SIZE = 100
MUTATION_RATE = 0.1
GENERATIONS = 100

SUBJECTS = ['IS', 'Mobile platforms', 'IT', 'MPC', 'MSM', 'Management']
TEACHERS = ['Omelchuk', 'Trotsenko', 'Tkachenko', 'Voloshyn', 'Shyshatska', 'Polyshcuk']
GROUPS = ['TK-41', 'TK-42', 'TTP-41', 'TTP-42', 'MI-41', 'MI-42']
CLASSES_PER_DAY = 5

@dataclass
class Lecture:   # Цей клас представляє один заняття в розкладі з визначеним предметом, викладачем, групою та часом.
    subject: str
    teacher: str
    group: str
    time: int


class GeneticScheduler:
    def __init__(self, subjects, teachers, groups, classes_per_day): # Ініціалізація об'єкта з вхідними даними розкладу.
        self.subjects = subjects
        self.teachers = teachers
        self.groups = groups
        self.classes_per_day = classes_per_day

    def generate_random_schedule(self):
        schedule = []
        for subject in self.subjects:
            time = random.randint(1, self.classes_per_day)
            teacher = random.choice(self.teachers)
            group = random.choice(self.groups)
            schedule.append(Lecture(subject, teacher, group, time))
        return schedule

    def generate_random_population(self, population_size):
        population = []
        for i in range(population_size):
            population.append(self.generate_random_schedule())
        return population

    @staticmethod
    def calculate_fitness(schedule):
        conflicts = 0
        for i in range(len(schedule)):
            for j in range(i + 1, len(schedule)):
                if schedule[i].time == schedule[j].time:
                    conflicts += 1
                if schedule[i].teacher == schedule[j].teacher:
                    conflicts += 1
                if schedule[i].group == schedule[j].group:
                    conflicts += 1
        print(f'Conflicts: {conflicts}, Fitness: {1.0/(1.0+conflicts)}')
        return 1.0 / (conflicts + 1.0)


    def mutate(self, schedule):
        for i in range(len(schedule)):
            if random.random() < MUTATION_RATE:
                time = random.randint(1, self.classes_per_day)
                teacher = random.choice(self.teachers)
                group = random.choice(self.groups)
                subject = schedule[i].subject
                schedule[i] = Lecture(subject, teacher, group, time)
        return schedule


    def crossover(self, schedule1, schedule2):
        crossover_point = random.randint(1, len(self.subjects) - 1)
        return schedule1[:crossover_point] + schedule2[crossover_point:], schedule2[:crossover_point] + schedule1[
                                                                                                        crossover_point:]

    @staticmethod
    def select_best(population, fitness_scores):
        best = None
        best_score = 0
        for i in range(len(population)):
            if fitness_scores[i] > best_score:
                best = population[i]
                best_score = fitness_scores[i]
        return best

    def solve(self):
        population = self.generate_random_population(POPULATION_SIZE) # Він ініціалізує популяцію, оцінює її "здоров'я",
        best_schedule = [] #вибирає найкращі розклади для схрещування та мутації, і повторює цей процес
        for _ in range(GENERATIONS): # для вказаної кількості поколінь.
            fitness_scores = [GeneticScheduler.calculate_fitness(schedule) for schedule in population]
            best_schedule = GeneticScheduler.select_best(population, fitness_scores)
            new_population = []
            while len(new_population) < POPULATION_SIZE:
                parent1 = random.choices(population, weights=fitness_scores)[0]
                parent2 = random.choices(population, weights=fitness_scores)[0]
                child1, child2 = self.crossover(parent1, parent2)
                child1 = self.mutate(child1)
                child2 = self.mutate(child2)
                new_population.append(child1)
                new_population.append(child2)
            population = new_population
        return best_schedule, GeneticScheduler.calculate_fitness(best_schedule)


if __name__ == '__main__':
    scheduler = GeneticScheduler(SUBJECTS, TEACHERS, GROUPS, CLASSES_PER_DAY)
    best_schedule, fitness = scheduler.solve()
    print('Best schedule:')
    for lesson in best_schedule:
        print(lesson)
    print(f'Fitness score: {fitness}')
