from typing import Optional, List, Generator

OptColumn = Optional['Column']
OptRow = Optional['Row']


class Option:
    name: str
    items: str

    def __init__(self, name, items):
        self.name = name
        self.items = items


class Cell:

    def __init__(self, column: OptColumn, row: OptRow):
        self.left: Cell = self
        self.right: Cell = self
        self.up: Cell = self
        self.down: Cell = self
        self.column = column
        self.row = row

    def __repr__(self):
        return f'Cell({self.column.name}, {self.row.name})'

    def append_above(self, other: 'Cell'):
        other.up = self.up
        other.down = self
        self.up.down = other
        self.up = other

    def append_before(self, other: 'Cell'):
        other.left = self.left
        other.right = self
        self.left.right = other
        self.left = other

    def remove_horizontally(self):
        self.left.right = self.right
        self.right.left = self.left

    def restore_horizontally(self):
        self.left.right = self
        self.right.left = self

    def remove_vertically(self):
        self.up.down = self.down
        self.down.up = self.up

    def restore_vertically(self):
        self.up.down = self
        self.down.up = self


class Column(Cell):
    def __init__(self, name):
        super().__init__(self, None)
        self.name = name
        self.num_options = 0

    def __repr__(self):
        return f'Column({self.name}, {self.num_options})'


class Row(Cell):
    def __init__(self, name):
        super().__init__(None, self)
        self.name = name

    def __repr__(self):
        return f'Row({self.name})'


class Matrix(Cell):
    def __init__(self):
        super().__init__(None, None)
        self.name = 'Matrix'


# noinspection DuplicatedCode
class ExactCover:
    rows_header: Row

    def __init__(self, items: List[str], options: List[Option]):
        self.items = items
        self.options = options
        self.matrix = Matrix()
        self.columns_map = {}

        # initialize the header lines
        for item in self.items:
            col = Column(item)
            self.matrix.append_before(col)
            self.columns_map[col.name] = col

        for option in self.options:
            row = Row(option.name)
            self.matrix.append_above(row)
            for item in option.items:
                col = self.columns_map[item]
                cell = Cell(col, row)
                row.append_before(cell)
                col.append_above(cell)
                col.num_options += 1

    def column_iter(self) -> Generator[Column, None, None]:
        col = self.matrix.right
        while col != self.matrix:
            yield col
            col = col.right

    def row_iter(self) -> Generator[Row, None, None]:
        row = self.matrix.down
        while row != self.matrix:
            yield row
            row = row.down

    def num_columns(self):
        i = 0
        for _ in self.column_iter():
            i += 1
        return i

    def dump(self):
        print(f'{"":20}:', end='')
        print(''.join(f'{col.name:^8}' for col in self.column_iter()))
        print(f'{"":20}:', end='')
        print(''.join(f'{col.num_options:^8}' for col in self.column_iter()))
        print('-' * (20 + self.num_columns() * 8))

        for row in self.row_iter():
            print(f'{row.name:20}:', end='')
            cell = row.right
            for col in self.column_iter():
                if cell.column == col:
                    bit = 1
                    cell = cell.right
                else:
                    bit = 0
                print(f'{bit:^8}', end='')
            print()

    @classmethod
    def cover_column(cls, column: Column):
        column.remove_horizontally()
        i = column.down
        while i != column:
            j = i.right
            while j != i:
                j.remove_vertically()
                if j != j.row:
                    j.column.num_options -= 1
                j = j.right
            i = i.down

    @classmethod
    def uncover_column(cls, column: Column):
        i = column.up
        while i != column:
            j = i.left
            while j != i:
                j.restore_vertically()
                if j != j.row:
                    j.column.num_options += 1
                j = j.left
            i = i.up
        column.restore_horizontally()

    @classmethod
    def select_option(cls, row: Row):
        j = row.right
        while j != row:
            cls.cover_column(j.column)
            j = j.right

    @classmethod
    def restore_option(cls, row: Row):
        j = row.left
        while j != row:
            cls.uncover_column(j.column)
            j = j.left

    def _solve_rec(self, solution):
        if self.matrix.right == self.matrix:
            # We have a solution
            yield solution
            return

        col = min(self.column_iter(), key=lambda x: x.num_options)
        if col.num_options == 0:
            return
        j = col.down
        while j != col:
            solution.append(j.row.name)
            self.select_option(j.row)
            yield from self._solve_rec(solution)

            solution.pop()
            self.restore_option(j.row)
            j = j.down

    def solve(self):
        for solution in self._solve_rec([]):
            print(solution)

