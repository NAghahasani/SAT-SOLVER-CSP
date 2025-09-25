class CNF:
    def __init__(self, variables_list, hard_clauses_list, soft_clauses_list):
        """
        Initializes a Conjunctive Normal Form (CNF) object.

        Args:
            variables_list (list): List of variable names.
            hard_clauses_list (list): List of hard clauses.
            soft_clauses_list (list): List of soft clauses with weights at the end.
        """
        self.variables = variables_list
        self.hard_clauses = hard_clauses_list
        self.soft_clauses = soft_clauses_list

    def evaluate_clause(self, clause_condition, assignment_dict):
        """Checks if a single clause is satisfied given the assignments."""
        for literal_term in clause_condition:
            literal_term = str(literal_term)
            
            # Handle both numeric (1, ~1) and variable (X1, ~X1) formats
            if literal_term.startswith('~'):
                var_name = literal_term[1:]  # Remove the negation
                lit_value = not assignment_dict.get(var_name, False)
            else:
                var_name = literal_term
                lit_value = assignment_dict.get(var_name, False)
                
            if lit_value:
                return True
        return False

    def evaluate_negation(self, clause_condition, assignment_dict):
        """Checks if a negated variable assignment is satisfied."""
        return not self.evaluate_clause(clause_condition, assignment_dict)

    def calculate_weight(self, assignment_map):
        total_weight = 0
        for clause in self.soft_clauses:
            is_satisfied = False
            weight = int(clause[-1])  # Last element is the weight
            for literal_term in clause[:-1]:  # All elements except the last are literals
                is_negated = literal_term.startswith('~')
                variable_name = literal_term[1:] if is_negated else literal_term
                if variable_name in assignment_map:
                    value = assignment_map[variable_name]
                    if is_negated:
                        value = not value
                    if value:
                        is_satisfied = True
                        break
            if is_satisfied:
                total_weight += weight
        return total_weight
