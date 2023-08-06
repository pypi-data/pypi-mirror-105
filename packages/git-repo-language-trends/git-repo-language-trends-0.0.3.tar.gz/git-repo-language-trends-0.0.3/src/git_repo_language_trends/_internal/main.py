#!/usr/bin/env python3

# pylint: disable=C0116

import sys

from datetime import datetime
import os
import os.path
import pygit2

from .args import get_args
from .separated_values_output import SeparatedValuesOutput
from .matplotlib_output import MatplotlibOutput
from .utils import get_extensions_sorted_by_popularity, get_top_three_extensions


def main():
    args = get_args()
    outputs = get_outputs(args)
    if args.list:
        list_available_file_extensions(args)
    else:
        process_commits(args, outputs)


def list_available_file_extensions(args):
    data = get_data_for_first_commit(args)
    pop = get_extensions_sorted_by_popularity(data)
    foo = " ".join(pop)
    print(f"Available extensions (in first commit):\n{foo}")


# Calls process_commit for the first commit (possibly from --start-commit)
def get_data_for_first_commit(args):
    repo = get_repo()
    rev = repo.revparse_single(args.first_commit)
    return process_commit(rev.peel(pygit2.Commit), None)


def get_outputs(args):
    # TODO: Support multiple --output arguments
    outputs = []

    # TODO: CLI tests
    if args.output_ext == ".svg" or args.output_ext == ".png":
        outputs.append(MatplotlibOutput(args))
    elif args.output_ext == ".tsv":
        outputs.append(SeparatedValuesOutput(args, "\t"))
    elif args.output_ext == ".csv":
        outputs.append(SeparatedValuesOutput(args, ","))
    else:
        sys.exit(f"Output file format '{args.output_ext}' not supported")

    return outputs


def process_commits(args, outputs):
    columns = args.columns
    if len(columns) == 0:
        data = get_data_for_first_commit(args)
        columns = get_top_three_extensions(data)

    if len(columns) == 0:
        sys.exit("No extensions to count lines for")

    ext_to_column = generate_ext_to_column_dict(args.columns)

    commits_to_process = get_commits_to_process(args)

    # Print column headers
    for output in outputs:
        output.start(columns)

    # Print rows
    for commit in commits_to_process:
        date = get_commit_date(commit)
        column_to_lines_dict = process_commit(commit, ext_to_column)

        for output in outputs:
            output.add_row(columns, date, column_to_lines_dict)

    # Wrap things up
    for output in outputs:
        output.finish()


def get_commits_to_process(args):
    print("Figuring out what commits to analyze ...", file=sys.stderr)

    commits_to_process = []

    rows_left = args.max_commits

    date_of_last_row = None
    for commit in get_git_log_walker(args):
        if rows_left == 0:
            break

        # Make sure --min-interval days has passed since last printed commit before
        # processing and printing the data for another commit
        current_date = commit.commit_time
        if enough_days_passed(args, date_of_last_row, current_date):
            date_of_last_row = current_date

            commits_to_process.append(commit)

            rows_left -= 1

    # git log shows most recent first, but in the graph
    # you want to have from oldest to newest, so reverse
    commits_to_process.reverse()

    print(f"Will analyze {len(commits_to_process)} commits.", file=sys.stderr)

    return commits_to_process


def process_commit(commit, ext_to_column):
    """
    Counts lines for files with the given file extensions in a given commit.
    """

    blobs = get_blobs_in_commit(commit)

    # Loop through all blobs in the commit tree
    column_to_lines = {}
    for (blob, ext) in blobs:

        # Figure out if we should count the lines for the file extension this
        # blob has, by figuring out what column the lines should be added to,
        # if any
        column = ext_to_column.get(ext) if ext_to_column else ext
        # If no specific columns are requested, we are probably invoked
        # with --list, so count the lines for all extensions

        # If the blob has an extension we care about, count the lines!
        if column:
            lines = get_lines_in_blob(blob)
            column_to_lines[column] = column_to_lines.get(column, 0) + lines

    return column_to_lines


def get_all_blobs_in_tree(tree):
    blobs = []
    trees_left = [tree]
    # Say no to recursion
    while len(trees_left) > 0:
        tree = trees_left.pop()
        for obj in tree:
            if isinstance(obj, pygit2.Tree):
                trees_left.append(obj)
            elif isinstance(obj, pygit2.Blob):
                blobs.append(obj)
    return blobs


def get_blobs_in_commit(commit):
    blobs = []
    for obj in get_all_blobs_in_tree(commit.tree):
        ext = os.path.splitext(obj.name)[1]
        if ext:
            blobs.append((obj, ext))

    return blobs


c = {}  # TODO: Make optinal and measure memory usage for linux kernel


def get_lines_in_blob(blob):
    if blob.oid in c:
        return c[blob.oid]

    lines = 0
    for byte in memoryview(blob):
        if byte == 10:  # \n
            lines += 1

    c[blob.oid] = lines
    return lines


def get_repo():
    return pygit2.Repository(os.environ.get('GIT_DIR', '.'))


def get_git_log_walker(args):
    repo = get_repo()

    rev = repo.revparse_single(args.first_commit)

    walker = repo.walk(rev.peel(pygit2.Commit).oid)

    if not args.all_parents:
        walker.simplify_first_parent()

    return walker


def enough_days_passed(args, date_of_last_row, current_date):
    """
    Checks if enough days according to --min-interval has passed, i.e. if it is
    time to process and print another commit.
    """

    if date_of_last_row:
        days = ((date_of_last_row - current_date) / 60 / 60 / 24)
        return days > args.min_interval_days
    return True


def generate_ext_to_column_dict(columns):
    extension_to_column_dict = {}
    for column in columns:
        for ext in column.split('+'):
            extension_to_column_dict[ext] = column
    return extension_to_column_dict


def get_commit_date(commit):
    return datetime.utcfromtimestamp(commit.commit_time).strftime('%Y-%m-%d')
