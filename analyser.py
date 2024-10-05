import ast
import textwrap
import unittest
import ast
from io import StringIO
from contextlib import redirect_stdout

class UnnecessaryElseChecker(ast.NodeVisitor):
    def __init__(self, filename=None):
        self.unnecessary_else_blocks = []
        self.filename = filename or "unknown_file"

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
                print(f"{item['line_number']} line of '{item['file_name']}' file contains an unnecessary else block.")

def analyze_code_for_unnecessary_else(file_path):
    with open(file_path, "r") as source_code:
        tree = ast.parse(source_code.read())
    checker = UnnecessaryElseChecker(file_path)
    checker.visit(tree)
    checker.report()

class TestUnneccesaryElseChecker(unittest.TestCase):
    def run_analyser_on_code(self, code):
        with StringIO() as buf, redirect_stdout(buf):
            tree = ast.parse(code)
            checker = UnnecessaryElseChecker(filename="test_code")
            checker.visit(tree)
            checker.report()
            return buf.getvalue()
        
    def test_no_unnecessary_else(self):
        code = textwrap.dedent("""
            def test():
                if 4>5:
                    return "greater"
                return "less"
        """)
        output = self.run_analyser_on_code(code)
        self.assertIn("No unnecessary else blocks found.", output)

    def test_single_unnecessary_else(self):
        code = textwrap.dedent("""
            def test():
                if 4>5:
                    return "greater"
                else:
                    return "less"
        """)
        output = self.run_analyser_on_code(code)
        self.assertIn("Unnecessary else blocks found:", output)

    def test_nested_unnecessary_else(self):
        code = textwrap.dedent("""
            def test_func():
                if 5 > 3:
                    if 2 < 4:
                        return "inner condition true"
                    else:
                        return "inner condition false"
                else:
                    return "outer condition false"
        """)
        output = self.run_analyser_on_code(code)
        self.assertIn("Unnecessary else blocks found:", output)

    def test_func_without_if_else(self):
        code = textwrap.dedent("""
            def test_func():
                return "no conditions"
        """)
        output = self.run_analyser_on_code(code)
        self.assertIn("No unnecessary else blocks found.", output)


if __name__ == "__main__":
    # file_path = "test.py"
    # analyze_code_for_unnecessary_else(file_path)

    unittest.main()
