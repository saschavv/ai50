import unittest

from minesweeper import *

class TestSentence(unittest.TestCase):

    def assertCells(self, expected, values):
        self.assertEqual(len(expected), len(values))
        for v1,v2 in zip(expected,values):
            self.assertEqual(v1,v2)

    # Check known_mines

    def test_known_mines_when_no_cells(self):
        sentence = Sentence([], 0)
        mines = sentence.known_mines()
        self.assertFalse(mines)

    def test_known_all_mines(self):
        cells = [(1,2)]
        sentence = Sentence(cells, 1)
        mines = sentence.known_mines()
        self.assertCells(cells, mines)

    def test_no_mines(self):
        cells = [(1,2)]
        sentence = Sentence(cells, 0)
        mines = sentence.known_mines()
        self.assertFalse(mines)

    def test_nothing_less_then_number_of_cells(self):
        cells = [(1,2),(2,1)]
        sentence = Sentence(cells, 1)
        mines = sentence.known_mines()
        self.assertFalse(mines)

    # Check known_safes

    def test_known_saves_when_no_cells(self):
        sentence = Sentence([], 0)
        mines = sentence.known_safes()
        self.assertFalse(mines)

    def test_known_all_mines(self):
        cells = [(1,2)]
        sentence = Sentence(cells, 1)
        mines = sentence.known_safes()
        self.assertFalse(mines)

    def test_no_mines(self):
        cells = [(1,2)]
        sentence = Sentence(cells, 0)
        mines = sentence.known_safes()
        self.assertCells(cells, mines)


    # Mark mines

    def test_mark_mine(self):
        cells = [(1,2),(2,1)]
        sentence = Sentence(cells, 1)
        sentence.mark_mine((2,1))
        self.assertEqual(0, sentence.count)
        self.assertCells([(1,2)], sentence.cells)

    def test_mark_mine_non_existing(self):
        cells = [(1,2),(2,1)]
        sentence = Sentence(cells, 1)
        sentence.mark_mine((3,1))
        self.assertEqual(1, sentence.count)
        self.assertCells(cells, sentence.cells)


    # Mark safes
    def test_mark_safe(self):
        cells = [(1,2),(2,1)]
        sentence = Sentence(cells, 1)
        sentence.mark_safe((2,1))
        self.assertEqual(1, sentence.count)
        self.assertCells([(1,2)], sentence.cells)

    def test_mark_safe_non_existing(self):
        cells = [(1,2),(2,1)]
        sentence = Sentence(cells, 1)
        sentence.mark_mine((3,1))
        self.assertEqual(1, sentence.count)
        self.assertCells(cells, sentence.cells)

class TestMinesweeperAI(unittest.TestCase):

    def test_mark_mine_without_knowledge(self):
        sweeperAI = MinesweeperAI(3,3)
        sweeperAI.mark_mine((0,0))

        self.assertTrue((0,0) in sweeperAI.mines)
        self.assertFalse(sweeperAI.safes)
        self.assertFalse(sweeperAI.knowledge)

    def test_mark_mine_with_knowledge(self):
        sweeperAI = MinesweeperAI(3,3)

        cells = [(0,0),(1,1)]
        sentence = Sentence(cells, 1)

        sweeperAI.knowledge.append(sentence)
        
        sweeperAI.mark_mine((0,0))

        self.assertTrue((0,0) in sweeperAI.mines)

        expected = Sentence([(1,1)], 0)
        self.assertEqual([expected], sweeperAI.knowledge)

    def test_mark_safe_without_knowledge(self):
        sweeperAI = MinesweeperAI(3,3)
        sweeperAI.mark_safe((0,0))

        self.assertTrue((0,0) in sweeperAI.safes)
        self.assertFalse(sweeperAI.mines)
        self.assertFalse(sweeperAI.knowledge)

    def test_mark_safe_with_knowledge(self):
        sweeperAI = MinesweeperAI(3,3)

        cells = [(0,0),(1,1)]
        sentence = Sentence(cells, 1)

        sweeperAI.knowledge.append(sentence)
        
        sweeperAI.mark_safe((0,0))

        self.assertTrue((0,0) in sweeperAI.safes)

        expected = Sentence([(1,1)], 1)
        self.assertEqual([expected], sweeperAI.knowledge)

    def test_nearby_cells_noboarder(self):
        sweeperAI = MinesweeperAI(3,3)
        cells = sweeperAI.nearby_cells((1,1))
        expected = [(0,0),(0,1),(0,2),(1,0),(1,2),(2,0),(2,1),(2,2)]
        self.assertEqual(expected,cells)

    def test_nearby_cells_with_lower_boarder(self):
        sweeperAI = MinesweeperAI(3,3)
        cells = sweeperAI.nearby_cells((0,0))
        expected = [(0,1),(1,0),(1,1)]
        self.assertEqual(expected,cells)
    
    def test_nearby_cells_with_upper_boarder(self):
        sweeperAI = MinesweeperAI(3,3)
        cells = sweeperAI.nearby_cells((2,2))
        expected = [(1,1),(1,2),(2,1)]
        self.assertEqual(expected,cells)
        
    def test_add_knowledge_no_mines(self):
        sweeperAI = MinesweeperAI(3,3)
        sweeperAI.add_knowledge((0,0),0)

        self.assertTrue((0,0) in sweeperAI.moves_made)
        
        expected = {(0,1),(1,0),(1,1),(0,0)}
        self.assertEqual(expected,sweeperAI.safes)

        self.assertFalse(sweeperAI.knowledge)

    def test_add_knowledge_all_mines(self):
        sweeperAI = MinesweeperAI(3,3)
        sweeperAI.add_knowledge((0,0),3)

        self.assertTrue((0,0) in sweeperAI.moves_made)
        
        sweeperAI.print()
        
        expected_safes = {(0,0)}
        self.assertEqual(expected_safes,sweeperAI.safes)
        expected_mines = {(0,1),(1,0),(1,1)}
        self.assertEqual(expected_mines,sweeperAI.mines)

        self.assertFalse(sweeperAI.knowledge)

    def test_add_knowledge_combine(self):
        sweeperAI = MinesweeperAI(3,3)
        sweeperAI.add_knowledge((0,0),2)
        self.assertTrue(sweeperAI.knowledge)

        sweeperAI.add_knowledge((0,1),2)
        expected_safes = {(0,1),(0,2),(1,2),(0,0)}
        self.assertEqual(expected_safes,sweeperAI.safes)
        expected_mines = {(1,0),(1,1)}
        self.assertEqual(expected_mines,sweeperAI.mines)
        self.assertFalse(sweeperAI.knowledge)
        

        






