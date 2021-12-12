import unittest
from typing import cast
from exact_cover import ExactCover, Option, Row


class ExactCoverTestCase(unittest.TestCase):
    def test_simple(self):
        items = ['Item1', 'Item2', 'Item3', 'Item4', 'Item5', 'Item6', 'Item7']
        options = [
            Option('RowA', ['Item1', 'Item4', 'Item7']),
            Option('RowB', ['Item1', 'Item4']),
            Option('RowC', ['Item4', 'Item5', 'Item7']),
            Option('RowD', ['Item3', 'Item5', 'Item6']),
            Option('RowE', ['Item2', 'Item3', 'Item6', 'Item7']),
            Option('RowF', ['Item2', 'Item7']),
        ]
        cover = ExactCover(items, options)
        cover.dump()
        print('----')

        row = cast(Row, cover.matrix.down.down)
        cover.select_option(row)
        cover.dump()
        print('----')

        cover.restore_option(row)
        cover.dump()
        print('----')

        for col, item in zip(cover.column_iter(), items):
            self.assertEqual(col.name, item)
        for row, option in zip(cover.row_iter(), options):
            j = row.right
            it = iter(option.items)
            while j.right != row:
                it_name = next(it)
                self.assertEqual(j.column.name, it_name)
                j = j.right


if __name__ == '__main__':
    unittest.main()
