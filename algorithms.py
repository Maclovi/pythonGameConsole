import random
import time


def test(func, *params):
    start = time.time()
    func(*params)
    print(f"{time.time() - start:.10f}")


class Search:
    @classmethod
    def binary_search(cls, lst, item):
        low = 0
        high = len(lst) - 1
        while low <= high:
            middle = (low + high) // 2
            if lst[middle] == item:
                return middle
            if item > lst[middle]:
                low = middle + 1
            else:
                high = middle - 1


class Sort:
    @classmethod
    def intersection_sort(cls, lst):
        def find_min_elem(lst2):
            element = lst2[0]
            position = 0
            for i in range(len(lst2)):
                if lst2[i] < element:
                    element = lst2[i]
                    position = i
            return position, element

        lst = lst.copy()
        sort_result = []
        while lst:
            index, elem = find_min_elem(lst)
            del lst[index]
            sort_result.append(elem)

        return sort_result

    @classmethod
    def quick_sort(cls, lst):
        if len(lst) < 2:
            return lst
        pivot = lst.pop(random.randrange(len(lst)))
        less = list(filter(lambda x: x <= pivot, lst))
        greater = list(filter(lambda x: x > pivot, lst))
        return cls.quick_sort(less) + [pivot] + cls.quick_sort(greater)


class Fibonacci:
    @staticmethod
    def cache(func):
        cash = {}

        def wrapper(*args, **kwargs):
            nonlocal cash
            n = args[0]
            if n not in cash:
                cash[n] = func(*args, **kwargs)
            return cash[n]

        return wrapper

    @classmethod
    @cache
    def fib(cls, n):
        if n <= 1:
            return n
        return cls.fib(n - 1) + cls.fib(n - 2)

    @classmethod
    def fib2(cls, n):
        a, b = 0, 1
        for i in range(n):
            a, b = b + a, a
        return a


def dijkstra_graph(graph, start):
    all_vertex = []
    costs = {}
    parents = None
    processed = []

    find_min_vertex = lambda x: 1

    node = start
    while node:
        cost = costs[node]
        neighbors = node.links
        for link in neighbors:
            new_cost = cost + link.dist
            vertex = link.v2 if link.v2 != node else link.v1
            if new_cost < costs[vertex]:
                costs[vertex] = new_cost
                costs[vertex] += parents
                costs[vertex] += link

        processed.append(node)
        node = find_min_vertex(all_vertex)


binary_search = Search.binary_search
intersection_sort = Sort.intersection_sort
quick_sort = Sort.quick_sort
Fibonacci_recursion = Fibonacci.fib
Fibonacci_cycle = Fibonacci.fib2

lst = list(range(10_000_000))
random.shuffle(lst)
test(list.sort, lst)
