#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Mito.
# Distributed under the terms of the Modified BSD License.

"""
Generates a JSON list of function documentation objects from doc strings
of sheet functions in mitosheet/sheet_functions.py. See docs/README for 
a description of this object and more information.
"""
import json
import sys

def generate_markdown(function_doc_objects):
    """
    Prints a markdown representation of the sheet function
    documentation.
    """

    for function_doc_object in function_doc_objects:
        print("# ", function_doc_object['function'])
        print(function_doc_object['description'])
        print("")
        print("## Examples")
        for example in function_doc_object['examples']:
            print('- ', example)
        print("")
        print("## Syntax")
        print(function_doc_object['syntax'])
        print("")
        print("### Syntax Elements")
        for syntax_elements in function_doc_object['syntax_elements']:
            print(f'- **{syntax_elements["element"]}**: {syntax_elements["description"]}')
        print("")


def main():
    """
    Takes one of two commands:

    1. python docs/make_function_docs.py update_frontend

    Reads in all the sheet functions' documentation objects, 
    and writes them to src/data/function_documentation.json.

    2. python docs/make_function_docs.py generate_markdown

    Prints out a markdown representation of the objects for 
    uploading to the docs
    """

    command = sys.argv[1]

    from mitosheet.sheet_functions import FUNCTIONS

    function_doc_objects = []
    invalid = []
    for function_name, function in FUNCTIONS.items():
        try:
            func_doc_obj = json.loads(function.__doc__)
            function_doc_objects.append(func_doc_obj)
            print(
                f'Build documentation for {function_name}!'
            )
        except:
            print(function.__doc__)
            # If we can't read in the function documentation, report that
            invalid.append(function_name)

    if len(invalid) > 0:
        invalid_str = ', '.join(invalid)
        print(f'\nUnable to generate documentation for {len(invalid)} functions: {invalid_str}. Make sure they are valid JSON objects as specificed in ./docs/README.md.')

    # Sort them alphabetically
    function_doc_objects.sort(key=lambda doc: doc['function'])

    if command == 'update_frontend':
        with open('./src/data/function_documentation.tsx', 'w+') as f:
        # We write the types for these objects as well!
            f.write("""
export interface FunctionDocumentationObject {
    function: string;
    description: string;
    examples?: (string)[] | null;
    syntax: string;
    syntax_elements?: (SyntaxElementsEntity)[] | null;
}

export interface SyntaxElementsEntity {
    element: string;
    description: string;
}

export const functionDocumentationObjects: FunctionDocumentationObject[] = """)

            f.write(json.dumps(function_doc_objects))

            print('\nWrote documentation to ./src/data/function_documentation.tsx!')
    elif command == 'generate_markdown':
        generate_markdown(function_doc_objects)


    

if __name__ == '__main__':
    main()