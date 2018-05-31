import sys


valuations = {}

def main():
    if len(sys.argv) != 2:
        sys.exit('Invald args')

    input = sys.argv[1]
    dimacs = []

    try:
        with open(input) as f:
            dimacs = parse_dimacs(f.read())
    except IOError:
        sys.exit('IOError')

    if DPLL(dimacs):
        print('\n\nValuation is: %s' % valuations)
    else: print('There is no valid valuation')


def parse_dimacs(dimacs_code):
    code = dimacs_code.split('\n')
    new_code = []

    for line in code:
        line = line.strip()
        if line.startswith('p') or line.startswith('c') or line == '':
            continue
        new_code.append(line)

    list = []
    for line in new_code:
        row = []
        numbers = line.split(' ')
        for number in numbers[:-1]:
            row.append(int(number.strip()))
        list.append(row)

    return list

def DPLL(D):
    # if there are no clauses, return True
    if not len(D):
        return True

    # pretprocessing: remove all Fs from clauses and replace -T with F and -F with T
    new_d = []
    for clause in D:
        new_c = []
        for lit in clause:
            if lit == '-T': new_c.append('F')
            if lit == '-F': new_c.append('T')
            if lit != 'F': new_c.append(lit)
        # if there is an empty clause, return False
        if not len(new_c):
            return False
        new_d.append(new_c)

    D = new_d
    new_d = []
    print("Pretprocessing:")
    print(D)

    # Step 1: Tauthology
    #           - if there is T in clause or p and -p, remove that clause
    has_changes = False

    for clause in D:
        keep_clause = True
        for lit in clause:
            if lit == 'T'or -lit  in clause:
                    keep_clause = False
                    break
        if keep_clause: new_d.append(clause)
        else: has_changes = True

    D = new_d
    print("Tauthology")
    print(D)

    if has_changes:
        res = DPLL(D)
        if res: return True
        else: return False


    # Step 2: Unit propagation
    #           - if there is only one element in the clause, and it is p
    #             replace p with T
    #           - if there is only one element in the clause and it is -p
    #             replace p with F (-p with T)
    has_changes = False
    for clause in D:
        if len(clause) == 1:
            has_changes = True
            lit = clause[0]
            D = [['T' if x == lit else 'F' if x == -lit else x for x in clause] for clause in D]
            valuations[abs(lit)] = False if lit < 0 else True

    print("Unit propagation:")
    print(D)

    if has_changes:
        res = DPLL(D)
        if res: return True
        else: return False

    # Step 3: Pure literal
    #           - if there is only p in D (-p doesn't exist in D), replace p with T
    #           - if there is only -p in D (p doesn't exist in D), replace p with F

    # list of literals that need to be changed
    literals = list(set([x for clause in D for x in clause]))
    literals = list(filter(lambda x: -x not in literals, literals))

    for lit in literals:
        D = [['T' if x == lit else x for x in clause] for clause in D]
        valuations[abs(lit)] = False if lit < 0 else True

    print("Pure literal:")
    print(D)

    # there was at least one change if literals is not an empty list
    if len(literals):
        res = DPLL(D)
        if res: return True
        else: return False


    # Step 4: Split
    #           - if there is no valuation for literal, and literal is p, change p with T
    #           - if there is no valuation for literal, and literal is -p, change p with F
    #           - after the change, check if the result of DPLL is True
    #           - if not, return the result of DPLL with changes reversed (p is F, -p is T)
    for clause in D:
        for lit in clause:
            if lit not in valuations:
                D = [['T' if x == lit else 'F' if x == -lit else x for x in clause] for clause in D]
                valuations[abs(lit)] = False if lit < 0 else True

                print("Split with T:")
                print(D)

                res = DPLL(D)
                if res: return True

                D = [['F' if x == lit else 'F' if x == -lit else x for x in clause] for clause in D]
                valuations[abs(lit)] = True if lit < 0 else False

                print("Split with F:")
                print(D)

                return DPLL(D)

    # there is no solution
    return None

if __name__ == '__main__':
    main()
