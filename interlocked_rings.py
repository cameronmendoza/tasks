"""
    Name: Cameron Mendoza
    Date: 5 Feb, 2017
    Hyper Anna Interlocked Rings task
"""
# from __future__ import division
import unittest

""" DESCRIPTION
Magic squares comes to mind when thinking about this task.
See https://en.wikipedia.org/wiki/Magic_square

Start off with provided case, where n = 5

n - denoted as number of rings interlocked

Objective:
- Determine minimum and maximum value of sum for each ring
- Extrapolate to n = 50 and n = 500. For n = 500 provide solution overview.

Brute force would work but let's be smart about how we determine valid upper and
lower bounds on equal sums for the rings given n and not just n = 5. My strategy
is to restrict the actual number of permutations carried out by narrowing the
permutation/search space as much as possible (i.e. lower (min) and upper (max) sum value)

For n = 5, testing permutations results in only four valid solutions (Valid sums= 11,13(x2),14). Proven.

Derive a general solution for n = 5 and any odd [n] number of rings. Then apply
general solution to any n. Note that for even numbers of rings that a valid
solution is not feasible based on small n cases such as n = 2,4,6,...



Considering the following layout with n = 5 (same case for any odd number of rings):
"Olympic ring layout"
n = 5
overlapping regions = 4 = n(5) - 1
A   E   I
 B D F H     <- overlapping regions {B,D,F,H}
  C   G

Aim is to find valid total for A..I such that:
A+B = B+C+D = D+E+F = F+G+H = H+I

Say R denotes the magic total for each ring in the above case.

We then have,

5R = (A+B) + (B+C+D) + (D+E+F) + (F+G+H) + (H+I)

Notice that the overlapping regions are counted twice.

Simplifying results in:

5R = (A+B+C+D+E+F+G+H+I) + (B+D+F+H)          -- in other words sum of all spaces plus overlapping regions
As per the question (A+...+I) is mapped as the numeral equivalent.
Therefore can treat as sum of 1 to 9.
=> 5R = n(n+1)/2 + (B+D+F+H)                  -- where n = 9
=> 5R = 45 + (B+D+F+H)
(***)=> R = 9 + (B+D+F+H)/5                        -- so the sum of overlapping regions must be divisible by 5!
Also (***) implies that R must be strictly greater than 9!

Min possible sum of 4 values from set {1..9} = 1+2+3+4 = 10       --  (B+D+F+H)
Max possible sum of 4 values from set {1..9} = 9+8+7+6 = 30       --  (B+D+F+H)
Plugging into (***), without any validation we obtain lower and upper bound possible sum.

Min: R = 9 + (10)/5 = 11
Max: R = 9 + (30)/5 = 15

(!!!)Further upper bound (max sum value) constraint can be achieved considering n = 5 example above:
Max sum of 15 is actually not possible if you look at the problem from regions above/below perspective
like the olympic layout when n = 5.
Consider upper rings when n = 5:
3R = (A+B) + (D+E+F) + (H+I)
3R = (A+B+C+D+E+F+G+H+I) - (C+G)
Consindering (A+...+I) as SUM(1 to 9)
3R = 45 - (C+G) or (C+G) = 45 - 3R

So smallest possible sum value for C+G is 1+2 and max possible is 9+8:
Obtain following relationship,
3 <= C+G <= 17
28 <= 3R <= 42
10 <= R <= 14
So we get a better upper bound for n = 5. 14 instead of 15 (less things to look at yay!)

General rule of thumb for odd number of rings:
For n rings, there exists 2n - 1 areas to fill with numbers {1 ... 2n-1} and
n - 1 overlapping regions.
Considering the above and below layout like the n = 5 case, there are
(n + 1)/2 regions above and (n - 1)/2 regions below.

So sum total as above (where n = number of rings and R is magic total):
nR = SUM(1 to 2n-1) + SUM(overlapping regions)
nR = n * (2n - 1) + SUM(overlapping regions)

=> R = (2n - 1) + (SUM(overlapping regions) / n)     -- again we see overlapping regions sum must be divisble by n
2 points to note:
1) R must be strictly greater than 2n - 1
2) SUM(overlapping regions) must be divisible by n (i.e. whole number result) given we only place integers
   in available spaces

We now have a way of determining R_min and R_max,
for R_min we fill overlapping regions with numbers {1,2,...,n-1},
for R_max we fill overlapping regions with numbers {2n-1,2n-2,...,2n-n-1}

So simplified version, R_min = (2n - 1) + (1+...+n-1) / n = (5n - 3) / 2
                       R_max = (2n - 1) + (2n-1+...+2n-n-1) / n = (7n - 5) / 2



QUESTION 3 (Solution overview):
- To validate upper and lower bound sum value we need to show that a valid solution exists within the bounds
- To do this we need to answer the question of how many ways can we add X numbers from the set {1..2N-1} (where X is the number of overlapping regions for a problem with N rings) and get a sum that is divisible by N.
- Using this program as a way of reducing the problem subspace we can focus on permuting valid solutions between the resulting min and max sum value.
- Still fairly brute force but not as bad since we have narrowed down what sums we are looking for.

"""

