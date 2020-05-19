class AlmostAlwaysTrue(object):
    def __init__(self, total_iterations=1):
        self.total_iterations = total_iterations
        self.current_iteration = 0

    def __bool__(self):
        self.current_iteration += 1
        if self.current_iteration < self.total_iterations:
            return True
        return False
