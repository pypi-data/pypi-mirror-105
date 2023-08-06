import os
import sys
from pathlib import Path

from rope.base import libutils
from rope.base.codeanalyze import SourceLinesAdapter
from rope.base.project import Project
from rope.refactor.extract import ExtractVariable, ExtractMethod
from rope.refactor.importutils import FromImport, NormalImport
from rope.refactor.importutils.module_imports import ModuleImports


def handle_add_import(project, resource, args):
    selection = os.getenv("kak_selection")
    if len(args) == 0:
        # Reminder: in kakoune, there's *always* a selection
        if len(selection) <= 1:
            sys.exit("add-import: no name given and selection too short")
        name = selection
        parent = None
    elif len(args) == 1:
        name = args[0]
        parent = None
    elif len(args) == 2:
        parent, name = args
    else:
        sys.exit("Could not parse add-import args")

    # Note: I alomst never use 'as', so aliases are always None
    if not parent:
        import_info = NormalImport([(name, None)])
    else:
        import_info = FromImport(parent, 0, [(name, None)])

    pymodule = project.get_pymodule(resource)
    module_imports = ModuleImports(project, pymodule)
    module_imports.add_import(import_info)
    changed_source = module_imports.get_changed_source()
    resource.write(changed_source)


def hande_extraction(kind, project, resource, args):
    code = resource.read()
    (new_name,) = args  # this works becaue of the -params 1 in kak-rope.kak
    source_lines_adapter = SourceLinesAdapter(code)
    selection_desc = os.getenv("kak_selection_desc")
    start, stop = selection_desc.split(",")
    start_line, start_column = [int(x) for x in start.split(".")]
    end_line, end_column = [int(x) for x in stop.split(".")]
    # kakoune columns start at 1, so we need -1 for the start, and nothing for the end
    start_offset = source_lines_adapter.get_line_start(start_line) + start_column - 1
    end_offset = source_lines_adapter.get_line_start(end_line) + end_column
    # kakoune selection maybe backwards, so start_offset maybe greater than stop_offset
    start_offset, end_offset = sorted([start_offset, end_offset])
    snippet = code[start_offset:end_offset]
    if kind == "variable":
        extractor = ExtractVariable(project, resource, start_offset, end_offset)
    else:
        extractor = ExtractMethod(project, resource, start_offset, end_offset)
    changes = extractor.get_changes(new_name)
    project.do(changes)


def guess_project_path(source_path):
    return Path.cwd()


def main():
    source_path = Path(os.getenv("kak_buffile"))
    project_path = guess_project_path(source_path)
    project = Project(project_path)
    resource = libutils.path_to_resource(project, source_path)

    _, action, *args = sys.argv
    if action == "add-import":
        handle_add_import(project, resource, args)
    elif action == "extract-variable":
        hande_extraction("variable", project, resource, args)
    elif action == "extract-method":
        hande_extraction("method", project, resource, args)
    else:
        sys.exit(f"Unknown action {action}")
