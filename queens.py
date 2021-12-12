import sys
from exact_cover import ExactCover, Option, Row


def main():
    if len(sys.argv) == 2:
        num_queens = int(sys.argv[1])
    else:
        num_queens = 8

    ranks = [f'Rank{i}' for i in range(num_queens)]
    rows = [f'Row{i}' for i in range(num_queens)]
    ne_diags = [f'NE{i}' for i in range(-num_queens+2, num_queens-1)]
    nw_diags = [f'NW{i}' for i in range(1, 2*num_queens - 2)]

    items = ranks + rows + ne_diags + nw_diags
    options = []

    for y in range(num_queens):
        for x in range(num_queens):
            sq_items = [f'Rank{x}', f'Row{y}']
            if (x != 0 or y != num_queens-1) and (x != num_queens-1 or y != 0):
                sq_items.append(f'NE{x-y}')
            if (x != 0 or y != 0) and (x != num_queens-1 or y != num_queens-1):
                sq_items.append(f'NW{x+y}')
            op = Option(f'({x}, {y})', sq_items)
            options.append(op)

    # extra options for all diagonals
    for d in range(-num_queens+2, num_queens-1):
        op = Option(f'ne{d}', [f'NE{d}'])
        options.append(op)
    for d in range(1, 2*num_queens - 2):
        op = Option(f'nw{d}', [f'NW{d}'])
        options.append(op)

    cover = ExactCover(items, options)
    cover.dump()

    num_solutions = 0
    for solution in cover.solve():
        num_solutions += 1
        print(solution)

    print(f'Total of {num_solutions} solutions')


if __name__ == '__main__':
    main()
