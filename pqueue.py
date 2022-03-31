import heapq

class PriorityQueue:
    def __init__(self):
        self.elements = []
        self.fifo = 0
    
    def empty(self) -> bool:
        return not self.elements
    
    def put(self, item, priority: float):
        heapq.heappush(self.elements, (priority, self.fifo, item))
        self.fifo += 1
    
    def get(self):
        return heapq.heappop(self.elements)[2]
