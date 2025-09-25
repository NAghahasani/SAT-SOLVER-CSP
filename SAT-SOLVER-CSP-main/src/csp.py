from cnf import CNF

class CSP:
    def __init__(self, cnf: CNF, use_mcv=True, use_mrv=True, use_lcv=True):
        self.cnf = cnf
        self.use_mcv = use_mcv
        self.use_mrv = use_mrv
        self.use_lcv = use_lcv
        self.variables = {}
        self.assigned_variables = {}
        
        for variable in self.cnf.variables:
            if not variable.startswith('~'):
                self.variables[variable] = [False, True]

    def assign(self, variable, value):
        self.assigned_variables[variable] = value

    def unassign(self, variable):
        if variable in self.assigned_variables:
            del self.assigned_variables[variable]

    def is_constraint_satisfied(self, clause):
        for literal in clause:
            is_negated = literal.startswith('~')
            var = literal[1:] if is_negated else literal
            if var in self.assigned_variables:
                value = self.assigned_variables[var]
                if is_negated:
                    value = not value
                if value:
                    return True
        return False

    def is_consistent(self, variable, value):
        self.assign(variable, value)
        
        for clause in self.cnf.hard_clauses:
            satisfied = False
            for literal in clause:
                is_negated = literal.startswith('~')
                var = literal[1:] if is_negated else literal
                
                if var in self.assigned_variables:
                    var_value = self.assigned_variables[var]
                    if is_negated:
                        var_value = not var_value
                    if var_value:
                        satisfied = True
                        break
            
            if not satisfied and all(self.extract_name(lit) in self.assigned_variables for lit in clause):
                self.unassign(variable)
                return False
        
        self.unassign(variable)
        return True
    
    def is_complete(self):
        return len(self.assigned_variables) == len(self.variables)
    
    def extract_name(self, literal):
        return literal[1:] if literal.startswith('~') else literal

    def mrv(self, unassigned):
        return min(unassigned, key=lambda var: sum(1 for val in [True, False] if self.is_consistent(var, val)))

    def mcv(self, unassigned):
        variable_counts = {}
        for var in unassigned:
            count = 0
            for clause in self.cnf.hard_clauses + self.cnf.soft_clauses:
                for literal in clause:
                    if var == self.extract_name(literal):
                        count += 1
                        break
            variable_counts[var] = count
        return max(unassigned, key=lambda var: variable_counts.get(var, 0))

    def select_unassigned_variable(self):
        unassigned = [var for var in self.variables if var not in self.assigned_variables]
        if not unassigned:
            return None

        if self.use_mrv:
            return self.mrv(unassigned)

        if self.use_mcv:
            return self.mcv(unassigned)

        return unassigned[0]

    def count_conflicts(self, variable, value):
        self.assign(variable, value)
        conflict_count = 0
        for clause in self.cnf.hard_clauses:
            if variable in clause or f'~{variable}' in clause:
                if not self.is_constraint_satisfied(clause):
                    conflict_count += 1
        self.unassign(variable)
        return conflict_count

    def lcv(self, variable):
        values = [True, False]
        
        if self.use_lcv:
            values.sort(key=lambda val: self.count_conflicts(variable, val))
            
        return values

    def solve(self):
        if self.is_complete():  
            for clause in self.cnf.hard_clauses:
                if not self.is_constraint_satisfied(clause):
                    return None, float('-inf')
            
            weight = self.cnf.calculate_weight(self.assigned_variables)
            return dict(self.assigned_variables), weight

        variable = self.select_unassigned_variable()
        if variable is None:
            return None, float('-inf')

        best_solution = None
        best_weight = float('-inf')

        for value in self.lcv(variable):
            if self.is_consistent(variable, value):
                self.assign(variable, value)
                result, weight = self.solve()
                if result is not None and weight >= best_weight:
                    best_solution = dict(result)
                    best_weight = weight
                self.unassign(variable)

        return best_solution, best_weight