# Helper functions
def is_odd(num):
    return True if (num & 1) else False

def sum_from_one_to_n(n):
    return (n * (n + 1)) / 2

# Returns number of blank spaces given
def num_blank_spaces(n):
    return (2 * n) - 1

def calculate_upper_bound_sum(n): # max sum value
    # See description for how this was obtained
    return ((7 * n) - 5) / 2

def calculate_lower_bound_sum(n): # min sum value
    # See description for how this was obtained
    return ((5 * n) - 3) / 2

def constrained_upper_bound_sum(num_rings, number_of_blanks): # based on (!!!) in description for odd ring case
    # consider number of upper+lower regions
    num_upper_regions = (num_rings + 1) / 2
    num_lower_regions = (num_rings - 1) / 2 # analogous to (C+G) in example
    values = range(1, number_of_blanks + 1)
    values_of_concern = values[:num_lower_regions]
    result = sum_from_one_to_n(number_of_blanks) - sum(values_of_concern)
    return result / num_upper_regions

def is_strictly_greater_than_num_blank_spaces(min_value, number_of_blanks):
    print "is_strictly_greater_than_num_blank_spaces() called with min_value=%r and number_of_blanks=%r" % (min_value, number_of_blanks)
    return True if (min_value > number_of_blanks) else False


num_rings = input("How many rings? ") # input() interprets type of input object
blank_spaces = num_blank_spaces(num_rings)

def solve_and_log(num_rings, blank_spaces):
    print "num_rings = %r" % num_rings
    print "blank_spaces = %r" % blank_spaces
    result = []
    print "Min sum value = %r" % calculate_lower_bound_sum(num_rings)
    result.append(calculate_lower_bound_sum(num_rings))
    if is_odd(num_rings): # utilize better upper bound
        print "Max sum value = %r" % constrained_upper_bound_sum(num_rings, blank_spaces)
        result.append(constrained_upper_bound_sum(num_rings, blank_spaces))
    else:
        print "Max sum value = %r" % calculate_upper_bound_sum(num_rings)
        result.append(calculate_upper_bound_sum(num_rings))
    # print result
    return result

solve_and_log(num_rings, blank_spaces)

print "--------------RUNNING UNIT TESTS--------------"

# Helper function for Rule 2)
def naive_check_possible_ranges_for_divisibility(n, overlapping):
    for i in xrange(1, n):
        if (sum(range(i, i + overlapping)) % n == 0): # FOUND A DIVISIBLE RANGE
            print "GOT ONE"
            print i
            return True
    return False

naive_check_possible_ranges_for_divisibility(50, 49)
naive_check_possible_ranges_for_divisibility(500,499)

# Unit tests
class TestSumOneToNMethod(unittest.TestCase):
    def test_simple_known_cases(self):
        self.assertEqual(sum_from_one_to_n(3), 6)
        self.assertEqual(sum_from_one_to_n(9), 45)

class TestIsOddMethod(unittest.TestCase):
    def test_odd_numbers(self):
        self.assertTrue(is_odd(1))
        self.assertTrue(is_odd(3))
        self.assertTrue(is_odd(7))
        self.assertTrue(is_odd(1337))

    def test_even_numbers(self):
        self.assertFalse(is_odd(2))
        self.assertFalse(is_odd(4))
        self.assertFalse(is_odd(10))

class TestQuestionTwo(unittest.TestCase): # n = 50
    # From General rule of thumb
    # validate 1) and 2)
    def test_rule_one_holds(self):
        # compare min with 2n - 1
        self.assertTrue(is_strictly_greater_than_num_blank_spaces(solve_and_log(50,99)[0], 99))

    def test_rule_two_holds(self): # can use knapsack problem idea to find suitable sum divisible by 50
        # with n - 1 overlapping regions = 49 overlapping regions for n=50
        # sum of 49 overlapping regions must be divisible by 50
        self.assertTrue(naive_check_possible_ranges_for_divisibility(50, 49))

class TestQuestionThree(unittest.TestCase): # n = 500
    # From General rule of thumb
    # validate 1) and 2)
    def test_rule_one_holds(self):
        # compare min with 2n - 1
        self.assertTrue(is_strictly_greater_than_num_blank_spaces(solve_and_log(500,999)[0], 999))

    def test_rule_two_holds(self): # can use knapsack problem idea to find suitable sum divisible by 500
        # with n - 1 overlapping regions = 499 overlapping regions for n=500
        # sum of 499 overlapping regions must be divisible by 500
        self.assertTrue(naive_check_possible_ranges_for_divisibility(500, 499))

if __name__ == '__main__':
    unittest.main()
