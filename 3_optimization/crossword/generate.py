import sys

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        # self.domains iteralas
        # .lenght megadja a hosszast.
        
        for var in self.domains:
            # iterate over the copy of the initial set.
            for word in set(self.domains[var]):
                if len(word) != var.length:
                    self.domains[var].remove(word)

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        # check overlap
        if self.crossword.overlaps[x, y]:
            i, j = self.crossword.overlaps[x, y]
            # check if the ith char of word_x is the same as the jth char of word_y
            revised = False
            for word_x in set(self.domains[x]):
                match_flag = False
                for word_y in self.domains[y]:
                    if word_x[i] == word_y[j]:
                        match_flag = True
                        break
                # remove word_x if does not match with anything in self.domains[y]
                if not match_flag:
                    # remove word_x
                    self.domains[x].remove(word_x)
                    revised = True
            return revised
        
        else: 
            return False

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        # creating a new queue if arcs is None
        if arcs is None:
            queue = []
            for x in self.crossword.variables:
                for y in self.crossword.neighbors(x):
                    queue.append((x, y))              
        
        else:
            queue = list(arcs)
        queue = set(queue)

        # iterating over the elements of the queue
        while queue:
            (x, y) = queue.pop()
            # if arc consistency is established
            if self.revise(x, y):
                # if the domain is empty return fals
                if len(self.domains[x]) == 0:
                    return False
                # else check the neighbouring variables how they are affected by the change > adding new elements to the queue
                for z in self.crossword.neighbors(x):
                    if z != y:
                        queue.add((z, x))    
        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        for var in self.crossword.variables:
            if var not in assignment or not assignment[var]:
                return False
        return True      

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        
        for var in assignment:
            if var.length != len(assignment[var]):
                return False
            for neighbor in self.crossword.neighbors(var):
                if neighbor in assignment and assignment[neighbor]:
                    if assignment[neighbor] == assignment[var]:
                        return False
                    i, j = self.crossword.overlaps[var, neighbor]
                    if assignment[var][i] != assignment[neighbor][j]:
                        return False
        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        conflicts = {}

        if var not in assignment:
            for word_var in self.domains[var]:
                total_neighbor_elim = 0
                for neighbor in self.crossword.neighbors(var):
                    i, j = self.crossword.overlaps[var, neighbor]
                    if len(word_var) == var.length:
                        for word_neighbor in self.domains[neighbor]:
                            if word_var[i] != word_neighbor[j]:
                                total_neighbor_elim += 1
                conflicts[word_var] = total_neighbor_elim
            
            order_domain = sorted(conflicts, key=lambda k: conflicts[k])
            return order_domain

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        unassigned_list = []
        for var in self.crossword.variables:
            if var not in assignment:
                unassigned_list.append(var)

        unassigned_dict = {}
        for var in unassigned_list:
            length = len(self.domains[var])
            unassigned_dict[var] = length
        
        min_value = min(unassigned_dict.values())
        unassigned_list = [key for key in unassigned_dict.keys() if unassigned_dict[key] == min_value]

        neighbor_count = {}
        if len(unassigned_list) > 1:
            for var in unassigned_list:
                neighbor_count[var] = len(self.crossword.neighbors(var))
            min_value_neigh = min(neighbor_count.values())
            var_min_neighbor = [key for key in neighbor_count.keys() if neighbor_count[key] == min_value_neigh]
            return var_min_neighbor[0]
        else: 
            return unassigned_list[0]

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        if self.assignment_complete(assignment):
            return assignment
        
        var = self.select_unassigned_variable(assignment)
        value_list = self.order_domain_values(var, assignment)

        for value in value_list:
            assignment[var] = value

            if self.consistent(assignment):
                result = self.backtrack(assignment)
                if result is not None:
                    return result
            
            del assignment[var]
        
        return None


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
