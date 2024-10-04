import ast

class UnnecessaryElseChecker(ast.NodeVisitor):
    def __init__(self, filename):
        self.unnecessary_else_blocks = []
        self.filename = filename

    def visit_FunctionDef(self, node):
        self.check_unnecessary_else(node)
        self.generic_visit(node)

    def check_unnecessary_else(self, node):
        for body_item in node.body:
            if isinstance(body_item, ast.If):
                if self.contains_return(body_item.body) and body_item.orelse:
                    self.unnecessary_else_blocks.append({
                        'file_name': self.filename,
                        'line_number': body_item.orelse[0].lineno,
                        'explanation': "The return statement in the if block makes else statement redundant. Remove else and return directly instead."
                    })

    def contains_return(self, statements):
        for stmt in statements:
            if isinstance(stmt, ast.Return):
                return True
            elif isinstance(stmt, ast.If):
                if self.contains_return(stmt.body):
                    return True
        return False

    def report(self):
        if not self.unnecessary_else_blocks:
            print("No unnecessary else blocks found.")
        else:
            print("Unnecessary else blocks found:")
            for item in self.unnecessary_else_blocks:
                print(f"Function '{item['function_name']}' at line {item['line_number']} contains an unnecessary else block.")

def analyze_code_for_unnecessary_else(file_path):
    with open(file_path, "r") as source_code:
        tree = ast.parse(source_code.read())
    checker = UnnecessaryElseChecker(file_path)
    checker.visit(tree)
    checker.report()


if __name__ == "__main__":
    file_path = "test.py"
    analyze_code_for_unnecessary_else(file_path)
