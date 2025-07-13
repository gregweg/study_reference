import unittest


def find_rotation_point(words):
    # Find the rotation point in the list
    first_word = words[0]
    floor_index = 0
    ceiling_index = len(words) - 1
    
    while floor_index < ceiling_index:
        
        guess_index = floor_index + ((ceiling_index - floor_index) // 2)
        
        if words[guess_index] >= first_word:
            # Right
            floor_index = guess_index
        else:
            # Left
            ceiling_index = guess_index
        
        # If floor and ceiling have converged
        if floor_index + 1 == ceiling_index:
            return ceiling_index
            
class Test(unittest.TestCase):

    def test_small_list(self):
        actual = find_rotation_point(['cape', 'cake'])
        expected = 1
        self.assertEqual(actual, expected)

    def test_medium_list(self):
        actual = find_rotation_point(['grape', 'orange', 'plum',
                                      'radish', 'apple'])
        expected = 4
        self.assertEqual(actual, expected)

    def test_large_list(self):
        actual = find_rotation_point(['ptolemaic', 'retrograde', 'supplant',
                                      'undulate', 'xenoepist', 'asymptote',
                                      'babka', 'banoffee', 'engender',
                                      'karpatka', 'othellolagkage'])
        expected = 5
        self.assertEqual(actual, expected)
unittest.main(verbosity=2)