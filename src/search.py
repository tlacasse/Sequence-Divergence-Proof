
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
