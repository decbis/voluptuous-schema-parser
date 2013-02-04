import ast

from schemaparser.visitor import SchemaVisitor

def load(file_name):
    return loads(file_name.read())

def loads(script):
    node = ast.parse(script)
    visitor = SchemaVisitor()
    visitor.visit(node)
    return visitor.entities
