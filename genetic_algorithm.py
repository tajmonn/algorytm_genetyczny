from random import choice, uniform
from numpy import mean


# kodawanie binarne
# 0 - znak liczby, 1-(binary_length-1) - liczba w kodzie binarnym
def encode(x, binary_length):
    x_sign = 0 if x > 0 else 1  # 0 - znak liczby dodatni, 1 - znak liczby ujemny
    x_abs = abs(x)  # wartosc bezwzgledna

    # zamiana na binarny
    reminder_bin = []
    while x_abs > 0:
        reminder_bin.append(reminder_int % 2)
        reminder_int = reminder_int // 2

    # dodanie zer do listy, aby wybrana długość zakodowanego osobnika była spełniona pamiętając o pierwszym bicie - znaku
    while len(reminder_bin) < binary_length - 1:
        reminder_bin.append(0)

    # odwrócenie listy - największa potęga na początku
    reminder_bin.reverse()

    # zwrócenie listy z zakodowaną liczbą
    encoded = [x_sign] + reminder_bin
    return encoded


# dekodowanie binarne
def decode(listed):
    sign = (-1) ** listed[0]  # znak liczby
    r = len(listed)  # długość listy
    # liczba binarna zamieniona na dziesiętną
    summ = 0
    for i in range(1, r):
        summ += listed[i] * 2 ** (r - i - 1)
    # zwrócenie liczby z uwzględnieniem znaku
    return sign * summ


# wybór populacji początkowej - losowe osobniki
def initial_population(population_size, binary_length):
    # inicjalizacja populacji początkowej losowymi osobnikami
    population = []
    for _ in range(population_size):
        individual = [
            choice([0, 1]) for _ in range(binary_length)
        ]  # losowy osobnik o długości binary_length
        population.append(individual)
    return population


# ocena osobników
def evaluate(population, function):
    # obliczenie wartości funkcji dla każdego osobnika
    # zwrócenie listy wartości funkcji dla każdego osobnika
    evaluated = []
    for individual in population:
        x = decode(individual)
        evaluated.append(function(x))

    return evaluated


# sprawdzenie warunku stopu
def stop_condition(evaluated, stop_value, old_value):
    # sprawdzenie odległości skarnych wartości ocen osobników
    # zwrócenie True jeśli odległość jest mniejsza od stop_value, False jeśli nie
    new_value = mean(evaluated)
    if abs(new_value - old_value) <= stop_value:
        return True, new_value

    return False, new_value


# selekcja osobników metodą ruletki
def selection(evaluated, population, population_size):
    # obliczenie prawdopodobieństwa wyboru każdego osobnika
    # zwrócenie listy prawdopodobieństw wyboru każdego osobnika
    evaluated_sum = sum(evaluated)
    probabilities = [
        x / evaluated_sum for x in evaluated
    ]  # lista prawdopodobieństw wyboru każdego osobnika
    # log
    with open("log.txt", "a") as f:
        maxi = evaluated.index(max(evaluated))
        mini = evaluated.index(min(evaluated))

        occurrence_dict = {}

        for item in evaluated:
            if item in occurrence_dict:
                occurrence_dict[item] += 1
            else:
                occurrence_dict[item] = 1

        f.write(
            "max: "
            + str(probabilities[maxi])
            + " "
            + str(decode(population[maxi]))
            + " "
            + str(population[maxi])
            + " "
            + "min: "
            + str(probabilities[mini])
            + " "
            + str(decode(population[mini]))
            + " "
            + str(population[mini])
            + " "
            + str(evaluated_sum)
            + "\n"
            + str(occurrence_dict)
            + "\n"
        )

    selected = []
    for _ in range(population_size):
        # wybór osobnika na podstawie prawdopodobieństwa
        # dodawanie kolejnych prawdopodobieństw aż ich suma przekroczy (lub zrówna się) w losowa liczba z przedziału [0,1]
        random_number = uniform(0, 1)
        length = 0
        for inviduals_number in range(population_size):
            length += probabilities[inviduals_number]
            if random_number <= length:
                selected.append(population[inviduals_number].copy())
                break

    # zwrócenie listy wybranych osobników
    return selected


