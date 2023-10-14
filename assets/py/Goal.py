class Goals:
    def __init__(self, savings):
        self.goals = {}
        self.savings = savings

    def update_savings(self, new_savings):
        self.savings = new_savings

    def contribute(self, goal, amount):
        if goal not in self.goals:
            return "Error: goal does not exist"
        t = 0
        for amt in self.goals.values():
            t += amt[1]
        t += amount
        if self.savings <= t:
            return "Error: contribution exceed savings."
        self.goals[goal][1] += amount
        if self.goals[goal][0] < self.goals[goal][1]:
            return "Goal Reached"

        return "processed"

    def decontribute(self, goal, amount):
        if goal not in self.goals:
            return "Error: goal does not exist"
        elif amount > self.goals[goal][1]:
            return f"Error: goal cannot decontribute exceeding {self.goals[goal][1]} amount"
        self.goals[goal][1] -= amount
        return "processed"

    def add_goal(self, goal, total):
        if goal in self.goals:
            return "Error: goal is already in goals"
        if total <= 0:
            return "Error: total cannot be less than or equal to 0"
        self.goals[goal] = [total, 0]
        return "processed"

    def remove_goal(self, goal):
        if goal in self.goals:
            del self.goals[goal]

    def change_total(self, goal, total):
        self.goals[goal][0] = total
        if self.goals[goal][0] <= 0:
            return "Error: total cannot be less than or equal to 0"
        elif self.goals[goal][0] < self.goals[goal][1]:
            return "Goal Reached"
        return "processed"

