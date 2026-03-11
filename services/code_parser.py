from tree_sitter_languages import get_parser

parser = get_parser("python")

def parse_code(file_content):

    tree = parser.parse(bytes(file_content, "utf8"))

    root = tree.root_node

    functions = []
    classes = []

    def traverse(node):

        if node.type == "function_definition":
            name = node.child_by_field_name("name")
            if name:
                functions.append(name.text.decode())

        if node.type == "class_definition":
            name = node.child_by_field_name("name")
            if name:
                classes.append(name.text.decode())

        for child in node.children:
            traverse(child)

    traverse(root)

    return {
        "functions": functions,
        "classes": classes
    }