# krzyżowanie osobników (jednolite)
def crossover(selected, crossover_probability, binary_length):
    crossed = []
    for _ in range(len(selected) // 2):
        # wybór dwóch osobników z listy wybranych i usunięcie ich z tej listy
        parent1 = choice(selected)
        selected.remove(parent1)
        parent2 = choice(selected)
        selected.remove(parent2)

        # sprawdzenie czy osobniki się NIE krzyżują z prawdopodobieństwem crossover_probability
        if (
            uniform(0, 1) > crossover_probability
        ):  # jeżeli się nie krzyżują to są dodawane do listy skrzyżowanych
            crossed.append(parent1)
            crossed.append(parent2)
            continue  # przejście do następnej iteracji

        # stworzenie maski krzyżowania
        crossover_mask = [choice([0, 1]) for _ in range(binary_length)]
        for bit in range(binary_length):
            if (
                crossover_mask[bit] == 1
            ):  # jeżeli bit maski jest równy 1 to zamieniane są bity w osobnikach
                parent1[bit], parent2[bit] = parent2[bit], parent1[bit]

        # dodanie skrzyżowanych osobników do listy skrzyżowanych
        crossed.append(parent1)
        crossed.append(parent2)

    # zwrot listy skrzyżowanych osobników
    return crossed


# mutacja osobników
def mutation(population, mutation_probability, binary_length):
    for individual in population:  # dla każdego osobnika w populacji
        for bit in range(binary_length):  # dla każdego bitu w osobniku
            if (
                uniform(0, 1) < mutation_probability
            ):  # jeżeli prawdopodobieństwo mutacji jest większe od losowej liczby z przedziału [0,1]
                # to zamieniany jest bit na przeciwny
                individual[bit] = 1 - individual[bit]
    # zwrócenie zmutowanej populacji
    return population


# wyprowadzenie najlepszego osobnika
def best_individual(population, evaluated):
    # zwrócenie najlepszego osobnika
    return population[evaluated.index(max(evaluated))]


def genetic_algorithm(
    function,
    population_size,
    binary_length,
    stop_value,
    crossover_probability,
    mutation_probability,
    old_value,
):
    # pierwsze przejście algorytmu do warunku stopu

    # inicjalizacja populacji początkowej
    population = initial_population(population_size, binary_length)

    # ocena
    evaluated = evaluate(population, function)
    # sprawdzenie warunku stopu
    stop, old_value = stop_condition(evaluated, stop_value, old_value)
    if stop:  # jeżeli warunek stopu jest spełniony to zwracany jest najlepszy osobnik
        return best_individual(population, evaluated)
    # w przeciwnym wypadku algorytm przechodzi do pętli głównej
    # pętla główna
    while not stop:
        # selekcja
        selected = selection(evaluated, population, population_size)
        # krzyżowanie
        crossed = crossover(selected, crossover_probability, binary_length)
        # mutacja
        mutated = mutation(crossed, mutation_probability, binary_length)
        # ocena
        evaluated = evaluate(mutated, function)  # (mutated, function)
        # sprawdzenie warunku stopu
        stop, old_value = stop_condition(evaluated, stop_value, old_value)
        # aktualizacja populacji
        population = mutated

    # zwrócenie najlepszego osobnika
    return best_individual(population, evaluated)


# funkcja do optymalizacji
def funtion_to_optimize(x):
    return -((x + 7) ** 2) / 100 + 10


# uruchomienie algorytmu
if __name__ == "__main__":
    old_value = 0
    function = funtion_to_optimize  # funkcja do optymalizacji
    population_size = 1000  # rozmiar populacji
    binary_length = 5  # długość zakodowanego osobnika
    stop_value = 0.001  # odległość skrajnych wartości ocen osobników
    crossover_probability = 0.50  # prawdopodobieństwo krzyżowania
    mutation_probability = 0.01  # prawdopodobieństwo mutacji dla każdego bitu
    best = genetic_algorithm(
        function,
        population_size,
        binary_length,
        stop_value,
        crossover_probability,
        mutation_probability,
        old_value,
    )
    print(best)
    print(decode(best))
