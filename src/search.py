from keras.models import load_model
from exprdata import map_exprs_to_array, map_array_to_real
from exprmap import exprmap

class AbstractSearchMethod:
    
    def __init__(self):
        pass
        
    def start(self, problem):
        pass
    
    def remaining(self):
        return 0
        
    def remove(self):
        return None
    
    def add(self, new_path):
        pass
    
class DFSSearch(AbstractSearchMethod):
    
    def __init__(self):
        super().__init__()
        self.frontier = None
        
    def start(self, problem):
        self.frontier = [[problem]]
        
    def remaining(self):
        return len(self.frontier)
        
    def remove(self):
        return self.frontier.pop()
    
    def add(self, new_path):
        self.frontier.append(new_path)
        
class NeuralNetworkSearch(AbstractSearchMethod):
    
    def __init__(self):
        super().__init__()
        self.frontier = None
        self.last_point = None
        self.model = load_model('data/nn.h5')
        
    def start(self, problem):
        self.frontier = [[problem]]
        self.last_point = problem
    
    def remaining(self):
        return len(self.frontier)
        
    def remove(self):
        x = map_exprs_to_array([self.last_point])
        y = self.model.predict(x)
        y = map_array_to_real(y[0])
        self.frontier.sort(key=(lambda f: self._frontier_sort(f, y)))
        next_node = self.frontier.pop(0)
        self.last_point = next_node[-1]
        return next_node
    
    def add(self, new_path):
        self.frontier.append(new_path)
        
    def _frontier_sort(self, f, y):
        y_top = y[0]
        y_bot = y[1]
        f_top = exprmap(f[-1].top)
        f_bot = exprmap(f[-1].bot)
        return abs(y_top - f_top) + abs(y_bot - f_bot)
