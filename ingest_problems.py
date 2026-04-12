import requests
import json

BASE_URL = "https://pypycode.com/api/problems/public-ingest"
#BASE_URL = "http://localhost:81/api/problems/public-ingest"
INGEST_KEY = "EMDgUmg7tzsgdf5r3eFd"

problems = [
    # ─────────────────────────────────────────────
    # 1
    {
        "slug": "pair-sum-finder",
        "title": "Pair Sum Finder",
        "difficulty": "easy",
        "description": (
            "You are given a basket of integers and a magic number called the 'goal'. "
            "Your task is to find two numbers in the basket that add up to the goal and return their positions. "
            "Each basket has exactly one valid pair, and you cannot reuse the same item twice. "
            "Return the indices in any order."
        ),
        "starterCode": "def pairSum(nums: list, target: int) -> list:\n    pass",
        "examples": [
            {"input": "nums = [2,7,11,15], target = 9", "output": "[0,1]", "explanation": "nums[0]+nums[1]=9"},
            {"input": "nums = [3,2,4], target = 6", "output": "[1,2]", "explanation": "nums[1]+nums[2]=6"},
            {"input": "nums = [1,5,3,7], target = 8", "output": "[1,3]", "explanation": "nums[1]+nums[3]=8"},
        ],
        "testCases": [
            {"function": "pairSum", "input": "[2,7,11,15], 9", "expectedOutput": "[0,1]"},
            {"function": "pairSum", "input": "[3,2,4], 6", "expectedOutput": "[1,2]"},
            {"function": "pairSum", "input": "[1,5,3,7], 8", "expectedOutput": "[1,3]"},
            {"function": "pairSum", "input": "[1,2,3,4,5], 9", "expectedOutput": "[3,4]"},
            {"function": "pairSum", "input": "[-1,-2,-3,-4], -6", "expectedOutput": "[1,3]"},
            {"function": "pairSum", "input": "[0,4,3,0], 0", "expectedOutput": "[0,3]"},
            {"function": "pairSum", "input": "[100,200,300], 500", "expectedOutput": "[1,2]"},
            {"function": "pairSum", "input": "[5,5], 10", "expectedOutput": "[0,1]"},
            {"function": "pairSum", "input": "[1,3,5,7,9], 12", "expectedOutput": "[2,4]"},
            {"function": "pairSum", "input": "[10,20,30,40,50], 70", "expectedOutput": "[2,4]"},
        ],
        "tags": ["array", "hash-table", "two-pointers"],
    },
    # ─────────────────────────────────────────────
    # 2
    {
        "slug": "flip-the-chain",
        "title": "Flip the Chain",
        "difficulty": "easy",
        "description": (
            "Imagine a chain of numbered beads stored as a linked list. "
            "A magician wants to flip the entire chain so the last bead becomes the first. "
            "Given the head of a singly linked list, return the head of the reversed chain. "
            "You must do this without allocating a new list — rearrange the pointers in place."
        ),
        "starterCode": "class ListNode:\n    def __init__(self, val=0, next=None):\n        self.val = val\n        self.next = next\n\ndef flipChain(head):\n    pass",
        "examples": [
            {"input": "head = [1,2,3,4,5]", "output": "[5,4,3,2,1]", "explanation": "All nodes reversed."},
            {"input": "head = [1,2]", "output": "[2,1]", "explanation": "Two nodes swapped."},
            {"input": "head = [7]", "output": "[7]", "explanation": "Single node unchanged."},
        ],
        "testCases": [
            {"function": "flipChain", "input": "[1,2,3,4,5]", "expectedOutput": "[5,4,3,2,1]"},
            {"function": "flipChain", "input": "[1,2]", "expectedOutput": "[2,1]"},
            {"function": "flipChain", "input": "[7]", "expectedOutput": "[7]"},
            {"function": "flipChain", "input": "[1,2,3]", "expectedOutput": "[3,2,1]"},
            {"function": "flipChain", "input": "[10,20,30,40]", "expectedOutput": "[40,30,20,10]"},
            {"function": "flipChain", "input": "[-1,-2,-3]", "expectedOutput": "[-3,-2,-1]"},
            {"function": "flipChain", "input": "[0,0,0]", "expectedOutput": "[0,0,0]"},
            {"function": "flipChain", "input": "[100,200]", "expectedOutput": "[200,100]"},
            {"function": "flipChain", "input": "[1,2,3,4,5,6]", "expectedOutput": "[6,5,4,3,2,1]"},
            {"function": "flipChain", "input": "[5,4,3,2,1]", "expectedOutput": "[1,2,3,4,5]"},
        ],
        "tags": ["linked-list", "two-pointers", "recursion"],
    },
    # ─────────────────────────────────────────────
    # 3
    {
        "slug": "bracket-harmony",
        "title": "Bracket Harmony",
        "difficulty": "easy",
        "description": (
            "A text editor plugin checks whether bracket usage in a code snippet is harmonious. "
            "A string is harmonious if every opening bracket has a matching closing bracket of the same type "
            "and they are properly nested. "
            "Given a string containing only '(', ')', '{', '}', '[', ']', return True if it is harmonious, else False."
        ),
        "starterCode": "def bracketHarmony(s: str) -> bool:\n    pass",
        "examples": [
            {"input": "s = \"()\"", "output": "True", "explanation": "One matched pair."},
            {"input": "s = \"()[{}]\"", "output": "True", "explanation": "All nested correctly."},
            {"input": "s = \"(]\"", "output": "False", "explanation": "Type mismatch."},
        ],
        "testCases": [
            {"function": "bracketHarmony", "input": "\"()\"", "expectedOutput": "True"},
            {"function": "bracketHarmony", "input": "\"()[{}]\"", "expectedOutput": "True"},
            {"function": "bracketHarmony", "input": "\"(]\"", "expectedOutput": "False"},
            {"function": "bracketHarmony", "input": "\"\"", "expectedOutput": "True"},
            {"function": "bracketHarmony", "input": "\"{[]}\"", "expectedOutput": "True"},
            {"function": "bracketHarmony", "input": "\"([)]\"", "expectedOutput": "False"},
            {"function": "bracketHarmony", "input": "\"]\"", "expectedOutput": "False"},
            {"function": "bracketHarmony", "input": "\"(((())))\"", "expectedOutput": "True"},
            {"function": "bracketHarmony", "input": "\"{{}[]()}\"", "expectedOutput": "True"},
            {"function": "bracketHarmony", "input": "\"((()\"", "expectedOutput": "False"},
        ],
        "tags": ["string", "stack"],
    },
    # ─────────────────────────────────────────────
    # 4
    {
        "slug": "staircase-paths",
        "title": "Staircase Paths",
        "difficulty": "easy",
        "description": (
            "A frog sits at the bottom of a staircase with n steps. "
            "Each jump the frog can hop exactly 1 or 2 steps forward. "
            "Count the total number of distinct hop sequences the frog can use to reach the top step. "
            "The answer grows quickly — notice the Fibonacci pattern hiding inside."
        ),
        "starterCode": "def staircasePaths(n: int) -> int:\n    pass",
        "examples": [
            {"input": "n = 2", "output": "2", "explanation": "Sequences: [1,1] or [2]."},
            {"input": "n = 3", "output": "3", "explanation": "Sequences: [1,1,1],[1,2],[2,1]."},
            {"input": "n = 4", "output": "5", "explanation": "Five distinct hop sequences."},
        ],
        "testCases": [
            {"function": "staircasePaths", "input": "1", "expectedOutput": "1"},
            {"function": "staircasePaths", "input": "2", "expectedOutput": "2"},
            {"function": "staircasePaths", "input": "3", "expectedOutput": "3"},
            {"function": "staircasePaths", "input": "4", "expectedOutput": "5"},
            {"function": "staircasePaths", "input": "5", "expectedOutput": "8"},
            {"function": "staircasePaths", "input": "6", "expectedOutput": "13"},
            {"function": "staircasePaths", "input": "7", "expectedOutput": "21"},
            {"function": "staircasePaths", "input": "10", "expectedOutput": "89"},
            {"function": "staircasePaths", "input": "15", "expectedOutput": "987"},
            {"function": "staircasePaths", "input": "20", "expectedOutput": "10946"},
        ],
        "tags": ["dynamic-programming", "memoization", "math"],
    },
    # ─────────────────────────────────────────────
    # 5
    {
        "slug": "sorted-array-probe",
        "title": "Sorted Array Probe",
        "difficulty": "easy",
        "description": (
            "A sorted list of integers represents a timeline of events. "
            "You need to probe the timeline to find when a specific event occurred — or report that it never happened. "
            "Return the index of the target event, or -1 if it is absent. "
            "Your solution must run in O(log n) time — linear scans are too slow."
        ),
        "starterCode": "def sortedProbe(nums: list, target: int) -> int:\n    pass",
        "examples": [
            {"input": "nums = [-1,0,3,5,9,12], target = 9", "output": "4", "explanation": "9 is at index 4."},
            {"input": "nums = [-1,0,3,5,9,12], target = 2", "output": "-1", "explanation": "2 is absent."},
            {"input": "nums = [1,3,5,7], target = 1", "output": "0", "explanation": "1 is at index 0."},
        ],
        "testCases": [
            {"function": "sortedProbe", "input": "[-1,0,3,5,9,12], 9", "expectedOutput": "4"},
            {"function": "sortedProbe", "input": "[-1,0,3,5,9,12], 2", "expectedOutput": "-1"},
            {"function": "sortedProbe", "input": "[1,3,5,7], 1", "expectedOutput": "0"},
            {"function": "sortedProbe", "input": "[5], 5", "expectedOutput": "0"},
            {"function": "sortedProbe", "input": "[5], 6", "expectedOutput": "-1"},
            {"function": "sortedProbe", "input": "[1,2,3,4,5,6,7,8,9,10], 7", "expectedOutput": "6"},
            {"function": "sortedProbe", "input": "[2,4,6,8,10], 10", "expectedOutput": "4"},
            {"function": "sortedProbe", "input": "[2,4,6,8,10], 3", "expectedOutput": "-1"},
            {"function": "sortedProbe", "input": "[-10,-5,0,5,10], 0", "expectedOutput": "2"},
            {"function": "sortedProbe", "input": "[100,200,300], 300", "expectedOutput": "2"},
        ],
        "tags": ["array", "binary-search"],
    },
    # ─────────────────────────────────────────────
    # 6
    {
        "slug": "peak-profit-window",
        "title": "Peak Profit Window",
        "difficulty": "easy",
        "description": (
            "A merchant records daily prices of a commodity in an array. "
            "They want to buy on one day and sell on a later day to maximise profit. "
            "Find the maximum profit achievable. "
            "If no profit is possible (prices only fall), return 0. "
            "You may only complete one buy-sell transaction."
        ),
        "starterCode": "def peakProfit(prices: list) -> int:\n    pass",
        "examples": [
            {"input": "prices = [7,1,5,3,6,4]", "output": "5", "explanation": "Buy at 1, sell at 6."},
            {"input": "prices = [7,6,4,3,1]", "output": "0", "explanation": "Prices only fall."},
            {"input": "prices = [1,2]", "output": "1", "explanation": "Buy at 1, sell at 2."},
        ],
        "testCases": [
            {"function": "peakProfit", "input": "[7,1,5,3,6,4]", "expectedOutput": "5"},
            {"function": "peakProfit", "input": "[7,6,4,3,1]", "expectedOutput": "0"},
            {"function": "peakProfit", "input": "[1,2]", "expectedOutput": "1"},
            {"function": "peakProfit", "input": "[2,4,1]", "expectedOutput": "2"},
            {"function": "peakProfit", "input": "[3,3,3]", "expectedOutput": "0"},
            {"function": "peakProfit", "input": "[1,2,3,4,5]", "expectedOutput": "4"},
            {"function": "peakProfit", "input": "[5,4,3,2,1,10]", "expectedOutput": "9"},
            {"function": "peakProfit", "input": "[1]", "expectedOutput": "0"},
            {"function": "peakProfit", "input": "[1,100,1,100]", "expectedOutput": "99"},
            {"function": "peakProfit", "input": "[10,5,4,3,8,2]", "expectedOutput": "5"},
        ],
        "tags": ["array", "greedy", "sliding-window"],
    },
    # ─────────────────────────────────────────────
    # 7
    {
        "slug": "ripple-sum",
        "title": "Ripple Sum",
        "difficulty": "medium",
        "description": (
            "Given an integer array, find the contiguous sub-sequence whose elements sum to the largest value. "
            "Think of each element as a water ripple — you want the stretch of water that rises highest in total. "
            "The sub-sequence must contain at least one element. "
            "Return the maximum sum."
        ),
        "starterCode": "def rippleSum(nums: list) -> int:\n    pass",
        "examples": [
            {"input": "nums = [-2,1,-3,4,-1,2,1,-5,4]", "output": "6", "explanation": "[4,-1,2,1] sums to 6."},
            {"input": "nums = [1]", "output": "1", "explanation": "Only one element."},
            {"input": "nums = [5,4,-1,7,8]", "output": "23", "explanation": "Entire array sums to 23."},
        ],
        "testCases": [
            {"function": "rippleSum", "input": "[-2,1,-3,4,-1,2,1,-5,4]", "expectedOutput": "6"},
            {"function": "rippleSum", "input": "[1]", "expectedOutput": "1"},
            {"function": "rippleSum", "input": "[5,4,-1,7,8]", "expectedOutput": "23"},
            {"function": "rippleSum", "input": "[-1,-2,-3,-4]", "expectedOutput": "-1"},
            {"function": "rippleSum", "input": "[0,0,0]", "expectedOutput": "0"},
            {"function": "rippleSum", "input": "[100,-1,100]", "expectedOutput": "199"},
            {"function": "rippleSum", "input": "[-5,8,-3,9,-2]", "expectedOutput": "14"},
            {"function": "rippleSum", "input": "[1,2,3,4,5]", "expectedOutput": "15"},
            {"function": "rippleSum", "input": "[-10,5,-1,5,-1,5]", "expectedOutput": "13"},
            {"function": "rippleSum", "input": "[3,-1,3,-1,3]", "expectedOutput": "7"},
        ],
        "tags": ["array", "dynamic-programming", "divide-and-conquer", "kadane"],
    },
    # ─────────────────────────────────────────────
    # 8
    {
        "slug": "island-counter",
        "title": "Island Counter",
        "difficulty": "medium",
        "description": (
            "A satellite image is represented as a 2D grid of '1' (land) and '0' (water). "
            "An island is a group of land cells connected horizontally or vertically, surrounded by water. "
            "Count how many distinct islands appear in the image. "
            "You may modify the grid in place during traversal."
        ),
        "starterCode": "def islandCounter(grid: list) -> int:\n    pass",
        "examples": [
            {"input": "grid = [[\"1\",\"1\",\"0\"],[\"0\",\"1\",\"0\"],[\"0\",\"0\",\"1\"]]", "output": "2", "explanation": "Two separate islands."},
            {"input": "grid = [[\"1\",\"1\",\"1\"],[\"0\",\"1\",\"0\"]]", "output": "1", "explanation": "All land is connected."},
            {"input": "grid = [[\"0\",\"0\"],[\"0\",\"0\"]]", "output": "0", "explanation": "No land at all."},
        ],
        "testCases": [
            {"function": "islandCounter", "input": "[[\"1\",\"1\",\"0\"],[\"0\",\"1\",\"0\"],[\"0\",\"0\",\"1\"]]", "expectedOutput": "2"},
            {"function": "islandCounter", "input": "[[\"1\",\"1\",\"1\"],[\"0\",\"1\",\"0\"]]", "expectedOutput": "1"},
            {"function": "islandCounter", "input": "[[\"0\",\"0\"],[\"0\",\"0\"]]", "expectedOutput": "0"},
            {"function": "islandCounter", "input": "[[\"1\"]]", "expectedOutput": "1"},
            {"function": "islandCounter", "input": "[[\"1\",\"0\",\"1\"]]", "expectedOutput": "2"},
            {"function": "islandCounter", "input": "[[\"1\",\"0\"],[\"0\",\"1\"]]", "expectedOutput": "2"},
            {"function": "islandCounter", "input": "[[\"1\",\"1\"],[\"1\",\"1\"]]", "expectedOutput": "1"},
            {"function": "islandCounter", "input": "[[\"1\",\"0\",\"1\"],[\"0\",\"1\",\"0\"],[\"1\",\"0\",\"1\"]]", "expectedOutput": "5"},
            {"function": "islandCounter", "input": "[[\"1\",\"1\",\"0\",\"1\"]]", "expectedOutput": "2"},
            {"function": "islandCounter", "input": "[[\"1\"],[\"1\"],[\"0\"],[\"1\"]]", "expectedOutput": "2"},
        ],
        "tags": ["graph", "dfs", "bfs", "matrix", "union-find"],
    },
    # ─────────────────────────────────────────────
    # 9
    {
        "slug": "tree-level-snapshot",
        "title": "Tree Level Snapshot",
        "difficulty": "medium",
        "description": (
            "A photographer captures each floor of a building as a group photo. "
            "Given the root of a binary tree, return a list of lists where each inner list contains "
            "the values of nodes at that depth level, from left to right. "
            "This is a level-by-level snapshot of the tree."
        ),
        "starterCode": "class TreeNode:\n    def __init__(self, val=0, left=None, right=None):\n        self.val = val\n        self.left = left\n        self.right = right\n\ndef levelSnapshot(root) -> list:\n    pass",
        "examples": [
            {"input": "root = [3,9,20,null,null,15,7]", "output": "[[3],[9,20],[15,7]]", "explanation": "Three levels captured."},
            {"input": "root = [1]", "output": "[[1]]", "explanation": "Single node, one level."},
            {"input": "root = []", "output": "[]", "explanation": "Empty tree."},
        ],
        "testCases": [
            {"function": "levelSnapshot", "input": "[3,9,20,null,null,15,7]", "expectedOutput": "[[3],[9,20],[15,7]]"},
            {"function": "levelSnapshot", "input": "[1]", "expectedOutput": "[[1]]"},
            {"function": "levelSnapshot", "input": "[]", "expectedOutput": "[]"},
            {"function": "levelSnapshot", "input": "[1,2,3]", "expectedOutput": "[[1],[2,3]]"},
            {"function": "levelSnapshot", "input": "[1,2,null,3]", "expectedOutput": "[[1],[2],[3]]"},
            {"function": "levelSnapshot", "input": "[1,null,2,null,3]", "expectedOutput": "[[1],[2],[3]]"},
            {"function": "levelSnapshot", "input": "[5,3,8,1,4,7,9]", "expectedOutput": "[[5],[3,8],[1,4,7,9]]"},
            {"function": "levelSnapshot", "input": "[1,2,3,4,5,6,7]", "expectedOutput": "[[1],[2,3],[4,5,6,7]]"},
            {"function": "levelSnapshot", "input": "[10,5,15]", "expectedOutput": "[[10],[5,15]]"},
            {"function": "levelSnapshot", "input": "[1,2,3,null,null,4,5]", "expectedOutput": "[[1],[2,3],[4,5]]"},
        ],
        "tags": ["tree", "bfs", "binary-tree", "queue"],
    },
    # ─────────────────────────────────────────────
    # 10
    {
        "slug": "anagram-detective",
        "title": "Anagram Detective",
        "difficulty": "easy",
        "description": (
            "A linguistics tool checks whether two words are secret rearrangements of each other. "
            "Given two strings s and t, return True if t is an anagram of s, else False. "
            "Both strings consist only of lowercase English letters. "
            "An anagram uses all the same characters the same number of times, just in a different order."
        ),
        "starterCode": "def anagramDetective(s: str, t: str) -> bool:\n    pass",
        "examples": [
            {"input": "s = \"anagram\", t = \"nagaram\"", "output": "True", "explanation": "Same characters rearranged."},
            {"input": "s = \"rat\", t = \"car\"", "output": "False", "explanation": "Different characters."},
            {"input": "s = \"listen\", t = \"silent\"", "output": "True", "explanation": "Classic anagram pair."},
        ],
        "testCases": [
            {"function": "anagramDetective", "input": "\"anagram\", \"nagaram\"", "expectedOutput": "True"},
            {"function": "anagramDetective", "input": "\"rat\", \"car\"", "expectedOutput": "False"},
            {"function": "anagramDetective", "input": "\"listen\", \"silent\"", "expectedOutput": "True"},
            {"function": "anagramDetective", "input": "\"a\", \"a\"", "expectedOutput": "True"},
            {"function": "anagramDetective", "input": "\"ab\", \"ba\"", "expectedOutput": "True"},
            {"function": "anagramDetective", "input": "\"abc\", \"ab\"", "expectedOutput": "False"},
            {"function": "anagramDetective", "input": "\"aab\", \"aba\"", "expectedOutput": "True"},
            {"function": "anagramDetective", "input": "\"hello\", \"world\"", "expectedOutput": "False"},
            {"function": "anagramDetective", "input": "\"abcd\", \"dcba\"", "expectedOutput": "True"},
            {"function": "anagramDetective", "input": "\"aaab\", \"aaba\"", "expectedOutput": "True"},
        ],
        "tags": ["string", "hash-table", "sorting"],
    },
    # ─────────────────────────────────────────────
    # 11
    {
        "slug": "palindrome-probe",
        "title": "Palindrome Probe",
        "difficulty": "easy",
        "description": (
            "A quality-control system scans product serial codes to verify they read the same forwards and backwards. "
            "Given an integer x, return True if it is a palindrome, False otherwise. "
            "Negative numbers are never palindromes. "
            "Solve it without converting the number to a string."
        ),
        "starterCode": "def palindromeProbe(x: int) -> bool:\n    pass",
        "examples": [
            {"input": "x = 121", "output": "True", "explanation": "Reads 121 both ways."},
            {"input": "x = -121", "output": "False", "explanation": "Negative numbers fail."},
            {"input": "x = 10", "output": "False", "explanation": "Reversed is 01, not 10."},
        ],
        "testCases": [
            {"function": "palindromeProbe", "input": "121", "expectedOutput": "True"},
            {"function": "palindromeProbe", "input": "-121", "expectedOutput": "False"},
            {"function": "palindromeProbe", "input": "10", "expectedOutput": "False"},
            {"function": "palindromeProbe", "input": "0", "expectedOutput": "True"},
            {"function": "palindromeProbe", "input": "1221", "expectedOutput": "True"},
            {"function": "palindromeProbe", "input": "12321", "expectedOutput": "True"},
            {"function": "palindromeProbe", "input": "123", "expectedOutput": "False"},
            {"function": "palindromeProbe", "input": "1001", "expectedOutput": "True"},
            {"function": "palindromeProbe", "input": "9", "expectedOutput": "True"},
            {"function": "palindromeProbe", "input": "11", "expectedOutput": "True"},
        ],
        "tags": ["math"],
    },
    # ─────────────────────────────────────────────
    # 12
    {
        "slug": "merge-two-rails",
        "title": "Merge Two Rails",
        "difficulty": "easy",
        "description": (
            "Two railway lines each have stations sorted by distance. "
            "Merge both lines into a single sorted line. "
            "Given the heads of two sorted linked lists, merge them into one sorted linked list "
            "and return its head. Do not allocate new nodes — reuse the existing ones."
        ),
        "starterCode": "class ListNode:\n    def __init__(self, val=0, next=None):\n        self.val = val\n        self.next = next\n\ndef mergeTwoRails(l1, l2):\n    pass",
        "examples": [
            {"input": "l1 = [1,2,4], l2 = [1,3,4]", "output": "[1,1,2,3,4,4]", "explanation": "Interleaved in order."},
            {"input": "l1 = [], l2 = []", "output": "[]", "explanation": "Both empty."},
            {"input": "l1 = [], l2 = [0]", "output": "[0]", "explanation": "One empty list."},
        ],
        "testCases": [
            {"function": "mergeTwoRails", "input": "[1,2,4], [1,3,4]", "expectedOutput": "[1,1,2,3,4,4]"},
            {"function": "mergeTwoRails", "input": "[], []", "expectedOutput": "[]"},
            {"function": "mergeTwoRails", "input": "[], [0]", "expectedOutput": "[0]"},
            {"function": "mergeTwoRails", "input": "[1], [2]", "expectedOutput": "[1,2]"},
            {"function": "mergeTwoRails", "input": "[2], [1]", "expectedOutput": "[1,2]"},
            {"function": "mergeTwoRails", "input": "[1,3,5], [2,4,6]", "expectedOutput": "[1,2,3,4,5,6]"},
            {"function": "mergeTwoRails", "input": "[1,1,1], [1,1,1]", "expectedOutput": "[1,1,1,1,1,1]"},
            {"function": "mergeTwoRails", "input": "[5], [1,2,3]", "expectedOutput": "[1,2,3,5]"},
            {"function": "mergeTwoRails", "input": "[1,2,3], [4,5,6]", "expectedOutput": "[1,2,3,4,5,6]"},
            {"function": "mergeTwoRails", "input": "[-3,-1], [-2,0]", "expectedOutput": "[-3,-2,-1,0]"},
        ],
        "tags": ["linked-list", "recursion", "two-pointers"],
    },
    # ─────────────────────────────────────────────
    # 13
    {
        "slug": "depth-of-forest",
        "title": "Depth of the Forest",
        "difficulty": "easy",
        "description": (
            "A forest ranger measures the deepest point of a tree by counting levels from root to the farthest leaf. "
            "Given a binary tree root, return the maximum depth — "
            "the number of nodes along the longest path from the root to any leaf node."
        ),
        "starterCode": "class TreeNode:\n    def __init__(self, val=0, left=None, right=None):\n        self.val = val\n        self.left = left\n        self.right = right\n\ndef depthOfForest(root) -> int:\n    pass",
        "examples": [
            {"input": "root = [3,9,20,null,null,15,7]", "output": "3", "explanation": "Deepest path has 3 nodes."},
            {"input": "root = [1,null,2]", "output": "2", "explanation": "Right-skewed depth 2."},
            {"input": "root = []", "output": "0", "explanation": "Empty tree."},
        ],
        "testCases": [
            {"function": "depthOfForest", "input": "[3,9,20,null,null,15,7]", "expectedOutput": "3"},
            {"function": "depthOfForest", "input": "[1,null,2]", "expectedOutput": "2"},
            {"function": "depthOfForest", "input": "[]", "expectedOutput": "0"},
            {"function": "depthOfForest", "input": "[1]", "expectedOutput": "1"},
            {"function": "depthOfForest", "input": "[1,2,3,4]", "expectedOutput": "3"},
            {"function": "depthOfForest", "input": "[1,2,3,4,5,6,7]", "expectedOutput": "3"},
            {"function": "depthOfForest", "input": "[1,2,null,3,null,4]", "expectedOutput": "4"},
            {"function": "depthOfForest", "input": "[10,5,15,3,7]", "expectedOutput": "3"},
            {"function": "depthOfForest", "input": "[1,2]", "expectedOutput": "2"},
            {"function": "depthOfForest", "input": "[1,2,3,null,null,null,4]", "expectedOutput": "3"},
        ],
        "tags": ["tree", "dfs", "bfs", "binary-tree", "recursion"],
    },
    # ─────────────────────────────────────────────
    # 14
    {
        "slug": "roman-decoder",
        "title": "Roman Decoder",
        "difficulty": "easy",
        "description": (
            "An archaeologist discovers inscriptions in Roman numerals and needs an automatic decoder. "
            "Given a valid Roman numeral string, convert it to an integer. "
            "Remember the subtraction rule: IV=4, IX=9, XL=40, XC=90, CD=400, CM=900. "
            "Input is guaranteed to be in range [1, 3999]."
        ),
        "starterCode": "def romanDecoder(s: str) -> int:\n    pass",
        "examples": [
            {"input": "s = \"III\"", "output": "3", "explanation": "3 = 1+1+1."},
            {"input": "s = \"IX\"", "output": "9", "explanation": "9 = 10-1."},
            {"input": "s = \"MCMXCIV\"", "output": "1994", "explanation": "1000+900+90+4."},
        ],
        "testCases": [
            {"function": "romanDecoder", "input": "\"III\"", "expectedOutput": "3"},
            {"function": "romanDecoder", "input": "\"IX\"", "expectedOutput": "9"},
            {"function": "romanDecoder", "input": "\"MCMXCIV\"", "expectedOutput": "1994"},
            {"function": "romanDecoder", "input": "\"IV\"", "expectedOutput": "4"},
            {"function": "romanDecoder", "input": "\"LVIII\"", "expectedOutput": "58"},
            {"function": "romanDecoder", "input": "\"XL\"", "expectedOutput": "40"},
            {"function": "romanDecoder", "input": "\"CD\"", "expectedOutput": "400"},
            {"function": "romanDecoder", "input": "\"CM\"", "expectedOutput": "900"},
            {"function": "romanDecoder", "input": "\"MMXXIV\"", "expectedOutput": "2024"},
            {"function": "romanDecoder", "input": "\"DCCCXC\"", "expectedOutput": "890"},
        ],
        "tags": ["string", "hash-table", "math"],
    },
    # ─────────────────────────────────────────────
    # 15
    {
        "slug": "spiral-matrix-scan",
        "title": "Spiral Matrix Scan",
        "difficulty": "medium",
        "description": (
            "A printer head moves in a clockwise spiral to print all cells of a 2D matrix. "
            "Given an m x n matrix, return all elements in the order the printer head visits them — "
            "starting from the top-left, moving right, then down, then left, then up, spiralling inward."
        ),
        "starterCode": "def spiralMatrixScan(matrix: list) -> list:\n    pass",
        "examples": [
            {"input": "matrix = [[1,2,3],[4,5,6],[7,8,9]]", "output": "[1,2,3,6,9,8,7,4,5]", "explanation": "Clockwise spiral from top-left."},
            {"input": "matrix = [[1,2,3,4],[5,6,7,8],[9,10,11,12]]", "output": "[1,2,3,4,8,12,11,10,9,5,6,7]", "explanation": "3x4 spiral."},
            {"input": "matrix = [[1]]", "output": "[1]", "explanation": "Single element."},
        ],
        "testCases": [
            {"function": "spiralMatrixScan", "input": "[[1,2,3],[4,5,6],[7,8,9]]", "expectedOutput": "[1,2,3,6,9,8,7,4,5]"},
            {"function": "spiralMatrixScan", "input": "[[1,2,3,4],[5,6,7,8],[9,10,11,12]]", "expectedOutput": "[1,2,3,4,8,12,11,10,9,5,6,7]"},
            {"function": "spiralMatrixScan", "input": "[[1]]", "expectedOutput": "[1]"},
            {"function": "spiralMatrixScan", "input": "[[1,2],[3,4]]", "expectedOutput": "[1,2,4,3]"},
            {"function": "spiralMatrixScan", "input": "[[1,2,3]]", "expectedOutput": "[1,2,3]"},
            {"function": "spiralMatrixScan", "input": "[[1],[2],[3]]", "expectedOutput": "[1,2,3]"},
            {"function": "spiralMatrixScan", "input": "[[1,2,3],[4,5,6]]", "expectedOutput": "[1,2,3,6,5,4]"},
            {"function": "spiralMatrixScan", "input": "[[1,2],[3,4],[5,6]]", "expectedOutput": "[1,2,4,6,5,3]"},
            {"function": "spiralMatrixScan", "input": "[[1,2,3,4],[5,6,7,8]]", "expectedOutput": "[1,2,3,4,8,7,6,5]"},
            {"function": "spiralMatrixScan", "input": "[[1,2,3],[4,5,6],[7,8,9],[10,11,12]]", "expectedOutput": "[1,2,3,6,9,12,11,10,7,4,5,8]"},
        ],
        "tags": ["array", "matrix", "simulation"],
    },
    # ─────────────────────────────────────────────
    # 16
    {
        "slug": "word-path-search",
        "title": "Word Path Search",
        "difficulty": "medium",
        "description": (
            "A word is hidden inside a 2D grid of letters. "
            "You can trace the word by moving to adjacent cells (up, down, left, right) without reusing a cell in the same path. "
            "Given a board and a word, return True if the word can be traced, False otherwise."
        ),
        "starterCode": "def wordPathSearch(board: list, word: str) -> bool:\n    pass",
        "examples": [
            {"input": "board = [[\"A\",\"B\",\"C\"],[\"D\",\"E\",\"F\"]], word = \"BEF\"", "output": "True", "explanation": "B->E->F is a valid path."},
            {"input": "board = [[\"A\",\"B\"],[\"C\",\"D\"]], word = \"ABDC\"", "output": "True", "explanation": "A->B->D->C traced."},
            {"input": "board = [[\"A\",\"B\"],[\"C\",\"D\"]], word = \"ABCD\"", "output": "False", "explanation": "D and C are not adjacent after B."},
        ],
        "testCases": [
            {"function": "wordPathSearch", "input": "[[\"A\",\"B\",\"C\"],[\"D\",\"E\",\"F\"]], \"BEF\"", "expectedOutput": "True"},
            {"function": "wordPathSearch", "input": "[[\"A\",\"B\"],[\"C\",\"D\"]], \"ABDC\"", "expectedOutput": "True"},
            {"function": "wordPathSearch", "input": "[[\"A\",\"B\"],[\"C\",\"D\"]], \"ABCD\"", "expectedOutput": "False"},
            {"function": "wordPathSearch", "input": "[[\"A\"]], \"A\"", "expectedOutput": "True"},
            {"function": "wordPathSearch", "input": "[[\"A\"]], \"B\"", "expectedOutput": "False"},
            {"function": "wordPathSearch", "input": "[[\"A\",\"B\",\"C\"],[\"D\",\"E\",\"F\"],[\"G\",\"H\",\"I\"]], \"AEI\"", "expectedOutput": "False"},
            {"function": "wordPathSearch", "input": "[[\"A\",\"B\",\"C\"],[\"D\",\"E\",\"F\"],[\"G\",\"H\",\"I\"]], \"DEF\"", "expectedOutput": "True"},
            {"function": "wordPathSearch", "input": "[[\"A\",\"B\",\"C\"],[\"D\",\"E\",\"F\"],[\"G\",\"H\",\"I\"]], \"ABCFEI\"", "expectedOutput": "True"},
            {"function": "wordPathSearch", "input": "[[\"A\",\"A\"],[\"A\",\"A\"]], \"AAAA\"", "expectedOutput": "True"},
            {"function": "wordPathSearch", "input": "[[\"A\",\"A\"],[\"A\",\"A\"]], \"AAAAA\"", "expectedOutput": "False"},
        ],
        "tags": ["matrix", "dfs", "backtracking"],
    },
    # ─────────────────────────────────────────────
    # 17
    {
        "slug": "coin-change-greedy",
        "title": "Coin Change Challenge",
        "difficulty": "medium",
        "description": (
            "A vending machine has coins of various denominations. "
            "Given a list of coin denominations and a target amount, "
            "return the fewest number of coins needed to make up that amount exactly. "
            "If it is impossible, return -1. You have an unlimited supply of each denomination."
        ),
        "starterCode": "def coinChange(coins: list, amount: int) -> int:\n    pass",
        "examples": [
            {"input": "coins = [1,5,6,9], amount = 11", "output": "2", "explanation": "Use coins 5+6=11."},
            {"input": "coins = [2], amount = 3", "output": "-1", "explanation": "Cannot make 3 with only 2s."},
            {"input": "coins = [1,2,5], amount = 11", "output": "3", "explanation": "5+5+1=11."},
        ],
        "testCases": [
            {"function": "coinChange", "input": "[1,5,6,9], 11", "expectedOutput": "2"},
            {"function": "coinChange", "input": "[2], 3", "expectedOutput": "-1"},
            {"function": "coinChange", "input": "[1,2,5], 11", "expectedOutput": "3"},
            {"function": "coinChange", "input": "[1], 0", "expectedOutput": "0"},
            {"function": "coinChange", "input": "[1], 1", "expectedOutput": "1"},
            {"function": "coinChange", "input": "[1], 100", "expectedOutput": "100"},
            {"function": "coinChange", "input": "[2,5,10], 6", "expectedOutput": "3"},
            {"function": "coinChange", "input": "[186,419,83,408], 6249", "expectedOutput": "20"},
            {"function": "coinChange", "input": "[1,2,5], 0", "expectedOutput": "0"},
            {"function": "coinChange", "input": "[3,7], 10", "expectedOutput": "2"},
        ],
        "tags": ["dynamic-programming", "bfs", "array"],
    },
    # ─────────────────────────────────────────────
    # 18
    {
        "slug": "rotting-spread",
        "title": "Rotting Spread",
        "difficulty": "medium",
        "description": (
            "In a fruit warehouse, some oranges are already rotten. "
            "Each minute, a rotten orange infects all fresh neighbours (up/down/left/right). "
            "Given a grid where 0=empty, 1=fresh, 2=rotten, return the minimum minutes until no fresh orange remains. "
            "If some fresh oranges can never rot, return -1."
        ),
        "starterCode": "def rottingSpread(grid: list) -> int:\n    pass",
        "examples": [
            {"input": "grid = [[2,1,1],[1,1,0],[0,1,1]]", "output": "4", "explanation": "All infected after 4 minutes."},
            {"input": "grid = [[2,1,1],[0,1,1],[1,0,1]]", "output": "-1", "explanation": "Bottom-left orange isolated."},
            {"input": "grid = [[0,2]]", "output": "0", "explanation": "No fresh oranges."},
        ],
        "testCases": [
            {"function": "rottingSpread", "input": "[[2,1,1],[1,1,0],[0,1,1]]", "expectedOutput": "4"},
            {"function": "rottingSpread", "input": "[[2,1,1],[0,1,1],[1,0,1]]", "expectedOutput": "-1"},
            {"function": "rottingSpread", "input": "[[0,2]]", "expectedOutput": "0"},
            {"function": "rottingSpread", "input": "[[1]]", "expectedOutput": "-1"},
            {"function": "rottingSpread", "input": "[[2]]", "expectedOutput": "0"},
            {"function": "rottingSpread", "input": "[[0]]", "expectedOutput": "0"},
            {"function": "rottingSpread", "input": "[[2,1],[1,1]]", "expectedOutput": "2"},
            {"function": "rottingSpread", "input": "[[1,2],[1,1]]", "expectedOutput": "2"},
            {"function": "rottingSpread", "input": "[[2,2],[2,2]]", "expectedOutput": "0"},
            {"function": "rottingSpread", "input": "[[1,1,1],[1,2,1],[1,1,1]]", "expectedOutput": "2"},
        ],
        "tags": ["graph", "bfs", "matrix"],
    },
    # ─────────────────────────────────────────────
    # 19
    {
        "slug": "course-prerequisites",
        "title": "Course Prerequisites",
        "difficulty": "medium",
        "description": (
            "A university offers n courses numbered 0 to n-1. "
            "Some courses have prerequisites — you must finish course A before taking course B. "
            "Given the number of courses and a list of [course, prerequisite] pairs, "
            "determine if it is possible to complete all courses. "
            "Return True if possible, False if a circular dependency exists."
        ),
        "starterCode": "def canFinishCourses(numCourses: int, prerequisites: list) -> bool:\n    pass",
        "examples": [
            {"input": "numCourses = 2, prerequisites = [[1,0]]", "output": "True", "explanation": "Take 0 then 1."},
            {"input": "numCourses = 2, prerequisites = [[1,0],[0,1]]", "output": "False", "explanation": "Circular: each requires the other."},
            {"input": "numCourses = 4, prerequisites = [[1,0],[2,1],[3,2]]", "output": "True", "explanation": "Linear chain, no cycle."},
        ],
        "testCases": [
            {"function": "canFinishCourses", "input": "2, [[1,0]]", "expectedOutput": "True"},
            {"function": "canFinishCourses", "input": "2, [[1,0],[0,1]]", "expectedOutput": "False"},
            {"function": "canFinishCourses", "input": "4, [[1,0],[2,1],[3,2]]", "expectedOutput": "True"},
            {"function": "canFinishCourses", "input": "1, []", "expectedOutput": "True"},
            {"function": "canFinishCourses", "input": "3, [[0,1],[0,2],[1,2]]", "expectedOutput": "True"},
            {"function": "canFinishCourses", "input": "3, [[0,1],[1,2],[2,0]]", "expectedOutput": "False"},
            {"function": "canFinishCourses", "input": "5, [[0,1],[1,2],[2,3],[3,4]]", "expectedOutput": "True"},
            {"function": "canFinishCourses", "input": "5, [[0,1],[1,2],[2,3],[3,4],[4,2]]", "expectedOutput": "False"},
            {"function": "canFinishCourses", "input": "2, []", "expectedOutput": "True"},
            {"function": "canFinishCourses", "input": "4, [[0,1],[3,1],[1,3],[3,2]]", "expectedOutput": "False"},
        ],
        "tags": ["graph", "dfs", "bfs", "topological-sort", "cycle-detection"],
    },
    # ─────────────────────────────────────────────
    # 20
    {
        "slug": "longest-no-repeat",
        "title": "Longest No-Repeat Stretch",
        "difficulty": "medium",
        "description": (
            "A data analyst wants to find the longest stretch of a message where no character repeats. "
            "Given a string s, return the length of the longest substring that contains all unique characters. "
            "Use a sliding window approach for an efficient solution."
        ),
        "starterCode": "def longestNoRepeat(s: str) -> int:\n    pass",
        "examples": [
            {"input": "s = \"abcabcbb\"", "output": "3", "explanation": "\"abc\" is the longest unique substring."},
            {"input": "s = \"bbbbb\"", "output": "1", "explanation": "Only single 'b' is unique."},
            {"input": "s = \"pwwkew\"", "output": "3", "explanation": "\"wke\" is the longest."},
        ],
        "testCases": [
            {"function": "longestNoRepeat", "input": "\"abcabcbb\"", "expectedOutput": "3"},
            {"function": "longestNoRepeat", "input": "\"bbbbb\"", "expectedOutput": "1"},
            {"function": "longestNoRepeat", "input": "\"pwwkew\"", "expectedOutput": "3"},
            {"function": "longestNoRepeat", "input": "\"\"", "expectedOutput": "0"},
            {"function": "longestNoRepeat", "input": "\" \"", "expectedOutput": "1"},
            {"function": "longestNoRepeat", "input": "\"au\"", "expectedOutput": "2"},
            {"function": "longestNoRepeat", "input": "\"dvdf\"", "expectedOutput": "3"},
            {"function": "longestNoRepeat", "input": "\"abcdefg\"", "expectedOutput": "7"},
            {"function": "longestNoRepeat", "input": "\"aab\"", "expectedOutput": "2"},
            {"function": "longestNoRepeat", "input": "\"tmmzuxt\"", "expectedOutput": "5"},
        ],
        "tags": ["string", "sliding-window", "hash-table", "two-pointers"],
    },
    # ─────────────────────────────────────────────
    # 21
    {
        "slug": "matrix-zero-spreader",
        "title": "Matrix Zero Spreader",
        "difficulty": "medium",
        "description": (
            "A simulation grid has certain cells marked zero. "
            "Whenever a cell is zero, its entire row and column must also become zero. "
            "Given an m x n integer matrix, apply this rule in-place. "
            "Use O(1) extra space (excluding the matrix itself)."
        ),
        "starterCode": "def matrixZeroSpreader(matrix: list) -> None:\n    pass",
        "examples": [
            {"input": "matrix = [[1,1,1],[1,0,1],[1,1,1]]", "output": "[[1,0,1],[0,0,0],[1,0,1]]", "explanation": "Row 1 and col 1 zeroed."},
            {"input": "matrix = [[0,1,2,0],[3,4,5,2],[1,3,1,5]]", "output": "[[0,0,0,0],[0,4,5,0],[0,3,1,0]]", "explanation": "Row 0 and cols 0,3 zeroed."},
            {"input": "matrix = [[1]]", "output": "[[1]]", "explanation": "No zeros, unchanged."},
        ],
        "testCases": [
            {"function": "matrixZeroSpreader", "input": "[[1,1,1],[1,0,1],[1,1,1]]", "expectedOutput": "[[1,0,1],[0,0,0],[1,0,1]]"},
            {"function": "matrixZeroSpreader", "input": "[[0,1,2,0],[3,4,5,2],[1,3,1,5]]", "expectedOutput": "[[0,0,0,0],[0,4,5,0],[0,3,1,0]]"},
            {"function": "matrixZeroSpreader", "input": "[[1]]", "expectedOutput": "[[1]]"},
            {"function": "matrixZeroSpreader", "input": "[[0]]", "expectedOutput": "[[0]]"},
            {"function": "matrixZeroSpreader", "input": "[[1,0],[1,1]]", "expectedOutput": "[[0,0],[1,0]]"},
            {"function": "matrixZeroSpreader", "input": "[[1,2,3],[4,0,6],[7,8,9]]", "expectedOutput": "[[1,0,3],[0,0,0],[7,0,9]]"},
            {"function": "matrixZeroSpreader", "input": "[[1,1],[0,1]]", "expectedOutput": "[[0,1],[0,0]]"},
            {"function": "matrixZeroSpreader", "input": "[[1,2],[3,4]]", "expectedOutput": "[[1,2],[3,4]]"},
            {"function": "matrixZeroSpreader", "input": "[[0,0],[0,0]]", "expectedOutput": "[[0,0],[0,0]]"},
            {"function": "matrixZeroSpreader", "input": "[[1,0,3],[0,5,6],[7,8,9]]", "expectedOutput": "[[0,0,0],[0,0,0],[0,0,9]]"},
        ],
        "tags": ["matrix", "array", "hash-table"],
    },
    # ─────────────────────────────────────────────
    # 22
    {
        "slug": "jump-game-reach",
        "title": "Jump Game Reach",
        "difficulty": "medium",
        "description": (
            "A frog sits on index 0 of an array. Each element tells the frog the maximum jump length from that spot. "
            "The frog wants to reach the last index. "
            "Return True if the last index is reachable, False otherwise. "
            "Greedy thinking works here — always check the farthest reachable position."
        ),
        "starterCode": "def jumpGameReach(nums: list) -> bool:\n    pass",
        "examples": [
            {"input": "nums = [2,3,1,1,4]", "output": "True", "explanation": "Jump 1 to index 1, then 3 to the end."},
            {"input": "nums = [3,2,1,0,4]", "output": "False", "explanation": "Always land on 0, stuck."},
            {"input": "nums = [0]", "output": "True", "explanation": "Already at last index."},
        ],
        "testCases": [
            {"function": "jumpGameReach", "input": "[2,3,1,1,4]", "expectedOutput": "True"},
            {"function": "jumpGameReach", "input": "[3,2,1,0,4]", "expectedOutput": "False"},
            {"function": "jumpGameReach", "input": "[0]", "expectedOutput": "True"},
            {"function": "jumpGameReach", "input": "[1,0]", "expectedOutput": "True"},
            {"function": "jumpGameReach", "input": "[0,1]", "expectedOutput": "False"},
            {"function": "jumpGameReach", "input": "[2,0,0]", "expectedOutput": "True"},
            {"function": "jumpGameReach", "input": "[1,1,1,1]", "expectedOutput": "True"},
            {"function": "jumpGameReach", "input": "[1,1,0,1]", "expectedOutput": "False"},
            {"function": "jumpGameReach", "input": "[5,0,0,0,0,0]", "expectedOutput": "True"},
            {"function": "jumpGameReach", "input": "[4,0,0,0,1]", "expectedOutput": "True"},
        ],
        "tags": ["array", "greedy", "dynamic-programming"],
    },
    # ─────────────────────────────────────────────
    # 23
    {
        "slug": "unique-paths-grid",
        "title": "Unique Paths in a Grid",
        "difficulty": "medium",
        "description": (
            "A delivery robot starts at the top-left corner of an m x n warehouse grid. "
            "It can only move right or down each step. "
            "How many distinct routes can the robot take to reach the bottom-right corner? "
            "Return the count of unique paths."
        ),
        "starterCode": "def uniquePathsGrid(m: int, n: int) -> int:\n    pass",
        "examples": [
            {"input": "m = 3, n = 7", "output": "28", "explanation": "28 distinct routes in a 3x7 grid."},
            {"input": "m = 3, n = 2", "output": "3", "explanation": "RD, DR, DR variants."},
            {"input": "m = 1, n = 1", "output": "1", "explanation": "Already at destination."},
        ],
        "testCases": [
            {"function": "uniquePathsGrid", "input": "3, 7", "expectedOutput": "28"},
            {"function": "uniquePathsGrid", "input": "3, 2", "expectedOutput": "3"},
            {"function": "uniquePathsGrid", "input": "1, 1", "expectedOutput": "1"},
            {"function": "uniquePathsGrid", "input": "2, 2", "expectedOutput": "2"},
            {"function": "uniquePathsGrid", "input": "1, 10", "expectedOutput": "1"},
            {"function": "uniquePathsGrid", "input": "10, 1", "expectedOutput": "1"},
            {"function": "uniquePathsGrid", "input": "3, 3", "expectedOutput": "6"},
            {"function": "uniquePathsGrid", "input": "4, 4", "expectedOutput": "20"},
            {"function": "uniquePathsGrid", "input": "5, 5", "expectedOutput": "70"},
            {"function": "uniquePathsGrid", "input": "7, 3", "expectedOutput": "28"},
        ],
        "tags": ["dynamic-programming", "math", "combinatorics"],
    },
    # ─────────────────────────────────────────────
    # 24
    {
        "slug": "word-ladder-transform",
        "title": "Word Ladder Transform",
        "difficulty": "hard",
        "description": (
            "A linguist transforms one word into another by changing exactly one letter at a time, "
            "where each intermediate word must exist in a given dictionary. "
            "Given beginWord, endWord, and a wordList, return the number of words in the shortest transformation sequence. "
            "Return 0 if no such sequence exists."
        ),
        "starterCode": "def wordLadder(beginWord: str, endWord: str, wordList: list) -> int:\n    pass",
        "examples": [
            {"input": "beginWord = \"hit\", endWord = \"cog\", wordList = [\"hot\",\"dot\",\"dog\",\"lot\",\"log\",\"cog\"]", "output": "5", "explanation": "hit->hot->dot->dog->cog"},
            {"input": "beginWord = \"hit\", endWord = \"cog\", wordList = [\"hot\",\"dot\",\"dog\",\"lot\",\"log\"]", "output": "0", "explanation": "cog not in wordList."},
            {"input": "beginWord = \"a\", endWord = \"c\", wordList = [\"a\",\"b\",\"c\"]", "output": "2", "explanation": "a->c directly."},
        ],
        "testCases": [
            {"function": "wordLadder", "input": "\"hit\", \"cog\", [\"hot\",\"dot\",\"dog\",\"lot\",\"log\",\"cog\"]", "expectedOutput": "5"},
            {"function": "wordLadder", "input": "\"hit\", \"cog\", [\"hot\",\"dot\",\"dog\",\"lot\",\"log\"]", "expectedOutput": "0"},
            {"function": "wordLadder", "input": "\"a\", \"c\", [\"a\",\"b\",\"c\"]", "expectedOutput": "2"},
            {"function": "wordLadder", "input": "\"hot\", \"dog\", [\"hot\",\"dog\"]", "expectedOutput": "0"},
            {"function": "wordLadder", "input": "\"hot\", \"dog\", [\"hot\",\"dot\",\"dog\"]", "expectedOutput": "3"},
            {"function": "wordLadder", "input": "\"cat\", \"dog\", [\"cat\",\"bat\",\"bad\",\"bag\",\"dag\",\"dog\"]", "expectedOutput": "5"},
            {"function": "wordLadder", "input": "\"red\", \"tax\", [\"ted\",\"tex\",\"red\",\"tax\",\"tad\",\"den\",\"rex\",\"pee\"]", "expectedOutput": "4"},
            {"function": "wordLadder", "input": "\"ab\", \"ba\", [\"aa\",\"ba\"]", "expectedOutput": "0"},
            {"function": "wordLadder", "input": "\"lost\", \"miss\", [\"most\",\"mist\",\"miss\",\"dost\",\"dist\",\"diss\"]", "expectedOutput": "6"},
            {"function": "wordLadder", "input": "\"ab\", \"ab\", [\"ab\"]", "expectedOutput": "1"},
        ],
        "tags": ["bfs", "graph", "hash-table", "string"],
    },
    # ─────────────────────────────────────────────
    # 25
    {
        "slug": "trapping-rainwater",
        "title": "Trapping Rainwater",
        "difficulty": "hard",
        "description": (
            "A landscape architect has an elevation map represented as an array of non-negative integers. "
            "After heavy rainfall, water collects between the peaks. "
            "Compute the total volume of water that can be trapped between the bars. "
            "Each bar has width 1."
        ),
        "starterCode": "def trappingRainwater(height: list) -> int:\n    pass",
        "examples": [
            {"input": "height = [0,1,0,2,1,0,1,3,2,1,2,1]", "output": "6", "explanation": "6 units of water trapped."},
            {"input": "height = [4,2,0,3,2,5]", "output": "9", "explanation": "9 units trapped."},
            {"input": "height = [1,0,1]", "output": "1", "explanation": "1 unit in the dip."},
        ],
        "testCases": [
            {"function": "trappingRainwater", "input": "[0,1,0,2,1,0,1,3,2,1,2,1]", "expectedOutput": "6"},
            {"function": "trappingRainwater", "input": "[4,2,0,3,2,5]", "expectedOutput": "9"},
            {"function": "trappingRainwater", "input": "[1,0,1]", "expectedOutput": "1"},
            {"function": "trappingRainwater", "input": "[3,0,2,0,4]", "expectedOutput": "7"},
            {"function": "trappingRainwater", "input": "[1,2,3,4,5]", "expectedOutput": "0"},
            {"function": "trappingRainwater", "input": "[5,4,3,2,1]", "expectedOutput": "0"},
            {"function": "trappingRainwater", "input": "[2,0,2]", "expectedOutput": "2"},
            {"function": "trappingRainwater", "input": "[0,0,0]", "expectedOutput": "0"},
            {"function": "trappingRainwater", "input": "[1,0,0,0,1]", "expectedOutput": "3"},
            {"function": "trappingRainwater", "input": "[2,1,3,1,2]", "expectedOutput": "3"},
        ],
        "tags": ["array", "two-pointers", "dynamic-programming", "stack", "monotonic-stack"],
    },
    # ─────────────────────────────────────────────
    # 26
    {
        "slug": "number-of-provinces",
        "title": "Number of Provinces",
        "difficulty": "medium",
        "description": (
            "Cities in a country are connected by roads. "
            "A province is a group of cities that are directly or indirectly connected. "
            "Given an n x n adjacency matrix isConnected where isConnected[i][j]=1 means city i and j are connected, "
            "return the number of provinces."
        ),
        "starterCode": "def numberOfProvinces(isConnected: list) -> int:\n    pass",
        "examples": [
            {"input": "isConnected = [[1,1,0],[1,1,0],[0,0,1]]", "output": "2", "explanation": "Cities 0 and 1 form one province; city 2 is another."},
            {"input": "isConnected = [[1,0,0],[0,1,0],[0,0,1]]", "output": "3", "explanation": "All cities isolated."},
            {"input": "isConnected = [[1,1,1],[1,1,1],[1,1,1]]", "output": "1", "explanation": "All connected."},
        ],
        "testCases": [
            {"function": "numberOfProvinces", "input": "[[1,1,0],[1,1,0],[0,0,1]]", "expectedOutput": "2"},
            {"function": "numberOfProvinces", "input": "[[1,0,0],[0,1,0],[0,0,1]]", "expectedOutput": "3"},
            {"function": "numberOfProvinces", "input": "[[1,1,1],[1,1,1],[1,1,1]]", "expectedOutput": "1"},
            {"function": "numberOfProvinces", "input": "[[1]]", "expectedOutput": "1"},
            {"function": "numberOfProvinces", "input": "[[1,0],[0,1]]", "expectedOutput": "2"},
            {"function": "numberOfProvinces", "input": "[[1,1],[1,1]]", "expectedOutput": "1"},
            {"function": "numberOfProvinces", "input": "[[1,0,0,1],[0,1,1,0],[0,1,1,0],[1,0,0,1]]", "expectedOutput": "2"},
            {"function": "numberOfProvinces", "input": "[[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]", "expectedOutput": "4"},
            {"function": "numberOfProvinces", "input": "[[1,1,0,0],[1,1,0,0],[0,0,1,1],[0,0,1,1]]", "expectedOutput": "2"},
            {"function": "numberOfProvinces", "input": "[[1,1,1,0],[1,1,0,0],[1,0,1,0],[0,0,0,1]]", "expectedOutput": "2"},
        ],
        "tags": ["graph", "dfs", "bfs", "union-find"],
    },
    # ─────────────────────────────────────────────
    # 27
    {
        "slug": "bst-validator",
        "title": "BST Validator",
        "difficulty": "medium",
        "description": (
            "A database index must obey the Binary Search Tree property: "
            "every left child is strictly smaller than its parent, "
            "and every right child is strictly larger. "
            "Given a binary tree root, return True if it is a valid BST, False otherwise."
        ),
        "starterCode": "class TreeNode:\n    def __init__(self, val=0, left=None, right=None):\n        self.val = val\n        self.left = left\n        self.right = right\n\ndef bstValidator(root) -> bool:\n    pass",
        "examples": [
            {"input": "root = [2,1,3]", "output": "True", "explanation": "1 < 2 < 3, valid BST."},
            {"input": "root = [5,1,4,null,null,3,6]", "output": "False", "explanation": "4 in right subtree but 3 < 5 violates BST."},
            {"input": "root = [1]", "output": "True", "explanation": "Single node is valid."},
        ],
        "testCases": [
            {"function": "bstValidator", "input": "[2,1,3]", "expectedOutput": "True"},
            {"function": "bstValidator", "input": "[5,1,4,null,null,3,6]", "expectedOutput": "False"},
            {"function": "bstValidator", "input": "[1]", "expectedOutput": "True"},
            {"function": "bstValidator", "input": "[2,2,2]", "expectedOutput": "False"},
            {"function": "bstValidator", "input": "[1,null,2]", "expectedOutput": "True"},
            {"function": "bstValidator", "input": "[3,1,5,null,2]", "expectedOutput": "True"},
            {"function": "bstValidator", "input": "[10,5,15,null,null,6,20]", "expectedOutput": "False"},
            {"function": "bstValidator", "input": "[5,4,6,null,null,3,7]", "expectedOutput": "False"},
            {"function": "bstValidator", "input": "[5,3,7,2,4,6,8]", "expectedOutput": "True"},
            {"function": "bstValidator", "input": "[2147483647]", "expectedOutput": "True"},
        ],
        "tags": ["tree", "dfs", "bfs", "binary-search-tree"],
    },
    # ─────────────────────────────────────────────
    # 28
    {
        "slug": "house-robbery-streak",
        "title": "House Robbery Streak",
        "difficulty": "medium",
        "description": (
            "A thief plans to rob houses on a street, but the security system alerts police if two adjacent houses are robbed. "
            "Each house holds a certain amount of cash. "
            "Given an array of non-negative integers representing cash per house, "
            "return the maximum total cash the thief can steal without triggering the alarm."
        ),
        "starterCode": "def houseRobbery(nums: list) -> int:\n    pass",
        "examples": [
            {"input": "nums = [1,2,3,1]", "output": "4", "explanation": "Rob house 0 and house 2: 1+3=4."},
            {"input": "nums = [2,7,9,3,1]", "output": "12", "explanation": "Rob houses 0,2,4: 2+9+1=12."},
            {"input": "nums = [0]", "output": "0", "explanation": "Nothing to steal."},
        ],
        "testCases": [
            {"function": "houseRobbery", "input": "[1,2,3,1]", "expectedOutput": "4"},
            {"function": "houseRobbery", "input": "[2,7,9,3,1]", "expectedOutput": "12"},
            {"function": "houseRobbery", "input": "[0]", "expectedOutput": "0"},
            {"function": "houseRobbery", "input": "[1]", "expectedOutput": "1"},
            {"function": "houseRobbery", "input": "[1,2]", "expectedOutput": "2"},
            {"function": "houseRobbery", "input": "[2,1,1,2]", "expectedOutput": "4"},
            {"function": "houseRobbery", "input": "[5,3,4,11,2]", "expectedOutput": "16"},
            {"function": "houseRobbery", "input": "[0,0,0,0]", "expectedOutput": "0"},
            {"function": "houseRobbery", "input": "[10,1,1,10]", "expectedOutput": "20"},
            {"function": "houseRobbery", "input": "[1,3,1,3,100]", "expectedOutput": "103"},
        ],
        "tags": ["dynamic-programming", "array"],
    },
    # ─────────────────────────────────────────────
    # 29
    {
        "slug": "lru-cache-design",
        "title": "LRU Cache Design",
        "difficulty": "medium",
        "description": (
            "Design a Least Recently Used (LRU) cache with a fixed capacity. "
            "Implement get(key) which returns the value if the key exists or -1 otherwise, "
            "and put(key, value) which inserts or updates a key-value pair, "
            "evicting the least recently used item when over capacity. "
            "Both operations must run in O(1) average time."
        ),
        "starterCode": "class LRUCache:\n    def __init__(self, capacity: int):\n        pass\n    def get(self, key: int) -> int:\n        pass\n    def put(self, key: int, value: int) -> None:\n        pass",
        "examples": [
            {"input": "capacity=2; put(1,1); put(2,2); get(1); put(3,3); get(2)", "output": "1, -1", "explanation": "Key 2 evicted when key 3 added."},
            {"input": "capacity=1; put(2,1); get(2); put(3,2); get(2); get(3)", "output": "1, -1, 2", "explanation": "Capacity 1 evicts on each put."},
            {"input": "capacity=2; put(1,1); get(1); put(2,2); get(2)", "output": "1, 2", "explanation": "Basic get after put."},
        ],
        "testCases": [
            {"function": "LRUCache", "input": "capacity=2; put(1,1); put(2,2); get(1)", "expectedOutput": "1"},
            {"function": "LRUCache", "input": "capacity=2; put(1,1); put(2,2); put(3,3); get(1)", "expectedOutput": "-1"},
            {"function": "LRUCache", "input": "capacity=2; put(1,1); put(2,2); get(2); put(3,3); get(2)", "expectedOutput": "2"},
            {"function": "LRUCache", "input": "capacity=1; put(1,1); get(1)", "expectedOutput": "1"},
            {"function": "LRUCache", "input": "capacity=1; put(1,1); put(2,2); get(1)", "expectedOutput": "-1"},
            {"function": "LRUCache", "input": "capacity=2; put(2,1); put(1,1); put(2,3); get(2)", "expectedOutput": "3"},
            {"function": "LRUCache", "input": "capacity=2; put(1,0); put(2,2); get(1); put(3,3); get(2)", "expectedOutput": "-1"},
            {"function": "LRUCache", "input": "capacity=3; put(1,1); put(2,2); put(3,3); get(1); put(4,4); get(2)", "expectedOutput": "-1"},
            {"function": "LRUCache", "input": "capacity=2; put(1,1); put(2,2); get(1); put(3,3); get(1)", "expectedOutput": "1"},
            {"function": "LRUCache", "input": "capacity=3; put(1,1); put(2,2); put(3,3); get(3)", "expectedOutput": "3"},
        ],
        "tags": ["design", "hash-table", "linked-list", "doubly-linked-list"],
    },
    # ─────────────────────────────────────────────
    # 30
    {
        "slug": "longest-increasing-trail",
        "title": "Longest Increasing Trail",
        "difficulty": "medium",
        "description": (
            "A hiker marks waypoints on a trail, each with an elevation number. "
            "Find the length of the longest subsequence of waypoints where elevations strictly increase — "
            "the waypoints don't need to be consecutive. "
            "Given an integer array nums, return the length of the longest strictly increasing subsequence."
        ),
        "starterCode": "def longestIncreasingTrail(nums: list) -> int:\n    pass",
        "examples": [
            {"input": "nums = [10,9,2,5,3,7,101,18]", "output": "4", "explanation": "[2,3,7,101] length 4."},
            {"input": "nums = [0,1,0,3,2,3]", "output": "4", "explanation": "[0,1,2,3] length 4."},
            {"input": "nums = [7,7,7,7,7]", "output": "1", "explanation": "No increase possible."},
        ],
        "testCases": [
            {"function": "longestIncreasingTrail", "input": "[10,9,2,5,3,7,101,18]", "expectedOutput": "4"},
            {"function": "longestIncreasingTrail", "input": "[0,1,0,3,2,3]", "expectedOutput": "4"},
            {"function": "longestIncreasingTrail", "input": "[7,7,7,7,7]", "expectedOutput": "1"},
            {"function": "longestIncreasingTrail", "input": "[1]", "expectedOutput": "1"},
            {"function": "longestIncreasingTrail", "input": "[1,2,3,4,5]", "expectedOutput": "5"},
            {"function": "longestIncreasingTrail", "input": "[5,4,3,2,1]", "expectedOutput": "1"},
            {"function": "longestIncreasingTrail", "input": "[1,3,2,4,3,5]", "expectedOutput": "4"},
            {"function": "longestIncreasingTrail", "input": "[2,2,2,2,3]", "expectedOutput": "2"},
            {"function": "longestIncreasingTrail", "input": "[1,5,2,4,3]", "expectedOutput": "3"},
            {"function": "longestIncreasingTrail", "input": "[3,1,4,1,5,9,2,6]", "expectedOutput": "4"},
        ],
        "tags": ["dynamic-programming", "binary-search", "array"],
    },
    # ─────────────────────────────────────────────
    # 31
    {
        "slug": "k-closest-stars",
        "title": "K Closest Stars",
        "difficulty": "medium",
        "description": (
            "An astronomer records star distances from Earth as an array of integers. "
            "Find the k stars closest to Earth (smallest values). "
            "Return the k values in any order. "
            "Aim for better than O(n log n) using a heap."
        ),
        "starterCode": "def kClosestStars(nums: list, k: int) -> list:\n    pass",
        "examples": [
            {"input": "nums = [3,2,1,5,6,4], k = 2", "output": "[1,2]", "explanation": "Closest two are 1 and 2."},
            {"input": "nums = [3,2,3,1,2,4,5,5,6], k = 4", "output": "[1,2,2,3]", "explanation": "Four smallest values."},
            {"input": "nums = [1], k = 1", "output": "[1]", "explanation": "Single element."},
        ],
        "testCases": [
            {"function": "kClosestStars", "input": "[3,2,1,5,6,4], 2", "expectedOutput": "[1,2]"},
            {"function": "kClosestStars", "input": "[3,2,3,1,2,4,5,5,6], 4", "expectedOutput": "[1,2,2,3]"},
            {"function": "kClosestStars", "input": "[1], 1", "expectedOutput": "[1]"},
            {"function": "kClosestStars", "input": "[5,4,3,2,1], 3", "expectedOutput": "[1,2,3]"},
            {"function": "kClosestStars", "input": "[1,2,3,4,5], 5", "expectedOutput": "[1,2,3,4,5]"},
            {"function": "kClosestStars", "input": "[7,10,4,3,20,15], 3", "expectedOutput": "[3,4,7]"},
            {"function": "kClosestStars", "input": "[1,1,1,1], 2", "expectedOutput": "[1,1]"},
            {"function": "kClosestStars", "input": "[-3,-1,0,2,5], 2", "expectedOutput": "[-3,-1]"},
            {"function": "kClosestStars", "input": "[100,50,25,10], 1", "expectedOutput": "[10]"},
            {"function": "kClosestStars", "input": "[9,8,7,6,5,4,3,2,1], 5", "expectedOutput": "[1,2,3,4,5]"},
        ],
        "tags": ["heap", "priority-queue", "sorting", "array"],
    },
    # ─────────────────────────────────────────────
    # 32
    {
        "slug": "serialize-tree",
        "title": "Serialize and Deserialize a Tree",
        "difficulty": "hard",
        "description": (
            "A distributed system needs to transmit binary trees over a network as text strings. "
            "Design two functions: serialize converts a binary tree to a string, "
            "and deserialize reconstructs the original tree from that string. "
            "Your format can be anything as long as it round-trips correctly."
        ),
        "starterCode": "class TreeNode:\n    def __init__(self, val=0, left=None, right=None):\n        self.val = val\n        self.left = left\n        self.right = right\n\ndef serialize(root) -> str:\n    pass\n\ndef deserialize(data: str):\n    pass",
        "examples": [
            {"input": "root = [1,2,3,null,null,4,5]", "output": "[1,2,3,null,null,4,5]", "explanation": "Round-trip preserves structure."},
            {"input": "root = []", "output": "[]", "explanation": "Empty tree."},
            {"input": "root = [1]", "output": "[1]", "explanation": "Single node."},
        ],
        "testCases": [
            {"function": "serialize+deserialize", "input": "[1,2,3,null,null,4,5]", "expectedOutput": "[1,2,3,null,null,4,5]"},
            {"function": "serialize+deserialize", "input": "[]", "expectedOutput": "[]"},
            {"function": "serialize+deserialize", "input": "[1]", "expectedOutput": "[1]"},
            {"function": "serialize+deserialize", "input": "[1,2]", "expectedOutput": "[1,2]"},
            {"function": "serialize+deserialize", "input": "[1,null,2]", "expectedOutput": "[1,null,2]"},
            {"function": "serialize+deserialize", "input": "[1,2,3]", "expectedOutput": "[1,2,3]"},
            {"function": "serialize+deserialize", "input": "[5,3,8,1,4,7,9]", "expectedOutput": "[5,3,8,1,4,7,9]"},
            {"function": "serialize+deserialize", "input": "[1,2,null,3,null,4]", "expectedOutput": "[1,2,null,3,null,4]"},
            {"function": "serialize+deserialize", "input": "[10,5,15,3,7,12,20]", "expectedOutput": "[10,5,15,3,7,12,20]"},
            {"function": "serialize+deserialize", "input": "[-1,-2,-3]", "expectedOutput": "[-1,-2,-3]"},
        ],
        "tags": ["tree", "dfs", "bfs", "design", "string"],
    },
    # ─────────────────────────────────────────────
    # 33
    {
        "slug": "skyline-contour",
        "title": "Skyline Contour",
        "difficulty": "hard",
        "description": (
            "An architect receives a list of buildings as [left, right, height] triplets. "
            "Compute the city skyline — the outline formed when all buildings are viewed from a distance. "
            "Return the key points where the silhouette height changes, as [x, height] pairs, "
            "ordered by x coordinate."
        ),
        "starterCode": "def skylineContour(buildings: list) -> list:\n    pass",
        "examples": [
            {"input": "buildings = [[2,9,10],[3,7,15],[5,12,12],[15,20,10],[19,24,8]]", "output": "[[2,10],[3,15],[7,12],[12,0],[15,10],[20,8],[24,0]]", "explanation": "Key silhouette change points."},
            {"input": "buildings = [[0,2,3],[2,5,3]]", "output": "[[0,3],[5,0]]", "explanation": "Same height, flat top."},
            {"input": "buildings = [[1,5,11],[2,7,6]]", "output": "[[1,11],[5,6],[7,0]]", "explanation": "Taller building dominates."},
        ],
        "testCases": [
            {"function": "skylineContour", "input": "[[2,9,10],[3,7,15],[5,12,12],[15,20,10],[19,24,8]]", "expectedOutput": "[[2,10],[3,15],[7,12],[12,0],[15,10],[20,8],[24,0]]"},
            {"function": "skylineContour", "input": "[[0,2,3],[2,5,3]]", "expectedOutput": "[[0,3],[5,0]]"},
            {"function": "skylineContour", "input": "[[1,5,11],[2,7,6]]", "expectedOutput": "[[1,11],[5,6],[7,0]]"},
            {"function": "skylineContour", "input": "[[1,2,1]]", "expectedOutput": "[[1,1],[2,0]]"},
            {"function": "skylineContour", "input": "[[1,2,1],[2,3,1]]", "expectedOutput": "[[1,1],[3,0]]"},
            {"function": "skylineContour", "input": "[[1,3,3],[2,4,4],[5,7,2]]", "expectedOutput": "[[1,3],[2,4],[4,0],[5,2],[7,0]]"},
            {"function": "skylineContour", "input": "[[0,5,5],[1,3,6]]", "expectedOutput": "[[0,5],[1,6],[3,5],[5,0]]"},
            {"function": "skylineContour", "input": "[[0,10,10]]", "expectedOutput": "[[0,10],[10,0]]"},
            {"function": "skylineContour", "input": "[[1,2,2],[2,3,2],[3,4,2]]", "expectedOutput": "[[1,2],[4,0]]"},
            {"function": "skylineContour", "input": "[[1,5,3],[2,3,7],[4,6,2]]", "expectedOutput": "[[1,3],[2,7],[3,3],[5,2],[6,0]]"},
        ],
        "tags": ["heap", "divide-and-conquer", "sorted-set", "sweep-line"],
    },
    # ─────────────────────────────────────────────
    # 34
    {
        "slug": "path-sum-tree",
        "title": "Path Sum in a Tree",
        "difficulty": "easy",
        "description": (
            "A treasure hunter follows a path from the root of a binary tree to any leaf node, "
            "collecting values along the way. "
            "Given a root and a targetSum, return True if any root-to-leaf path "
            "has values summing exactly to targetSum."
        ),
        "starterCode": "class TreeNode:\n    def __init__(self, val=0, left=None, right=None):\n        self.val = val\n        self.left = left\n        self.right = right\n\ndef pathSumTree(root, targetSum: int) -> bool:\n    pass",
        "examples": [
            {"input": "root = [5,4,8,11,null,13,4,7,2,null,null,null,1], targetSum = 22", "output": "True", "explanation": "5->4->11->2 sums to 22."},
            {"input": "root = [1,2,3], targetSum = 5", "output": "False", "explanation": "No path sums to 5."},
            {"input": "root = [], targetSum = 0", "output": "False", "explanation": "Empty tree."},
        ],
        "testCases": [
            {"function": "pathSumTree", "input": "[5,4,8,11,null,13,4,7,2,null,null,null,1], 22", "expectedOutput": "True"},
            {"function": "pathSumTree", "input": "[1,2,3], 5", "expectedOutput": "False"},
            {"function": "pathSumTree", "input": "[], 0", "expectedOutput": "False"},
            {"function": "pathSumTree", "input": "[1], 1", "expectedOutput": "True"},
            {"function": "pathSumTree", "input": "[1], 0", "expectedOutput": "False"},
            {"function": "pathSumTree", "input": "[1,2], 3", "expectedOutput": "True"},
            {"function": "pathSumTree", "input": "[1,2], 1", "expectedOutput": "False"},
            {"function": "pathSumTree", "input": "[-5,4,8,-3,null,13,4], -4", "expectedOutput": "True"},
            {"function": "pathSumTree", "input": "[1,2,3,4,5], 7", "expectedOutput": "True"},
            {"function": "pathSumTree", "input": "[1,2,3,4,5], 10", "expectedOutput": "False"},
        ],
        "tags": ["tree", "dfs", "binary-tree"],
    },
    # ─────────────────────────────────────────────
    # 35
    {
        "slug": "permutation-generator",
        "title": "Permutation Generator",
        "difficulty": "medium",
        "description": (
            "A password generator creates all possible arrangements of a set of distinct digits. "
            "Given an array of distinct integers, return all possible permutations in any order. "
            "For n elements, there are n! permutations. Use backtracking to generate them."
        ),
        "starterCode": "def permutationGenerator(nums: list) -> list:\n    pass",
        "examples": [
            {"input": "nums = [1,2,3]", "output": "[[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]", "explanation": "All 6 permutations."},
            {"input": "nums = [0,1]", "output": "[[0,1],[1,0]]", "explanation": "2 permutations."},
            {"input": "nums = [1]", "output": "[[1]]", "explanation": "Only one arrangement."},
        ],
        "testCases": [
            {"function": "permutationGenerator", "input": "[1,2,3]", "expectedOutput": "6 permutations"},
            {"function": "permutationGenerator", "input": "[0,1]", "expectedOutput": "[[0,1],[1,0]]"},
            {"function": "permutationGenerator", "input": "[1]", "expectedOutput": "[[1]]"},
            {"function": "permutationGenerator", "input": "[1,2]", "expectedOutput": "[[1,2],[2,1]]"},
            {"function": "permutationGenerator", "input": "[-1,1]", "expectedOutput": "[[-1,1],[1,-1]]"},
            {"function": "permutationGenerator", "input": "[1,2,3,4]", "expectedOutput": "24 permutations"},
            {"function": "permutationGenerator", "input": "[0,1,2]", "expectedOutput": "6 permutations"},
            {"function": "permutationGenerator", "input": "[3,2,1]", "expectedOutput": "6 permutations"},
            {"function": "permutationGenerator", "input": "[-2,0,2]", "expectedOutput": "6 permutations"},
            {"function": "permutationGenerator", "input": "[5]", "expectedOutput": "[[5]]"},
        ],
        "tags": ["backtracking", "recursion", "array"],
    },
    # ─────────────────────────────────────────────
    # 36
    {
        "slug": "power-function",
        "title": "Fast Power Function",
        "difficulty": "medium",
        "description": (
            "A scientific calculator needs to compute x raised to the power n efficiently. "
            "Implement pow(x, n) where n can be negative or zero. "
            "Use the fast exponentiation approach (repeated squaring) to achieve O(log n) time. "
            "Do not use the built-in ** or pow() functions."
        ),
        "starterCode": "def fastPow(x: float, n: int) -> float:\n    pass",
        "examples": [
            {"input": "x = 2.0, n = 10", "output": "1024.0", "explanation": "2^10 = 1024."},
            {"input": "x = 2.1, n = 3", "output": "9.261", "explanation": "2.1^3 ≈ 9.261."},
            {"input": "x = 2.0, n = -2", "output": "0.25", "explanation": "2^-2 = 1/4."},
        ],
        "testCases": [
            {"function": "fastPow", "input": "2.0, 10", "expectedOutput": "1024.0"},
            {"function": "fastPow", "input": "2.0, -2", "expectedOutput": "0.25"},
            {"function": "fastPow", "input": "2.0, 0", "expectedOutput": "1.0"},
            {"function": "fastPow", "input": "1.0, 100", "expectedOutput": "1.0"},
            {"function": "fastPow", "input": "0.0, 5", "expectedOutput": "0.0"},
            {"function": "fastPow", "input": "-2.0, 3", "expectedOutput": "-8.0"},
            {"function": "fastPow", "input": "-2.0, 2", "expectedOutput": "4.0"},
            {"function": "fastPow", "input": "3.0, 4", "expectedOutput": "81.0"},
            {"function": "fastPow", "input": "5.0, -1", "expectedOutput": "0.2"},
            {"function": "fastPow", "input": "2.0, 1", "expectedOutput": "2.0"},
        ],
        "tags": ["math", "recursion", "binary-search", "divide-and-conquer"],
    },
    # ─────────────────────────────────────────────
    # 37
    {
        "slug": "subsets-enumerator",
        "title": "Subsets Enumerator",
        "difficulty": "medium",
        "description": (
            "A botanist wants to examine every possible combination of plant specimens from a set. "
            "Given an array of unique integers, return all possible subsets (the power set), "
            "including the empty set. "
            "The output should not contain duplicate subsets."
        ),
        "starterCode": "def subsetsEnumerator(nums: list) -> list:\n    pass",
        "examples": [
            {"input": "nums = [1,2,3]", "output": "[[],[1],[2],[3],[1,2],[1,3],[2,3],[1,2,3]]", "explanation": "All 8 subsets of 3 elements."},
            {"input": "nums = [0]", "output": "[[],[0]]", "explanation": "Empty set and {0}."},
            {"input": "nums = [1,2]", "output": "[[],[1],[2],[1,2]]", "explanation": "4 subsets."},
        ],
        "testCases": [
            {"function": "subsetsEnumerator", "input": "[1,2,3]", "expectedOutput": "8 subsets"},
            {"function": "subsetsEnumerator", "input": "[0]", "expectedOutput": "[[],[0]]"},
            {"function": "subsetsEnumerator", "input": "[1,2]", "expectedOutput": "4 subsets"},
            {"function": "subsetsEnumerator", "input": "[]", "expectedOutput": "[[]]"},
            {"function": "subsetsEnumerator", "input": "[4]", "expectedOutput": "[[],[4]]"},
            {"function": "subsetsEnumerator", "input": "[1,2,3,4]", "expectedOutput": "16 subsets"},
            {"function": "subsetsEnumerator", "input": "[-1,0,1]", "expectedOutput": "8 subsets"},
            {"function": "subsetsEnumerator", "input": "[5,6]", "expectedOutput": "[[],[5],[6],[5,6]]"},
            {"function": "subsetsEnumerator", "input": "[1,2,3,4,5]", "expectedOutput": "32 subsets"},
            {"function": "subsetsEnumerator", "input": "[10,20]", "expectedOutput": "[[],[10],[20],[10,20]]"},
        ],
        "tags": ["backtracking", "bit-manipulation", "array"],
    },
    # ─────────────────────────────────────────────
    # 38
    {
        "slug": "flatten-nested-list",
        "title": "Flatten Nested List",
        "difficulty": "medium",
        "description": (
            "A document parser receives deeply nested lists of integers. "
            "Flatten all levels into a single list of integers. "
            "Given a list that may contain integers or other lists (to any depth), "
            "return all integers in their original left-to-right order in a flat list."
        ),
        "starterCode": "def flattenNestedList(nested) -> list:\n    pass",
        "examples": [
            {"input": "nested = [[1,[4,[6]]],2,[[3],5]]", "output": "[1,4,6,2,3,5]", "explanation": "All levels flattened in order."},
            {"input": "nested = [1,2,3]", "output": "[1,2,3]", "explanation": "Already flat."},
            {"input": "nested = [[[]]]", "output": "[]", "explanation": "Empty nested list."},
        ],
        "testCases": [
            {"function": "flattenNestedList", "input": "[[1,[4,[6]]],2,[[3],5]]", "expectedOutput": "[1,4,6,2,3,5]"},
            {"function": "flattenNestedList", "input": "[1,2,3]", "expectedOutput": "[1,2,3]"},
            {"function": "flattenNestedList", "input": "[[[]]]", "expectedOutput": "[]"},
            {"function": "flattenNestedList", "input": "[]", "expectedOutput": "[]"},
            {"function": "flattenNestedList", "input": "[[1,2],[3,[4,5]]]", "expectedOutput": "[1,2,3,4,5]"},
            {"function": "flattenNestedList", "input": "[[[1]]]", "expectedOutput": "[1]"},
            {"function": "flattenNestedList", "input": "[1,[2,[3,[4]]]]", "expectedOutput": "[1,2,3,4]"},
            {"function": "flattenNestedList", "input": "[[1],[2],[3]]", "expectedOutput": "[1,2,3]"},
            {"function": "flattenNestedList", "input": "[-1,[-2,[-3]]]", "expectedOutput": "[-1,-2,-3]"},
            {"function": "flattenNestedList", "input": "[[[2,3]],1]", "expectedOutput": "[2,3,1]"},
        ],
        "tags": ["recursion", "dfs", "stack", "array"],
    },
    # ─────────────────────────────────────────────
    # 39
    {
        "slug": "min-bracket-additions",
        "title": "Min Bracket Additions",
        "difficulty": "medium",
        "description": (
            "A code formatter needs to make a string of parentheses valid by adding the minimum number of characters. "
            "Given a string of '(' and ')', return the minimum number of insertions "
            "needed so that the string becomes a valid parentheses sequence."
        ),
        "starterCode": "def minBracketAdditions(s: str) -> int:\n    pass",
        "examples": [
            {"input": "s = \"())\"", "output": "1", "explanation": "Add one '(' at the start."},
            {"input": "s = \"((\"", "output": "2", "explanation": "Add two ')' at the end."},
            {"input": "s = \"(())\"", "output": "0", "explanation": "Already valid."},
        ],
        "testCases": [
            {"function": "minBracketAdditions", "input": "\"())\"", "expectedOutput": "1"},
            {"function": "minBracketAdditions", "input": "\"((\"", "expectedOutput": "2"},
            {"function": "minBracketAdditions", "input": "\"(())\"", "expectedOutput": "0"},
            {"function": "minBracketAdditions", "input": "\"\"", "expectedOutput": "0"},
            {"function": "minBracketAdditions", "input": "\")\"", "expectedOutput": "1"},
            {"function": "minBracketAdditions", "input": "\"(\"", "expectedOutput": "1"},
            {"function": "minBracketAdditions", "input": "\"))(\"", "expectedOutput": "3"},
            {"function": "minBracketAdditions", "input": "\"()))((\"", "expectedOutput": "4"},
            {"function": "minBracketAdditions", "input": "\"(())(\"", "expectedOutput": "1"},
            {"function": "minBracketAdditions", "input": "\")))\"", "expectedOutput": "3"},
        ],
        "tags": ["stack", "greedy", "string"],
    },
    # ─────────────────────────────────────────────
    # 40
    {
        "slug": "count-good-nodes",
        "title": "Count Good Nodes in Tree",
        "difficulty": "medium",
        "description": (
            "A node in a binary tree is called 'good' if no value along the path from the root to that node "
            "is greater than the node's own value. "
            "Given the root of a binary tree, count and return the total number of good nodes."
        ),
        "starterCode": "class TreeNode:\n    def __init__(self, val=0, left=None, right=None):\n        self.val = val\n        self.left = left\n        self.right = right\n\ndef countGoodNodes(root) -> int:\n    pass",
        "examples": [
            {"input": "root = [3,1,4,3,null,1,5]", "output": "4", "explanation": "Nodes 3,4,3,5 are good."},
            {"input": "root = [3,3,null,4,2]", "output": "3", "explanation": "Root, left child, and 4 are good."},
            {"input": "root = [1]", "output": "1", "explanation": "Single root is always good."},
        ],
        "testCases": [
            {"function": "countGoodNodes", "input": "[3,1,4,3,null,1,5]", "expectedOutput": "4"},
            {"function": "countGoodNodes", "input": "[3,3,null,4,2]", "expectedOutput": "3"},
            {"function": "countGoodNodes", "input": "[1]", "expectedOutput": "1"},
            {"function": "countGoodNodes", "input": "[2,null,4,10,8,null,null,4]", "expectedOutput": "4"},
            {"function": "countGoodNodes", "input": "[1,2,3]", "expectedOutput": "3"},
            {"function": "countGoodNodes", "input": "[5,3,7,2,4,6,8]", "expectedOutput": "4"},
            {"function": "countGoodNodes", "input": "[1,1,1,1,1]", "expectedOutput": "5"},
            {"function": "countGoodNodes", "input": "[3,1,4]", "expectedOutput": "2"},
            {"function": "countGoodNodes", "input": "[10,5,15,3,7]", "expectedOutput": "3"},
            {"function": "countGoodNodes", "input": "[-1,-2,-3]", "expectedOutput": "1"},
        ],
        "tags": ["tree", "dfs", "binary-tree"],
    },
    # ─────────────────────────────────────────────
    # 41
    {
        "slug": "min-cost-path",
        "title": "Minimum Cost Path",
        "difficulty": "medium",
        "description": (
            "A robot navigates an m x n grid. Each cell has a cost to enter. "
            "The robot starts at the top-left and must reach the bottom-right, "
            "moving only right or down. "
            "Return the path with the minimum total cost."
        ),
        "starterCode": "def minCostPath(grid: list) -> int:\n    pass",
        "examples": [
            {"input": "grid = [[1,3,1],[1,5,1],[4,2,1]]", "output": "7", "explanation": "1+3+1+1+1=7."},
            {"input": "grid = [[1,2],[3,4]]", "output": "7", "explanation": "1+2+4=7 or 1+3+4=8."},
            {"input": "grid = [[1]]", "output": "1", "explanation": "Single cell."},
        ],
        "testCases": [
            {"function": "minCostPath", "input": "[[1,3,1],[1,5,1],[4,2,1]]", "expectedOutput": "7"},
            {"function": "minCostPath", "input": "[[1,2],[3,4]]", "expectedOutput": "7"},
            {"function": "minCostPath", "input": "[[1]]", "expectedOutput": "1"},
            {"function": "minCostPath", "input": "[[1,2,3],[4,5,6]]", "expectedOutput": "12"},
            {"function": "minCostPath", "input": "[[1,1,1],[1,1,1],[1,1,1]]", "expectedOutput": "5"},
            {"function": "minCostPath", "input": "[[0,0,0],[0,0,0]]", "expectedOutput": "0"},
            {"function": "minCostPath", "input": "[[9,1],[1,9]]", "expectedOutput": "11"},
            {"function": "minCostPath", "input": "[[1,2,5],[3,2,1]]", "expectedOutput": "6"},
            {"function": "minCostPath", "input": "[[5,1],[2,1]]", "expectedOutput": "7"},
            {"function": "minCostPath", "input": "[[1,3],[2,4],[1,2]]", "expectedOutput": "8"},
        ],
        "tags": ["dynamic-programming", "matrix", "array"],
    },
    # ─────────────────────────────────────────────
    # 42
    {
        "slug": "top-k-frequent",
        "title": "Top K Frequent Elements",
        "difficulty": "medium",
        "description": (
            "A word-frequency tool must identify the most commonly occurring numbers in a dataset. "
            "Given an integer array and an integer k, return the k elements that appear most frequently. "
            "The answer can be in any order. "
            "Your solution should be better than O(n log n)."
        ),
        "starterCode": "def topKFrequent(nums: list, k: int) -> list:\n    pass",
        "examples": [
            {"input": "nums = [1,1,1,2,2,3], k = 2", "output": "[1,2]", "explanation": "1 appears 3x, 2 appears 2x."},
            {"input": "nums = [1], k = 1", "output": "[1]", "explanation": "Only one element."},
            {"input": "nums = [3,0,1,0,3,3], k = 2", "output": "[3,0]", "explanation": "3 appears 3x, 0 appears 2x."},
        ],
        "testCases": [
            {"function": "topKFrequent", "input": "[1,1,1,2,2,3], 2", "expectedOutput": "[1,2]"},
            {"function": "topKFrequent", "input": "[1], 1", "expectedOutput": "[1]"},
            {"function": "topKFrequent", "input": "[3,0,1,0,3,3], 2", "expectedOutput": "[3,0]"},
            {"function": "topKFrequent", "input": "[4,4,4,5,5,6], 1", "expectedOutput": "[4]"},
            {"function": "topKFrequent", "input": "[1,2,3,4,5], 5", "expectedOutput": "[1,2,3,4,5]"},
            {"function": "topKFrequent", "input": "[1,1,2,2,3,3], 3", "expectedOutput": "[1,2,3]"},
            {"function": "topKFrequent", "input": "[-1,-1,0,1,1], 2", "expectedOutput": "[-1,1]"},
            {"function": "topKFrequent", "input": "[7,7,7,8,8,9], 2", "expectedOutput": "[7,8]"},
            {"function": "topKFrequent", "input": "[10,10,10], 1", "expectedOutput": "[10]"},
            {"function": "topKFrequent", "input": "[1,2,2,3,3,3,4,4,4,4], 2", "expectedOutput": "[4,3]"},
        ],
        "tags": ["heap", "priority-queue", "hash-table", "bucket-sort"],
    },
    # ─────────────────────────────────────────────
    # 43
    {
        "slug": "rotate-matrix-clockwise",
        "title": "Rotate Matrix Clockwise",
        "difficulty": "medium",
        "description": (
            "An image-processing tool rotates a square pixel grid 90 degrees clockwise. "
            "Given an n x n integer matrix, rotate it in-place — no new matrix may be created. "
            "A 90-degree clockwise rotation means the first row becomes the last column."
        ),
        "starterCode": "def rotateMatrix(matrix: list) -> None:\n    pass",
        "examples": [
            {"input": "matrix = [[1,2,3],[4,5,6],[7,8,9]]", "output": "[[7,4,1],[8,5,2],[9,6,3]]", "explanation": "90° clockwise."},
            {"input": "matrix = [[5,1,9,11],[2,4,8,10],[13,3,6,7],[15,14,12,16]]", "output": "[[15,13,2,5],[14,3,4,1],[12,6,8,9],[16,7,10,11]]", "explanation": "4x4 rotation."},
            {"input": "matrix = [[1]]", "output": "[[1]]", "explanation": "Single element unchanged."},
        ],
        "testCases": [
            {"function": "rotateMatrix", "input": "[[1,2,3],[4,5,6],[7,8,9]]", "expectedOutput": "[[7,4,1],[8,5,2],[9,6,3]]"},
            {"function": "rotateMatrix", "input": "[[5,1,9,11],[2,4,8,10],[13,3,6,7],[15,14,12,16]]", "expectedOutput": "[[15,13,2,5],[14,3,4,1],[12,6,8,9],[16,7,10,11]]"},
            {"function": "rotateMatrix", "input": "[[1]]", "expectedOutput": "[[1]]"},
            {"function": "rotateMatrix", "input": "[[1,2],[3,4]]", "expectedOutput": "[[3,1],[4,2]]"},
            {"function": "rotateMatrix", "input": "[[1,2,3],[4,5,6],[7,8,9]]", "expectedOutput": "[[7,4,1],[8,5,2],[9,6,3]]"},
            {"function": "rotateMatrix", "input": "[[0,0],[0,0]]", "expectedOutput": "[[0,0],[0,0]]"},
            {"function": "rotateMatrix", "input": "[[1,3],[2,4]]", "expectedOutput": "[[2,1],[4,3]]"},
            {"function": "rotateMatrix", "input": "[[1,2,3],[0,0,0],[3,2,1]]", "expectedOutput": "[[3,0,1],[2,0,2],[1,0,3]]"},
            {"function": "rotateMatrix", "input": "[[5,6],[7,8]]", "expectedOutput": "[[7,5],[8,6]]"},
            {"function": "rotateMatrix", "input": "[[1,0,0],[0,1,0],[0,0,1]]", "expectedOutput": "[[0,0,1],[0,1,0],[1,0,0]]"},
        ],
        "tags": ["matrix", "array", "math"],
    },
    # ─────────────────────────────────────────────
    # 44
    {
        "slug": "three-sum-triplets",
        "title": "Three Sum Triplets",
        "difficulty": "medium",
        "description": (
            "A chemistry tool looks for combinations of three reagent quantities that balance to zero. "
            "Given an integer array, find all unique triplets [a, b, c] such that a + b + c = 0. "
            "No duplicate triplets in the output. "
            "Use the two-pointer technique after sorting for an O(n²) solution."
        ),
        "starterCode": "def threeSumTriplets(nums: list) -> list:\n    pass",
        "examples": [
            {"input": "nums = [-1,0,1,2,-1,-4]", "output": "[[-1,-1,2],[-1,0,1]]", "explanation": "Two unique triplets."},
            {"input": "nums = [0,1,1]", "output": "[]", "explanation": "No triplet sums to zero."},
            {"input": "nums = [0,0,0]", "output": "[[0,0,0]]", "explanation": "All zeros."},
        ],
        "testCases": [
            {"function": "threeSumTriplets", "input": "[-1,0,1,2,-1,-4]", "expectedOutput": "[[-1,-1,2],[-1,0,1]]"},
            {"function": "threeSumTriplets", "input": "[0,1,1]", "expectedOutput": "[]"},
            {"function": "threeSumTriplets", "input": "[0,0,0]", "expectedOutput": "[[0,0,0]]"},
            {"function": "threeSumTriplets", "input": "[-2,0,1,1,2]", "expectedOutput": "[[-2,0,2],[-2,1,1]]"},
            {"function": "threeSumTriplets", "input": "[-4,-2,-2,-2,0,1,2,2,2,3,3,4,4,6,6]", "expectedOutput": "multiple triplets"},
            {"function": "threeSumTriplets", "input": "[1,2,3]", "expectedOutput": "[]"},
            {"function": "threeSumTriplets", "input": "[-1,-1,0,1,1]", "expectedOutput": "[[-1,0,1]]"},
            {"function": "threeSumTriplets", "input": "[1,-1,0]", "expectedOutput": "[[-1,0,1]]"},
            {"function": "threeSumTriplets", "input": "[-2,0,0,2,2]", "expectedOutput": "[[-2,0,2]]"},
            {"function": "threeSumTriplets", "input": "[]", "expectedOutput": "[]"},
        ],
        "tags": ["array", "two-pointers", "sorting"],
    },
    # ─────────────────────────────────────────────
    # 45
    {
        "slug": "graph-clone",
        "title": "Graph Clone",
        "difficulty": "medium",
        "description": (
            "A backup system needs to create a deep copy of a social network graph. "
            "Each node has a value and a list of neighbours. "
            "Given a reference to a node, return a deep clone of the entire graph. "
            "The cloned graph must be a separate structure with no shared references."
        ),
        "starterCode": "class Node:\n    def __init__(self, val=0, neighbors=None):\n        self.val = val\n        self.neighbors = neighbors if neighbors is not None else []\n\ndef graphClone(node):\n    pass",
        "examples": [
            {"input": "adjList = [[2,4],[1,3],[2,4],[1,3]]", "output": "[[2,4],[1,3],[2,4],[1,3]]", "explanation": "Deep clone of a 4-node cycle graph."},
            {"input": "adjList = [[]]", "output": "[[]]", "explanation": "Single node, no neighbours."},
            {"input": "adjList = []", "output": "[]", "explanation": "Empty graph."},
        ],
        "testCases": [
            {"function": "graphClone", "input": "[[2,4],[1,3],[2,4],[1,3]]", "expectedOutput": "[[2,4],[1,3],[2,4],[1,3]]"},
            {"function": "graphClone", "input": "[[]]", "expectedOutput": "[[]]"},
            {"function": "graphClone", "input": "[]", "expectedOutput": "[]"},
            {"function": "graphClone", "input": "[[2],[1]]", "expectedOutput": "[[2],[1]]"},
            {"function": "graphClone", "input": "[[2,3],[1,3],[1,2]]", "expectedOutput": "[[2,3],[1,3],[1,2]]"},
            {"function": "graphClone", "input": "[[2],[1,3],[2]]", "expectedOutput": "[[2],[1,3],[2]]"},
            {"function": "graphClone", "input": "[[2,3,4],[1,3],[1,2,4],[1,3]]", "expectedOutput": "[[2,3,4],[1,3],[1,2,4],[1,3]]"},
            {"function": "graphClone", "input": "[[2],[3],[4],[1]]", "expectedOutput": "[[2],[3],[4],[1]]"},
            {"function": "graphClone", "input": "[[3],[3],[1,2]]", "expectedOutput": "[[3],[3],[1,2]]"},
            {"function": "graphClone", "input": "[[2,5],[1,3],[2,4],[3,5],[4,1]]", "expectedOutput": "[[2,5],[1,3],[2,4],[3,5],[4,1]]"},
        ],
        "tags": ["graph", "dfs", "bfs", "hash-table"],
    },
    # ─────────────────────────────────────────────
    # 46–100 follow same structure
    {
        "slug": "diameter-of-tree",
        "title": "Diameter of a Binary Tree",
        "difficulty": "easy",
        "description": (
            "The diameter of a binary tree is the length of the longest path between any two nodes. "
            "The path may or may not pass through the root. "
            "Length is measured in number of edges. "
            "Given a binary tree root, return its diameter."
        ),
        "starterCode": "class TreeNode:\n    def __init__(self, val=0, left=None, right=None):\n        self.val = val\n        self.left = left\n        self.right = right\n\ndef diameterOfTree(root) -> int:\n    pass",
        "examples": [
            {"input": "root = [1,2,3,4,5]", "output": "3", "explanation": "Path [4,2,1,3] or [5,2,1,3]."},
            {"input": "root = [1,2]", "output": "1", "explanation": "One edge."},
            {"input": "root = [1]", "output": "0", "explanation": "Single node, no edges."},
        ],
        "testCases": [
            {"function": "diameterOfTree", "input": "[1,2,3,4,5]", "expectedOutput": "3"},
            {"function": "diameterOfTree", "input": "[1,2]", "expectedOutput": "1"},
            {"function": "diameterOfTree", "input": "[1]", "expectedOutput": "0"},
            {"function": "diameterOfTree", "input": "[1,2,3]", "expectedOutput": "2"},
            {"function": "diameterOfTree", "input": "[4,2,null,1,3]", "expectedOutput": "3"},
            {"function": "diameterOfTree", "input": "[1,2,null,3,null,4]", "expectedOutput": "3"},
            {"function": "diameterOfTree", "input": "[1,2,3,4,null,null,5]", "expectedOutput": "4"},
            {"function": "diameterOfTree", "input": "[1,2,3,4,5,6,7]", "expectedOutput": "4"},
            {"function": "diameterOfTree", "input": "[]", "expectedOutput": "0"},
            {"function": "diameterOfTree", "input": "[1,null,2,null,3,null,4]", "expectedOutput": "3"},
        ],
        "tags": ["tree", "dfs", "binary-tree"],
    },
    {
        "slug": "balanced-tree-check",
        "title": "Balanced Tree Check",
        "difficulty": "easy",
        "description": (
            "A balanced binary tree is one where the left and right subtrees of every node "
            "differ in height by no more than one. "
            "Given a binary tree root, return True if it is height-balanced, False otherwise."
        ),
        "starterCode": "class TreeNode:\n    def __init__(self, val=0, left=None, right=None):\n        self.val = val\n        self.left = left\n        self.right = right\n\ndef balancedTreeCheck(root) -> bool:\n    pass",
        "examples": [
            {"input": "root = [3,9,20,null,null,15,7]", "output": "True", "explanation": "All subtrees balanced."},
            {"input": "root = [1,2,2,3,3,null,null,4,4]", "output": "False", "explanation": "Left subtree too deep."},
            {"input": "root = []", "output": "True", "explanation": "Empty tree is balanced."},
        ],
        "testCases": [
            {"function": "balancedTreeCheck", "input": "[3,9,20,null,null,15,7]", "expectedOutput": "True"},
            {"function": "balancedTreeCheck", "input": "[1,2,2,3,3,null,null,4,4]", "expectedOutput": "False"},
            {"function": "balancedTreeCheck", "input": "[]", "expectedOutput": "True"},
            {"function": "balancedTreeCheck", "input": "[1]", "expectedOutput": "True"},
            {"function": "balancedTreeCheck", "input": "[1,2,3]", "expectedOutput": "True"},
            {"function": "balancedTreeCheck", "input": "[1,2,null,3]", "expectedOutput": "False"},
            {"function": "balancedTreeCheck", "input": "[1,2,3,4,null,null,5]", "expectedOutput": "True"},
            {"function": "balancedTreeCheck", "input": "[1,2,null,3,null,4]", "expectedOutput": "False"},
            {"function": "balancedTreeCheck", "input": "[5,3,8,1,4,7,9]", "expectedOutput": "True"},
            {"function": "balancedTreeCheck", "input": "[1,2,null,3,null,null,null,4]", "expectedOutput": "False"},
        ],
        "tags": ["tree", "dfs", "binary-tree"],
    },
    {
        "slug": "sliding-window-max",
        "title": "Sliding Window Maximum",
        "difficulty": "hard",
        "description": (
            "A sensor array reports values every second. A control system monitors the maximum "
            "reading within a sliding window of width k. "
            "Given an array and window size k, return the list of maximums for each window position. "
            "Aim for O(n) using a deque."
        ),
        "starterCode": "def slidingWindowMax(nums: list, k: int) -> list:\n    pass",
        "examples": [
            {"input": "nums = [1,3,-1,-3,5,3,6,7], k = 3", "output": "[3,3,5,5,6,7]", "explanation": "Max of each 3-window."},
            {"input": "nums = [1], k = 1", "output": "[1]", "explanation": "Single window."},
            {"input": "nums = [9,11], k = 2", "output": "[11]", "explanation": "One window."},
        ],
        "testCases": [
            {"function": "slidingWindowMax", "input": "[1,3,-1,-3,5,3,6,7], 3", "expectedOutput": "[3,3,5,5,6,7]"},
            {"function": "slidingWindowMax", "input": "[1], 1", "expectedOutput": "[1]"},
            {"function": "slidingWindowMax", "input": "[9,11], 2", "expectedOutput": "[11]"},
            {"function": "slidingWindowMax", "input": "[4,-2], 2", "expectedOutput": "[4]"},
            {"function": "slidingWindowMax", "input": "[1,2,3,4,5], 2", "expectedOutput": "[2,3,4,5]"},
            {"function": "slidingWindowMax", "input": "[5,4,3,2,1], 3", "expectedOutput": "[5,4,3]"},
            {"function": "slidingWindowMax", "input": "[2,1,5,3,6,4,8,7], 3", "expectedOutput": "[5,5,6,6,8,8]"},
            {"function": "slidingWindowMax", "input": "[1,3,1,2,0,5], 3", "expectedOutput": "[3,3,2,5]"},
            {"function": "slidingWindowMax", "input": "[7,2,4], 2", "expectedOutput": "[7,4]"},
            {"function": "slidingWindowMax", "input": "[1,1,1,1], 2", "expectedOutput": "[1,1,1]"},
        ],
        "tags": ["array", "sliding-window", "deque", "monotonic-queue"],
    },
    {
        "slug": "trie-builder",
        "title": "Trie Builder",
        "difficulty": "medium",
        "description": (
            "An autocomplete engine uses a trie (prefix tree) to quickly look up words. "
            "Implement a Trie class with insert(word), search(word) that returns True if the word exists, "
            "and startsWith(prefix) that returns True if any word has that prefix."
        ),
        "starterCode": "class Trie:\n    def __init__(self):\n        pass\n    def insert(self, word: str) -> None:\n        pass\n    def search(self, word: str) -> bool:\n        pass\n    def startsWith(self, prefix: str) -> bool:\n        pass",
        "examples": [
            {"input": "insert('apple'); search('apple'); search('app'); startsWith('app')", "output": "True, False, True", "explanation": "Full word vs prefix."},
            {"input": "insert('apple'); insert('app'); search('app')", "output": "True", "explanation": "Shorter word inserted."},
            {"input": "insert('ab'); startsWith('abc')", "output": "False", "explanation": "Prefix longer than word."},
        ],
        "testCases": [
            {"function": "Trie", "input": "insert('apple'); search('apple')", "expectedOutput": "True"},
            {"function": "Trie", "input": "insert('apple'); search('app')", "expectedOutput": "False"},
            {"function": "Trie", "input": "insert('apple'); startsWith('app')", "expectedOutput": "True"},
            {"function": "Trie", "input": "insert('apple'); insert('app'); search('app')", "expectedOutput": "True"},
            {"function": "Trie", "input": "search('anything')", "expectedOutput": "False"},
            {"function": "Trie", "input": "startsWith('')", "expectedOutput": "True"},
            {"function": "Trie", "input": "insert('hello'); insert('world'); search('world')", "expectedOutput": "True"},
            {"function": "Trie", "input": "insert('abc'); startsWith('abcd')", "expectedOutput": "False"},
            {"function": "Trie", "input": "insert('a'); search('a'); search('ab')", "expectedOutput": "True, False"},
            {"function": "Trie", "input": "insert('cat'); insert('car'); startsWith('ca')", "expectedOutput": "True"},
        ],
        "tags": ["trie", "design", "string", "hash-table"],
    },
    {
        "slug": "stock-span-calculator",
        "title": "Stock Span Calculator",
        "difficulty": "medium",
        "description": (
            "A financial analyst calculates the 'span' of a stock's price — "
            "the number of consecutive days (including today) where the price was less than or equal to today's price. "
            "Given a list of daily prices, return the span for each day. "
            "Use a monotonic stack for O(n) efficiency."
        ),
        "starterCode": "def stockSpan(prices: list) -> list:\n    pass",
        "examples": [
            {"input": "prices = [100,80,60,70,60,75,85]", "output": "[1,1,1,2,1,4,6]", "explanation": "Span computed per day."},
            {"input": "prices = [10,4,5,90,120,80]", "output": "[1,1,2,4,5,1]", "explanation": "Rising prices extend span."},
            {"input": "prices = [1,1,1,1]", "output": "[1,2,3,4]", "explanation": "Equal prices extend span."},
        ],
        "testCases": [
            {"function": "stockSpan", "input": "[100,80,60,70,60,75,85]", "expectedOutput": "[1,1,1,2,1,4,6]"},
            {"function": "stockSpan", "input": "[10,4,5,90,120,80]", "expectedOutput": "[1,1,2,4,5,1]"},
            {"function": "stockSpan", "input": "[1,1,1,1]", "expectedOutput": "[1,2,3,4]"},
            {"function": "stockSpan", "input": "[5]", "expectedOutput": "[1]"},
            {"function": "stockSpan", "input": "[1,2,3,4,5]", "expectedOutput": "[1,2,3,4,5]"},
            {"function": "stockSpan", "input": "[5,4,3,2,1]", "expectedOutput": "[1,1,1,1,1]"},
            {"function": "stockSpan", "input": "[3,3,3]", "expectedOutput": "[1,2,3]"},
            {"function": "stockSpan", "input": "[2,3,4,2,5]", "expectedOutput": "[1,2,3,1,5]"},
            {"function": "stockSpan", "input": "[7,5,6,8]", "expectedOutput": "[1,1,2,4]"},
            {"function": "stockSpan", "input": "[100,50,100]", "expectedOutput": "[1,1,3]"},
        ],
        "tags": ["stack", "monotonic-stack", "array"],
    },
    {
        "slug": "detect-cycle-list",
        "title": "Detect Cycle in Linked List",
        "difficulty": "easy",
        "description": (
            "A network packet logger suspects its packet list has a loop — "
            "packets keep circling endlessly. "
            "Given the head of a linked list, return True if it contains a cycle, False otherwise. "
            "Use Floyd's tortoise-and-hare algorithm so no extra space is needed."
        ),
        "starterCode": "class ListNode:\n    def __init__(self, val=0, next=None):\n        self.val = val\n        self.next = next\n\ndef detectCycle(head) -> bool:\n    pass",
        "examples": [
            {"input": "head = [3,2,0,-4], pos = 1", "output": "True", "explanation": "Tail connects to index 1."},
            {"input": "head = [1,2], pos = 0", "output": "True", "explanation": "Tail connects to index 0."},
            {"input": "head = [1], pos = -1", "output": "False", "explanation": "No cycle."},
        ],
        "testCases": [
            {"function": "detectCycle", "input": "[3,2,0,-4] cycle at 1", "expectedOutput": "True"},
            {"function": "detectCycle", "input": "[1,2] cycle at 0", "expectedOutput": "True"},
            {"function": "detectCycle", "input": "[1] no cycle", "expectedOutput": "False"},
            {"function": "detectCycle", "input": "[] no cycle", "expectedOutput": "False"},
            {"function": "detectCycle", "input": "[1,2,3,4,5] no cycle", "expectedOutput": "False"},
            {"function": "detectCycle", "input": "[1,2,3,4,5] cycle at 2", "expectedOutput": "True"},
            {"function": "detectCycle", "input": "[1,1] cycle at 0", "expectedOutput": "True"},
            {"function": "detectCycle", "input": "[1,2] no cycle", "expectedOutput": "False"},
            {"function": "detectCycle", "input": "[0] cycle at 0", "expectedOutput": "True"},
            {"function": "detectCycle", "input": "[1,2,3] cycle at 0", "expectedOutput": "True"},
        ],
        "tags": ["linked-list", "two-pointers", "floyd-cycle-detection"],
    },
    {
        "slug": "minimum-spanning-tree",
        "title": "Minimum Spanning Tree Cost",
        "difficulty": "hard",
        "description": (
            "A network engineer wants to connect n servers with cables, minimising total cable length. "
            "Given n points and a list of weighted edges [u, v, cost], "
            "find the minimum total cost to connect all servers. "
            "Return -1 if it is impossible to connect all servers."
        ),
        "starterCode": "def minSpanningTree(n: int, edges: list) -> int:\n    pass",
        "examples": [
            {"input": "n = 4, edges = [[0,1,10],[0,2,6],[0,3,5],[1,3,15],[2,3,4]]", "output": "19", "explanation": "Edges 2-3, 0-3, 0-1 cost 4+5+10=19."},
            {"input": "n = 2, edges = [[0,1,1]]", "output": "1", "explanation": "Single edge connects both."},
            {"input": "n = 3, edges = [[0,1,1],[1,2,2]]", "output": "3", "explanation": "Chain of two edges."},
        ],
        "testCases": [
            {"function": "minSpanningTree", "input": "4, [[0,1,10],[0,2,6],[0,3,5],[1,3,15],[2,3,4]]", "expectedOutput": "19"},
            {"function": "minSpanningTree", "input": "2, [[0,1,1]]", "expectedOutput": "1"},
            {"function": "minSpanningTree", "input": "3, [[0,1,1],[1,2,2]]", "expectedOutput": "3"},
            {"function": "minSpanningTree", "input": "3, [[0,1,5],[1,2,3],[0,2,1]]", "expectedOutput": "4"},
            {"function": "minSpanningTree", "input": "1, []", "expectedOutput": "0"},
            {"function": "minSpanningTree", "input": "4, [[0,1,1],[1,2,1],[2,3,1],[0,3,10]]", "expectedOutput": "3"},
            {"function": "minSpanningTree", "input": "3, []", "expectedOutput": "-1"},
            {"function": "minSpanningTree", "input": "5, [[0,1,2],[0,3,6],[1,2,3],[1,3,8],[1,4,5],[2,4,7]]", "expectedOutput": "16"},
            {"function": "minSpanningTree", "input": "2, [[0,1,100]]", "expectedOutput": "100"},
            {"function": "minSpanningTree", "input": "4, [[0,1,1],[2,3,2]]", "expectedOutput": "-1"},
        ],
        "tags": ["graph", "union-find", "greedy", "kruskal", "prim"],
    },
    {
        "slug": "generate-parentheses",
        "title": "Generate All Parentheses",
        "difficulty": "medium",
        "description": (
            "A LaTeX formatter needs all valid bracket combinations for a given depth. "
            "Given n pairs of parentheses, generate all valid combinations. "
            "A combination is valid if every opening bracket has a corresponding closing bracket "
            "and they are properly nested. Use backtracking."
        ),
        "starterCode": "def generateParentheses(n: int) -> list:\n    pass",
        "examples": [
            {"input": "n = 3", "output": "[\"((()))\",\"(()())\",\"(())()\",\"()(())\",\"()()()\"]", "explanation": "All 5 valid combinations."},
            {"input": "n = 1", "output": "[\"()\"]", "explanation": "Only one pair."},
            {"input": "n = 2", "output": "[\"(())\",\"()()\"]", "explanation": "Two valid combinations."},
        ],
        "testCases": [
            {"function": "generateParentheses", "input": "3", "expectedOutput": "5 combinations"},
            {"function": "generateParentheses", "input": "1", "expectedOutput": "[\"()\"]"},
            {"function": "generateParentheses", "input": "2", "expectedOutput": "[\"(())\",\"()()\"]"},
            {"function": "generateParentheses", "input": "4", "expectedOutput": "14 combinations"},
            {"function": "generateParentheses", "input": "0", "expectedOutput": "[\"\"]"},
            {"function": "generateParentheses", "input": "5", "expectedOutput": "42 combinations"},
            {"function": "generateParentheses", "input": "2", "expectedOutput": "contains (())"},
            {"function": "generateParentheses", "input": "3", "expectedOutput": "contains ((()))"},
            {"function": "generateParentheses", "input": "1", "expectedOutput": "length 1"},
            {"function": "generateParentheses", "input": "2", "expectedOutput": "length 2"},
        ],
        "tags": ["backtracking", "string", "recursion"],
    },
    {
        "slug": "number-of-1-bits",
        "title": "Count the 1 Bits",
        "difficulty": "easy",
        "description": (
            "A hardware diagnostics tool counts how many bits are set to 1 in a 32-bit unsigned integer "
            "(the Hamming weight). "
            "Given an integer n, return the number of 1 bits in its binary representation. "
            "Also known as popcount."
        ),
        "starterCode": "def countOneBits(n: int) -> int:\n    pass",
        "examples": [
            {"input": "n = 11", "output": "3", "explanation": "1011 in binary has three 1s."},
            {"input": "n = 128", "output": "1", "explanation": "10000000 has one 1."},
            {"input": "n = 4294967293", "output": "31", "explanation": "32-bit number with 31 ones."},
        ],
        "testCases": [
            {"function": "countOneBits", "input": "11", "expectedOutput": "3"},
            {"function": "countOneBits", "input": "128", "expectedOutput": "1"},
            {"function": "countOneBits", "input": "4294967293", "expectedOutput": "31"},
            {"function": "countOneBits", "input": "0", "expectedOutput": "0"},
            {"function": "countOneBits", "input": "1", "expectedOutput": "1"},
            {"function": "countOneBits", "input": "255", "expectedOutput": "8"},
            {"function": "countOneBits", "input": "65535", "expectedOutput": "16"},
            {"function": "countOneBits", "input": "4294967295", "expectedOutput": "32"},
            {"function": "countOneBits", "input": "2", "expectedOutput": "1"},
            {"function": "countOneBits", "input": "7", "expectedOutput": "3"},
        ],
        "tags": ["bit-manipulation", "math"],
    },
    {
        "slug": "missing-number-finder",
        "title": "Missing Number Finder",
        "difficulty": "easy",
        "description": (
            "A lottery machine draws n distinct numbers from the range [0, n], but one number slips out. "
            "Given an array containing n distinct numbers in the range [0, n], "
            "find and return the missing number. "
            "Aim for O(1) extra space using XOR or the sum formula."
        ),
        "starterCode": "def missingNumber(nums: list) -> int:\n    pass",
        "examples": [
            {"input": "nums = [3,0,1]", "output": "2", "explanation": "2 is missing from [0,3]."},
            {"input": "nums = [0,1]", "output": "2", "explanation": "2 is missing from [0,2]."},
            {"input": "nums = [9,6,4,2,3,5,7,0,1]", "output": "8", "explanation": "8 is missing."},
        ],
        "testCases": [
            {"function": "missingNumber", "input": "[3,0,1]", "expectedOutput": "2"},
            {"function": "missingNumber", "input": "[0,1]", "expectedOutput": "2"},
            {"function": "missingNumber", "input": "[9,6,4,2,3,5,7,0,1]", "expectedOutput": "8"},
            {"function": "missingNumber", "input": "[0]", "expectedOutput": "1"},
            {"function": "missingNumber", "input": "[1]", "expectedOutput": "0"},
            {"function": "missingNumber", "input": "[0,2]", "expectedOutput": "1"},
            {"function": "missingNumber", "input": "[1,2,3]", "expectedOutput": "0"},
            {"function": "missingNumber", "input": "[0,1,2]", "expectedOutput": "3"},
            {"function": "missingNumber", "input": "[2,3,4,5,6,7,8,9,10,0]", "expectedOutput": "1"},
            {"function": "missingNumber", "input": "[0,1,2,3,4,5,6,7,9]", "expectedOutput": "8"},
        ],
        "tags": ["array", "bit-manipulation", "math", "hash-table"],
    },
    {
        "slug": "largest-rectangle-histogram",
        "title": "Largest Rectangle in Histogram",
        "difficulty": "hard",
        "description": (
            "An architect evaluates the largest rectangular space that can be cut from a histogram skyline. "
            "Given an array of bar heights representing a histogram with bar width 1, "
            "find the area of the largest rectangle that fits within the histogram. "
            "Use a monotonic stack for an O(n) solution."
        ),
        "starterCode": "def largestRectangle(heights: list) -> int:\n    pass",
        "examples": [
            {"input": "heights = [2,1,5,6,2,3]", "output": "10", "explanation": "Rectangle of height 5 and width 2."},
            {"input": "heights = [2,4]", "output": "4", "explanation": "Rectangle of height 2 width 2 = 4, or height 4 width 1 = 4."},
            {"input": "heights = [1]", "output": "1", "explanation": "Single bar."},
        ],
        "testCases": [
            {"function": "largestRectangle", "input": "[2,1,5,6,2,3]", "expectedOutput": "10"},
            {"function": "largestRectangle", "input": "[2,4]", "expectedOutput": "4"},
            {"function": "largestRectangle", "input": "[1]", "expectedOutput": "1"},
            {"function": "largestRectangle", "input": "[1,1]", "expectedOutput": "2"},
            {"function": "largestRectangle", "input": "[0,0]", "expectedOutput": "0"},
            {"function": "largestRectangle", "input": "[6,2,5,4,5,1,6]", "expectedOutput": "12"},
            {"function": "largestRectangle", "input": "[5,5,5,5,5]", "expectedOutput": "25"},
            {"function": "largestRectangle", "input": "[1,2,3,4,5]", "expectedOutput": "9"},
            {"function": "largestRectangle", "input": "[5,4,3,2,1]", "expectedOutput": "9"},
            {"function": "largestRectangle", "input": "[4,2,0,3,2,5]", "expectedOutput": "6"},
        ],
        "tags": ["stack", "monotonic-stack", "array", "divide-and-conquer"],
    },
    {
        "slug": "kth-largest-stream",
        "title": "Kth Largest in a Stream",
        "difficulty": "easy",
        "description": (
            "A live leaderboard always shows the kth highest score seen so far. "
            "Design a class KthLargest that takes k and an initial array of scores, "
            "then supports add(val) which adds a new score and returns the current kth largest."
        ),
        "starterCode": "class KthLargest:\n    def __init__(self, k: int, nums: list):\n        pass\n    def add(self, val: int) -> int:\n        pass",
        "examples": [
            {"input": "k=3, nums=[4,5,8,2]; add(3); add(5); add(10); add(9); add(4)", "output": "4,5,5,8,8", "explanation": "3rd largest after each add."},
            {"input": "k=1, nums=[]; add(1); add(2)", "output": "1,2", "explanation": "1st largest grows."},
            {"input": "k=2, nums=[1,2,3]; add(0)", "output": "2", "explanation": "2nd largest is 2."},
        ],
        "testCases": [
            {"function": "KthLargest", "input": "k=3, nums=[4,5,8,2]; add(3)", "expectedOutput": "4"},
            {"function": "KthLargest", "input": "k=3, nums=[4,5,8,2]; add(3); add(5)", "expectedOutput": "5"},
            {"function": "KthLargest", "input": "k=3, nums=[4,5,8,2]; add(3); add(5); add(10)", "expectedOutput": "5"},
            {"function": "KthLargest", "input": "k=3, nums=[4,5,8,2]; add(3); add(5); add(10); add(9)", "expectedOutput": "8"},
            {"function": "KthLargest", "input": "k=1, nums=[]; add(1)", "expectedOutput": "1"},
            {"function": "KthLargest", "input": "k=1, nums=[]; add(1); add(2)", "expectedOutput": "2"},
            {"function": "KthLargest", "input": "k=2, nums=[1,2,3]; add(0)", "expectedOutput": "2"},
            {"function": "KthLargest", "input": "k=2, nums=[1,2,3]; add(4)", "expectedOutput": "3"},
            {"function": "KthLargest", "input": "k=3, nums=[1]; add(2); add(3)", "expectedOutput": "1"},
            {"function": "KthLargest", "input": "k=2, nums=[]; add(1); add(2); add(3)", "expectedOutput": "2"},
        ],
        "tags": ["heap", "priority-queue", "design", "sorting"],
    },
    {
        "slug": "sum-of-subarray-minimums",
        "title": "Sum of Subarray Minimums",
        "difficulty": "medium",
        "description": (
            "For every contiguous subarray of an integer array, find its minimum value. "
            "Return the sum of all those minimums. "
            "Since the answer can be huge, return it modulo 10^9 + 7. "
            "Use a monotonic stack to avoid O(n^2) brute force."
        ),
        "starterCode": "def sumSubarrayMins(arr: list) -> int:\n    pass",
        "examples": [
            {"input": "arr = [3,1,2,4]", "output": "17", "explanation": "Minimums: 3,1,1,1,2,1,2,4 sum to 17."},
            {"input": "arr = [11,81,94,43,3]", "output": "444", "explanation": "Sum of all subarray minimums."},
            {"input": "arr = [1]", "output": "1", "explanation": "Single subarray."},
        ],
        "testCases": [
            {"function": "sumSubarrayMins", "input": "[3,1,2,4]", "expectedOutput": "17"},
            {"function": "sumSubarrayMins", "input": "[11,81,94,43,3]", "expectedOutput": "444"},
            {"function": "sumSubarrayMins", "input": "[1]", "expectedOutput": "1"},
            {"function": "sumSubarrayMins", "input": "[1,2]", "expectedOutput": "4"},
            {"function": "sumSubarrayMins", "input": "[2,1]", "expectedOutput": "4"},
            {"function": "sumSubarrayMins", "input": "[1,2,3]", "expectedOutput": "10"},
            {"function": "sumSubarrayMins", "input": "[3,2,1]", "expectedOutput": "10"},
            {"function": "sumSubarrayMins", "input": "[2,2,2]", "expectedOutput": "12"},
            {"function": "sumSubarrayMins", "input": "[5,3,1,2]", "expectedOutput": "18"},
            {"function": "sumSubarrayMins", "input": "[1,3,2,4,1]", "expectedOutput": "23"},
        ],
        "tags": ["stack", "monotonic-stack", "dynamic-programming", "array"],
    },
    {
        "slug": "count-paths-obstacles",
        "title": "Count Paths with Obstacles",
        "difficulty": "medium",
        "description": (
            "A drone navigates an m x n warehouse grid from top-left to bottom-right, "
            "moving only right or down. Some cells are blocked by obstacles (marked 1). "
            "Count the number of unique paths that avoid all obstacles. "
            "Return the count modulo 10^9 + 7."
        ),
        "starterCode": "def countPathsObstacles(grid: list) -> int:\n    pass",
        "examples": [
            {"input": "grid = [[0,0,0],[0,1,0],[0,0,0]]", "output": "2", "explanation": "Obstacle blocks one path."},
            {"input": "grid = [[0,1],[0,0]]", "output": "1", "explanation": "One path avoids obstacle."},
            {"input": "grid = [[1,0]]", "output": "0", "explanation": "Start is blocked."},
        ],
        "testCases": [
            {"function": "countPathsObstacles", "input": "[[0,0,0],[0,1,0],[0,0,0]]", "expectedOutput": "2"},
            {"function": "countPathsObstacles", "input": "[[0,1],[0,0]]", "expectedOutput": "1"},
            {"function": "countPathsObstacles", "input": "[[1,0]]", "expectedOutput": "0"},
            {"function": "countPathsObstacles", "input": "[[0]]", "expectedOutput": "1"},
            {"function": "countPathsObstacles", "input": "[[0,0],[0,0]]", "expectedOutput": "2"},
            {"function": "countPathsObstacles", "input": "[[0,0],[1,0]]", "expectedOutput": "1"},
            {"function": "countPathsObstacles", "input": "[[0,0,0],[0,0,0]]", "expectedOutput": "3"},
            {"function": "countPathsObstacles", "input": "[[0,0],[0,1]]", "expectedOutput": "0"},
            {"function": "countPathsObstacles", "input": "[[0,1,0],[0,0,0]]", "expectedOutput": "2"},
            {"function": "countPathsObstacles", "input": "[[0,0,0,0],[0,1,0,0],[0,0,0,0]]", "expectedOutput": "4"},
        ],
        "tags": ["dynamic-programming", "matrix", "array"],
    },
    {
        "slug": "all-paths-source-target",
        "title": "All Paths from Source to Target",
        "difficulty": "medium",
        "description": (
            "A GPS app finds every possible route from city 0 to the last city in a directed acyclic graph. "
            "Given a DAG as an adjacency list, return all paths from node 0 to node n-1. "
            "The output paths can be in any order."
        ),
        "starterCode": "def allPaths(graph: list) -> list:\n    pass",
        "examples": [
            {"input": "graph = [[1,2],[3],[3],[]]", "output": "[[0,1,3],[0,2,3]]", "explanation": "Two routes to node 3."},
            {"input": "graph = [[4,3,1],[3,2,4],[3],[4],[]]", "output": "[[0,4],[0,3,4],[0,1,3,4],[0,1,2,3,4],[0,1,4]]", "explanation": "Five routes."},
            {"input": "graph = [[1],[]]", "output": "[[0,1]]", "explanation": "Single path."},
        ],
        "testCases": [
            {"function": "allPaths", "input": "[[1,2],[3],[3],[]]", "expectedOutput": "[[0,1,3],[0,2,3]]"},
            {"function": "allPaths", "input": "[[1],[]]", "expectedOutput": "[[0,1]]"},
            {"function": "allPaths", "input": "[[]]", "expectedOutput": "[[0]]"},
            {"function": "allPaths", "input": "[[1,2],[2],[]]", "expectedOutput": "[[0,1,2],[0,2]]"},
            {"function": "allPaths", "input": "[[1,2,3],[3],[3],[]]", "expectedOutput": "[[0,1,3],[0,2,3],[0,3]]"},
            {"function": "allPaths", "input": "[[1],[2],[3],[]]", "expectedOutput": "[[0,1,2,3]]"},
            {"function": "allPaths", "input": "[[2],[2],[]]", "expectedOutput": "[[0,2],[1,2]] or similar"},
            {"function": "allPaths", "input": "[[1,3],[2],[3],[]]", "expectedOutput": "[[0,1,2,3],[0,3]]"},
            {"function": "allPaths", "input": "[[1],[2,3],[3],[]]", "expectedOutput": "[[0,1,2,3],[0,1,3]]"},
            {"function": "allPaths", "input": "[[2,3,4],[],[3,4],[4],[]]", "expectedOutput": "5 paths"},
        ],
        "tags": ["graph", "dfs", "backtracking", "dag"],
    },
    {
        "slug": "decode-ways",
        "title": "Decode Ways",
        "difficulty": "medium",
        "description": (
            "A spy agency encodes messages as numeric strings where A=1, B=2, ..., Z=26. "
            "Given a non-empty string of digits, return the total number of ways it can be decoded. "
            "For example '12' can be decoded as 'AB' (1,2) or 'L' (12). "
            "Return 0 if no valid decoding exists."
        ),
        "starterCode": "def decodeWays(s: str) -> int:\n    pass",
        "examples": [
            {"input": "s = \"12\"", "output": "2", "explanation": "'AB' or 'L'."},
            {"input": "s = \"226\"", "output": "3", "explanation": "'BZ','VF','BBF'."},
            {"input": "s = \"06\"", "output": "0", "explanation": "Leading zero, invalid."},
        ],
        "testCases": [
            {"function": "decodeWays", "input": "\"12\"", "expectedOutput": "2"},
            {"function": "decodeWays", "input": "\"226\"", "expectedOutput": "3"},
            {"function": "decodeWays", "input": "\"06\"", "expectedOutput": "0"},
            {"function": "decodeWays", "input": "\"0\"", "expectedOutput": "0"},
            {"function": "decodeWays", "input": "\"1\"", "expectedOutput": "1"},
            {"function": "decodeWays", "input": "\"10\"", "expectedOutput": "1"},
            {"function": "decodeWays", "input": "\"11\"", "expectedOutput": "2"},
            {"function": "decodeWays", "input": "\"100\"", "expectedOutput": "0"},
            {"function": "decodeWays", "input": "\"111\"", "expectedOutput": "3"},
            {"function": "decodeWays", "input": "\"2611055971756562\"", "expectedOutput": "4"},
        ],
        "tags": ["dynamic-programming", "string"],
    },
    {
        "slug": "min-stack-design",
        "title": "Min Stack Design",
        "difficulty": "easy",
        "description": (
            "A calculator keeps a history stack and needs to instantly recall the smallest value ever on the stack. "
            "Design a MinStack class that supports push(val), pop(), top() and getMin() — "
            "all in O(1) time. The getMin() must return the minimum element in the current stack."
        ),
        "starterCode": "class MinStack:\n    def __init__(self):\n        pass\n    def push(self, val: int) -> None:\n        pass\n    def pop(self) -> None:\n        pass\n    def top(self) -> int:\n        pass\n    def getMin(self) -> int:\n        pass",
        "examples": [
            {"input": "push(-2); push(0); push(-3); getMin(); pop(); top(); getMin()", "output": "-3, 0, -2", "explanation": "Min tracks the minimum at each state."},
            {"input": "push(5); push(3); getMin(); pop(); getMin()", "output": "3, 5", "explanation": "Min updates after pop."},
            {"input": "push(1); top(); getMin()", "output": "1, 1", "explanation": "Single element."},
        ],
        "testCases": [
            {"function": "MinStack", "input": "push(-2); push(0); push(-3); getMin()", "expectedOutput": "-3"},
            {"function": "MinStack", "input": "push(-2); push(0); push(-3); pop(); getMin()", "expectedOutput": "-2"},
            {"function": "MinStack", "input": "push(-2); push(0); push(-3); pop(); top()", "expectedOutput": "0"},
            {"function": "MinStack", "input": "push(5); getMin()", "expectedOutput": "5"},
            {"function": "MinStack", "input": "push(5); push(3); getMin()", "expectedOutput": "3"},
            {"function": "MinStack", "input": "push(5); push(3); pop(); getMin()", "expectedOutput": "5"},
            {"function": "MinStack", "input": "push(1); push(2); top()", "expectedOutput": "2"},
            {"function": "MinStack", "input": "push(3); push(1); push(2); getMin()", "expectedOutput": "1"},
            {"function": "MinStack", "input": "push(0); push(1); push(0); getMin()", "expectedOutput": "0"},
            {"function": "MinStack", "input": "push(2); push(0); push(3); push(0); getMin()", "expectedOutput": "0"},
        ],
        "tags": ["stack", "design"],
    },
    {
        "slug": "find-anagram-windows",
        "title": "Find Anagram Windows",
        "difficulty": "medium",
        "description": (
            "A bioinformatics tool scans a genome string for all positions where a gene pattern (or any anagram of it) begins. "
            "Given strings s and p, return all starting indices in s where a substring of length len(p) "
            "is an anagram of p. Return indices in ascending order."
        ),
        "starterCode": "def findAnagramWindows(s: str, p: str) -> list:\n    pass",
        "examples": [
            {"input": "s = \"cbaebabacd\", p = \"abc\"", "output": "[0,6]", "explanation": "Anagrams at index 0 and 6."},
            {"input": "s = \"abab\", p = \"ab\"", "output": "[0,1,2]", "explanation": "Anagram at every position."},
            {"input": "s = \"aaa\", p = \"aa\"", "output": "[0,1]", "explanation": "Two overlapping anagrams."},
        ],
        "testCases": [
            {"function": "findAnagramWindows", "input": "\"cbaebabacd\", \"abc\"", "expectedOutput": "[0,6]"},
            {"function": "findAnagramWindows", "input": "\"abab\", \"ab\"", "expectedOutput": "[0,1,2]"},
            {"function": "findAnagramWindows", "input": "\"aaa\", \"aa\"", "expectedOutput": "[0,1]"},
            {"function": "findAnagramWindows", "input": "\"af\", \"be\"", "expectedOutput": "[]"},
            {"function": "findAnagramWindows", "input": "\"baa\", \"aa\"", "expectedOutput": "[1]"},
            {"function": "findAnagramWindows", "input": "\"abc\", \"abc\"", "expectedOutput": "[0]"},
            {"function": "findAnagramWindows", "input": "\"abcde\", \"cba\"", "expectedOutput": "[0]"},
            {"function": "findAnagramWindows", "input": "\"eidbaooo\", \"ab\"", "expectedOutput": "[3]"},
            {"function": "findAnagramWindows", "input": "\"abaacbabc\", \"abc\"", "expectedOutput": "[3,4,6]"},
            {"function": "findAnagramWindows", "input": "\"xyz\", \"zy\"", "expectedOutput": "[1]"},
        ],
        "tags": ["sliding-window", "hash-table", "string", "two-pointers"],
    },
    {
        "slug": "network-delay-time",
        "title": "Network Delay Time",
        "difficulty": "medium",
        "description": (
            "A network engineer sends a signal from server k to all other servers in a weighted directed graph. "
            "Each edge represents a one-way connection with a travel time. "
            "Return the minimum time for the signal to reach all servers, "
            "or -1 if some server is unreachable. Use Dijkstra's algorithm."
        ),
        "starterCode": "def networkDelay(times: list, n: int, k: int) -> int:\n    pass",
        "examples": [
            {"input": "times = [[2,1,1],[2,3,1],[3,4,1]], n = 4, k = 2", "output": "2", "explanation": "All reached in 2 time units."},
            {"input": "times = [[1,2,1]], n = 2, k = 1", "output": "1", "explanation": "Direct path."},
            {"input": "times = [[1,2,1]], n = 2, k = 2", "output": "-1", "explanation": "Server 1 unreachable from 2."},
        ],
        "testCases": [
            {"function": "networkDelay", "input": "[[2,1,1],[2,3,1],[3,4,1]], 4, 2", "expectedOutput": "2"},
            {"function": "networkDelay", "input": "[[1,2,1]], 2, 1", "expectedOutput": "1"},
            {"function": "networkDelay", "input": "[[1,2,1]], 2, 2", "expectedOutput": "-1"},
            {"function": "networkDelay", "input": "[[1,2,1],[2,3,2],[1,3,4]], 3, 1", "expectedOutput": "3"},
            {"function": "networkDelay", "input": "[[1,2,1],[1,3,1],[2,4,1],[3,4,1]], 4, 1", "expectedOutput": "2"},
            {"function": "networkDelay", "input": "[[1,2,1],[2,1,3]], 2, 1", "expectedOutput": "1"},
            {"function": "networkDelay", "input": "[[1,2,1],[1,3,1],[2,4,1]], 4, 1", "expectedOutput": "2"},
            {"function": "networkDelay", "input": "[[2,3,1],[2,4,1],[3,5,2],[4,5,1]], 5, 2", "expectedOutput": "2"},
            {"function": "networkDelay", "input": "[[1,2,1]], 3, 1", "expectedOutput": "-1"},
            {"function": "networkDelay", "input": "[[1,2,1],[2,3,1],[3,1,1]], 3, 1", "expectedOutput": "2"},
        ],
        "tags": ["graph", "dijkstra", "shortest-path", "heap"],
    },
    {
        "slug": "partition-equal-subsets",
        "title": "Partition Into Equal Subsets",
        "difficulty": "medium",
        "description": (
            "A delivery manager wants to split a list of package weights into two groups "
            "with exactly equal total weight. "
            "Given an integer array, return True if it can be partitioned into two subsets with equal sum, "
            "False otherwise. Use dynamic programming."
        ),
        "starterCode": "def partitionEqualSubsets(nums: list) -> bool:\n    pass",
        "examples": [
            {"input": "nums = [1,5,11,5]", "output": "True", "explanation": "[1,5,5] and [11]."},
            {"input": "nums = [1,2,3,5]", "output": "False", "explanation": "No equal partition possible."},
            {"input": "nums = [2,2]", "output": "True", "explanation": "Each subset gets one 2."},
        ],
        "testCases": [
            {"function": "partitionEqualSubsets", "input": "[1,5,11,5]", "expectedOutput": "True"},
            {"function": "partitionEqualSubsets", "input": "[1,2,3,5]", "expectedOutput": "False"},
            {"function": "partitionEqualSubsets", "input": "[2,2]", "expectedOutput": "True"},
            {"function": "partitionEqualSubsets", "input": "[1,1]", "expectedOutput": "True"},
            {"function": "partitionEqualSubsets", "input": "[1,2]", "expectedOutput": "False"},
            {"function": "partitionEqualSubsets", "input": "[3,3,3,4,5]", "expectedOutput": "True"},
            {"function": "partitionEqualSubsets", "input": "[1,2,3,4,5,6,7]", "expectedOutput": "True"},
            {"function": "partitionEqualSubsets", "input": "[1]", "expectedOutput": "False"},
            {"function": "partitionEqualSubsets", "input": "[100,100]", "expectedOutput": "True"},
            {"function": "partitionEqualSubsets", "input": "[1,2,5]", "expectedOutput": "False"},
        ],
        "tags": ["dynamic-programming", "array", "subset-sum"],
    },
    {
        "slug": "word-break-check",
        "title": "Word Break Check",
        "difficulty": "medium",
        "description": (
            "A spell-checker segments a compound string into individual dictionary words. "
            "Given a string s and a dictionary wordDict, return True if s can be segmented "
            "into a space-separated sequence of one or more dictionary words. "
            "Words in the dictionary may be reused."
        ),
        "starterCode": "def wordBreak(s: str, wordDict: list) -> bool:\n    pass",
        "examples": [
            {"input": "s = \"leetcode\", wordDict = [\"leet\",\"code\"]", "output": "True", "explanation": "'leet code'."},
            {"input": "s = \"applepenapple\", wordDict = [\"apple\",\"pen\"]", "output": "True", "explanation": "'apple pen apple'."},
            {"input": "s = \"catsandog\", wordDict = [\"cats\",\"dog\",\"sand\",\"and\",\"cat\"]", "output": "False", "explanation": "Cannot fully segment."},
        ],
        "testCases": [
            {"function": "wordBreak", "input": "\"leetcode\", [\"leet\",\"code\"]", "expectedOutput": "True"},
            {"function": "wordBreak", "input": "\"applepenapple\", [\"apple\",\"pen\"]", "expectedOutput": "True"},
            {"function": "wordBreak", "input": "\"catsandog\", [\"cats\",\"dog\",\"sand\",\"and\",\"cat\"]", "expectedOutput": "False"},
            {"function": "wordBreak", "input": "\"a\", [\"a\"]", "expectedOutput": "True"},
            {"function": "wordBreak", "input": "\"ab\", [\"a\",\"b\"]", "expectedOutput": "True"},
            {"function": "wordBreak", "input": "\"aaaa\", [\"a\",\"aa\"]", "expectedOutput": "True"},
            {"function": "wordBreak", "input": "\"cars\", [\"car\",\"ca\",\"rs\"]", "expectedOutput": "True"},
            {"function": "wordBreak", "input": "\"abc\", [\"a\",\"bc\",\"abc\"]", "expectedOutput": "True"},
            {"function": "wordBreak", "input": "\"hello\", [\"he\",\"world\"]", "expectedOutput": "False"},
            {"function": "wordBreak", "input": "\"goalspecial\", [\"go\",\"goal\",\"goals\",\"special\"]", "expectedOutput": "True"},
        ],
        "tags": ["dynamic-programming", "string", "trie", "hash-table"],
    },
    {
        "slug": "number-of-connected-components",
        "title": "Number of Connected Components",
        "difficulty": "medium",
        "description": (
            "A social network analyst counts distinct friend groups. "
            "Given n people (nodes 0 to n-1) and a list of friendships (edges), "
            "find the number of connected components in the undirected graph. "
            "Use Union-Find or DFS."
        ),
        "starterCode": "def countComponents(n: int, edges: list) -> int:\n    pass",
        "examples": [
            {"input": "n = 5, edges = [[0,1],[1,2],[3,4]]", "output": "2", "explanation": "{0,1,2} and {3,4}."},
            {"input": "n = 5, edges = [[0,1],[1,2],[2,3],[3,4]]", "output": "1", "explanation": "All connected."},
            {"input": "n = 3, edges = []", "output": "3", "explanation": "No edges, all isolated."},
        ],
        "testCases": [
            {"function": "countComponents", "input": "5, [[0,1],[1,2],[3,4]]", "expectedOutput": "2"},
            {"function": "countComponents", "input": "5, [[0,1],[1,2],[2,3],[3,4]]", "expectedOutput": "1"},
            {"function": "countComponents", "input": "3, []", "expectedOutput": "3"},
            {"function": "countComponents", "input": "1, []", "expectedOutput": "1"},
            {"function": "countComponents", "input": "2, [[0,1]]", "expectedOutput": "1"},
            {"function": "countComponents", "input": "4, [[0,1],[2,3]]", "expectedOutput": "2"},
            {"function": "countComponents", "input": "4, [[0,1],[1,2],[2,3]]", "expectedOutput": "1"},
            {"function": "countComponents", "input": "6, [[0,1],[2,3],[4,5]]", "expectedOutput": "3"},
            {"function": "countComponents", "input": "5, [[0,1],[0,2],[0,3],[0,4]]", "expectedOutput": "1"},
            {"function": "countComponents", "input": "5, []", "expectedOutput": "5"},
        ],
        "tags": ["graph", "union-find", "dfs", "bfs"],
    },
    {
        "slug": "longest-common-subsequence",
        "title": "Longest Common Subsequence",
        "difficulty": "medium",
        "description": (
            "A version control tool computes how similar two file versions are by finding their longest common subsequence. "
            "A subsequence can skip characters but must maintain order. "
            "Given two strings text1 and text2, return the length of their longest common subsequence. "
            "Return 0 if none exists."
        ),
        "starterCode": "def longestCommonSubsequence(text1: str, text2: str) -> int:\n    pass",
        "examples": [
            {"input": "text1 = \"abcde\", text2 = \"ace\"", "output": "3", "explanation": "LCS is 'ace'."},
            {"input": "text1 = \"abc\", text2 = \"abc\"", "output": "3", "explanation": "Identical strings."},
            {"input": "text1 = \"abc\", text2 = \"def\"", "output": "0", "explanation": "No common characters."},
        ],
        "testCases": [
            {"function": "longestCommonSubsequence", "input": "\"abcde\", \"ace\"", "expectedOutput": "3"},
            {"function": "longestCommonSubsequence", "input": "\"abc\", \"abc\"", "expectedOutput": "3"},
            {"function": "longestCommonSubsequence", "input": "\"abc\", \"def\"", "expectedOutput": "0"},
            {"function": "longestCommonSubsequence", "input": "\"a\", \"a\"", "expectedOutput": "1"},
            {"function": "longestCommonSubsequence", "input": "\"a\", \"b\"", "expectedOutput": "0"},
            {"function": "longestCommonSubsequence", "input": "\"bsbininm\", \"jmjkbkjkv\"", "expectedOutput": "1"},
            {"function": "longestCommonSubsequence", "input": "\"ezupkr\", \"ubmrapg\"", "expectedOutput": "2"},
            {"function": "longestCommonSubsequence", "input": "\"abcba\", \"abcbcba\"", "expectedOutput": "5"},
            {"function": "longestCommonSubsequence", "input": "\"psnw\", \"vozsh\"", "expectedOutput": "1"},
            {"function": "longestCommonSubsequence", "input": "\"oxcpqrsvwf\", \"shmtulqrypy\"", "expectedOutput": "2"},
        ],
        "tags": ["dynamic-programming", "string"],
    },
    {
        "slug": "flood-fill-paint",
        "title": "Flood Fill Paint",
        "difficulty": "easy",
        "description": (
            "A paint bucket tool in a graphics editor fills a connected region of the same color with a new color. "
            "Given an image as a 2D grid of integers, a starting pixel (sr, sc), and a new color, "
            "perform the flood fill — change the starting pixel and all connected pixels of the same original color. "
            "Return the modified image."
        ),
        "starterCode": "def floodFillPaint(image: list, sr: int, sc: int, color: int) -> list:\n    pass",
        "examples": [
            {"input": "image = [[1,1,1],[1,1,0],[1,0,1]], sr = 1, sc = 1, color = 2", "output": "[[2,2,2],[2,2,0],[2,0,1]]", "explanation": "All connected 1s changed to 2."},
            {"input": "image = [[0,0,0],[0,0,0]], sr = 0, sc = 0, color = 0", "output": "[[0,0,0],[0,0,0]]", "explanation": "Same color, no change."},
            {"input": "image = [[1,0],[0,1]], sr = 0, sc = 0, color = 2", "output": "[[2,0],[0,1]]", "explanation": "Only top-left filled."},
        ],
        "testCases": [
            {"function": "floodFillPaint", "input": "[[1,1,1],[1,1,0],[1,0,1]], 1, 1, 2", "expectedOutput": "[[2,2,2],[2,2,0],[2,0,1]]"},
            {"function": "floodFillPaint", "input": "[[0,0,0],[0,0,0]], 0, 0, 0", "expectedOutput": "[[0,0,0],[0,0,0]]"},
            {"function": "floodFillPaint", "input": "[[1,0],[0,1]], 0, 0, 2", "expectedOutput": "[[2,0],[0,1]]"},
            {"function": "floodFillPaint", "input": "[[1]], 0, 0, 2", "expectedOutput": "[[2]]"},
            {"function": "floodFillPaint", "input": "[[0,0,0],[0,1,1]], 1, 1, 1", "expectedOutput": "[[0,0,0],[0,1,1]]"},
            {"function": "floodFillPaint", "input": "[[1,1,1],[1,1,1],[1,1,1]], 1, 1, 5", "expectedOutput": "[[5,5,5],[5,5,5],[5,5,5]]"},
            {"function": "floodFillPaint", "input": "[[0,0,0],[0,0,0],[0,0,0]], 0, 0, 3", "expectedOutput": "[[3,3,3],[3,3,3],[3,3,3]]"},
            {"function": "floodFillPaint", "input": "[[1,0,1],[0,1,0]], 0, 0, 2", "expectedOutput": "[[2,0,1],[0,1,0]]"},
            {"function": "floodFillPaint", "input": "[[2,2,2],[2,0,2]], 0, 0, 1", "expectedOutput": "[[1,1,1],[1,0,1]]"},
            {"function": "floodFillPaint", "input": "[[1,1],[1,2]], 0, 0, 3", "expectedOutput": "[[3,3],[3,2]]"},
        ],
        "tags": ["graph", "dfs", "bfs", "matrix"],
    },
    {
        "slug": "edit-distance",
        "title": "Edit Distance",
        "difficulty": "hard",
        "description": (
            "A spell-corrector calculates the minimum number of single-character edits needed to transform one word into another. "
            "Allowed operations are: insert a character, delete a character, or replace a character. "
            "Given two strings word1 and word2, return the minimum edit distance (Levenshtein distance)."
        ),
        "starterCode": "def editDistance(word1: str, word2: str) -> int:\n    pass",
        "examples": [
            {"input": "word1 = \"horse\", word2 = \"ros\"", "output": "3", "explanation": "horse->rorse->rose->ros."},
            {"input": "word1 = \"intention\", word2 = \"execution\"", "output": "5", "explanation": "Five edits needed."},
            {"input": "word1 = \"abc\", word2 = \"abc\"", "output": "0", "explanation": "Identical strings."},
        ],
        "testCases": [
            {"function": "editDistance", "input": "\"horse\", \"ros\"", "expectedOutput": "3"},
            {"function": "editDistance", "input": "\"intention\", \"execution\"", "expectedOutput": "5"},
            {"function": "editDistance", "input": "\"abc\", \"abc\"", "expectedOutput": "0"},
            {"function": "editDistance", "input": "\"\", \"abc\"", "expectedOutput": "3"},
            {"function": "editDistance", "input": "\"abc\", \"\"", "expectedOutput": "3"},
            {"function": "editDistance", "input": "\"\", \"\"", "expectedOutput": "0"},
            {"function": "editDistance", "input": "\"a\", \"b\"", "expectedOutput": "1"},
            {"function": "editDistance", "input": "\"kitten\", \"sitting\"", "expectedOutput": "3"},
            {"function": "editDistance", "input": "\"park\", \"spake\"", "expectedOutput": "3"},
            {"function": "editDistance", "input": "\"abcd\", \"dcba\"", "expectedOutput": "4"},
        ],
        "tags": ["dynamic-programming", "string"],
    },
    {
        "slug": "gas-station-circuit",
        "title": "Gas Station Circuit",
        "difficulty": "medium",
        "description": (
            "A road trip planner checks if a car can complete a full circular route through n gas stations. "
            "At station i, you collect gas[i] litres but spend cost[i] to reach the next station. "
            "Return the starting station index if a complete circuit is possible, or -1 if not. "
            "A solution always exists uniquely if one exists."
        ),
        "starterCode": "def gasStationCircuit(gas: list, cost: list) -> int:\n    pass",
        "examples": [
            {"input": "gas = [1,2,3,4,5], cost = [3,4,5,1,2]", "output": "3", "explanation": "Start at station 3."},
            {"input": "gas = [2,3,4], cost = [3,4,3]", "output": "-1", "explanation": "Cannot complete circuit."},
            {"input": "gas = [5,1,2,3,4], cost = [4,4,1,5,1]", "output": "4", "explanation": "Start at station 4."},
        ],
        "testCases": [
            {"function": "gasStationCircuit", "input": "[1,2,3,4,5], [3,4,5,1,2]", "expectedOutput": "3"},
            {"function": "gasStationCircuit", "input": "[2,3,4], [3,4,3]", "expectedOutput": "-1"},
            {"function": "gasStationCircuit", "input": "[5,1,2,3,4], [4,4,1,5,1]", "expectedOutput": "4"},
            {"function": "gasStationCircuit", "input": "[1], [1]", "expectedOutput": "0"},
            {"function": "gasStationCircuit", "input": "[1], [2]", "expectedOutput": "-1"},
            {"function": "gasStationCircuit", "input": "[3,3,4], [3,4,4]", "expectedOutput": "-1"},
            {"function": "gasStationCircuit", "input": "[4,5,2,6,5,3], [3,2,7,3,2,9]", "expectedOutput": "1"},
            {"function": "gasStationCircuit", "input": "[2,0,1,2,3,4], [0,1,0,0,0,0]", "expectedOutput": "0"},
            {"function": "gasStationCircuit", "input": "[0,1,2,3,4], [4,0,1,2,3]", "expectedOutput": "1"},
            {"function": "gasStationCircuit", "input": "[1,2,3], [2,3,4]", "expectedOutput": "-1"},
        ],
        "tags": ["greedy", "array"],
    },
    {
        "slug": "matrix-search-sorted",
        "title": "Search in Sorted Matrix",
        "difficulty": "medium",
        "description": (
            "A database stores records in a 2D grid where each row is sorted left to right, "
            "and each column is sorted top to bottom. "
            "Given a target value, return True if it exists in the matrix, False otherwise. "
            "Achieve O(m + n) time by starting from the top-right corner."
        ),
        "starterCode": "def searchSortedMatrix(matrix: list, target: int) -> bool:\n    pass",
        "examples": [
            {"input": "matrix = [[1,4,7,11],[2,5,8,12],[3,6,9,16],[10,13,14,17]], target = 5", "output": "True", "explanation": "5 found at [1][1]."},
            {"input": "matrix = [[1,4,7,11],[2,5,8,12],[3,6,9,16],[10,13,14,17]], target = 20", "output": "False", "explanation": "20 not present."},
            {"input": "matrix = [[1,1]], target = 2", "output": "False", "explanation": "2 not in matrix."},
        ],
        "testCases": [
            {"function": "searchSortedMatrix", "input": "[[1,4,7,11],[2,5,8,12],[3,6,9,16],[10,13,14,17]], 5", "expectedOutput": "True"},
            {"function": "searchSortedMatrix", "input": "[[1,4,7,11],[2,5,8,12],[3,6,9,16],[10,13,14,17]], 20", "expectedOutput": "False"},
            {"function": "searchSortedMatrix", "input": "[[1,1]], 2", "expectedOutput": "False"},
            {"function": "searchSortedMatrix", "input": "[[1]], 1", "expectedOutput": "True"},
            {"function": "searchSortedMatrix", "input": "[[1,3,5],[2,4,6],[3,6,9]], 4", "expectedOutput": "True"},
            {"function": "searchSortedMatrix", "input": "[[1,3,5],[2,4,6],[3,6,9]], 7", "expectedOutput": "False"},
            {"function": "searchSortedMatrix", "input": "[[-5]], -5", "expectedOutput": "True"},
            {"function": "searchSortedMatrix", "input": "[[1,4],[2,5]], 3", "expectedOutput": "False"},
            {"function": "searchSortedMatrix", "input": "[[1,2,3],[4,5,6],[7,8,9]], 9", "expectedOutput": "True"},
            {"function": "searchSortedMatrix", "input": "[[1,2,3],[4,5,6],[7,8,9]], 0", "expectedOutput": "False"},
        ],
        "tags": ["matrix", "binary-search", "two-pointers"],
    },
    {
        "slug": "count-islands-perimeter",
        "title": "Island Perimeter Calculator",
        "difficulty": "easy",
        "description": (
            "A cartographer measures the coastline length of an island on a grid map. "
            "Given a 2D grid where 1=land and 0=water, and there is exactly one island (no lakes inside), "
            "calculate and return the perimeter of the island."
        ),
        "starterCode": "def islandPerimeter(grid: list) -> int:\n    pass",
        "examples": [
            {"input": "grid = [[0,1,0,0],[1,1,1,0],[0,1,0,0],[1,1,0,0]]", "output": "16", "explanation": "Coastline has 16 edge units."},
            {"input": "grid = [[1]]", "output": "4", "explanation": "Single cell has 4 sides."},
            {"input": "grid = [[1,0]]", "output": "4", "explanation": "One cell, 4 edges."},
        ],
        "testCases": [
            {"function": "islandPerimeter", "input": "[[0,1,0,0],[1,1,1,0],[0,1,0,0],[1,1,0,0]]", "expectedOutput": "16"},
            {"function": "islandPerimeter", "input": "[[1]]", "expectedOutput": "4"},
            {"function": "islandPerimeter", "input": "[[1,0]]", "expectedOutput": "4"},
            {"function": "islandPerimeter", "input": "[[1,1]]", "expectedOutput": "6"},
            {"function": "islandPerimeter", "input": "[[1],[1]]", "expectedOutput": "6"},
            {"function": "islandPerimeter", "input": "[[1,1],[1,1]]", "expectedOutput": "8"},
            {"function": "islandPerimeter", "input": "[[0,1],[1,0]]", "expectedOutput": "8"},
            {"function": "islandPerimeter", "input": "[[1,1,1]]", "expectedOutput": "8"},
            {"function": "islandPerimeter", "input": "[[0,1,0],[1,1,1],[0,1,0]]", "expectedOutput": "12"},
            {"function": "islandPerimeter", "input": "[[1,1,1],[1,0,1],[1,1,1]]", "expectedOutput": "16"},
        ],
        "tags": ["matrix", "dfs", "array"],
    },
    {
        "slug": "palindrome-partitioning",
        "title": "Palindrome Partitioning",
        "difficulty": "medium",
        "description": (
            "A cryptographer splits a string into the fewest parts so that each part reads the same forwards and backwards. "
            "Given a string s, return all possible ways to partition it such that every substring is a palindrome. "
            "Use backtracking."
        ),
        "starterCode": "def palindromePartitioning(s: str) -> list:\n    pass",
        "examples": [
            {"input": "s = \"aab\"", "output": "[[\"a\",\"a\",\"b\"],[\"aa\",\"b\"]]", "explanation": "Two valid partitions."},
            {"input": "s = \"a\"", "output": "[[\"a\"]]", "explanation": "Single character."},
            {"input": "s = \"aba\"", "output": "[[\"a\",\"b\",\"a\"],[\"aba\"]]", "explanation": "Two partitions."},
        ],
        "testCases": [
            {"function": "palindromePartitioning", "input": "\"aab\"", "expectedOutput": "[[\"a\",\"a\",\"b\"],[\"aa\",\"b\"]]"},
            {"function": "palindromePartitioning", "input": "\"a\"", "expectedOutput": "[[\"a\"]]"},
            {"function": "palindromePartitioning", "input": "\"aba\"", "expectedOutput": "[[\"a\",\"b\",\"a\"],[\"aba\"]]"},
            {"function": "palindromePartitioning", "input": "\"racecar\"", "expectedOutput": "includes [[\"racecar\"]]"},
            {"function": "palindromePartitioning", "input": "\"ab\"", "expectedOutput": "[[\"a\",\"b\"]]"},
            {"function": "palindromePartitioning", "input": "\"aa\"", "expectedOutput": "[[\"a\",\"a\"],[\"aa\"]]"},
            {"function": "palindromePartitioning", "input": "\"aaa\"", "expectedOutput": "3 partitions"},
            {"function": "palindromePartitioning", "input": "\"abc\"", "expectedOutput": "[[\"a\",\"b\",\"c\"]]"},
            {"function": "palindromePartitioning", "input": "\"aaaa\"", "expectedOutput": "5 partitions"},
            {"function": "palindromePartitioning", "input": "\"abba\"", "expectedOutput": "includes [[\"abba\"]]"},
        ],
        "tags": ["backtracking", "dynamic-programming", "string"],
    },
    {
        "slug": "n-queens-puzzle",
        "title": "N-Queens Puzzle",
        "difficulty": "hard",
        "description": (
            "Place n chess queens on an n x n board so no two queens threaten each other — "
            "no two queens share the same row, column, or diagonal. "
            "Return all distinct solutions. Each solution is a list of strings where 'Q' marks a queen and '.' marks empty. "
            "Use backtracking."
        ),
        "starterCode": "def nQueens(n: int) -> list:\n    pass",
        "examples": [
            {"input": "n = 4", "output": "[\".Q..\",\"...Q\",\"Q...\",\"..Q.\"], [\"..Q.\",\"Q...\",\"...Q\",\".Q..\"]", "explanation": "Two valid board layouts."},
            {"input": "n = 1", "output": "[[\"Q\"]]", "explanation": "One queen on 1x1 board."},
            {"input": "n = 3", "output": "[]", "explanation": "No solution for 3x3."},
        ],
        "testCases": [
            {"function": "nQueens", "input": "4", "expectedOutput": "2 solutions"},
            {"function": "nQueens", "input": "1", "expectedOutput": "1 solution"},
            {"function": "nQueens", "input": "3", "expectedOutput": "0 solutions"},
            {"function": "nQueens", "input": "2", "expectedOutput": "0 solutions"},
            {"function": "nQueens", "input": "5", "expectedOutput": "10 solutions"},
            {"function": "nQueens", "input": "6", "expectedOutput": "4 solutions"},
            {"function": "nQueens", "input": "7", "expectedOutput": "40 solutions"},
            {"function": "nQueens", "input": "8", "expectedOutput": "92 solutions"},
            {"function": "nQueens", "input": "1", "expectedOutput": "[[\"Q\"]]"},
            {"function": "nQueens", "input": "4", "expectedOutput": "includes .Q.. board"},
        ],
        "tags": ["backtracking", "matrix", "recursion"],
    },
    {
        "slug": "palindromic-substrings-count",
        "title": "Count Palindromic Substrings",
        "difficulty": "medium",
        "description": (
            "A lexical analyser counts how many substrings of a given string are palindromes. "
            "Single characters are always palindromes. "
            "Given a string s, return the number of palindromic substrings. "
            "Use the expand-around-center technique."
        ),
        "starterCode": "def countPalindromicSubstrings(s: str) -> int:\n    pass",
        "examples": [
            {"input": "s = \"abc\"", "output": "3", "explanation": "Three single-char palindromes."},
            {"input": "s = \"aaa\"", "output": "6", "explanation": "a,a,a,aa,aa,aaa."},
            {"input": "s = \"aba\"", "output": "4", "explanation": "a,b,a,aba."},
        ],
        "testCases": [
            {"function": "countPalindromicSubstrings", "input": "\"abc\"", "expectedOutput": "3"},
            {"function": "countPalindromicSubstrings", "input": "\"aaa\"", "expectedOutput": "6"},
            {"function": "countPalindromicSubstrings", "input": "\"aba\"", "expectedOutput": "4"},
            {"function": "countPalindromicSubstrings", "input": "\"a\"", "expectedOutput": "1"},
            {"function": "countPalindromicSubstrings", "input": "\"aa\"", "expectedOutput": "3"},
            {"function": "countPalindromicSubstrings", "input": "\"abba\"", "expectedOutput": "6"},
            {"function": "countPalindromicSubstrings", "input": "\"racecar\"", "expectedOutput": "10"},
            {"function": "countPalindromicSubstrings", "input": "\"ab\"", "expectedOutput": "2"},
            {"function": "countPalindromicSubstrings", "input": "\"abcd\"", "expectedOutput": "4"},
            {"function": "countPalindromicSubstrings", "input": "\"aaaa\"", "expectedOutput": "10"},
        ],
        "tags": ["string", "dynamic-programming", "two-pointers"],
    },
    {
        "slug": "daily-temperatures-wait",
        "title": "Daily Temperatures Wait",
        "difficulty": "medium",
        "description": (
            "A weather app tells users how many days they must wait until a warmer day. "
            "Given an array of daily temperatures, return an array where answer[i] is the number of days "
            "until a temperature warmer than temperatures[i]. "
            "If no warmer day ever arrives, answer[i] = 0. Use a monotonic stack."
        ),
        "starterCode": "def dailyTemperatures(temperatures: list) -> list:\n    pass",
        "examples": [
            {"input": "temperatures = [73,74,75,71,69,72,76,73]", "output": "[1,1,4,2,1,1,0,0]", "explanation": "Days until warmer."},
            {"input": "temperatures = [30,40,50,60]", "output": "[1,1,1,0]", "explanation": "Always warmer next day."},
            {"input": "temperatures = [30,60,90]", "output": "[1,1,0]", "explanation": "Strictly increasing."},
        ],
        "testCases": [
            {"function": "dailyTemperatures", "input": "[73,74,75,71,69,72,76,73]", "expectedOutput": "[1,1,4,2,1,1,0,0]"},
            {"function": "dailyTemperatures", "input": "[30,40,50,60]", "expectedOutput": "[1,1,1,0]"},
            {"function": "dailyTemperatures", "input": "[30,60,90]", "expectedOutput": "[1,1,0]"},
            {"function": "dailyTemperatures", "input": "[90,60,30]", "expectedOutput": "[0,0,0]"},
            {"function": "dailyTemperatures", "input": "[70,70,70]", "expectedOutput": "[0,0,0]"},
            {"function": "dailyTemperatures", "input": "[55,38,53,81,61,93,97,32,43,78]", "expectedOutput": "[3,1,1,2,1,1,0,2,1,0]"},
            {"function": "dailyTemperatures", "input": "[89,62,70,58,47,47,46,76,100,70]", "expectedOutput": "[8,1,5,4,3,2,1,1,0,0]"},
            {"function": "dailyTemperatures", "input": "[34,80,80]", "expectedOutput": "[1,0,0]"},
            {"function": "dailyTemperatures", "input": "[100]", "expectedOutput": "[0]"},
            {"function": "dailyTemperatures", "input": "[60,80,70,90]", "expectedOutput": "[1,2,1,0]"},
        ],
        "tags": ["stack", "monotonic-stack", "array"],
    },
    {
        "slug": "evaluate-rpn",
        "title": "Evaluate Reverse Polish Notation",
        "difficulty": "medium",
        "description": (
            "A calculator engine processes expressions in Reverse Polish Notation (postfix). "
            "Operands come before their operators. "
            "Given a list of tokens representing a valid arithmetic expression in RPN, "
            "evaluate it and return the integer result. "
            "Operators are +, -, *, and / (integer division truncating toward zero)."
        ),
        "starterCode": "def evaluateRPN(tokens: list) -> int:\n    pass",
        "examples": [
            {"input": "tokens = [\"2\",\"1\",\"+\",\"3\",\"*\"]", "output": "9", "explanation": "(2+1)*3=9."},
            {"input": "tokens = [\"4\",\"13\",\"5\",\"/\",\"+\"]", "output": "6", "explanation": "4+(13/5)=6."},
            {"input": "tokens = [\"10\",\"6\",\"9\",\"3\",\"+\",\"-11\",\"*\",\"/\",\"*\",\"17\",\"+\",\"5\",\"+\"]", "output": "22", "explanation": "Complex RPN expression."},
        ],
        "testCases": [
            {"function": "evaluateRPN", "input": "[\"2\",\"1\",\"+\",\"3\",\"*\"]", "expectedOutput": "9"},
            {"function": "evaluateRPN", "input": "[\"4\",\"13\",\"5\",\"/\",\"+\"]", "expectedOutput": "6"},
            {"function": "evaluateRPN", "input": "[\"10\",\"6\",\"9\",\"3\",\"+\",\"-11\",\"*\",\"/\",\"*\",\"17\",\"+\",\"5\",\"+\"]", "expectedOutput": "22"},
            {"function": "evaluateRPN", "input": "[\"3\",\"4\",\"+\"]", "expectedOutput": "7"},
            {"function": "evaluateRPN", "input": "[\"5\",\"1\",\"2\",\"+\",\"4\",\"*\",\"+\",\"3\",\"-\"]", "expectedOutput": "14"},
            {"function": "evaluateRPN", "input": "[\"2\",\"3\",\"-\"]", "expectedOutput": "-1"},
            {"function": "evaluateRPN", "input": "[\"2\"]", "expectedOutput": "2"},
            {"function": "evaluateRPN", "input": "[\"3\",\"3\",\"*\",\"3\",\"/\"]", "expectedOutput": "3"},
            {"function": "evaluateRPN", "input": "[\"0\",\"3\",\"/\"]", "expectedOutput": "0"},
            {"function": "evaluateRPN", "input": "[\"-3\",\"4\",\"*\"]", "expectedOutput": "-12"},
        ],
        "tags": ["stack", "math", "array"],
    },
    {
        "slug": "find-peak-element",
        "title": "Find Peak Element",
        "difficulty": "medium",
        "description": (
            "A seismology instrument detects a peak reading — a value greater than both its neighbours. "
            "Given an integer array where nums[-1] = nums[n] = -∞, "
            "find any peak element and return its index. "
            "Your solution must run in O(log n) using binary search."
        ),
        "starterCode": "def findPeakElement(nums: list) -> int:\n    pass",
        "examples": [
            {"input": "nums = [1,2,3,1]", "output": "2", "explanation": "3 is a peak at index 2."},
            {"input": "nums = [1,2,1,3,5,6,4]", "output": "5", "explanation": "6 is a peak at index 5."},
            {"input": "nums = [1]", "output": "0", "explanation": "Single element is a peak."},
        ],
        "testCases": [
            {"function": "findPeakElement", "input": "[1,2,3,1]", "expectedOutput": "2"},
            {"function": "findPeakElement", "input": "[1,2,1,3,5,6,4]", "expectedOutput": "5"},
            {"function": "findPeakElement", "input": "[1]", "expectedOutput": "0"},
            {"function": "findPeakElement", "input": "[1,2]", "expectedOutput": "1"},
            {"function": "findPeakElement", "input": "[2,1]", "expectedOutput": "0"},
            {"function": "findPeakElement", "input": "[1,2,3]", "expectedOutput": "2"},
            {"function": "findPeakElement", "input": "[3,2,1]", "expectedOutput": "0"},
            {"function": "findPeakElement", "input": "[1,3,2,4,3]", "expectedOutput": "1 or 3"},
            {"function": "findPeakElement", "input": "[1,2,1,2,1]", "expectedOutput": "1 or 3"},
            {"function": "findPeakElement", "input": "[5,4,3,2,1]", "expectedOutput": "0"},
        ],
        "tags": ["binary-search", "array"],
    },
    {
        "slug": "single-number-xor",
        "title": "Single Number XOR",
        "difficulty": "easy",
        "description": (
            "A data recovery tool scans a corrupted array. Every value appears exactly twice except one. "
            "Find the unique number that appears only once. "
            "Your solution must use O(1) extra space and O(n) time — use XOR bit manipulation. "
            "No hash tables or sorting allowed."
        ),
        "starterCode": "def singleNumber(nums: list) -> int:\n    pass",
        "examples": [
            {"input": "nums = [2,2,1]", "output": "1", "explanation": "1 appears once."},
            {"input": "nums = [4,1,2,1,2]", "output": "4", "explanation": "4 appears once."},
            {"input": "nums = [1]", "output": "1", "explanation": "Only one element."},
        ],
        "testCases": [
            {"function": "singleNumber", "input": "[2,2,1]", "expectedOutput": "1"},
            {"function": "singleNumber", "input": "[4,1,2,1,2]", "expectedOutput": "4"},
            {"function": "singleNumber", "input": "[1]", "expectedOutput": "1"},
            {"function": "singleNumber", "input": "[0,1,0]", "expectedOutput": "1"},
            {"function": "singleNumber", "input": "[3,3,5]", "expectedOutput": "5"},
            {"function": "singleNumber", "input": "[-1,-1,2]", "expectedOutput": "2"},
            {"function": "singleNumber", "input": "[100,1,100]", "expectedOutput": "1"},
            {"function": "singleNumber", "input": "[7,3,5,3,7]", "expectedOutput": "5"},
            {"function": "singleNumber", "input": "[1,0,1]", "expectedOutput": "0"},
            {"function": "singleNumber", "input": "[17,17,42]", "expectedOutput": "42"},
        ],
        "tags": ["bit-manipulation", "array"],
    },
    {
        "slug": "sort-colors-flag",
        "title": "Sort Colors Flag",
        "difficulty": "medium",
        "description": (
            "A painter sorts tiles into three colors: red (0), white (1), and blue (2). "
            "Given an array of 0s, 1s, and 2s, sort it in-place so all 0s come first, then 1s, then 2s. "
            "You must not use the built-in sort function. "
            "Use the Dutch National Flag algorithm for O(n) single-pass sorting."
        ),
        "starterCode": "def sortColors(nums: list) -> None:\n    pass",
        "examples": [
            {"input": "nums = [2,0,2,1,1,0]", "output": "[0,0,1,1,2,2]", "explanation": "Sorted into 3 groups."},
            {"input": "nums = [2,0,1]", "output": "[0,1,2]", "explanation": "One of each."},
            {"input": "nums = [0]", "output": "[0]", "explanation": "Single element."},
        ],
        "testCases": [
            {"function": "sortColors", "input": "[2,0,2,1,1,0]", "expectedOutput": "[0,0,1,1,2,2]"},
            {"function": "sortColors", "input": "[2,0,1]", "expectedOutput": "[0,1,2]"},
            {"function": "sortColors", "input": "[0]", "expectedOutput": "[0]"},
            {"function": "sortColors", "input": "[1]", "expectedOutput": "[1]"},
            {"function": "sortColors", "input": "[2]", "expectedOutput": "[2]"},
            {"function": "sortColors", "input": "[0,0,0]", "expectedOutput": "[0,0,0]"},
            {"function": "sortColors", "input": "[2,2,2]", "expectedOutput": "[2,2,2]"},
            {"function": "sortColors", "input": "[1,0,2]", "expectedOutput": "[0,1,2]"},
            {"function": "sortColors", "input": "[2,1,0,1,2,0]", "expectedOutput": "[0,0,1,1,2,2]"},
            {"function": "sortColors", "input": "[0,1,2,0,1,2]", "expectedOutput": "[0,0,1,1,2,2]"},
        ],
        "tags": ["array", "two-pointers", "sorting"],
    },
    {
        "slug": "max-area-container",
        "title": "Maximum Area Container",
        "difficulty": "medium",
        "description": (
            "An engineer designs water tanks using vertical walls of varying heights. "
            "Given an integer array height where height[i] is the height of the i-th wall, "
            "find two walls that together with the x-axis form a container holding the most water. "
            "Return the maximum water volume. Use the two-pointer approach."
        ),
        "starterCode": "def maxAreaContainer(height: list) -> int:\n    pass",
        "examples": [
            {"input": "height = [1,8,6,2,5,4,8,3,7]", "output": "49", "explanation": "Walls at index 1 and 8, height=7, width=7."},
            {"input": "height = [1,1]", "output": "1", "explanation": "Width 1, height 1."},
            {"input": "height = [4,3,2,1,4]", "output": "16", "explanation": "Walls at 0 and 4, height=4, width=4."},
        ],
        "testCases": [
            {"function": "maxAreaContainer", "input": "[1,8,6,2,5,4,8,3,7]", "expectedOutput": "49"},
            {"function": "maxAreaContainer", "input": "[1,1]", "expectedOutput": "1"},
            {"function": "maxAreaContainer", "input": "[4,3,2,1,4]", "expectedOutput": "16"},
            {"function": "maxAreaContainer", "input": "[1,2,1]", "expectedOutput": "2"},
            {"function": "maxAreaContainer", "input": "[1,2,3,4,5]", "expectedOutput": "6"},
            {"function": "maxAreaContainer", "input": "[5,4,3,2,1]", "expectedOutput": "6"},
            {"function": "maxAreaContainer", "input": "[2,3,4,5,18,17,6]", "expectedOutput": "17"},
            {"function": "maxAreaContainer", "input": "[1,3,2,5,25,24,5]", "expectedOutput": "24"},
            {"function": "maxAreaContainer", "input": "[3,1,2,4,0,1,3,2]", "expectedOutput": "18"},
            {"function": "maxAreaContainer", "input": "[1,2]", "expectedOutput": "1"},
        ],
        "tags": ["array", "two-pointers", "greedy"],
    },
    {
        "slug": "kth-smallest-bst",
        "title": "Kth Smallest in BST",
        "difficulty": "easy",
        "description": (
            "A leaderboard stores scores in a Binary Search Tree to allow fast ranking lookups. "
            "Given the root of a BST and an integer k, return the k-th smallest value in the tree. "
            "In-order traversal of a BST yields sorted values — leverage this property."
        ),
        "starterCode": "class TreeNode:\n    def __init__(self, val=0, left=None, right=None):\n        self.val = val\n        self.left = left\n        self.right = right\n\ndef kthSmallestBST(root, k: int) -> int:\n    pass",
        "examples": [
            {"input": "root = [3,1,4,null,2], k = 1", "output": "1", "explanation": "1 is the smallest."},
            {"input": "root = [5,3,6,2,4,null,null,1], k = 3", "output": "3", "explanation": "3rd smallest is 3."},
            {"input": "root = [1], k = 1", "output": "1", "explanation": "Single node."},
        ],
        "testCases": [
            {"function": "kthSmallestBST", "input": "[3,1,4,null,2], 1", "expectedOutput": "1"},
            {"function": "kthSmallestBST", "input": "[5,3,6,2,4,null,null,1], 3", "expectedOutput": "3"},
            {"function": "kthSmallestBST", "input": "[1], 1", "expectedOutput": "1"},
            {"function": "kthSmallestBST", "input": "[2,1,3], 2", "expectedOutput": "2"},
            {"function": "kthSmallestBST", "input": "[5,3,7,2,4,6,8], 4", "expectedOutput": "5"},
            {"function": "kthSmallestBST", "input": "[5,3,7,2,4,6,8], 1", "expectedOutput": "2"},
            {"function": "kthSmallestBST", "input": "[5,3,7,2,4,6,8], 7", "expectedOutput": "8"},
            {"function": "kthSmallestBST", "input": "[10,5,15,3,7], 2", "expectedOutput": "5"},
            {"function": "kthSmallestBST", "input": "[10,5,15,3,7], 4", "expectedOutput": "10"},
            {"function": "kthSmallestBST", "input": "[3,1,4,null,2], 3", "expectedOutput": "3"},
        ],
        "tags": ["tree", "binary-search-tree", "dfs", "inorder"],
    },
    {
        "slug": "product-except-self",
        "title": "Product of Array Except Self",
        "difficulty": "medium",
        "description": (
            "A signal processor needs each position's value replaced by the product of all other positions. "
            "Given an integer array nums, return an array answer where answer[i] equals the product of all elements "
            "except nums[i]. "
            "You must not use division and must run in O(n) time with O(1) extra space (ignoring output array)."
        ),
        "starterCode": "def productExceptSelf(nums: list) -> list:\n    pass",
        "examples": [
            {"input": "nums = [1,2,3,4]", "output": "[24,12,8,6]", "explanation": "Each element is product of all others."},
            {"input": "nums = [-1,1,0,-3,3]", "output": "[0,0,9,0,0]", "explanation": "Zero causes most products to be 0."},
            {"input": "nums = [2,3]", "output": "[3,2]", "explanation": "Each takes the other."},
        ],
        "testCases": [
            {"function": "productExceptSelf", "input": "[1,2,3,4]", "expectedOutput": "[24,12,8,6]"},
            {"function": "productExceptSelf", "input": "[-1,1,0,-3,3]", "expectedOutput": "[0,0,9,0,0]"},
            {"function": "productExceptSelf", "input": "[2,3]", "expectedOutput": "[3,2]"},
            {"function": "productExceptSelf", "input": "[1,1,1,1]", "expectedOutput": "[1,1,1,1]"},
            {"function": "productExceptSelf", "input": "[0,0]", "expectedOutput": "[0,0]"},
            {"function": "productExceptSelf", "input": "[1,0]", "expectedOutput": "[0,1]"},
            {"function": "productExceptSelf", "input": "[2,2,2]", "expectedOutput": "[4,4,4]"},
            {"function": "productExceptSelf", "input": "[5,2,3,4]", "expectedOutput": "[24,60,40,30]"},
            {"function": "productExceptSelf", "input": "[-2,3,-4]", "expectedOutput": "[-12,8,-6]"},
            {"function": "productExceptSelf", "input": "[1,2,3,4,5]", "expectedOutput": "[120,60,40,30,24]"},
        ],
        "tags": ["array", "prefix-sum"],
    },
    {
        "slug": "longest-palindromic-substring",
        "title": "Longest Palindromic Substring",
        "difficulty": "medium",
        "description": (
            "A DNA sequencing tool searches for the longest palindromic segment within a genetic string. "
            "Given a string s, return the longest substring that reads the same forwards and backwards. "
            "If multiple answers exist with the same length, return any one of them. "
            "Use the expand-around-center technique."
        ),
        "starterCode": "def longestPalindromicSubstring(s: str) -> str:\n    pass",
        "examples": [
            {"input": "s = \"babad\"", "output": "\"bab\"", "explanation": "bab is a palindrome of length 3."},
            {"input": "s = \"cbbd\"", "output": "\"bb\"", "explanation": "bb is the longest."},
            {"input": "s = \"a\"", "output": "\"a\"", "explanation": "Single character."},
        ],
        "testCases": [
            {"function": "longestPalindromicSubstring", "input": "\"babad\"", "expectedOutput": "\"bab\" or \"aba\""},
            {"function": "longestPalindromicSubstring", "input": "\"cbbd\"", "expectedOutput": "\"bb\""},
            {"function": "longestPalindromicSubstring", "input": "\"a\"", "expectedOutput": "\"a\""},
            {"function": "longestPalindromicSubstring", "input": "\"ac\"", "expectedOutput": "\"a\" or \"c\""},
            {"function": "longestPalindromicSubstring", "input": "\"racecar\"", "expectedOutput": "\"racecar\""},
            {"function": "longestPalindromicSubstring", "input": "\"abba\"", "expectedOutput": "\"abba\""},
            {"function": "longestPalindromicSubstring", "input": "\"aacabdkacaa\"", "expectedOutput": "\"aca\""},
            {"function": "longestPalindromicSubstring", "input": "\"xyzyx\"", "expectedOutput": "\"xyzyx\""},
            {"function": "longestPalindromicSubstring", "input": "\"aaaa\"", "expectedOutput": "\"aaaa\""},
            {"function": "longestPalindromicSubstring", "input": "\"abcba\"", "expectedOutput": "\"abcba\""},
        ],
        "tags": ["string", "dynamic-programming", "two-pointers"],
    },
    {
        "slug": "reverse-words-sentence",
        "title": "Reverse Words in a Sentence",
        "difficulty": "medium",
        "description": (
            "A text formatter reverses word order in a sentence. "
            "Given a string s containing words separated by spaces, "
            "return the string with word order reversed. "
            "Leading/trailing spaces must be removed, and multiple spaces between words "
            "reduced to a single space."
        ),
        "starterCode": "def reverseWords(s: str) -> str:\n    pass",
        "examples": [
            {"input": "s = \"the sky is blue\"", "output": "\"blue is sky the\"", "explanation": "Words reversed."},
            {"input": "s = \"  hello world  \"", "output": "\"world hello\"", "explanation": "Extra spaces trimmed."},
            {"input": "s = \"a good   example\"", "output": "\"example good a\"", "explanation": "Multiple spaces reduced."},
        ],
        "testCases": [
            {"function": "reverseWords", "input": "\"the sky is blue\"", "expectedOutput": "\"blue is sky the\""},
            {"function": "reverseWords", "input": "\"  hello world  \"", "expectedOutput": "\"world hello\""},
            {"function": "reverseWords", "input": "\"a good   example\"", "expectedOutput": "\"example good a\""},
            {"function": "reverseWords", "input": "\"a\"", "expectedOutput": "\"a\""},
            {"function": "reverseWords", "input": "\"Alice does not even like Bob\"", "expectedOutput": "\"Bob like even not does Alice\""},
            {"function": "reverseWords", "input": "\"  spaces  \"", "expectedOutput": "\"spaces\""},
            {"function": "reverseWords", "input": "\"one\"", "expectedOutput": "\"one\""},
            {"function": "reverseWords", "input": "\"two words\"", "expectedOutput": "\"words two\""},
            {"function": "reverseWords", "input": "\"  multiple   spaces  between  \"", "expectedOutput": "\"between spaces multiple\""},
            {"function": "reverseWords", "input": "\"end with space \"", "expectedOutput": "\"space with end\""},
        ],
        "tags": ["string", "two-pointers"],
    },
    {
        "slug": "task-scheduler",
        "title": "Task Scheduler",
        "difficulty": "medium",
        "description": (
            "A CPU scheduler processes tasks (labeled A-Z). After running a task, the CPU must wait n intervals "
            "before running the same task again (it can idle or run other tasks during the cooldown). "
            "Given a list of tasks and cooldown n, return the minimum total intervals needed to finish all tasks."
        ),
        "starterCode": "def taskScheduler(tasks: list, n: int) -> int:\n    pass",
        "examples": [
            {"input": "tasks = [\"A\",\"A\",\"A\",\"B\",\"B\",\"B\"], n = 2", "output": "8", "explanation": "A->B->idle->A->B->idle->A->B."},
            {"input": "tasks = [\"A\",\"A\",\"A\",\"B\",\"B\",\"B\"], n = 0", "output": "6", "explanation": "No cooldown, run all 6."},
            {"input": "tasks = [\"A\",\"A\",\"A\",\"A\",\"A\",\"A\",\"B\",\"C\",\"D\",\"E\",\"F\",\"G\"], n = 2", "output": "16", "explanation": "A is the bottleneck."},
        ],
        "testCases": [
            {"function": "taskScheduler", "input": "[\"A\",\"A\",\"A\",\"B\",\"B\",\"B\"], 2", "expectedOutput": "8"},
            {"function": "taskScheduler", "input": "[\"A\",\"A\",\"A\",\"B\",\"B\",\"B\"], 0", "expectedOutput": "6"},
            {"function": "taskScheduler", "input": "[\"A\",\"A\",\"A\",\"A\",\"A\",\"A\",\"B\",\"C\",\"D\",\"E\",\"F\",\"G\"], 2", "expectedOutput": "16"},
            {"function": "taskScheduler", "input": "[\"A\"], 0", "expectedOutput": "1"},
            {"function": "taskScheduler", "input": "[\"A\",\"A\"], 2", "expectedOutput": "4"},
            {"function": "taskScheduler", "input": "[\"A\",\"B\",\"C\"], 1", "expectedOutput": "3"},
            {"function": "taskScheduler", "input": "[\"A\",\"A\",\"B\",\"B\"], 2", "expectedOutput": "7"},
            {"function": "taskScheduler", "input": "[\"A\",\"A\",\"A\",\"B\",\"B\",\"B\",\"C\",\"C\",\"C\"], 2", "expectedOutput": "9"},
            {"function": "taskScheduler", "input": "[\"A\",\"B\",\"A\",\"B\",\"A\",\"B\"], 3", "expectedOutput": "14"},
            {"function": "taskScheduler", "input": "[\"A\",\"A\",\"A\",\"B\",\"B\",\"B\",\"C\",\"C\"], 2", "expectedOutput": "8"},
        ],
        "tags": ["heap", "greedy", "hash-table", "sorting"],
    },
    {
        "slug": "merge-intervals",
        "title": "Merge Intervals",
        "difficulty": "medium",
        "description": (
            "A calendar app merges overlapping time slots into consolidated blocks. "
            "Given a list of intervals [start, end], merge all overlapping intervals "
            "and return the resulting non-overlapping intervals sorted by start time."
        ),
        "starterCode": "def mergeIntervals(intervals: list) -> list:\n    pass",
        "examples": [
            {"input": "intervals = [[1,3],[2,6],[8,10],[15,18]]", "output": "[[1,6],[8,10],[15,18]]", "explanation": "[1,3] and [2,6] overlap, merged to [1,6]."},
            {"input": "intervals = [[1,4],[4,5]]", "output": "[[1,5]]", "explanation": "Touch at 4, merged."},
            {"input": "intervals = [[1,4],[2,3]]", "output": "[[1,4]]", "explanation": "One contains the other."},
        ],
        "testCases": [
            {"function": "mergeIntervals", "input": "[[1,3],[2,6],[8,10],[15,18]]", "expectedOutput": "[[1,6],[8,10],[15,18]]"},
            {"function": "mergeIntervals", "input": "[[1,4],[4,5]]", "expectedOutput": "[[1,5]]"},
            {"function": "mergeIntervals", "input": "[[1,4],[2,3]]", "expectedOutput": "[[1,4]]"},
            {"function": "mergeIntervals", "input": "[[1,2]]", "expectedOutput": "[[1,2]]"},
            {"function": "mergeIntervals", "input": "[[1,2],[3,4]]", "expectedOutput": "[[1,2],[3,4]]"},
            {"function": "mergeIntervals", "input": "[[1,10],[2,3],[4,5],[6,7]]", "expectedOutput": "[[1,10]]"},
            {"function": "mergeIntervals", "input": "[[2,3],[2,2],[3,3],[1,3],[5,7],[2,2],[4,6]]", "expectedOutput": "[[1,3],[4,7]]"},
            {"function": "mergeIntervals", "input": "[[1,4],[0,4]]", "expectedOutput": "[[0,4]]"},
            {"function": "mergeIntervals", "input": "[[1,4],[0,0]]", "expectedOutput": "[[0,0],[1,4]]"},
            {"function": "mergeIntervals", "input": "[[0,0],[1,18],[2,3]]", "expectedOutput": "[[0,0],[1,18]]"},
        ],
        "tags": ["array", "sorting", "greedy"],
    },
    {
        "slug": "inorder-successor-bst",
        "title": "Inorder Successor in BST",
        "difficulty": "medium",
        "description": (
            "A leaderboard ranking system finds the next player above a given player's score in a BST. "
            "Given the root of a BST and a node p, return the in-order successor of p — "
            "the node with the smallest key greater than p.val. "
            "Return None if no such node exists."
        ),
        "starterCode": "class TreeNode:\n    def __init__(self, val=0, left=None, right=None):\n        self.val = val\n        self.left = left\n        self.right = right\n\ndef inorderSuccessor(root, p):\n    pass",
        "examples": [
            {"input": "root = [2,1,3], p = 1", "output": "2", "explanation": "Inorder is [1,2,3], successor of 1 is 2."},
            {"input": "root = [5,3,6,2,4], p = 6", "output": "None", "explanation": "6 is the maximum."},
            {"input": "root = [5,3,6,2,4], p = 4", "output": "5", "explanation": "Successor of 4 is 5."},
        ],
        "testCases": [
            {"function": "inorderSuccessor", "input": "[2,1,3], 1", "expectedOutput": "2"},
            {"function": "inorderSuccessor", "input": "[5,3,6,2,4], 6", "expectedOutput": "None"},
            {"function": "inorderSuccessor", "input": "[5,3,6,2,4], 4", "expectedOutput": "5"},
            {"function": "inorderSuccessor", "input": "[5,3,6,2,4], 3", "expectedOutput": "4"},
            {"function": "inorderSuccessor", "input": "[5,3,6,2,4], 2", "expectedOutput": "3"},
            {"function": "inorderSuccessor", "input": "[5,3,6,2,4], 5", "expectedOutput": "6"},
            {"function": "inorderSuccessor", "input": "[1], 1", "expectedOutput": "None"},
            {"function": "inorderSuccessor", "input": "[2,1,3], 2", "expectedOutput": "3"},
            {"function": "inorderSuccessor", "input": "[10,5,15,3,7,12,20], 7", "expectedOutput": "10"},
            {"function": "inorderSuccessor", "input": "[10,5,15,3,7,12,20], 15", "expectedOutput": "20"},
        ],
        "tags": ["tree", "binary-search-tree", "dfs"],
    },
    {
        "slug": "max-depth-n-ary-tree",
        "title": "Max Depth of N-ary Tree",
        "difficulty": "easy",
        "description": (
            "An organizational chart is stored as an N-ary tree where each node can have any number of children. "
            "Find the maximum depth — the number of nodes along the longest path from root to the deepest leaf. "
            "Given the root, return this depth."
        ),
        "starterCode": "class Node:\n    def __init__(self, val=None, children=None):\n        self.val = val\n        self.children = children if children else []\n\ndef maxDepthNAry(root) -> int:\n    pass",
        "examples": [
            {"input": "root = [1,null,3,2,4,null,5,6]", "output": "3", "explanation": "Deepest path has 3 nodes."},
            {"input": "root = [1,null,2,3,4,5,null,null,6,7,null,8,null,9,10,null,null,11,null,12,null,13,null,null,14]", "output": "5", "explanation": "Complex tree depth 5."},
            {"input": "root = []", "output": "0", "explanation": "Empty tree."},
        ],
        "testCases": [
            {"function": "maxDepthNAry", "input": "[1,null,3,2,4,null,5,6]", "expectedOutput": "3"},
            {"function": "maxDepthNAry", "input": "[]", "expectedOutput": "0"},
            {"function": "maxDepthNAry", "input": "[1]", "expectedOutput": "1"},
            {"function": "maxDepthNAry", "input": "[1,null,2]", "expectedOutput": "2"},
            {"function": "maxDepthNAry", "input": "[1,null,2,3]", "expectedOutput": "2"},
            {"function": "maxDepthNAry", "input": "[1,null,2,null,3]", "expectedOutput": "3"},
            {"function": "maxDepthNAry", "input": "[1,null,2,3,4]", "expectedOutput": "2"},
            {"function": "maxDepthNAry", "input": "[1,null,2,3,4,null,5,6]", "expectedOutput": "3"},
            {"function": "maxDepthNAry", "input": "[1,null,null]", "expectedOutput": "1"},
            {"function": "maxDepthNAry", "input": "[1,null,2,null,3,null,4]", "expectedOutput": "4"},
        ],
        "tags": ["tree", "dfs", "bfs"],
    },
]


def post_problem(problem):
    payload = {**problem, "ingestKey": INGEST_KEY}
    try:
        response = requests.post(BASE_URL, json=payload, timeout=15)
        return response.status_code, response.text
    except Exception as e:
        return None, str(e)


def main():
    print(f"Posting {len(problems)} problems to {BASE_URL}\n")
    success, failed = 0, 0

    for i, problem in enumerate(problems, 1):
        status, body = post_problem(problem)
        if status and 200 <= status < 300:
            print(f"[{i:3d}/100] ✅  {problem['title']} ({problem['difficulty']})")
            success += 1
        else:
            print(f"[{i:3d}/100] ❌  {problem['title']} — {status}: {body[:120]}")
            failed += 1

    print(f"\n{'='*50}")
    print(f"Done. {success} succeeded, {failed} failed.")


if __name__ == "__main__":
    main()
