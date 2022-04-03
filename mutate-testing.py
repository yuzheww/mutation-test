import ast
from astor import to_source
import sys
from random import random
from random import choice
from random import seed

"""
The python script reads a .py file and decompose the python code into AST.
Then, it mutates the operators in the original file to create mutants for
mutation testing.

The first argument is the path to the python script you want to test.
The second argument is the number of mutants you want to generate. 
For example, "python mutation-testing.py ./fuzzywuzzy.py 10" will generate
10 mutants of fuzzywuzzy.py. 
"""
path = sys.argv[1]
num = sys.argv[2]



seed(38)
binary = [ast.Add(), ast.Sub(), ast.Mult(), ast.Div()]
rate = 0.85
assignrate = 0.5
turned = True

class ComparisonVisitor(ast.NodeTransformer):
    # 1. comparison
    def visit_Gt(self, node):
        if random() > rate:
            return ast.LtE()
        else:
            return node
        
    def visit_GtE(self, node):
        if random() > rate:
            return ast.Lt()
        else:
            return node
        
    def visit_Lt(self, node):
        if random() > rate:
            return ast.GtE()
        else:
            return node  
    
    def visit_LtE(self, node):
        if random() > rate:
            return ast.Gt()
        else:
            return node  
    
    def visit_Eq(self, node):
        if random() > rate:
            return ast.NotEq()
        else:
            return node 

    def visit_NotEq(self, node):
        if random() > rate:
            return ast.Eq()
        else:
            return node 

    # 3. remove some assignments
    # no AugAssign or AnnAssign
    # def visit_Assign(self, node):
    #     if random() > assignrate:
    #         return None
    #     else:
    #         return node 



class BinaryVisitor(ast.NodeTransformer):
    # 2. binary operations
    def visit_Add(self, node):
        if random() > rate:
            return ast.Sub()
        else:
            return node
        
    def visit_Sub(self, node):
        if random() > rate:
            return ast.Sub()
        else:
            return node
        
    def visit_Mult(self, node):
        if random() > rate:
            return ast.Add()
        else:
            return node
        
    def visit_Div(self, node):
        if random() > rate:
            return ast.Sub()
        else:
            return node
    
    def visit_In(self, node):
        if random() > rate:
            return ast.NotIn()
        else:
            return node


class AssignVisitor(ast.NodeTransformer):
    # 2. binary operations
    def visit_Assign(self, node):
        if random() > rate:
            # turned = False
            targets = node.targets
            return ast.Assign(targets=targets,
                       value=ast.Name(id='\"mutate\"', ctx=ast.Load()))
        else:
            return node
        
# def mutate(filename):
#     file = open(path)
#     contents = file.read()
#     tree = ast.parse(contents)

#     nodeVisitor = Visitor()
#     newcode = nodeVisitor.visit(tree)
#     newfile = to_source(newcode)
#     with open(filename, 'w') as file:
#         file.write(newfile)

num = int(num)
part1 = 0.3
part2 = 0.35
for i in range(num):
    filename = '%d.py' % i
    file = open(path)
    contents = file.read()
    tree = ast.parse(contents)

    if i < (part1 * num):
        # Swapping Comparison Operators can help distinguish between
        #  Test Suites B, C, D and E.
        base = 16 / 17
        rate = base
        nodeVisitor = ComparisonVisitor()
        tree = nodeVisitor.visit(tree)
    elif i < ((part1 + part2) * num):
        # Swapping Binary Operators can help distinguish 
        # Test Suites A and B from Test Suites C, D and E.
        # 16 / 17
        base = 19 / 20
        # rate = (1 - base) * i / num + base
        rate = base
        binaryVisitor = BinaryVisitor()
        tree = binaryVisitor.visit(tree)
    else:
        base = 96 / 97
        rate = base
        assignVisitor = AssignVisitor()
        tree = assignVisitor.visit(tree)
        
    newfile = to_source(tree)
    with open(filename, 'w') as file:
        file.write(newfile)