import requests

BASE_URL = "https://pypycode.com/api/problems/public-ingest"
#BASE_URL = "http://localhost:81/api/problems/public-ingest"
INGEST_KEY = "EMDgUmg7tzsgdf5r3eFd"

problems = [
    # ─── 1 ───
    {
        "slug": "two-sum-hash",
        "title": "Two Sum",
        "difficulty": "easy",
        "description": (
            "Given a list of integers and a target value, find the two numbers that add up to the target "
            "and return their indices. Each input has exactly one valid answer, and you cannot use the "
            "same element twice. Return the answer in any order."
        ),
        "starterCode": "def twoSum(nums: list, target: int) -> list:\n    pass",
        "examples": [
            {"input": "nums = [2,7,11,15], target = 9", "output": "[0,1]", "explanation": "2+7=9"},
            {"input": "nums = [3,2,4], target = 6", "output": "[1,2]", "explanation": "2+4=6"},
            {"input": "nums = [3,3], target = 6", "output": "[0,1]", "explanation": "3+3=6"},
        ],
        "testCases": [
            {"function": "twoSum", "input": "[2,7,11,15], 9", "expectedOutput": "[0,1]"},
            {"function": "twoSum", "input": "[3,2,4], 6", "expectedOutput": "[1,2]"},
            {"function": "twoSum", "input": "[3,3], 6", "expectedOutput": "[0,1]"},
            {"function": "twoSum", "input": "[1,2,3,4,5], 9", "expectedOutput": "[3,4]"},
            {"function": "twoSum", "input": "[-1,-2,-3,-4,-5], -8", "expectedOutput": "[2,4]"},
            {"function": "twoSum", "input": "[0,4,3,0], 0", "expectedOutput": "[0,3]"},
            {"function": "twoSum", "input": "[1,5,3,7], 8", "expectedOutput": "[1,3]"},
            {"function": "twoSum", "input": "[10,20,30,40], 50", "expectedOutput": "[1,2]"},
            {"function": "twoSum", "input": "[2,5,5,11], 10", "expectedOutput": "[1,2]"},
            {"function": "twoSum", "input": "[100,1,99], 200", "expectedOutput": "[0,2]"},
        ],
        "tags": ["array", "hash-table"],
    },
    # ─── 2 ───
    {
        "slug": "fizzbuzz-classic",
        "title": "FizzBuzz",
        "difficulty": "easy",
        "description": (
            "Print numbers from 1 to n, but for multiples of 3 print 'Fizz', "
            "for multiples of 5 print 'Buzz', and for multiples of both print 'FizzBuzz'. "
            "Return the result as a list of strings."
        ),
        "starterCode": "def fizzBuzz(n: int) -> list:\n    pass",
        "examples": [
            {"input": "n = 3", "output": "[\"1\",\"2\",\"Fizz\"]", "explanation": "3 is multiple of 3."},
            {"input": "n = 5", "output": "[\"1\",\"2\",\"Fizz\",\"4\",\"Buzz\"]", "explanation": "5 is multiple of 5."},
            {"input": "n = 15", "output": "last element is FizzBuzz", "explanation": "15 is multiple of both."},
        ],
        "testCases": [
            {"function": "fizzBuzz", "input": "1", "expectedOutput": "[\"1\"]"},
            {"function": "fizzBuzz", "input": "3", "expectedOutput": "[\"1\",\"2\",\"Fizz\"]"},
            {"function": "fizzBuzz", "input": "5", "expectedOutput": "[\"1\",\"2\",\"Fizz\",\"4\",\"Buzz\"]"},
            {"function": "fizzBuzz", "input": "15", "expectedOutput": "last is FizzBuzz"},
            {"function": "fizzBuzz", "input": "6", "expectedOutput": "contains Fizz at index 2 and 5"},
            {"function": "fizzBuzz", "input": "10", "expectedOutput": "contains Buzz at index 4 and 9"},
            {"function": "fizzBuzz", "input": "2", "expectedOutput": "[\"1\",\"2\"]"},
            {"function": "fizzBuzz", "input": "30", "expectedOutput": "index 29 is FizzBuzz"},
            {"function": "fizzBuzz", "input": "4", "expectedOutput": "[\"1\",\"2\",\"Fizz\",\"4\"]"},
            {"function": "fizzBuzz", "input": "20", "expectedOutput": "length 20"},
        ],
        "tags": ["math", "string", "simulation"],
    },
    # ─── 3 ───
    {
        "slug": "factorial-recursive",
        "title": "Factorial",
        "difficulty": "easy",
        "description": (
            "Calculate the factorial of a non-negative integer n (written n!). "
            "The factorial is the product of all positive integers up to n. "
            "By definition, 0! = 1. Implement both a recursive and iterative version — "
            "return the result."
        ),
        "starterCode": "def factorial(n: int) -> int:\n    pass",
        "examples": [
            {"input": "n = 5", "output": "120", "explanation": "5*4*3*2*1=120"},
            {"input": "n = 0", "output": "1", "explanation": "0! is defined as 1"},
            {"input": "n = 1", "output": "1", "explanation": "1! = 1"},
        ],
        "testCases": [
            {"function": "factorial", "input": "0", "expectedOutput": "1"},
            {"function": "factorial", "input": "1", "expectedOutput": "1"},
            {"function": "factorial", "input": "2", "expectedOutput": "2"},
            {"function": "factorial", "input": "3", "expectedOutput": "6"},
            {"function": "factorial", "input": "4", "expectedOutput": "24"},
            {"function": "factorial", "input": "5", "expectedOutput": "120"},
            {"function": "factorial", "input": "6", "expectedOutput": "720"},
            {"function": "factorial", "input": "7", "expectedOutput": "5040"},
            {"function": "factorial", "input": "10", "expectedOutput": "3628800"},
            {"function": "factorial", "input": "12", "expectedOutput": "479001600"},
        ],
        "tags": ["math", "recursion"],
    },
    # ─── 4 ───
    {
        "slug": "fibonacci-sequence",
        "title": "Fibonacci Number",
        "difficulty": "easy",
        "description": (
            "The Fibonacci sequence starts with 0 and 1, and each subsequent number is the sum of the two before it: "
            "0, 1, 1, 2, 3, 5, 8, 13, ... "
            "Given n, return the nth Fibonacci number (0-indexed). "
            "Optimize with memoization or iteration to avoid exponential time."
        ),
        "starterCode": "def fibonacci(n: int) -> int:\n    pass",
        "examples": [
            {"input": "n = 0", "output": "0", "explanation": "F(0)=0"},
            {"input": "n = 1", "output": "1", "explanation": "F(1)=1"},
            {"input": "n = 10", "output": "55", "explanation": "F(10)=55"},
        ],
        "testCases": [
            {"function": "fibonacci", "input": "0", "expectedOutput": "0"},
            {"function": "fibonacci", "input": "1", "expectedOutput": "1"},
            {"function": "fibonacci", "input": "2", "expectedOutput": "1"},
            {"function": "fibonacci", "input": "3", "expectedOutput": "2"},
            {"function": "fibonacci", "input": "4", "expectedOutput": "3"},
            {"function": "fibonacci", "input": "5", "expectedOutput": "5"},
            {"function": "fibonacci", "input": "6", "expectedOutput": "8"},
            {"function": "fibonacci", "input": "7", "expectedOutput": "13"},
            {"function": "fibonacci", "input": "10", "expectedOutput": "55"},
            {"function": "fibonacci", "input": "15", "expectedOutput": "610"},
        ],
        "tags": ["math", "recursion", "dynamic-programming", "memoization"],
    },
    # ─── 5 ───
    {
        "slug": "reverse-string-inplace",
        "title": "Reverse a String",
        "difficulty": "easy",
        "description": (
            "Given a list of characters, reverse them in-place without allocating extra space. "
            "Modify the input array directly and return it. "
            "Use two pointers starting at each end and swap toward the center."
        ),
        "starterCode": "def reverseString(s: list) -> list:\n    pass",
        "examples": [
            {"input": "s = ['h','e','l','l','o']", "output": "['o','l','l','e','h']", "explanation": "Reversed in place."},
            {"input": "s = ['H','a','n','n','a','h']", "output": "['h','a','n','n','a','H']", "explanation": "Reversed in place."},
            {"input": "s = ['a']", "output": "['a']", "explanation": "Single char unchanged."},
        ],
        "testCases": [
            {"function": "reverseString", "input": "['h','e','l','l','o']", "expectedOutput": "['o','l','l','e','h']"},
            {"function": "reverseString", "input": "['H','a','n','n','a','h']", "expectedOutput": "['h','a','n','n','a','H']"},
            {"function": "reverseString", "input": "['a']", "expectedOutput": "['a']"},
            {"function": "reverseString", "input": "['a','b']", "expectedOutput": "['b','a']"},
            {"function": "reverseString", "input": "['1','2','3']", "expectedOutput": "['3','2','1']"},
            {"function": "reverseString", "input": "['a','b','c','d']", "expectedOutput": "['d','c','b','a']"},
            {"function": "reverseString", "input": "['z']", "expectedOutput": "['z']"},
            {"function": "reverseString", "input": "['x','y']", "expectedOutput": "['y','x']"},
            {"function": "reverseString", "input": "['1','2','3','4','5']", "expectedOutput": "['5','4','3','2','1']"},
            {"function": "reverseString", "input": "['a','b','c','d','e','f']", "expectedOutput": "['f','e','d','c','b','a']"},
        ],
        "tags": ["string", "two-pointers", "recursion"],
    },
    # ─── 6 ───
    {
        "slug": "check-prime-number",
        "title": "Check Prime Number",
        "difficulty": "easy",
        "description": (
            "A prime number is a natural number greater than 1 that has no divisors other than 1 and itself. "
            "Given an integer n, return True if n is prime, False otherwise. "
            "Optimize by only checking divisors up to the square root of n."
        ),
        "starterCode": "def isPrime(n: int) -> bool:\n    pass",
        "examples": [
            {"input": "n = 2", "output": "True", "explanation": "Smallest prime."},
            {"input": "n = 1", "output": "False", "explanation": "1 is not prime."},
            {"input": "n = 17", "output": "True", "explanation": "17 has no divisors except 1 and 17."},
        ],
        "testCases": [
            {"function": "isPrime", "input": "2", "expectedOutput": "True"},
            {"function": "isPrime", "input": "1", "expectedOutput": "False"},
            {"function": "isPrime", "input": "0", "expectedOutput": "False"},
            {"function": "isPrime", "input": "3", "expectedOutput": "True"},
            {"function": "isPrime", "input": "4", "expectedOutput": "False"},
            {"function": "isPrime", "input": "17", "expectedOutput": "True"},
            {"function": "isPrime", "input": "25", "expectedOutput": "False"},
            {"function": "isPrime", "input": "97", "expectedOutput": "True"},
            {"function": "isPrime", "input": "100", "expectedOutput": "False"},
            {"function": "isPrime", "input": "101", "expectedOutput": "True"},
        ],
        "tags": ["math"],
    },
    # ─── 7 ───
    {
        "slug": "count-vowels-string",
        "title": "Count Vowels in a String",
        "difficulty": "easy",
        "description": (
            "Given a string, count and return the total number of vowels (a, e, i, o, u) it contains. "
            "Count both uppercase and lowercase vowels. "
            "This is a foundational string scanning problem."
        ),
        "starterCode": "def countVowels(s: str) -> int:\n    pass",
        "examples": [
            {"input": "s = \"hello\"", "output": "2", "explanation": "e and o are vowels."},
            {"input": "s = \"aeiou\"", "output": "5", "explanation": "All characters are vowels."},
            {"input": "s = \"rhythm\"", "output": "0", "explanation": "No vowels."},
        ],
        "testCases": [
            {"function": "countVowels", "input": "\"hello\"", "expectedOutput": "2"},
            {"function": "countVowels", "input": "\"aeiou\"", "expectedOutput": "5"},
            {"function": "countVowels", "input": "\"rhythm\"", "expectedOutput": "0"},
            {"function": "countVowels", "input": "\"AEIOU\"", "expectedOutput": "5"},
            {"function": "countVowels", "input": "\"\"", "expectedOutput": "0"},
            {"function": "countVowels", "input": "\"Python\"", "expectedOutput": "1"},
            {"function": "countVowels", "input": "\"programming\"", "expectedOutput": "3"},
            {"function": "countVowels", "input": "\"AaBbEe\"", "expectedOutput": "4"},
            {"function": "countVowels", "input": "\"xyz\"", "expectedOutput": "0"},
            {"function": "countVowels", "input": "\"education\"", "expectedOutput": "5"},
        ],
        "tags": ["string"],
    },
    # ─── 8 ───
    {
        "slug": "find-max-min-array",
        "title": "Find Max and Min in Array",
        "difficulty": "easy",
        "description": (
            "Given an unsorted list of integers, find and return both the maximum and minimum values "
            "in a single pass without sorting the array. "
            "Return them as a tuple (min, max)."
        ),
        "starterCode": "def findMaxMin(nums: list) -> tuple:\n    pass",
        "examples": [
            {"input": "nums = [3,1,4,1,5,9,2,6]", "output": "(1, 9)", "explanation": "Min is 1, max is 9."},
            {"input": "nums = [-5,-1,-3]", "output": "(-5, -1)", "explanation": "All negative."},
            {"input": "nums = [7]", "output": "(7, 7)", "explanation": "Single element."},
        ],
        "testCases": [
            {"function": "findMaxMin", "input": "[3,1,4,1,5,9,2,6]", "expectedOutput": "(1, 9)"},
            {"function": "findMaxMin", "input": "[-5,-1,-3]", "expectedOutput": "(-5, -1)"},
            {"function": "findMaxMin", "input": "[7]", "expectedOutput": "(7, 7)"},
            {"function": "findMaxMin", "input": "[1,2]", "expectedOutput": "(1, 2)"},
            {"function": "findMaxMin", "input": "[100,0,-100]", "expectedOutput": "(-100, 100)"},
            {"function": "findMaxMin", "input": "[5,5,5]", "expectedOutput": "(5, 5)"},
            {"function": "findMaxMin", "input": "[0]", "expectedOutput": "(0, 0)"},
            {"function": "findMaxMin", "input": "[10,9,8,7,6]", "expectedOutput": "(6, 10)"},
            {"function": "findMaxMin", "input": "[-2,0,2]", "expectedOutput": "(-2, 2)"},
            {"function": "findMaxMin", "input": "[1000,-1000,0]", "expectedOutput": "(-1000, 1000)"},
        ],
        "tags": ["array"],
    },
    # ─── 9 ───
    {
        "slug": "sum-of-digits",
        "title": "Sum of Digits",
        "difficulty": "easy",
        "description": (
            "Given a non-negative integer, compute the sum of its individual digits. "
            "For example, 1234 has digit sum 1+2+3+4=10. "
            "Return the sum. Handle multi-digit results as-is (do not repeatedly sum)."
        ),
        "starterCode": "def sumOfDigits(n: int) -> int:\n    pass",
        "examples": [
            {"input": "n = 1234", "output": "10", "explanation": "1+2+3+4=10"},
            {"input": "n = 0", "output": "0", "explanation": "Single digit 0."},
            {"input": "n = 9999", "output": "36", "explanation": "9*4=36."},
        ],
        "testCases": [
            {"function": "sumOfDigits", "input": "1234", "expectedOutput": "10"},
            {"function": "sumOfDigits", "input": "0", "expectedOutput": "0"},
            {"function": "sumOfDigits", "input": "9999", "expectedOutput": "36"},
            {"function": "sumOfDigits", "input": "1", "expectedOutput": "1"},
            {"function": "sumOfDigits", "input": "10", "expectedOutput": "1"},
            {"function": "sumOfDigits", "input": "99", "expectedOutput": "18"},
            {"function": "sumOfDigits", "input": "123456789", "expectedOutput": "45"},
            {"function": "sumOfDigits", "input": "1000", "expectedOutput": "1"},
            {"function": "sumOfDigits", "input": "55", "expectedOutput": "10"},
            {"function": "sumOfDigits", "input": "100", "expectedOutput": "1"},
        ],
        "tags": ["math"],
    },
    # ─── 10 ───
    {
        "slug": "bubble-sort-basic",
        "title": "Bubble Sort",
        "difficulty": "easy",
        "description": (
            "Implement the bubble sort algorithm from scratch. "
            "Repeatedly step through the list, compare adjacent elements, and swap them if they are in the wrong order. "
            "Continue until no swaps are needed. "
            "Return the sorted array. Do not use built-in sort."
        ),
        "starterCode": "def bubbleSort(nums: list) -> list:\n    pass",
        "examples": [
            {"input": "nums = [5,3,1,4,2]", "output": "[1,2,3,4,5]", "explanation": "Sorted ascending."},
            {"input": "nums = [1]", "output": "[1]", "explanation": "Single element."},
            {"input": "nums = [2,1]", "output": "[1,2]", "explanation": "One swap needed."},
        ],
        "testCases": [
            {"function": "bubbleSort", "input": "[5,3,1,4,2]", "expectedOutput": "[1,2,3,4,5]"},
            {"function": "bubbleSort", "input": "[1]", "expectedOutput": "[1]"},
            {"function": "bubbleSort", "input": "[2,1]", "expectedOutput": "[1,2]"},
            {"function": "bubbleSort", "input": "[1,2,3,4,5]", "expectedOutput": "[1,2,3,4,5]"},
            {"function": "bubbleSort", "input": "[5,4,3,2,1]", "expectedOutput": "[1,2,3,4,5]"},
            {"function": "bubbleSort", "input": "[3,3,3]", "expectedOutput": "[3,3,3]"},
            {"function": "bubbleSort", "input": "[-3,-1,-2]", "expectedOutput": "[-3,-2,-1]"},
            {"function": "bubbleSort", "input": "[10,0,-10]", "expectedOutput": "[-10,0,10]"},
            {"function": "bubbleSort", "input": "[100,50,75,25]", "expectedOutput": "[25,50,75,100]"},
            {"function": "bubbleSort", "input": "[1,3,2,4,3,5]", "expectedOutput": "[1,2,3,3,4,5]"},
        ],
        "tags": ["array", "sorting"],
    },
    # ─── 11 ───
    {
        "slug": "count-duplicates",
        "title": "Count Duplicates",
        "difficulty": "easy",
        "description": (
            "Given a list of integers, find and return a list of all elements that appear more than once. "
            "Each duplicate should appear only once in the output. "
            "Return the duplicates in the order they were first seen."
        ),
        "starterCode": "def countDuplicates(nums: list) -> list:\n    pass",
        "examples": [
            {"input": "nums = [4,3,2,7,8,2,3,1]", "output": "[2,3]", "explanation": "2 and 3 appear twice."},
            {"input": "nums = [1,1,2]", "output": "[1]", "explanation": "Only 1 duplicated."},
            {"input": "nums = [1,2,3]", "output": "[]", "explanation": "No duplicates."},
        ],
        "testCases": [
            {"function": "countDuplicates", "input": "[4,3,2,7,8,2,3,1]", "expectedOutput": "[2,3]"},
            {"function": "countDuplicates", "input": "[1,1,2]", "expectedOutput": "[1]"},
            {"function": "countDuplicates", "input": "[1,2,3]", "expectedOutput": "[]"},
            {"function": "countDuplicates", "input": "[1,1,1,1]", "expectedOutput": "[1]"},
            {"function": "countDuplicates", "input": "[]", "expectedOutput": "[]"},
            {"function": "countDuplicates", "input": "[1,2,1,3,2]", "expectedOutput": "[1,2]"},
            {"function": "countDuplicates", "input": "[5,5,5,3,3,2]", "expectedOutput": "[5,3]"},
            {"function": "countDuplicates", "input": "[10]", "expectedOutput": "[]"},
            {"function": "countDuplicates", "input": "[0,0]", "expectedOutput": "[0]"},
            {"function": "countDuplicates", "input": "[-1,-1,2,3,3]", "expectedOutput": "[-1,3]"},
        ],
        "tags": ["array", "hash-table"],
    },
    # ─── 12 ───
    {
        "slug": "merge-sorted-arrays",
        "title": "Merge Two Sorted Arrays",
        "difficulty": "easy",
        "description": (
            "Given two sorted integer arrays nums1 and nums2, merge them into a single sorted array. "
            "Return the merged result. Do not use built-in sort — use the two-pointer merge technique "
            "for O(m+n) time."
        ),
        "starterCode": "def mergeSortedArrays(nums1: list, nums2: list) -> list:\n    pass",
        "examples": [
            {"input": "nums1 = [1,3,5], nums2 = [2,4,6]", "output": "[1,2,3,4,5,6]", "explanation": "Interleaved in order."},
            {"input": "nums1 = [], nums2 = [1,2,3]", "output": "[1,2,3]", "explanation": "Empty first array."},
            {"input": "nums1 = [1,2,3], nums2 = []", "output": "[1,2,3]", "explanation": "Empty second array."},
        ],
        "testCases": [
            {"function": "mergeSortedArrays", "input": "[1,3,5], [2,4,6]", "expectedOutput": "[1,2,3,4,5,6]"},
            {"function": "mergeSortedArrays", "input": "[], [1,2,3]", "expectedOutput": "[1,2,3]"},
            {"function": "mergeSortedArrays", "input": "[1,2,3], []", "expectedOutput": "[1,2,3]"},
            {"function": "mergeSortedArrays", "input": "[1], [1]", "expectedOutput": "[1,1]"},
            {"function": "mergeSortedArrays", "input": "[1,2], [3,4]", "expectedOutput": "[1,2,3,4]"},
            {"function": "mergeSortedArrays", "input": "[3,4], [1,2]", "expectedOutput": "[1,2,3,4]"},
            {"function": "mergeSortedArrays", "input": "[-3,-1], [-2,0]", "expectedOutput": "[-3,-2,-1,0]"},
            {"function": "mergeSortedArrays", "input": "[1,1,1], [1,1]", "expectedOutput": "[1,1,1,1,1]"},
            {"function": "mergeSortedArrays", "input": "[10,20], [5,15,25]", "expectedOutput": "[5,10,15,20,25]"},
            {"function": "mergeSortedArrays", "input": "[0], [0]", "expectedOutput": "[0,0]"},
        ],
        "tags": ["array", "two-pointers", "sorting"],
    },
    # ─── 13 ───
    {
        "slug": "string-compression",
        "title": "String Compression",
        "difficulty": "easy",
        "description": (
            "Compress a string using run-length encoding: consecutive identical characters are replaced "
            "by the character followed by the count. If the compressed string is not shorter, return the original. "
            "For example, 'aabcccdddd' becomes 'a2b1c3d4'."
        ),
        "starterCode": "def compressString(s: str) -> str:\n    pass",
        "examples": [
            {"input": "s = \"aabcccdddd\"", "output": "\"a2b1c3d4\"", "explanation": "Each run encoded."},
            {"input": "s = \"abc\"", "output": "\"abc\"", "explanation": "Compressed is longer, return original."},
            {"input": "s = \"aaa\"", "output": "\"a3\"", "explanation": "Three a's."},
        ],
        "testCases": [
            {"function": "compressString", "input": "\"aabcccdddd\"", "expectedOutput": "\"a2b1c3d4\""},
            {"function": "compressString", "input": "\"abc\"", "expectedOutput": "\"abc\""},
            {"function": "compressString", "input": "\"aaa\"", "expectedOutput": "\"a3\""},
            {"function": "compressString", "input": "\"a\"", "expectedOutput": "\"a\""},
            {"function": "compressString", "input": "\"aabb\"", "expectedOutput": "\"aabb\""},
            {"function": "compressString", "input": "\"aaabb\"", "expectedOutput": "\"a3b2\""},
            {"function": "compressString", "input": "\"\"", "expectedOutput": "\"\""},
            {"function": "compressString", "input": "\"aaaaaaa\"", "expectedOutput": "\"a7\""},
            {"function": "compressString", "input": "\"ab\"", "expectedOutput": "\"ab\""},
            {"function": "compressString", "input": "\"aabbcc\"", "expectedOutput": "\"aabbcc\""},
        ],
        "tags": ["string", "two-pointers"],
    },
    # ─── 14 ───
    {
        "slug": "find-second-largest",
        "title": "Find Second Largest",
        "difficulty": "easy",
        "description": (
            "Given an array of integers, find and return the second largest distinct value. "
            "If no second largest exists (e.g. all elements are the same or array has fewer than 2 distinct values), "
            "return -1. Solve in a single pass without sorting."
        ),
        "starterCode": "def secondLargest(nums: list) -> int:\n    pass",
        "examples": [
            {"input": "nums = [1,2,3,4,5]", "output": "4", "explanation": "4 is second largest."},
            {"input": "nums = [1,1,1]", "output": "-1", "explanation": "No distinct second largest."},
            {"input": "nums = [10,5]", "output": "5", "explanation": "5 is second largest."},
        ],
        "testCases": [
            {"function": "secondLargest", "input": "[1,2,3,4,5]", "expectedOutput": "4"},
            {"function": "secondLargest", "input": "[1,1,1]", "expectedOutput": "-1"},
            {"function": "secondLargest", "input": "[10,5]", "expectedOutput": "5"},
            {"function": "secondLargest", "input": "[3,1,4,1,5,9,2,6]", "expectedOutput": "6"},
            {"function": "secondLargest", "input": "[1]", "expectedOutput": "-1"},
            {"function": "secondLargest", "input": "[-1,-2,-3]", "expectedOutput": "-2"},
            {"function": "secondLargest", "input": "[100,100,99]", "expectedOutput": "99"},
            {"function": "secondLargest", "input": "[5,5,4,4,3]", "expectedOutput": "4"},
            {"function": "secondLargest", "input": "[0,0]", "expectedOutput": "-1"},
            {"function": "secondLargest", "input": "[7,3,7,5]", "expectedOutput": "5"},
        ],
        "tags": ["array"],
    },
    # ─── 15 ───
    {
        "slug": "matrix-transpose",
        "title": "Matrix Transpose",
        "difficulty": "easy",
        "description": (
            "The transpose of a matrix flips it along the main diagonal — rows become columns and columns become rows. "
            "Given an m x n matrix, return its transpose as an n x m matrix. "
            "Do not modify the original."
        ),
        "starterCode": "def transposeMatrix(matrix: list) -> list:\n    pass",
        "examples": [
            {"input": "matrix = [[1,2,3],[4,5,6],[7,8,9]]", "output": "[[1,4,7],[2,5,8],[3,6,9]]", "explanation": "Rows become columns."},
            {"input": "matrix = [[1,2],[3,4]]", "output": "[[1,3],[2,4]]", "explanation": "2x2 transpose."},
            {"input": "matrix = [[1,2,3]]", "output": "[[1],[2],[3]]", "explanation": "1x3 becomes 3x1."},
        ],
        "testCases": [
            {"function": "transposeMatrix", "input": "[[1,2,3],[4,5,6],[7,8,9]]", "expectedOutput": "[[1,4,7],[2,5,8],[3,6,9]]"},
            {"function": "transposeMatrix", "input": "[[1,2],[3,4]]", "expectedOutput": "[[1,3],[2,4]]"},
            {"function": "transposeMatrix", "input": "[[1,2,3]]", "expectedOutput": "[[1],[2],[3]]"},
            {"function": "transposeMatrix", "input": "[[1],[2],[3]]", "expectedOutput": "[[1,2,3]]"},
            {"function": "transposeMatrix", "input": "[[1]]", "expectedOutput": "[[1]]"},
            {"function": "transposeMatrix", "input": "[[1,2],[3,4],[5,6]]", "expectedOutput": "[[1,3,5],[2,4,6]]"},
            {"function": "transposeMatrix", "input": "[[0,0],[0,0]]", "expectedOutput": "[[0,0],[0,0]]"},
            {"function": "transposeMatrix", "input": "[[1,2,3],[4,5,6]]", "expectedOutput": "[[1,4],[2,5],[3,6]]"},
            {"function": "transposeMatrix", "input": "[[5,10],[15,20]]", "expectedOutput": "[[5,15],[10,20]]"},
            {"function": "transposeMatrix", "input": "[[1,0,0],[0,1,0],[0,0,1]]", "expectedOutput": "[[1,0,0],[0,1,0],[0,0,1]]"},
        ],
        "tags": ["matrix", "array"],
    },
    # ─── 16 ───
    {
        "slug": "two-pointer-remove-duplicates",
        "title": "Remove Duplicates from Sorted Array",
        "difficulty": "easy",
        "description": (
            "Given a sorted integer array, remove all duplicate elements in-place so each value appears only once. "
            "Return the number of unique elements. The first k elements of the array must contain the unique values "
            "in their original order. Use two pointers for O(1) extra space."
        ),
        "starterCode": "def removeDuplicatesSorted(nums: list) -> int:\n    pass",
        "examples": [
            {"input": "nums = [1,1,2]", "output": "2", "explanation": "Two unique values: 1 and 2."},
            {"input": "nums = [0,0,1,1,1,2,2,3,3,4]", "output": "5", "explanation": "Five unique values."},
            {"input": "nums = [1]", "output": "1", "explanation": "Single element."},
        ],
        "testCases": [
            {"function": "removeDuplicatesSorted", "input": "[1,1,2]", "expectedOutput": "2"},
            {"function": "removeDuplicatesSorted", "input": "[0,0,1,1,1,2,2,3,3,4]", "expectedOutput": "5"},
            {"function": "removeDuplicatesSorted", "input": "[1]", "expectedOutput": "1"},
            {"function": "removeDuplicatesSorted", "input": "[1,2,3]", "expectedOutput": "3"},
            {"function": "removeDuplicatesSorted", "input": "[1,1,1]", "expectedOutput": "1"},
            {"function": "removeDuplicatesSorted", "input": "[-3,-1,-1,0,0,1]", "expectedOutput": "4"},
            {"function": "removeDuplicatesSorted", "input": "[0,0,0,0]", "expectedOutput": "1"},
            {"function": "removeDuplicatesSorted", "input": "[1,2]", "expectedOutput": "2"},
            {"function": "removeDuplicatesSorted", "input": "[1,1,2,3,3]", "expectedOutput": "3"},
            {"function": "removeDuplicatesSorted", "input": "[1,2,3,4,5]", "expectedOutput": "5"},
        ],
        "tags": ["array", "two-pointers"],
    },
    # ─── 17 ───
    {
        "slug": "longest-word-in-sentence",
        "title": "Longest Word in Sentence",
        "difficulty": "easy",
        "description": (
            "Given a sentence (a string of words separated by spaces), find and return the longest word. "
            "If there are multiple words of the same maximum length, return the first one encountered. "
            "Words contain only alphabetic characters."
        ),
        "starterCode": "def longestWord(sentence: str) -> str:\n    pass",
        "examples": [
            {"input": "sentence = \"the quick brown fox\"", "output": "\"quick\"", "explanation": "quick has 5 chars."},
            {"input": "sentence = \"hello world\"", "output": "\"hello\"", "explanation": "Both have 5, return first."},
            {"input": "sentence = \"I am here\"", "output": "\"here\"", "explanation": "here has 4 chars."},
        ],
        "testCases": [
            {"function": "longestWord", "input": "\"the quick brown fox\"", "expectedOutput": "\"quick\""},
            {"function": "longestWord", "input": "\"hello world\"", "expectedOutput": "\"hello\""},
            {"function": "longestWord", "input": "\"I am here\"", "expectedOutput": "\"here\""},
            {"function": "longestWord", "input": "\"a\"", "expectedOutput": "\"a\""},
            {"function": "longestWord", "input": "\"fun programming\"", "expectedOutput": "\"programming\""},
            {"function": "longestWord", "input": "\"go to school\"", "expectedOutput": "\"school\""},
            {"function": "longestWord", "input": "\"cat bat rat\"", "expectedOutput": "\"cat\""},
            {"function": "longestWord", "input": "\"python java c\"", "expectedOutput": "\"python\""},
            {"function": "longestWord", "input": "\"one two three four five\"", "expectedOutput": "\"three\""},
            {"function": "longestWord", "input": "\"abcde fghij\"", "expectedOutput": "\"abcde\""},
        ],
        "tags": ["string"],
    },
    # ─── 18 ───
    {
        "slug": "gcd-two-numbers",
        "title": "Greatest Common Divisor",
        "difficulty": "easy",
        "description": (
            "The Greatest Common Divisor (GCD) of two integers is the largest integer that divides both without a remainder. "
            "Implement the Euclidean algorithm: repeatedly replace the larger number with the remainder when divided by the smaller. "
            "Given two non-negative integers a and b, return their GCD."
        ),
        "starterCode": "def gcd(a: int, b: int) -> int:\n    pass",
        "examples": [
            {"input": "a = 48, b = 18", "output": "6", "explanation": "GCD(48,18)=6."},
            {"input": "a = 0, b = 5", "output": "5", "explanation": "GCD(0,n)=n."},
            {"input": "a = 7, b = 7", "output": "7", "explanation": "Same numbers."},
        ],
        "testCases": [
            {"function": "gcd", "input": "48, 18", "expectedOutput": "6"},
            {"function": "gcd", "input": "0, 5", "expectedOutput": "5"},
            {"function": "gcd", "input": "7, 7", "expectedOutput": "7"},
            {"function": "gcd", "input": "100, 75", "expectedOutput": "25"},
            {"function": "gcd", "input": "1, 1", "expectedOutput": "1"},
            {"function": "gcd", "input": "13, 7", "expectedOutput": "1"},
            {"function": "gcd", "input": "56, 98", "expectedOutput": "14"},
            {"function": "gcd", "input": "0, 0", "expectedOutput": "0"},
            {"function": "gcd", "input": "270, 192", "expectedOutput": "6"},
            {"function": "gcd", "input": "1000, 500", "expectedOutput": "500"},
        ],
        "tags": ["math", "recursion"],
    },
    # ─── 19 ───
    {
        "slug": "search-insert-position",
        "title": "Search Insert Position",
        "difficulty": "easy",
        "description": (
            "Given a sorted array of distinct integers and a target, "
            "return the index of the target if found, or the index where it would be inserted to keep the array sorted. "
            "You must use an O(log n) algorithm."
        ),
        "starterCode": "def searchInsert(nums: list, target: int) -> int:\n    pass",
        "examples": [
            {"input": "nums = [1,3,5,6], target = 5", "output": "2", "explanation": "5 is at index 2."},
            {"input": "nums = [1,3,5,6], target = 2", "output": "1", "explanation": "2 would be inserted at index 1."},
            {"input": "nums = [1,3,5,6], target = 7", "output": "4", "explanation": "7 goes at the end."},
        ],
        "testCases": [
            {"function": "searchInsert", "input": "[1,3,5,6], 5", "expectedOutput": "2"},
            {"function": "searchInsert", "input": "[1,3,5,6], 2", "expectedOutput": "1"},
            {"function": "searchInsert", "input": "[1,3,5,6], 7", "expectedOutput": "4"},
            {"function": "searchInsert", "input": "[1,3,5,6], 0", "expectedOutput": "0"},
            {"function": "searchInsert", "input": "[1], 1", "expectedOutput": "0"},
            {"function": "searchInsert", "input": "[1], 0", "expectedOutput": "0"},
            {"function": "searchInsert", "input": "[1], 2", "expectedOutput": "1"},
            {"function": "searchInsert", "input": "[1,3], 2", "expectedOutput": "1"},
            {"function": "searchInsert", "input": "[2,7,8,9,10], 6", "expectedOutput": "1"},
            {"function": "searchInsert", "input": "[1,3,5,7,9], 4", "expectedOutput": "2"},
        ],
        "tags": ["binary-search", "array"],
    },
    # ─── 20 ───
    {
        "slug": "plus-one-array",
        "title": "Increment Number Array",
        "difficulty": "easy",
        "description": (
            "A large integer is stored as an array of its digits, with the most significant digit first. "
            "Add 1 to the number and return the resulting digit array. "
            "Handle carry propagation correctly, including numbers like 999."
        ),
        "starterCode": "def plusOne(digits: list) -> list:\n    pass",
        "examples": [
            {"input": "digits = [1,2,3]", "output": "[1,2,4]", "explanation": "123+1=124."},
            {"input": "digits = [9]", "output": "[1,0]", "explanation": "9+1=10."},
            {"input": "digits = [9,9,9]", "output": "[1,0,0,0]", "explanation": "999+1=1000."},
        ],
        "testCases": [
            {"function": "plusOne", "input": "[1,2,3]", "expectedOutput": "[1,2,4]"},
            {"function": "plusOne", "input": "[9]", "expectedOutput": "[1,0]"},
            {"function": "plusOne", "input": "[9,9,9]", "expectedOutput": "[1,0,0,0]"},
            {"function": "plusOne", "input": "[0]", "expectedOutput": "[1]"},
            {"function": "plusOne", "input": "[4,3,2,1]", "expectedOutput": "[4,3,2,2]"},
            {"function": "plusOne", "input": "[1,9]", "expectedOutput": "[2,0]"},
            {"function": "plusOne", "input": "[9,9]", "expectedOutput": "[1,0,0]"},
            {"function": "plusOne", "input": "[8]", "expectedOutput": "[9]"},
            {"function": "plusOne", "input": "[1,0,0]", "expectedOutput": "[1,0,1]"},
            {"function": "plusOne", "input": "[2,9,9]", "expectedOutput": "[3,0,0]"},
        ],
        "tags": ["array", "math"],
    },
    # ─── 21 ───
    {
        "slug": "sqrt-integer",
        "title": "Integer Square Root",
        "difficulty": "easy",
        "description": (
            "Given a non-negative integer x, return the floor of its square root — "
            "the largest integer r such that r*r <= x. "
            "Do not use any built-in sqrt functions. "
            "Use binary search for an O(log x) solution."
        ),
        "starterCode": "def mySqrt(x: int) -> int:\n    pass",
        "examples": [
            {"input": "x = 4", "output": "2", "explanation": "sqrt(4)=2."},
            {"input": "x = 8", "output": "2", "explanation": "floor(sqrt(8))=2."},
            {"input": "x = 0", "output": "0", "explanation": "sqrt(0)=0."},
        ],
        "testCases": [
            {"function": "mySqrt", "input": "4", "expectedOutput": "2"},
            {"function": "mySqrt", "input": "8", "expectedOutput": "2"},
            {"function": "mySqrt", "input": "0", "expectedOutput": "0"},
            {"function": "mySqrt", "input": "1", "expectedOutput": "1"},
            {"function": "mySqrt", "input": "9", "expectedOutput": "3"},
            {"function": "mySqrt", "input": "16", "expectedOutput": "4"},
            {"function": "mySqrt", "input": "15", "expectedOutput": "3"},
            {"function": "mySqrt", "input": "100", "expectedOutput": "10"},
            {"function": "mySqrt", "input": "2147395599", "expectedOutput": "46339"},
            {"function": "mySqrt", "input": "25", "expectedOutput": "5"},
        ],
        "tags": ["math", "binary-search"],
    },
    # ─── 22 ───
    {
        "slug": "move-zeros-end",
        "title": "Move Zeros to End",
        "difficulty": "easy",
        "description": (
            "Given an array of integers, move all zeroes to the end while preserving the relative order "
            "of non-zero elements. Do this in-place with O(1) extra space. "
            "Minimise the total number of operations."
        ),
        "starterCode": "def moveZeros(nums: list) -> None:\n    pass",
        "examples": [
            {"input": "nums = [0,1,0,3,12]", "output": "[1,3,12,0,0]", "explanation": "Zeros moved to end."},
            {"input": "nums = [0]", "output": "[0]", "explanation": "Single zero."},
            {"input": "nums = [1]", "output": "[1]", "explanation": "No zeros."},
        ],
        "testCases": [
            {"function": "moveZeros", "input": "[0,1,0,3,12]", "expectedOutput": "[1,3,12,0,0]"},
            {"function": "moveZeros", "input": "[0]", "expectedOutput": "[0]"},
            {"function": "moveZeros", "input": "[1]", "expectedOutput": "[1]"},
            {"function": "moveZeros", "input": "[1,2,3]", "expectedOutput": "[1,2,3]"},
            {"function": "moveZeros", "input": "[0,0,0]", "expectedOutput": "[0,0,0]"},
            {"function": "moveZeros", "input": "[0,0,1]", "expectedOutput": "[1,0,0]"},
            {"function": "moveZeros", "input": "[1,0,2,0,3]", "expectedOutput": "[1,2,3,0,0]"},
            {"function": "moveZeros", "input": "[0,1]", "expectedOutput": "[1,0]"},
            {"function": "moveZeros", "input": "[4,0,5,0,0,6]", "expectedOutput": "[4,5,6,0,0,0]"},
            {"function": "moveZeros", "input": "[2,1]", "expectedOutput": "[2,1]"},
        ],
        "tags": ["array", "two-pointers"],
    },
    # ─── 23 ───
    {
        "slug": "count-characters-frequency",
        "title": "Character Frequency Counter",
        "difficulty": "easy",
        "description": (
            "Given a string, return a dictionary mapping each unique character to its frequency (number of occurrences). "
            "Count all characters including spaces and special characters. "
            "This is a fundamental frequency-counting pattern."
        ),
        "starterCode": "def charFrequency(s: str) -> dict:\n    pass",
        "examples": [
            {"input": "s = \"hello\"", "output": "{h:1,e:1,l:2,o:1}", "explanation": "l appears twice."},
            {"input": "s = \"aaa\"", "output": "{a:3}", "explanation": "a appears 3 times."},
            {"input": "s = \"\"", "output": "{}", "explanation": "Empty string."},
        ],
        "testCases": [
            {"function": "charFrequency", "input": "\"hello\"", "expectedOutput": "{h:1,e:1,l:2,o:1}"},
            {"function": "charFrequency", "input": "\"aaa\"", "expectedOutput": "{a:3}"},
            {"function": "charFrequency", "input": "\"\"", "expectedOutput": "{}"},
            {"function": "charFrequency", "input": "\"abc\"", "expectedOutput": "{a:1,b:1,c:1}"},
            {"function": "charFrequency", "input": "\"aabb\"", "expectedOutput": "{a:2,b:2}"},
            {"function": "charFrequency", "input": "\"a b\"", "expectedOutput": "{a:1,' ':1,b:1}"},
            {"function": "charFrequency", "input": "\"zzz\"", "expectedOutput": "{z:3}"},
            {"function": "charFrequency", "input": "\"1122\"", "expectedOutput": "{1:2,2:2}"},
            {"function": "charFrequency", "input": "\"abcabc\"", "expectedOutput": "{a:2,b:2,c:2}"},
            {"function": "charFrequency", "input": "\"x\"", "expectedOutput": "{x:1}"},
        ],
        "tags": ["string", "hash-table"],
    },
    # ─── 24 ───
    {
        "slug": "intersection-two-arrays",
        "title": "Intersection of Two Arrays",
        "difficulty": "easy",
        "description": (
            "Given two integer arrays, return a list containing all elements that appear in both arrays. "
            "Each element in the result should appear only once (unique intersection). "
            "The result can be in any order."
        ),
        "starterCode": "def intersection(nums1: list, nums2: list) -> list:\n    pass",
        "examples": [
            {"input": "nums1 = [1,2,2,1], nums2 = [2,2]", "output": "[2]", "explanation": "2 is common and unique."},
            {"input": "nums1 = [4,9,5], nums2 = [9,4,9,8,4]", "output": "[4,9]", "explanation": "4 and 9 are common."},
            {"input": "nums1 = [1,2,3], nums2 = [4,5,6]", "output": "[]", "explanation": "No common elements."},
        ],
        "testCases": [
            {"function": "intersection", "input": "[1,2,2,1], [2,2]", "expectedOutput": "[2]"},
            {"function": "intersection", "input": "[4,9,5], [9,4,9,8,4]", "expectedOutput": "[4,9]"},
            {"function": "intersection", "input": "[1,2,3], [4,5,6]", "expectedOutput": "[]"},
            {"function": "intersection", "input": "[1], [1]", "expectedOutput": "[1]"},
            {"function": "intersection", "input": "[], []", "expectedOutput": "[]"},
            {"function": "intersection", "input": "[1,2,3], [3]", "expectedOutput": "[3]"},
            {"function": "intersection", "input": "[1,1,1], [1]", "expectedOutput": "[1]"},
            {"function": "intersection", "input": "[1,2], [2,3]", "expectedOutput": "[2]"},
            {"function": "intersection", "input": "[5,10,15], [10,20,30]", "expectedOutput": "[10]"},
            {"function": "intersection", "input": "[1,2,3,4,5], [3,4,5,6,7]", "expectedOutput": "[3,4,5]"},
        ],
        "tags": ["array", "hash-table", "two-pointers", "sorting"],
    },
    # ─── 25 ───
    {
        "slug": "power-of-two",
        "title": "Power of Two",
        "difficulty": "easy",
        "description": (
            "Given an integer n, return True if n is a power of 2 (i.e., there exists an integer k such that n = 2^k). "
            "Return False otherwise. "
            "Solve it using bit manipulation: a power of 2 has exactly one bit set in binary."
        ),
        "starterCode": "def isPowerOfTwo(n: int) -> bool:\n    pass",
        "examples": [
            {"input": "n = 1", "output": "True", "explanation": "2^0=1."},
            {"input": "n = 16", "output": "True", "explanation": "2^4=16."},
            {"input": "n = 3", "output": "False", "explanation": "Not a power of 2."},
        ],
        "testCases": [
            {"function": "isPowerOfTwo", "input": "1", "expectedOutput": "True"},
            {"function": "isPowerOfTwo", "input": "16", "expectedOutput": "True"},
            {"function": "isPowerOfTwo", "input": "3", "expectedOutput": "False"},
            {"function": "isPowerOfTwo", "input": "0", "expectedOutput": "False"},
            {"function": "isPowerOfTwo", "input": "-1", "expectedOutput": "False"},
            {"function": "isPowerOfTwo", "input": "2", "expectedOutput": "True"},
            {"function": "isPowerOfTwo", "input": "4", "expectedOutput": "True"},
            {"function": "isPowerOfTwo", "input": "6", "expectedOutput": "False"},
            {"function": "isPowerOfTwo", "input": "1024", "expectedOutput": "True"},
            {"function": "isPowerOfTwo", "input": "1000", "expectedOutput": "False"},
        ],
        "tags": ["math", "bit-manipulation", "recursion"],
    },
    # ─── 26 ───
    {
        "slug": "remove-element-inplace",
        "title": "Remove Element In-Place",
        "difficulty": "easy",
        "description": (
            "Given an array and a value val, remove all occurrences of val in-place and return "
            "the new length. The order of remaining elements does not need to be preserved. "
            "Do not allocate extra space — use O(1) memory."
        ),
        "starterCode": "def removeElement(nums: list, val: int) -> int:\n    pass",
        "examples": [
            {"input": "nums = [3,2,2,3], val = 3", "output": "2", "explanation": "Remove both 3s, length=2."},
            {"input": "nums = [0,1,2,2,3,0,4,2], val = 2", "output": "5", "explanation": "5 elements remain."},
            {"input": "nums = [1], val = 1", "output": "0", "explanation": "All removed."},
        ],
        "testCases": [
            {"function": "removeElement", "input": "[3,2,2,3], 3", "expectedOutput": "2"},
            {"function": "removeElement", "input": "[0,1,2,2,3,0,4,2], 2", "expectedOutput": "5"},
            {"function": "removeElement", "input": "[1], 1", "expectedOutput": "0"},
            {"function": "removeElement", "input": "[1], 2", "expectedOutput": "1"},
            {"function": "removeElement", "input": "[], 0", "expectedOutput": "0"},
            {"function": "removeElement", "input": "[4,5], 4", "expectedOutput": "1"},
            {"function": "removeElement", "input": "[1,2,3,4], 5", "expectedOutput": "4"},
            {"function": "removeElement", "input": "[2,2,2], 2", "expectedOutput": "0"},
            {"function": "removeElement", "input": "[1,1,2,3], 1", "expectedOutput": "2"},
            {"function": "removeElement", "input": "[1,2,3], 2", "expectedOutput": "2"},
        ],
        "tags": ["array", "two-pointers"],
    },
    # ─── 27 ───
    {
        "slug": "majority-element-vote",
        "title": "Majority Element",
        "difficulty": "easy",
        "description": (
            "A majority element appears more than n/2 times in an array of n elements. "
            "Given an array, find and return the majority element — it is guaranteed to always exist. "
            "Use Boyer-Moore Voting Algorithm for O(n) time and O(1) space."
        ),
        "starterCode": "def majorityElement(nums: list) -> int:\n    pass",
        "examples": [
            {"input": "nums = [3,2,3]", "output": "3", "explanation": "3 appears 2 out of 3 times."},
            {"input": "nums = [2,2,1,1,1,2,2]", "output": "2", "explanation": "2 appears 4 times."},
            {"input": "nums = [1]", "output": "1", "explanation": "Single element."},
        ],
        "testCases": [
            {"function": "majorityElement", "input": "[3,2,3]", "expectedOutput": "3"},
            {"function": "majorityElement", "input": "[2,2,1,1,1,2,2]", "expectedOutput": "2"},
            {"function": "majorityElement", "input": "[1]", "expectedOutput": "1"},
            {"function": "majorityElement", "input": "[1,1]", "expectedOutput": "1"},
            {"function": "majorityElement", "input": "[6,5,5]", "expectedOutput": "5"},
            {"function": "majorityElement", "input": "[1,2,1,2,1]", "expectedOutput": "1"},
            {"function": "majorityElement", "input": "[3,3,4]", "expectedOutput": "3"},
            {"function": "majorityElement", "input": "[5,5,5,3,3]", "expectedOutput": "5"},
            {"function": "majorityElement", "input": "[1,1,1,2,3]", "expectedOutput": "1"},
            {"function": "majorityElement", "input": "[10,10,10,1,2,3,10,10]", "expectedOutput": "10"},
        ],
        "tags": ["array", "hash-table", "sorting", "boyer-moore"],
    },
    # ─── 28 ───
    {
        "slug": "contains-duplicate-check",
        "title": "Contains Duplicate",
        "difficulty": "easy",
        "description": (
            "Given an integer array, return True if any value appears at least twice, "
            "False if all elements are distinct. "
            "This is the classic duplicate detection problem. Use a hash set for O(n) time."
        ),
        "starterCode": "def containsDuplicate(nums: list) -> bool:\n    pass",
        "examples": [
            {"input": "nums = [1,2,3,1]", "output": "True", "explanation": "1 appears twice."},
            {"input": "nums = [1,2,3,4]", "output": "False", "explanation": "All distinct."},
            {"input": "nums = [1,1,1,3,3,4,3,2,4,2]", "output": "True", "explanation": "Many duplicates."},
        ],
        "testCases": [
            {"function": "containsDuplicate", "input": "[1,2,3,1]", "expectedOutput": "True"},
            {"function": "containsDuplicate", "input": "[1,2,3,4]", "expectedOutput": "False"},
            {"function": "containsDuplicate", "input": "[1,1,1,3,3,4,3,2,4,2]", "expectedOutput": "True"},
            {"function": "containsDuplicate", "input": "[]", "expectedOutput": "False"},
            {"function": "containsDuplicate", "input": "[1]", "expectedOutput": "False"},
            {"function": "containsDuplicate", "input": "[0,0]", "expectedOutput": "True"},
            {"function": "containsDuplicate", "input": "[-1,-1]", "expectedOutput": "True"},
            {"function": "containsDuplicate", "input": "[1,2,3,4,5]", "expectedOutput": "False"},
            {"function": "containsDuplicate", "input": "[100,200,300,100]", "expectedOutput": "True"},
            {"function": "containsDuplicate", "input": "[1,2,3,4,5,6,7,8,9,10]", "expectedOutput": "False"},
        ],
        "tags": ["array", "hash-table", "sorting"],
    },
    # ─── 29 ───
    {
        "slug": "max-subarray-length-k",
        "title": "Max Average Subarray of Length K",
        "difficulty": "easy",
        "description": (
            "Given an integer array and an integer k, find the contiguous subarray of length exactly k "
            "that has the maximum average value. Return the maximum average. "
            "Use a sliding window to achieve O(n) time."
        ),
        "starterCode": "def maxAverageSubarray(nums: list, k: int) -> float:\n    pass",
        "examples": [
            {"input": "nums = [1,12,-5,-6,50,3], k = 4", "output": "12.75", "explanation": "Max avg subarray [12,-5,-6,50] = 51/4 = 12.75."},
            {"input": "nums = [5], k = 1", "output": "5.0", "explanation": "Single element."},
            {"input": "nums = [0,1,1,3,3], k = 4", "output": "2.0", "explanation": "[1,1,3,3]/4=2.0."},
        ],
        "testCases": [
            {"function": "maxAverageSubarray", "input": "[1,12,-5,-6,50,3], 4", "expectedOutput": "12.75"},
            {"function": "maxAverageSubarray", "input": "[5], 1", "expectedOutput": "5.0"},
            {"function": "maxAverageSubarray", "input": "[0,1,1,3,3], 4", "expectedOutput": "2.0"},
            {"function": "maxAverageSubarray", "input": "[1,2,3,4,5], 2", "expectedOutput": "4.5"},
            {"function": "maxAverageSubarray", "input": "[3,3,3,3], 2", "expectedOutput": "3.0"},
            {"function": "maxAverageSubarray", "input": "[-1,-2,-3,-4], 2", "expectedOutput": "-1.5"},
            {"function": "maxAverageSubarray", "input": "[10,2,3], 3", "expectedOutput": "5.0"},
            {"function": "maxAverageSubarray", "input": "[1,2,3,4,5], 1", "expectedOutput": "5.0"},
            {"function": "maxAverageSubarray", "input": "[4,2,1,3,3], 3", "expectedOutput": "3.0"},
            {"function": "maxAverageSubarray", "input": "[0,0,0,100], 2", "expectedOutput": "50.0"},
        ],
        "tags": ["array", "sliding-window"],
    },
    # ─── 30 ───
    {
        "slug": "count-primes-sieve",
        "title": "Count Primes",
        "difficulty": "medium",
        "description": (
            "Given an integer n, return the number of prime numbers strictly less than n. "
            "Use the Sieve of Eratosthenes for an efficient O(n log log n) solution — "
            "mark composite numbers iteratively starting from each prime's square."
        ),
        "starterCode": "def countPrimes(n: int) -> int:\n    pass",
        "examples": [
            {"input": "n = 10", "output": "4", "explanation": "Primes < 10: 2,3,5,7."},
            {"input": "n = 0", "output": "0", "explanation": "No primes less than 0."},
            {"input": "n = 1", "output": "0", "explanation": "No primes less than 1."},
        ],
        "testCases": [
            {"function": "countPrimes", "input": "10", "expectedOutput": "4"},
            {"function": "countPrimes", "input": "0", "expectedOutput": "0"},
            {"function": "countPrimes", "input": "1", "expectedOutput": "0"},
            {"function": "countPrimes", "input": "2", "expectedOutput": "0"},
            {"function": "countPrimes", "input": "3", "expectedOutput": "1"},
            {"function": "countPrimes", "input": "20", "expectedOutput": "8"},
            {"function": "countPrimes", "input": "100", "expectedOutput": "25"},
            {"function": "countPrimes", "input": "50", "expectedOutput": "15"},
            {"function": "countPrimes", "input": "5", "expectedOutput": "2"},
            {"function": "countPrimes", "input": "1000", "expectedOutput": "168"},
        ],
        "tags": ["math", "sieve", "array"],
    },
    # ─── 31 ───
    {
        "slug": "happy-number",
        "title": "Happy Number",
        "difficulty": "easy",
        "description": (
            "A happy number is defined by replacing a number repeatedly with the sum of squares of its digits. "
            "If this process eventually reaches 1, the number is happy. If it loops endlessly without reaching 1, it is not. "
            "Given n, return True if it is a happy number, False otherwise. "
            "Use Floyd's cycle detection."
        ),
        "starterCode": "def isHappy(n: int) -> bool:\n    pass",
        "examples": [
            {"input": "n = 19", "output": "True", "explanation": "1^2+9^2=82, 8^2+2^2=68, ... eventually reaches 1."},
            {"input": "n = 2", "output": "False", "explanation": "Enters a cycle, never reaches 1."},
            {"input": "n = 1", "output": "True", "explanation": "Already 1."},
        ],
        "testCases": [
            {"function": "isHappy", "input": "19", "expectedOutput": "True"},
            {"function": "isHappy", "input": "2", "expectedOutput": "False"},
            {"function": "isHappy", "input": "1", "expectedOutput": "True"},
            {"function": "isHappy", "input": "7", "expectedOutput": "True"},
            {"function": "isHappy", "input": "4", "expectedOutput": "False"},
            {"function": "isHappy", "input": "100", "expectedOutput": "True"},
            {"function": "isHappy", "input": "20", "expectedOutput": "False"},
            {"function": "isHappy", "input": "13", "expectedOutput": "True"},
            {"function": "isHappy", "input": "3", "expectedOutput": "False"},
            {"function": "isHappy", "input": "10", "expectedOutput": "True"},
        ],
        "tags": ["hash-table", "math", "two-pointers", "floyd-cycle-detection"],
    },
    # ─── 32 ───
    {
        "slug": "isomorphic-strings",
        "title": "Isomorphic Strings",
        "difficulty": "easy",
        "description": (
            "Two strings are isomorphic if the characters in one can be replaced consistently to get the other, "
            "with each character mapping to exactly one character and no two characters mapping to the same one. "
            "Given strings s and t, return True if they are isomorphic."
        ),
        "starterCode": "def isIsomorphic(s: str, t: str) -> bool:\n    pass",
        "examples": [
            {"input": "s = \"egg\", t = \"add\"", "output": "True", "explanation": "e->a, g->d."},
            {"input": "s = \"foo\", t = \"bar\"", "output": "False", "explanation": "o maps to two different chars."},
            {"input": "s = \"paper\", t = \"title\"", "output": "True", "explanation": "p->t, a->i, e->l, r->e."},
        ],
        "testCases": [
            {"function": "isIsomorphic", "input": "\"egg\", \"add\"", "expectedOutput": "True"},
            {"function": "isIsomorphic", "input": "\"foo\", \"bar\"", "expectedOutput": "False"},
            {"function": "isIsomorphic", "input": "\"paper\", \"title\"", "expectedOutput": "True"},
            {"function": "isIsomorphic", "input": "\"a\", \"a\"", "expectedOutput": "True"},
            {"function": "isIsomorphic", "input": "\"ab\", \"aa\"", "expectedOutput": "False"},
            {"function": "isIsomorphic", "input": "\"aa\", \"ab\"", "expectedOutput": "False"},
            {"function": "isIsomorphic", "input": "\"bbbaaaba\", \"aaabbbba\"", "expectedOutput": "False"},
            {"function": "isIsomorphic", "input": "\"abcd\", \"dcba\"", "expectedOutput": "True"},
            {"function": "isIsomorphic", "input": "\"abc\", \"xyz\"", "expectedOutput": "True"},
            {"function": "isIsomorphic", "input": "\"ba\", \"aa\"", "expectedOutput": "False"},
        ],
        "tags": ["string", "hash-table"],
    },
    # ─── 33 ───
    {
        "slug": "invert-binary-tree",
        "title": "Invert Binary Tree",
        "difficulty": "easy",
        "description": (
            "Given the root of a binary tree, invert it (mirror it) and return the new root. "
            "Inverting means swapping the left and right children of every node recursively. "
            "This can be solved elegantly with DFS recursion."
        ),
        "starterCode": "class TreeNode:\n    def __init__(self, val=0, left=None, right=None):\n        self.val = val\n        self.left = left\n        self.right = right\n\ndef invertTree(root):\n    pass",
        "examples": [
            {"input": "root = [4,2,7,1,3,6,9]", "output": "[4,7,2,9,6,3,1]", "explanation": "Left and right subtrees swapped at every level."},
            {"input": "root = [2,1,3]", "output": "[2,3,1]", "explanation": "Children swapped."},
            {"input": "root = []", "output": "[]", "explanation": "Empty tree."},
        ],
        "testCases": [
            {"function": "invertTree", "input": "[4,2,7,1,3,6,9]", "expectedOutput": "[4,7,2,9,6,3,1]"},
            {"function": "invertTree", "input": "[2,1,3]", "expectedOutput": "[2,3,1]"},
            {"function": "invertTree", "input": "[]", "expectedOutput": "[]"},
            {"function": "invertTree", "input": "[1]", "expectedOutput": "[1]"},
            {"function": "invertTree", "input": "[1,2]", "expectedOutput": "[1,null,2]"},
            {"function": "invertTree", "input": "[1,null,2]", "expectedOutput": "[1,2]"},
            {"function": "invertTree", "input": "[3,1,2]", "expectedOutput": "[3,2,1]"},
            {"function": "invertTree", "input": "[1,2,3,4,5,6,7]", "expectedOutput": "[1,3,2,7,6,5,4]"},
            {"function": "invertTree", "input": "[5,2,8]", "expectedOutput": "[5,8,2]"},
            {"function": "invertTree", "input": "[1,2,null,3]", "expectedOutput": "[1,null,2,null,3]"},
        ],
        "tags": ["tree", "dfs", "bfs", "binary-tree", "recursion"],
    },
    # ─── 34 ───
    {
        "slug": "linked-list-cycle-start",
        "title": "Find Cycle Start in Linked List",
        "difficulty": "medium",
        "description": (
            "Given a linked list that may contain a cycle, find and return the node where the cycle begins. "
            "If there is no cycle, return None. "
            "Use Floyd's algorithm: after detecting a cycle with slow/fast pointers, "
            "reset one pointer to head and advance both one step at a time — they meet at the cycle start."
        ),
        "starterCode": "class ListNode:\n    def __init__(self, val=0, next=None):\n        self.val = val\n        self.next = next\n\ndef detectCycleStart(head):\n    pass",
        "examples": [
            {"input": "head = [3,2,0,-4], cycle starts at node 1", "output": "node with val=2", "explanation": "Cycle begins at index 1."},
            {"input": "head = [1,2], cycle starts at node 0", "output": "node with val=1", "explanation": "Cycle at head."},
            {"input": "head = [1], no cycle", "output": "None", "explanation": "No cycle."},
        ],
        "testCases": [
            {"function": "detectCycleStart", "input": "[3,2,0,-4] cycle at 1", "expectedOutput": "node val 2"},
            {"function": "detectCycleStart", "input": "[1,2] cycle at 0", "expectedOutput": "node val 1"},
            {"function": "detectCycleStart", "input": "[1] no cycle", "expectedOutput": "None"},
            {"function": "detectCycleStart", "input": "[1,2,3,4] cycle at 1", "expectedOutput": "node val 2"},
            {"function": "detectCycleStart", "input": "[1,2,3,4] no cycle", "expectedOutput": "None"},
            {"function": "detectCycleStart", "input": "[1,2] no cycle", "expectedOutput": "None"},
            {"function": "detectCycleStart", "input": "[1,2,3] cycle at 0", "expectedOutput": "node val 1"},
            {"function": "detectCycleStart", "input": "[0,1,2,3,4] cycle at 2", "expectedOutput": "node val 2"},
            {"function": "detectCycleStart", "input": "[1,2,3,4,5] cycle at 4", "expectedOutput": "node val 5"},
            {"function": "detectCycleStart", "input": "[5,4,3,2,1] no cycle", "expectedOutput": "None"},
        ],
        "tags": ["linked-list", "two-pointers", "floyd-cycle-detection"],
    },
    # ─── 35 ───
    {
        "slug": "word-frequency-map",
        "title": "Word Frequency Counter",
        "difficulty": "easy",
        "description": (
            "Given a paragraph of text, count how many times each word appears. "
            "Ignore punctuation and treat words case-insensitively. "
            "Return a dictionary of word to count. "
            "Split on whitespace after cleaning."
        ),
        "starterCode": "def wordFrequency(text: str) -> dict:\n    pass",
        "examples": [
            {"input": "text = \"the cat sat on the mat\"", "output": "{the:2,cat:1,sat:1,on:1,mat:1}", "explanation": "'the' appears twice."},
            {"input": "text = \"hello hello world\"", "output": "{hello:2,world:1}", "explanation": "hello repeated."},
            {"input": "text = \"a\"", "output": "{a:1}", "explanation": "Single word."},
        ],
        "testCases": [
            {"function": "wordFrequency", "input": "\"the cat sat on the mat\"", "expectedOutput": "the:2"},
            {"function": "wordFrequency", "input": "\"hello hello world\"", "expectedOutput": "hello:2,world:1"},
            {"function": "wordFrequency", "input": "\"a\"", "expectedOutput": "{a:1}"},
            {"function": "wordFrequency", "input": "\"\"", "expectedOutput": "{}"},
            {"function": "wordFrequency", "input": "\"one two three\"", "expectedOutput": "each word count 1"},
            {"function": "wordFrequency", "input": "\"go go go\"", "expectedOutput": "{go:3}"},
            {"function": "wordFrequency", "input": "\"The the THE\"", "expectedOutput": "{the:3}"},
            {"function": "wordFrequency", "input": "\"hi there hi\"", "expectedOutput": "hi:2,there:1"},
            {"function": "wordFrequency", "input": "\"a b a b a\"", "expectedOutput": "a:3,b:2"},
            {"function": "wordFrequency", "input": "\"apple banana apple\"", "expectedOutput": "apple:2,banana:1"},
        ],
        "tags": ["string", "hash-table"],
    },
    # ─── 36 ───
    {
        "slug": "first-non-repeating-char",
        "title": "First Non-Repeating Character",
        "difficulty": "easy",
        "description": (
            "Given a string, find the index of the first character that appears only once. "
            "If no such character exists, return -1. "
            "Use two passes: first build a frequency map, then scan for the first with count 1."
        ),
        "starterCode": "def firstNonRepeating(s: str) -> int:\n    pass",
        "examples": [
            {"input": "s = \"leetcode\"", "output": "0", "explanation": "'l' appears once and is first."},
            {"input": "s = \"loveleetcode\"", "output": "2", "explanation": "'v' is first non-repeating."},
            {"input": "s = \"aabb\"", "output": "-1", "explanation": "All chars repeat."},
        ],
        "testCases": [
            {"function": "firstNonRepeating", "input": "\"leetcode\"", "expectedOutput": "0"},
            {"function": "firstNonRepeating", "input": "\"loveleetcode\"", "expectedOutput": "2"},
            {"function": "firstNonRepeating", "input": "\"aabb\"", "expectedOutput": "-1"},
            {"function": "firstNonRepeating", "input": "\"z\"", "expectedOutput": "0"},
            {"function": "firstNonRepeating", "input": "\"aabbcc\"", "expectedOutput": "-1"},
            {"function": "firstNonRepeating", "input": "\"abcabc\"", "expectedOutput": "-1"},
            {"function": "firstNonRepeating", "input": "\"abcd\"", "expectedOutput": "0"},
            {"function": "firstNonRepeating", "input": "\"aab\"", "expectedOutput": "2"},
            {"function": "firstNonRepeating", "input": "\"dddccdbba\"", "expectedOutput": "8"},
            {"function": "firstNonRepeating", "input": "\"cc\"", "expectedOutput": "-1"},
        ],
        "tags": ["string", "hash-table", "queue"],
    },
    # ─── 37 ───
    {
        "slug": "stack-using-queues",
        "title": "Stack Using Queues",
        "difficulty": "medium",
        "description": (
            "Implement a last-in-first-out (LIFO) stack using only standard queue operations: "
            "enqueue (push to back) and dequeue (pop from front). "
            "Support push(x), pop(), top(), and empty() operations. "
            "Each operation should work correctly even with only one queue."
        ),
        "starterCode": "from collections import deque\n\nclass StackUsingQueues:\n    def __init__(self):\n        pass\n    def push(self, x: int) -> None:\n        pass\n    def pop(self) -> int:\n        pass\n    def top(self) -> int:\n        pass\n    def empty(self) -> bool:\n        pass",
        "examples": [
            {"input": "push(1); push(2); top(); pop(); empty()", "output": "2, 2, False", "explanation": "LIFO order."},
            {"input": "push(5); empty(); pop()", "output": "False, 5", "explanation": "Pop returns 5."},
            {"input": "push(1); push(2); push(3); pop()", "output": "3", "explanation": "Last in, first out."},
        ],
        "testCases": [
            {"function": "StackUsingQueues", "input": "push(1); top()", "expectedOutput": "1"},
            {"function": "StackUsingQueues", "input": "push(1); push(2); top()", "expectedOutput": "2"},
            {"function": "StackUsingQueues", "input": "push(1); push(2); pop()", "expectedOutput": "2"},
            {"function": "StackUsingQueues", "input": "push(1); empty()", "expectedOutput": "False"},
            {"function": "StackUsingQueues", "input": "empty()", "expectedOutput": "True"},
            {"function": "StackUsingQueues", "input": "push(1); pop(); empty()", "expectedOutput": "True"},
            {"function": "StackUsingQueues", "input": "push(1); push(2); push(3); pop()", "expectedOutput": "3"},
            {"function": "StackUsingQueues", "input": "push(1); push(2); pop(); top()", "expectedOutput": "1"},
            {"function": "StackUsingQueues", "input": "push(5); top()", "expectedOutput": "5"},
            {"function": "StackUsingQueues", "input": "push(3); push(2); push(1); pop(); pop()", "expectedOutput": "2"},
        ],
        "tags": ["stack", "queue", "design"],
    },
    # ─── 38 ───
    {
        "slug": "queue-using-stacks",
        "title": "Queue Using Stacks",
        "difficulty": "easy",
        "description": (
            "Implement a first-in-first-out (FIFO) queue using only two stacks. "
            "Support push(x), pop(), peek(), and empty() operations. "
            "Use a lazy transfer approach: move elements from the input stack to the output stack "
            "only when the output stack is empty."
        ),
        "starterCode": "class QueueUsingStacks:\n    def __init__(self):\n        pass\n    def push(self, x: int) -> None:\n        pass\n    def pop(self) -> int:\n        pass\n    def peek(self) -> int:\n        pass\n    def empty(self) -> bool:\n        pass",
        "examples": [
            {"input": "push(1); push(2); peek(); pop(); empty()", "output": "1, 1, False", "explanation": "FIFO order."},
            {"input": "push(3); pop(); empty()", "output": "3, True", "explanation": "Queue empties."},
            {"input": "push(1); push(2); pop(); peek()", "output": "1, 2", "explanation": "First in, first out."},
        ],
        "testCases": [
            {"function": "QueueUsingStacks", "input": "push(1); peek()", "expectedOutput": "1"},
            {"function": "QueueUsingStacks", "input": "push(1); push(2); peek()", "expectedOutput": "1"},
            {"function": "QueueUsingStacks", "input": "push(1); push(2); pop()", "expectedOutput": "1"},
            {"function": "QueueUsingStacks", "input": "push(1); pop(); empty()", "expectedOutput": "True"},
            {"function": "QueueUsingStacks", "input": "empty()", "expectedOutput": "True"},
            {"function": "QueueUsingStacks", "input": "push(1); push(2); pop(); pop()", "expectedOutput": "2"},
            {"function": "QueueUsingStacks", "input": "push(1); push(2); push(3); pop()", "expectedOutput": "1"},
            {"function": "QueueUsingStacks", "input": "push(5); peek()", "expectedOutput": "5"},
            {"function": "QueueUsingStacks", "input": "push(1); push(2); peek(); pop(); peek()", "expectedOutput": "2"},
            {"function": "QueueUsingStacks", "input": "push(3); push(2); push(1); pop()", "expectedOutput": "3"},
        ],
        "tags": ["stack", "queue", "design"],
    },
    # ─── 39 ───
    {
        "slug": "symmetric-tree",
        "title": "Symmetric Tree",
        "difficulty": "easy",
        "description": (
            "A symmetric binary tree is one that is a mirror image of itself around its center. "
            "Given a binary tree root, return True if it is symmetric, False otherwise. "
            "Check both iteratively (using a queue) and recursively."
        ),
        "starterCode": "class TreeNode:\n    def __init__(self, val=0, left=None, right=None):\n        self.val = val\n        self.left = left\n        self.right = right\n\ndef isSymmetric(root) -> bool:\n    pass",
        "examples": [
            {"input": "root = [1,2,2,3,4,4,3]", "output": "True", "explanation": "Perfect mirror."},
            {"input": "root = [1,2,2,null,3,null,3]", "output": "False", "explanation": "Not mirrored."},
            {"input": "root = [1]", "output": "True", "explanation": "Single node is symmetric."},
        ],
        "testCases": [
            {"function": "isSymmetric", "input": "[1,2,2,3,4,4,3]", "expectedOutput": "True"},
            {"function": "isSymmetric", "input": "[1,2,2,null,3,null,3]", "expectedOutput": "False"},
            {"function": "isSymmetric", "input": "[1]", "expectedOutput": "True"},
            {"function": "isSymmetric", "input": "[]", "expectedOutput": "True"},
            {"function": "isSymmetric", "input": "[1,2,2]", "expectedOutput": "True"},
            {"function": "isSymmetric", "input": "[1,2,3]", "expectedOutput": "False"},
            {"function": "isSymmetric", "input": "[1,2,2,null,3,3,null]", "expectedOutput": "True"},
            {"function": "isSymmetric", "input": "[5,4,4,3,null,null,3]", "expectedOutput": "True"},
            {"function": "isSymmetric", "input": "[2,3,3,4,5,5,4]", "expectedOutput": "True"},
            {"function": "isSymmetric", "input": "[1,2,2,2,null,2]", "expectedOutput": "False"},
        ],
        "tags": ["tree", "dfs", "bfs", "binary-tree"],
    },
    # ─── 40 ───
    {
        "slug": "linked-list-nth-from-end",
        "title": "Remove Nth Node From End",
        "difficulty": "medium",
        "description": (
            "Given the head of a linked list and an integer n, remove the nth node from the end of the list "
            "and return the head. "
            "Use two pointers — advance one pointer n steps ahead, then move both until the fast one hits the end."
        ),
        "starterCode": "class ListNode:\n    def __init__(self, val=0, next=None):\n        self.val = val\n        self.next = next\n\ndef removeNthFromEnd(head, n: int):\n    pass",
        "examples": [
            {"input": "head = [1,2,3,4,5], n = 2", "output": "[1,2,3,5]", "explanation": "4 (2nd from end) removed."},
            {"input": "head = [1], n = 1", "output": "[]", "explanation": "Only node removed."},
            {"input": "head = [1,2], n = 1", "output": "[1]", "explanation": "Last node removed."},
        ],
        "testCases": [
            {"function": "removeNthFromEnd", "input": "[1,2,3,4,5], 2", "expectedOutput": "[1,2,3,5]"},
            {"function": "removeNthFromEnd", "input": "[1], 1", "expectedOutput": "[]"},
            {"function": "removeNthFromEnd", "input": "[1,2], 1", "expectedOutput": "[1]"},
            {"function": "removeNthFromEnd", "input": "[1,2], 2", "expectedOutput": "[2]"},
            {"function": "removeNthFromEnd", "input": "[1,2,3], 3", "expectedOutput": "[2,3]"},
            {"function": "removeNthFromEnd", "input": "[1,2,3], 1", "expectedOutput": "[1,2]"},
            {"function": "removeNthFromEnd", "input": "[1,2,3,4], 2", "expectedOutput": "[1,2,4]"},
            {"function": "removeNthFromEnd", "input": "[1,2,3,4,5], 5", "expectedOutput": "[2,3,4,5]"},
            {"function": "removeNthFromEnd", "input": "[1,2,3,4,5], 1", "expectedOutput": "[1,2,3,4]"},
            {"function": "removeNthFromEnd", "input": "[1,2,3], 2", "expectedOutput": "[1,3]"},
        ],
        "tags": ["linked-list", "two-pointers"],
    },
    # ─── 41 ───
    {
        "slug": "middle-of-linked-list",
        "title": "Middle of Linked List",
        "difficulty": "easy",
        "description": (
            "Given the head of a singly linked list, return the middle node. "
            "If the list has an even number of nodes, return the second middle node. "
            "Use the slow/fast pointer technique for a single-pass O(n) solution."
        ),
        "starterCode": "class ListNode:\n    def __init__(self, val=0, next=None):\n        self.val = val\n        self.next = next\n\ndef middleNode(head):\n    pass",
        "examples": [
            {"input": "head = [1,2,3,4,5]", "output": "[3,4,5]", "explanation": "Middle is node 3."},
            {"input": "head = [1,2,3,4,5,6]", "output": "[4,5,6]", "explanation": "Even list, second middle."},
            {"input": "head = [1]", "output": "[1]", "explanation": "Single node."},
        ],
        "testCases": [
            {"function": "middleNode", "input": "[1,2,3,4,5]", "expectedOutput": "node val 3"},
            {"function": "middleNode", "input": "[1,2,3,4,5,6]", "expectedOutput": "node val 4"},
            {"function": "middleNode", "input": "[1]", "expectedOutput": "node val 1"},
            {"function": "middleNode", "input": "[1,2]", "expectedOutput": "node val 2"},
            {"function": "middleNode", "input": "[1,2,3]", "expectedOutput": "node val 2"},
            {"function": "middleNode", "input": "[1,2,3,4]", "expectedOutput": "node val 3"},
            {"function": "middleNode", "input": "[1,2,3,4,5,6,7]", "expectedOutput": "node val 4"},
            {"function": "middleNode", "input": "[5,10]", "expectedOutput": "node val 10"},
            {"function": "middleNode", "input": "[1,2,3,4,5,6,7,8]", "expectedOutput": "node val 5"},
            {"function": "middleNode", "input": "[100]", "expectedOutput": "node val 100"},
        ],
        "tags": ["linked-list", "two-pointers"],
    },
    # ─── 42 ───
    {
        "slug": "number-to-roman",
        "title": "Integer to Roman",
        "difficulty": "medium",
        "description": (
            "Convert a positive integer to its Roman numeral representation. "
            "Roman numerals use symbols I, V, X, L, C, D, M and subtraction pairs IV, IX, XL, XC, CD, CM. "
            "Given an integer in the range [1, 3999], return its Roman numeral string."
        ),
        "starterCode": "def intToRoman(num: int) -> str:\n    pass",
        "examples": [
            {"input": "num = 3", "output": "\"III\"", "explanation": "Three ones."},
            {"input": "num = 58", "output": "\"LVIII\"", "explanation": "L=50, V=5, III=3."},
            {"input": "num = 1994", "output": "\"MCMXCIV\"", "explanation": "M=1000, CM=900, XC=90, IV=4."},
        ],
        "testCases": [
            {"function": "intToRoman", "input": "3", "expectedOutput": "\"III\""},
            {"function": "intToRoman", "input": "58", "expectedOutput": "\"LVIII\""},
            {"function": "intToRoman", "input": "1994", "expectedOutput": "\"MCMXCIV\""},
            {"function": "intToRoman", "input": "1", "expectedOutput": "\"I\""},
            {"function": "intToRoman", "input": "4", "expectedOutput": "\"IV\""},
            {"function": "intToRoman", "input": "9", "expectedOutput": "\"IX\""},
            {"function": "intToRoman", "input": "40", "expectedOutput": "\"XL\""},
            {"function": "intToRoman", "input": "400", "expectedOutput": "\"CD\""},
            {"function": "intToRoman", "input": "900", "expectedOutput": "\"CM\""},
            {"function": "intToRoman", "input": "3999", "expectedOutput": "\"MMMCMXCIX\""},
        ],
        "tags": ["string", "hash-table", "math"],
    },
    # ─── 43 ───
    {
        "slug": "preorder-traversal",
        "title": "Binary Tree Preorder Traversal",
        "difficulty": "easy",
        "description": (
            "Traverse a binary tree in preorder: visit the root first, then the left subtree, then the right subtree. "
            "Given a binary tree root, return the list of node values in preorder. "
            "Implement both recursively and iteratively using a stack."
        ),
        "starterCode": "class TreeNode:\n    def __init__(self, val=0, left=None, right=None):\n        self.val = val\n        self.left = left\n        self.right = right\n\ndef preorderTraversal(root) -> list:\n    pass",
        "examples": [
            {"input": "root = [1,null,2,3]", "output": "[1,2,3]", "explanation": "Root, left, right."},
            {"input": "root = []", "output": "[]", "explanation": "Empty tree."},
            {"input": "root = [1]", "output": "[1]", "explanation": "Single node."},
        ],
        "testCases": [
            {"function": "preorderTraversal", "input": "[1,null,2,3]", "expectedOutput": "[1,2,3]"},
            {"function": "preorderTraversal", "input": "[]", "expectedOutput": "[]"},
            {"function": "preorderTraversal", "input": "[1]", "expectedOutput": "[1]"},
            {"function": "preorderTraversal", "input": "[1,2,3]", "expectedOutput": "[1,2,3]"},
            {"function": "preorderTraversal", "input": "[3,1,2]", "expectedOutput": "[3,1,2]"},
            {"function": "preorderTraversal", "input": "[1,2,null,3]", "expectedOutput": "[1,2,3]"},
            {"function": "preorderTraversal", "input": "[5,3,8,1,4,7,9]", "expectedOutput": "[5,3,1,4,8,7,9]"},
            {"function": "preorderTraversal", "input": "[1,2,3,4,5,6,7]", "expectedOutput": "[1,2,4,5,3,6,7]"},
            {"function": "preorderTraversal", "input": "[1,null,2]", "expectedOutput": "[1,2]"},
            {"function": "preorderTraversal", "input": "[4,2,6,1,3,5,7]", "expectedOutput": "[4,2,1,3,6,5,7]"},
        ],
        "tags": ["tree", "dfs", "stack", "recursion"],
    },
    # ─── 44 ───
    {
        "slug": "inorder-traversal",
        "title": "Binary Tree Inorder Traversal",
        "difficulty": "easy",
        "description": (
            "Traverse a binary tree inorder: visit the left subtree, then the root, then the right subtree. "
            "For a BST, inorder traversal produces sorted output. "
            "Given a root, return the list of values in inorder. "
            "Implement iteratively using an explicit stack."
        ),
        "starterCode": "class TreeNode:\n    def __init__(self, val=0, left=None, right=None):\n        self.val = val\n        self.left = left\n        self.right = right\n\ndef inorderTraversal(root) -> list:\n    pass",
        "examples": [
            {"input": "root = [1,null,2,3]", "output": "[1,3,2]", "explanation": "Left, root, right."},
            {"input": "root = []", "output": "[]", "explanation": "Empty tree."},
            {"input": "root = [1]", "output": "[1]", "explanation": "Single node."},
        ],
        "testCases": [
            {"function": "inorderTraversal", "input": "[1,null,2,3]", "expectedOutput": "[1,3,2]"},
            {"function": "inorderTraversal", "input": "[]", "expectedOutput": "[]"},
            {"function": "inorderTraversal", "input": "[1]", "expectedOutput": "[1]"},
            {"function": "inorderTraversal", "input": "[1,2,3]", "expectedOutput": "[2,1,3]"},
            {"function": "inorderTraversal", "input": "[5,3,8,1,4,7,9]", "expectedOutput": "[1,3,4,5,7,8,9]"},
            {"function": "inorderTraversal", "input": "[4,2,6,1,3,5,7]", "expectedOutput": "[1,2,3,4,5,6,7]"},
            {"function": "inorderTraversal", "input": "[1,2]", "expectedOutput": "[2,1]"},
            {"function": "inorderTraversal", "input": "[1,null,2]", "expectedOutput": "[1,2]"},
            {"function": "inorderTraversal", "input": "[3,1,4,null,2]", "expectedOutput": "[1,2,3,4]"},
            {"function": "inorderTraversal", "input": "[1,2,3,4,5,6,7]", "expectedOutput": "[4,2,5,1,6,3,7]"},
        ],
        "tags": ["tree", "dfs", "stack", "recursion"],
    },
    # ─── 45 ───
    {
        "slug": "postorder-traversal",
        "title": "Binary Tree Postorder Traversal",
        "difficulty": "easy",
        "description": (
            "Traverse a binary tree postorder: visit the left subtree, then the right subtree, then the root. "
            "Postorder is useful for deleting a tree or evaluating expression trees. "
            "Given a root, return the node values in postorder."
        ),
        "starterCode": "class TreeNode:\n    def __init__(self, val=0, left=None, right=None):\n        self.val = val\n        self.left = left\n        self.right = right\n\ndef postorderTraversal(root) -> list:\n    pass",
        "examples": [
            {"input": "root = [1,null,2,3]", "output": "[3,2,1]", "explanation": "Left, right, root."},
            {"input": "root = []", "output": "[]", "explanation": "Empty tree."},
            {"input": "root = [1]", "output": "[1]", "explanation": "Single node."},
        ],
        "testCases": [
            {"function": "postorderTraversal", "input": "[1,null,2,3]", "expectedOutput": "[3,2,1]"},
            {"function": "postorderTraversal", "input": "[]", "expectedOutput": "[]"},
            {"function": "postorderTraversal", "input": "[1]", "expectedOutput": "[1]"},
            {"function": "postorderTraversal", "input": "[1,2,3]", "expectedOutput": "[2,3,1]"},
            {"function": "postorderTraversal", "input": "[5,3,8,1,4,7,9]", "expectedOutput": "[1,4,3,7,9,8,5]"},
            {"function": "postorderTraversal", "input": "[4,2,6,1,3,5,7]", "expectedOutput": "[1,3,2,5,7,6,4]"},
            {"function": "postorderTraversal", "input": "[1,2]", "expectedOutput": "[2,1]"},
            {"function": "postorderTraversal", "input": "[1,null,2]", "expectedOutput": "[2,1]"},
            {"function": "postorderTraversal", "input": "[1,2,3,4,5,6,7]", "expectedOutput": "[4,5,2,6,7,3,1]"},
            {"function": "postorderTraversal", "input": "[3,1,4,null,2]", "expectedOutput": "[2,1,4,3]"},
        ],
        "tags": ["tree", "dfs", "stack", "recursion"],
    },
    # ─── 46 ───
    {
        "slug": "zigzag-level-order",
        "title": "Zigzag Level Order Traversal",
        "difficulty": "medium",
        "description": (
            "Given a binary tree, return its level order traversal in zigzag fashion — "
            "left to right for odd levels and right to left for even levels (1-indexed). "
            "Return a list of lists. Use a BFS queue and a level-flip flag."
        ),
        "starterCode": "class TreeNode:\n    def __init__(self, val=0, left=None, right=None):\n        self.val = val\n        self.left = left\n        self.right = right\n\ndef zigzagLevelOrder(root) -> list:\n    pass",
        "examples": [
            {"input": "root = [3,9,20,null,null,15,7]", "output": "[[3],[20,9],[15,7]]", "explanation": "Alternating direction."},
            {"input": "root = [1]", "output": "[[1]]", "explanation": "Single level."},
            {"input": "root = []", "output": "[]", "explanation": "Empty tree."},
        ],
        "testCases": [
            {"function": "zigzagLevelOrder", "input": "[3,9,20,null,null,15,7]", "expectedOutput": "[[3],[20,9],[15,7]]"},
            {"function": "zigzagLevelOrder", "input": "[1]", "expectedOutput": "[[1]]"},
            {"function": "zigzagLevelOrder", "input": "[]", "expectedOutput": "[]"},
            {"function": "zigzagLevelOrder", "input": "[1,2,3]", "expectedOutput": "[[1],[3,2]]"},
            {"function": "zigzagLevelOrder", "input": "[1,2,3,4,5]", "expectedOutput": "[[1],[3,2],[4,5]]"},
            {"function": "zigzagLevelOrder", "input": "[5,3,8,1,4]", "expectedOutput": "[[5],[8,3],[1,4]]"},
            {"function": "zigzagLevelOrder", "input": "[1,2,3,4,5,6,7]", "expectedOutput": "[[1],[3,2],[4,5,6,7]]"},
            {"function": "zigzagLevelOrder", "input": "[1,2]", "expectedOutput": "[[1],[2]]"},
            {"function": "zigzagLevelOrder", "input": "[1,null,2]", "expectedOutput": "[[1],[2]]"},
            {"function": "zigzagLevelOrder", "input": "[1,2,3,null,4,5]", "expectedOutput": "[[1],[3,2],[4,5]]"},
        ],
        "tags": ["tree", "bfs", "binary-tree", "deque"],
    },
    # ─── 47 ───
    {
        "slug": "longest-common-prefix",
        "title": "Longest Common Prefix",
        "difficulty": "easy",
        "description": (
            "Given an array of strings, find the longest common prefix shared by all strings. "
            "If no common prefix exists, return an empty string. "
            "You can compare character by character or use vertical scanning."
        ),
        "starterCode": "def longestCommonPrefix(strs: list) -> str:\n    pass",
        "examples": [
            {"input": "strs = [\"flower\",\"flow\",\"flight\"]", "output": "\"fl\"", "explanation": "fl is common to all."},
            {"input": "strs = [\"dog\",\"racecar\",\"car\"]", "output": "\"\"", "explanation": "No common prefix."},
            {"input": "strs = [\"interview\",\"interact\",\"internal\"]", "output": "\"inter\"", "explanation": "inter is common."},
        ],
        "testCases": [
            {"function": "longestCommonPrefix", "input": "[\"flower\",\"flow\",\"flight\"]", "expectedOutput": "\"fl\""},
            {"function": "longestCommonPrefix", "input": "[\"dog\",\"racecar\",\"car\"]", "expectedOutput": "\"\""},
            {"function": "longestCommonPrefix", "input": "[\"interview\",\"interact\",\"internal\"]", "expectedOutput": "\"inter\""},
            {"function": "longestCommonPrefix", "input": "[\"a\"]", "expectedOutput": "\"a\""},
            {"function": "longestCommonPrefix", "input": "[\"\",\"b\"]", "expectedOutput": "\"\""},
            {"function": "longestCommonPrefix", "input": "[\"abc\",\"abc\"]", "expectedOutput": "\"abc\""},
            {"function": "longestCommonPrefix", "input": "[\"abc\",\"ab\",\"a\"]", "expectedOutput": "\"a\""},
            {"function": "longestCommonPrefix", "input": "[\"hello\",\"hello\",\"hello\"]", "expectedOutput": "\"hello\""},
            {"function": "longestCommonPrefix", "input": "[\"ab\",\"a\"]", "expectedOutput": "\"a\""},
            {"function": "longestCommonPrefix", "input": "[\"c\",\"c\"]", "expectedOutput": "\"c\""},
        ],
        "tags": ["string", "trie"],
    },
    # ─── 48 ───
    {
        "slug": "two-sum-sorted",
        "title": "Two Sum in Sorted Array",
        "difficulty": "easy",
        "description": (
            "Given a sorted (ascending) integer array and a target, find the two numbers that sum to the target. "
            "Return their 1-indexed positions. Use two pointers — one at each end — for O(n) time and O(1) space. "
            "The input guarantees exactly one solution."
        ),
        "starterCode": "def twoSumSorted(numbers: list, target: int) -> list:\n    pass",
        "examples": [
            {"input": "numbers = [2,7,11,15], target = 9", "output": "[1,2]", "explanation": "numbers[1]+numbers[2]=9 (1-indexed)."},
            {"input": "numbers = [2,3,4], target = 6", "output": "[1,3]", "explanation": "2+4=6."},
            {"input": "numbers = [-1,0], target = -1", "output": "[1,2]", "explanation": "-1+0=-1."},
        ],
        "testCases": [
            {"function": "twoSumSorted", "input": "[2,7,11,15], 9", "expectedOutput": "[1,2]"},
            {"function": "twoSumSorted", "input": "[2,3,4], 6", "expectedOutput": "[1,3]"},
            {"function": "twoSumSorted", "input": "[-1,0], -1", "expectedOutput": "[1,2]"},
            {"function": "twoSumSorted", "input": "[1,2,3,4,5], 9", "expectedOutput": "[4,5]"},
            {"function": "twoSumSorted", "input": "[1,3,5,7], 8", "expectedOutput": "[1,4]"},
            {"function": "twoSumSorted", "input": "[5,25,75], 100", "expectedOutput": "[2,3]"},
            {"function": "twoSumSorted", "input": "[-10,-3,2,9], -1", "expectedOutput": "[2,3]"},
            {"function": "twoSumSorted", "input": "[1,2], 3", "expectedOutput": "[1,2]"},
            {"function": "twoSumSorted", "input": "[0,1,2,3,4], 7", "expectedOutput": "[4,5]"},
            {"function": "twoSumSorted", "input": "[3,5,9,12,15], 24", "expectedOutput": "[3,5]"},
        ],
        "tags": ["array", "two-pointers", "binary-search"],
    },
    # ─── 49 ───
    {
        "slug": "subarray-sum-equals-k",
        "title": "Subarray Sum Equals K",
        "difficulty": "medium",
        "description": (
            "Given an array of integers and an integer k, return the total number of contiguous subarrays "
            "whose elements sum to exactly k. "
            "Use a prefix sum with a hash map to solve this in O(n) without nested loops."
        ),
        "starterCode": "def subarraySum(nums: list, k: int) -> int:\n    pass",
        "examples": [
            {"input": "nums = [1,1,1], k = 2", "output": "2", "explanation": "Two subarrays [1,1] sum to 2."},
            {"input": "nums = [1,2,3], k = 3", "expectedOutput": "2", "explanation": "[3] and [1,2] both sum to 3."},
            {"input": "nums = [1], k = 1", "output": "1", "explanation": "Single element equals k."},
        ],
        "testCases": [
            {"function": "subarraySum", "input": "[1,1,1], 2", "expectedOutput": "2"},
            {"function": "subarraySum", "input": "[1,2,3], 3", "expectedOutput": "2"},
            {"function": "subarraySum", "input": "[1], 1", "expectedOutput": "1"},
            {"function": "subarraySum", "input": "[1], 0", "expectedOutput": "0"},
            {"function": "subarraySum", "input": "[0,0,0], 0", "expectedOutput": "6"},
            {"function": "subarraySum", "input": "[-1,-1,1], 0", "expectedOutput": "1"},
            {"function": "subarraySum", "input": "[3,4,7,2,-3,1,4,2], 7", "expectedOutput": "4"},
            {"function": "subarraySum", "input": "[1,2,3,4,5], 5", "expectedOutput": "2"},
            {"function": "subarraySum", "input": "[1,-1,0], 0", "expectedOutput": "3"},
            {"function": "subarraySum", "input": "[2,2,2,2,2], 4", "expectedOutput": "4"},
        ],
        "tags": ["array", "hash-table", "prefix-sum"],
    },
    # ─── 50 ───
    {
        "slug": "rotate-array",
        "title": "Rotate Array",
        "difficulty": "medium",
        "description": (
            "Given an integer array, rotate it to the right by k steps — "
            "every element shifts k positions right, wrapping around. "
            "Do this in-place with O(1) extra space. "
            "Hint: reverse the whole array, then reverse the first k elements, then reverse the rest."
        ),
        "starterCode": "def rotateArray(nums: list, k: int) -> None:\n    pass",
        "examples": [
            {"input": "nums = [1,2,3,4,5,6,7], k = 3", "output": "[5,6,7,1,2,3,4]", "explanation": "Rotated right by 3."},
            {"input": "nums = [-1,-100,3,99], k = 2", "output": "[3,99,-1,-100]", "explanation": "Rotated right by 2."},
            {"input": "nums = [1,2], k = 1", "output": "[2,1]", "explanation": "Single rotation."},
        ],
        "testCases": [
            {"function": "rotateArray", "input": "[1,2,3,4,5,6,7], 3", "expectedOutput": "[5,6,7,1,2,3,4]"},
            {"function": "rotateArray", "input": "[-1,-100,3,99], 2", "expectedOutput": "[3,99,-1,-100]"},
            {"function": "rotateArray", "input": "[1,2], 1", "expectedOutput": "[2,1]"},
            {"function": "rotateArray", "input": "[1], 0", "expectedOutput": "[1]"},
            {"function": "rotateArray", "input": "[1,2,3], 4", "expectedOutput": "[3,1,2]"},
            {"function": "rotateArray", "input": "[1,2,3,4,5], 2", "expectedOutput": "[4,5,1,2,3]"},
            {"function": "rotateArray", "input": "[1,2,3], 3", "expectedOutput": "[1,2,3]"},
            {"function": "rotateArray", "input": "[1,2,3,4], 1", "expectedOutput": "[4,1,2,3]"},
            {"function": "rotateArray", "input": "[1,2,3,4,5,6], 6", "expectedOutput": "[1,2,3,4,5,6]"},
            {"function": "rotateArray", "input": "[1,2,3,4], 6", "expectedOutput": "[3,4,1,2]"},
        ],
        "tags": ["array", "two-pointers", "math"],
    },
    # ─── 51 ───
    {
        "slug": "check-balanced-brackets",
        "title": "Check Balanced Brackets",
        "difficulty": "easy",
        "description": (
            "Given a string containing only round brackets '(' and ')', "
            "determine whether the brackets are balanced. "
            "A string is balanced if every '(' has a matching ')' and they are properly ordered. "
            "Use a counter or stack."
        ),
        "starterCode": "def isBalanced(s: str) -> bool:\n    pass",
        "examples": [
            {"input": "s = \"((()))\"", "output": "True", "explanation": "All nested brackets balanced."},
            {"input": "s = \"(()\"", "output": "False", "explanation": "One unmatched opening bracket."},
            {"input": "s = \")()\"", "output": "False", "explanation": "Closing before opening."},
        ],
        "testCases": [
            {"function": "isBalanced", "input": "\"((()))\"", "expectedOutput": "True"},
            {"function": "isBalanced", "input": "\"(()\"", "expectedOutput": "False"},
            {"function": "isBalanced", "input": "\")()\"", "expectedOutput": "False"},
            {"function": "isBalanced", "input": "\"()\"", "expectedOutput": "True"},
            {"function": "isBalanced", "input": "\"\"", "expectedOutput": "True"},
            {"function": "isBalanced", "input": "\"((\"", "expectedOutput": "False"},
            {"function": "isBalanced", "input": "\"))\"", "expectedOutput": "False"},
            {"function": "isBalanced", "input": "\"(()())\"", "expectedOutput": "True"},
            {"function": "isBalanced", "input": "\"()()(()())\"", "expectedOutput": "True"},
            {"function": "isBalanced", "input": "\"(()()(\"", "expectedOutput": "False"},
        ],
        "tags": ["string", "stack"],
    },
    # ─── 52 ───
    {
        "slug": "flatten-binary-tree",
        "title": "Flatten Binary Tree to Linked List",
        "difficulty": "medium",
        "description": (
            "Given the root of a binary tree, flatten it to a linked list in-place using the same TreeNode structure. "
            "The linked list should follow the preorder traversal order, "
            "with each node's right pointer pointing to the next node and left pointer set to null."
        ),
        "starterCode": "class TreeNode:\n    def __init__(self, val=0, left=None, right=None):\n        self.val = val\n        self.left = left\n        self.right = right\n\ndef flattenTree(root) -> None:\n    pass",
        "examples": [
            {"input": "root = [1,2,5,3,4,null,6]", "output": "[1,null,2,null,3,null,4,null,5,null,6]", "explanation": "Preorder flattened."},
            {"input": "root = []", "output": "[]", "explanation": "Empty tree."},
            {"input": "root = [0]", "output": "[0]", "explanation": "Single node."},
        ],
        "testCases": [
            {"function": "flattenTree", "input": "[1,2,5,3,4,null,6]", "expectedOutput": "[1,null,2,null,3,null,4,null,5,null,6]"},
            {"function": "flattenTree", "input": "[]", "expectedOutput": "[]"},
            {"function": "flattenTree", "input": "[0]", "expectedOutput": "[0]"},
            {"function": "flattenTree", "input": "[1,2]", "expectedOutput": "[1,null,2]"},
            {"function": "flattenTree", "input": "[1,null,2]", "expectedOutput": "[1,null,2]"},
            {"function": "flattenTree", "input": "[1,2,3]", "expectedOutput": "[1,null,2,null,3]"},
            {"function": "flattenTree", "input": "[1,2,5,3,4]", "expectedOutput": "[1,null,2,null,3,null,4,null,5]"},
            {"function": "flattenTree", "input": "[3,1,2]", "expectedOutput": "[3,null,1,null,2]"},
            {"function": "flattenTree", "input": "[1,2,3,4,5,6]", "expectedOutput": "[1,null,2,null,4,null,5,null,3,null,6]"},
            {"function": "flattenTree", "input": "[5]", "expectedOutput": "[5]"},
        ],
        "tags": ["tree", "dfs", "linked-list", "stack"],
    },
    # ─── 53 ───
    {
        "slug": "binary-watch",
        "title": "Binary Watch",
        "difficulty": "easy",
        "description": (
            "A binary watch has 4 LEDs for hours (0-11) and 6 LEDs for minutes (0-59). "
            "Each LED represents a bit. Given the number of LEDs that are on (turnedOn), "
            "return all possible times the watch could display in 'H:MM' format. "
            "Order does not matter."
        ),
        "starterCode": "def readBinaryWatch(turnedOn: int) -> list:\n    pass",
        "examples": [
            {"input": "turnedOn = 1", "output": "[\"0:01\",\"0:02\",\"0:04\",\"0:08\",\"0:16\",\"0:32\",\"1:00\",\"2:00\",\"4:00\",\"8:00\"]", "explanation": "All times with exactly 1 LED on."},
            {"input": "turnedOn = 0", "output": "[\"0:00\"]", "explanation": "No LEDs, midnight."},
            {"input": "turnedOn = 9", "output": "[]", "explanation": "Impossible to represent."},
        ],
        "testCases": [
            {"function": "readBinaryWatch", "input": "0", "expectedOutput": "[\"0:00\"]"},
            {"function": "readBinaryWatch", "input": "1", "expectedOutput": "10 times"},
            {"function": "readBinaryWatch", "input": "2", "expectedOutput": "multiple times"},
            {"function": "readBinaryWatch", "input": "9", "expectedOutput": "[]"},
            {"function": "readBinaryWatch", "input": "3", "expectedOutput": "multiple times"},
            {"function": "readBinaryWatch", "input": "4", "expectedOutput": "multiple times"},
            {"function": "readBinaryWatch", "input": "5", "expectedOutput": "multiple times"},
            {"function": "readBinaryWatch", "input": "6", "expectedOutput": "multiple times"},
            {"function": "readBinaryWatch", "input": "7", "expectedOutput": "multiple times"},
            {"function": "readBinaryWatch", "input": "8", "expectedOutput": "multiple times"},
        ],
        "tags": ["bit-manipulation", "backtracking"],
    },
    # ─── 54 ───
    {
        "slug": "group-anagrams",
        "title": "Group Anagrams",
        "difficulty": "medium",
        "description": (
            "Given an array of strings, group the anagrams together and return a list of groups. "
            "Two strings are anagrams if they contain the same characters with the same frequencies. "
            "The order of groups and within groups does not matter. "
            "Use sorted keys or character-count tuples as hash map keys."
        ),
        "starterCode": "def groupAnagrams(strs: list) -> list:\n    pass",
        "examples": [
            {"input": "strs = [\"eat\",\"tea\",\"tan\",\"ate\",\"nat\",\"bat\"]", "output": "[[\"eat\",\"tea\",\"ate\"],[\"tan\",\"nat\"],[\"bat\"]]", "explanation": "Three anagram groups."},
            {"input": "strs = [\"\"]", "output": "[[\"\"]]", "explanation": "Single empty string."},
            {"input": "strs = [\"a\"]", "output": "[[\"a\"]]", "explanation": "Single string."},
        ],
        "testCases": [
            {"function": "groupAnagrams", "input": "[\"eat\",\"tea\",\"tan\",\"ate\",\"nat\",\"bat\"]", "expectedOutput": "3 groups"},
            {"function": "groupAnagrams", "input": "[\"\"]", "expectedOutput": "[[\"\"]]"},
            {"function": "groupAnagrams", "input": "[\"a\"]", "expectedOutput": "[[\"a\"]]"},
            {"function": "groupAnagrams", "input": "[\"a\",\"b\"]", "expectedOutput": "2 groups"},
            {"function": "groupAnagrams", "input": "[\"abc\",\"cba\",\"bac\"]", "expectedOutput": "1 group of 3"},
            {"function": "groupAnagrams", "input": "[\"aa\",\"aa\"]", "expectedOutput": "1 group of 2"},
            {"function": "groupAnagrams", "input": "[\"ab\",\"ba\",\"cd\",\"dc\"]", "expectedOutput": "2 groups"},
            {"function": "groupAnagrams", "input": "[\"ab\",\"cd\",\"ef\"]", "expectedOutput": "3 groups of 1"},
            {"function": "groupAnagrams", "input": "[\"listen\",\"silent\",\"enlist\"]", "expectedOutput": "1 group of 3"},
            {"function": "groupAnagrams", "input": "[\"rat\",\"car\",\"tar\",\"arc\"]", "expectedOutput": "2 groups"},
        ],
        "tags": ["string", "hash-table", "sorting"],
    },
    # ─── 55 ───
    {
        "slug": "find-all-duplicates",
        "title": "Find All Duplicates in Array",
        "difficulty": "medium",
        "description": (
            "Given an integer array of n elements where each element is in range [1, n], "
            "find all elements that appear exactly twice. "
            "Return them in any order. "
            "Solve in O(n) time and O(1) extra space by using the sign of array values as markers."
        ),
        "starterCode": "def findAllDuplicates(nums: list) -> list:\n    pass",
        "examples": [
            {"input": "nums = [4,3,2,7,8,2,3,1]", "output": "[2,3]", "explanation": "2 and 3 appear twice."},
            {"input": "nums = [1,1,2]", "output": "[1]", "explanation": "1 appears twice."},
            {"input": "nums = [1]", "output": "[]", "explanation": "No duplicates."},
        ],
        "testCases": [
            {"function": "findAllDuplicates", "input": "[4,3,2,7,8,2,3,1]", "expectedOutput": "[2,3]"},
            {"function": "findAllDuplicates", "input": "[1,1,2]", "expectedOutput": "[1]"},
            {"function": "findAllDuplicates", "input": "[1]", "expectedOutput": "[]"},
            {"function": "findAllDuplicates", "input": "[2,2]", "expectedOutput": "[2]"},
            {"function": "findAllDuplicates", "input": "[1,2,3]", "expectedOutput": "[]"},
            {"function": "findAllDuplicates", "input": "[1,1,2,2]", "expectedOutput": "[1,2]"},
            {"function": "findAllDuplicates", "input": "[3,1,3,4,2]", "expectedOutput": "[3]"},
            {"function": "findAllDuplicates", "input": "[5,4,6,7,9,8,5,4]", "expectedOutput": "[5,4]"},
            {"function": "findAllDuplicates", "input": "[1,2,3,4,5]", "expectedOutput": "[]"},
            {"function": "findAllDuplicates", "input": "[2,1,2,1]", "expectedOutput": "[2,1]"},
        ],
        "tags": ["array", "hash-table"],
    },
    # ─── 56 ───
    {
        "slug": "longest-palindrome-build",
        "title": "Longest Palindrome from Characters",
        "difficulty": "easy",
        "description": (
            "Given a string of characters, find the length of the longest palindrome that can be built using those characters. "
            "Characters with even counts can all be used. One character with an odd count can be placed in the center. "
            "Return the maximum length."
        ),
        "starterCode": "def longestPalindromeLength(s: str) -> int:\n    pass",
        "examples": [
            {"input": "s = \"abccccdd\"", "output": "7", "explanation": "dccaccd or similar, length 7."},
            {"input": "s = \"a\"", "output": "1", "explanation": "Single character."},
            {"input": "s = \"bb\"", "output": "2", "explanation": "bb is a palindrome."},
        ],
        "testCases": [
            {"function": "longestPalindromeLength", "input": "\"abccccdd\"", "expectedOutput": "7"},
            {"function": "longestPalindromeLength", "input": "\"a\"", "expectedOutput": "1"},
            {"function": "longestPalindromeLength", "input": "\"bb\"", "expectedOutput": "2"},
            {"function": "longestPalindromeLength", "input": "\"aabb\"", "expectedOutput": "4"},
            {"function": "longestPalindromeLength", "input": "\"abc\"", "expectedOutput": "1"},
            {"function": "longestPalindromeLength", "input": "\"aaaa\"", "expectedOutput": "4"},
            {"function": "longestPalindromeLength", "input": "\"aab\"", "expectedOutput": "3"},
            {"function": "longestPalindromeLength", "input": "\"ccc\"", "expectedOutput": "3"},
            {"function": "longestPalindromeLength", "input": "\"aaabbbccc\"", "expectedOutput": "7"},
            {"function": "longestPalindromeLength", "input": "\"abcba\"", "expectedOutput": "5"},
        ],
        "tags": ["string", "hash-table", "greedy"],
    },
    # ─── 57 ───
    {
        "slug": "max-points-on-line",
        "title": "Max Points on a Line",
        "difficulty": "hard",
        "description": (
            "Given an array of points on a 2D plane, find the maximum number of points "
            "that lie on the same straight line. "
            "Two points define a line; use the slope (as a reduced fraction) as a hash key. "
            "Watch out for vertical lines and duplicate points."
        ),
        "starterCode": "def maxPointsOnLine(points: list) -> int:\n    pass",
        "examples": [
            {"input": "points = [[1,1],[2,2],[3,3]]", "output": "3", "explanation": "All on y=x."},
            {"input": "points = [[1,1],[3,2],[5,3],[4,1],[2,3],[1,4]]", "output": "4", "explanation": "Four points collinear."},
            {"input": "points = [[1,1]]", "output": "1", "explanation": "Single point."},
        ],
        "testCases": [
            {"function": "maxPointsOnLine", "input": "[[1,1],[2,2],[3,3]]", "expectedOutput": "3"},
            {"function": "maxPointsOnLine", "input": "[[1,1],[3,2],[5,3],[4,1],[2,3],[1,4]]", "expectedOutput": "4"},
            {"function": "maxPointsOnLine", "input": "[[1,1]]", "expectedOutput": "1"},
            {"function": "maxPointsOnLine", "input": "[[1,1],[2,2]]", "expectedOutput": "2"},
            {"function": "maxPointsOnLine", "input": "[[0,0],[1,1],[0,0]]", "expectedOutput": "3"},
            {"function": "maxPointsOnLine", "input": "[[0,0],[1,0],[2,0]]", "expectedOutput": "3"},
            {"function": "maxPointsOnLine", "input": "[[0,0],[0,1],[0,2]]", "expectedOutput": "3"},
            {"function": "maxPointsOnLine", "input": "[[1,1],[2,3],[3,5],[4,7]]", "expectedOutput": "4"},
            {"function": "maxPointsOnLine", "input": "[[0,0],[1,1],[1,-1]]", "expectedOutput": "2"},
            {"function": "maxPointsOnLine", "input": "[[1,1],[2,2],[3,3],[4,5]]", "expectedOutput": "3"},
        ],
        "tags": ["array", "hash-table", "math", "geometry"],
    },
    # ─── 58 ───
    {
        "slug": "top-k-words",
        "title": "Top K Frequent Words",
        "difficulty": "medium",
        "description": (
            "Given an array of strings and an integer k, return the k most frequent words. "
            "Sort the result by frequency from highest to lowest; "
            "for ties, sort alphabetically. "
            "Use a heap or bucket sort for efficiency."
        ),
        "starterCode": "def topKWords(words: list, k: int) -> list:\n    pass",
        "examples": [
            {"input": "words = [\"i\",\"love\",\"leetcode\",\"i\",\"love\",\"coding\"], k = 2", "output": "[\"i\",\"love\"]", "explanation": "i and love appear twice."},
            {"input": "words = [\"the\",\"day\",\"is\",\"sunny\",\"the\",\"the\",\"the\",\"sunny\",\"is\",\"is\"], k = 4", "output": "[\"the\",\"is\",\"sunny\",\"day\"]", "explanation": "By frequency then alpha."},
            {"input": "words = [\"a\"], k = 1", "output": "[\"a\"]", "explanation": "Single word."},
        ],
        "testCases": [
            {"function": "topKWords", "input": "[\"i\",\"love\",\"leetcode\",\"i\",\"love\",\"coding\"], 2", "expectedOutput": "[\"i\",\"love\"]"},
            {"function": "topKWords", "input": "[\"the\",\"day\",\"is\",\"sunny\",\"the\",\"the\",\"the\",\"sunny\",\"is\",\"is\"], 4", "expectedOutput": "[\"the\",\"is\",\"sunny\",\"day\"]"},
            {"function": "topKWords", "input": "[\"a\"], 1", "expectedOutput": "[\"a\"]"},
            {"function": "topKWords", "input": "[\"a\",\"b\",\"a\",\"b\",\"c\"], 2", "expectedOutput": "[\"a\",\"b\"]"},
            {"function": "topKWords", "input": "[\"a\",\"b\",\"c\",\"d\"], 2", "expectedOutput": "[\"a\",\"b\"]"},
            {"function": "topKWords", "input": "[\"z\",\"z\",\"a\",\"a\"], 1", "expectedOutput": "[\"a\"]"},
            {"function": "topKWords", "input": "[\"hello\",\"world\",\"hello\"], 1", "expectedOutput": "[\"hello\"]"},
            {"function": "topKWords", "input": "[\"b\",\"a\",\"c\",\"b\",\"a\",\"a\"], 2", "expectedOutput": "[\"a\",\"b\"]"},
            {"function": "topKWords", "input": "[\"x\",\"y\",\"z\",\"x\",\"y\",\"x\"], 3", "expectedOutput": "[\"x\",\"y\",\"z\"]"},
            {"function": "topKWords", "input": "[\"aa\",\"aa\",\"bb\",\"bb\",\"cc\"], 2", "expectedOutput": "[\"aa\",\"bb\"]"},
        ],
        "tags": ["hash-table", "heap", "sorting", "string"],
    },
    # ─── 59 ───
    {
        "slug": "smallest-missing-positive",
        "title": "Smallest Missing Positive",
        "difficulty": "hard",
        "description": (
            "Given an unsorted integer array, find the smallest missing positive integer. "
            "Your algorithm must run in O(n) time and use O(1) extra space. "
            "Hint: use the array itself as a hash map by placing each number x at index x-1."
        ),
        "starterCode": "def firstMissingPositive(nums: list) -> int:\n    pass",
        "examples": [
            {"input": "nums = [1,2,0]", "output": "3", "explanation": "1 and 2 present, 3 missing."},
            {"input": "nums = [3,4,-1,1]", "output": "2", "explanation": "2 is missing."},
            {"input": "nums = [7,8,9,11,12]", "output": "1", "explanation": "1 not in array."},
        ],
        "testCases": [
            {"function": "firstMissingPositive", "input": "[1,2,0]", "expectedOutput": "3"},
            {"function": "firstMissingPositive", "input": "[3,4,-1,1]", "expectedOutput": "2"},
            {"function": "firstMissingPositive", "input": "[7,8,9,11,12]", "expectedOutput": "1"},
            {"function": "firstMissingPositive", "input": "[1]", "expectedOutput": "2"},
            {"function": "firstMissingPositive", "input": "[2]", "expectedOutput": "1"},
            {"function": "firstMissingPositive", "input": "[1,2,3]", "expectedOutput": "4"},
            {"function": "firstMissingPositive", "input": "[-1,-2,-3]", "expectedOutput": "1"},
            {"function": "firstMissingPositive", "input": "[0]", "expectedOutput": "1"},
            {"function": "firstMissingPositive", "input": "[1,1]", "expectedOutput": "2"},
            {"function": "firstMissingPositive", "input": "[2,3,4,5]", "expectedOutput": "1"},
        ],
        "tags": ["array", "hash-table"],
    },
    # ─── 60 ───
    {
        "slug": "excel-column-number",
        "title": "Excel Column Number",
        "difficulty": "easy",
        "description": (
            "Excel columns are labeled A, B, ..., Z, AA, AB, ... ZZ, AAA, etc. "
            "Given a column title as a string, return its corresponding column number. "
            "Think of it as a base-26 number system where A=1, Z=26, AA=27."
        ),
        "starterCode": "def excelColumnNumber(columnTitle: str) -> int:\n    pass",
        "examples": [
            {"input": "columnTitle = \"A\"", "output": "1", "explanation": "A is column 1."},
            {"input": "columnTitle = \"AB\"", "output": "28", "explanation": "26+2=28."},
            {"input": "columnTitle = \"ZY\"", "output": "701", "explanation": "26*26+25=701."},
        ],
        "testCases": [
            {"function": "excelColumnNumber", "input": "\"A\"", "expectedOutput": "1"},
            {"function": "excelColumnNumber", "input": "\"AB\"", "expectedOutput": "28"},
            {"function": "excelColumnNumber", "input": "\"ZY\"", "expectedOutput": "701"},
            {"function": "excelColumnNumber", "input": "\"Z\"", "expectedOutput": "26"},
            {"function": "excelColumnNumber", "input": "\"AA\"", "expectedOutput": "27"},
            {"function": "excelColumnNumber", "input": "\"AZ\"", "expectedOutput": "52"},
            {"function": "excelColumnNumber", "input": "\"BA\"", "expectedOutput": "53"},
            {"function": "excelColumnNumber", "input": "\"ZZ\"", "expectedOutput": "702"},
            {"function": "excelColumnNumber", "input": "\"AAA\"", "expectedOutput": "703"},
            {"function": "excelColumnNumber", "input": "\"FXSHRXW\"", "expectedOutput": "2147483647"},
        ],
        "tags": ["math", "string"],
    },
    # ─── 61 ───
    {
        "slug": "reverse-integer",
        "title": "Reverse Integer",
        "difficulty": "medium",
        "description": (
            "Given a signed 32-bit integer x, return x with its digits reversed. "
            "If the reversed integer overflows the 32-bit signed integer range [-2^31, 2^31-1], return 0. "
            "Do not use 64-bit integers."
        ),
        "starterCode": "def reverseInteger(x: int) -> int:\n    pass",
        "examples": [
            {"input": "x = 123", "output": "321", "explanation": "Digits reversed."},
            {"input": "x = -123", "output": "-321", "explanation": "Negative preserved."},
            {"input": "x = 120", "output": "21", "explanation": "Leading zero dropped."},
        ],
        "testCases": [
            {"function": "reverseInteger", "input": "123", "expectedOutput": "321"},
            {"function": "reverseInteger", "input": "-123", "expectedOutput": "-321"},
            {"function": "reverseInteger", "input": "120", "expectedOutput": "21"},
            {"function": "reverseInteger", "input": "0", "expectedOutput": "0"},
            {"function": "reverseInteger", "input": "1534236469", "expectedOutput": "0"},
            {"function": "reverseInteger", "input": "-2147483648", "expectedOutput": "0"},
            {"function": "reverseInteger", "input": "100", "expectedOutput": "1"},
            {"function": "reverseInteger", "input": "1000000003", "expectedOutput": "0"},
            {"function": "reverseInteger", "input": "7", "expectedOutput": "7"},
            {"function": "reverseInteger", "input": "-10", "expectedOutput": "-1"},
        ],
        "tags": ["math"],
    },
    # ─── 62 ───
    {
        "slug": "integer-to-english",
        "title": "Integer to English Words",
        "difficulty": "hard",
        "description": (
            "Convert a non-negative integer to its English words representation. "
            "Handle all numbers from 0 to 2,147,483,647. "
            "Break the number into groups of thousands (billion, million, thousand) "
            "and convert each group separately."
        ),
        "starterCode": "def numberToWords(num: int) -> str:\n    pass",
        "examples": [
            {"input": "num = 123", "output": "\"One Hundred Twenty Three\"", "explanation": "Three digit number."},
            {"input": "num = 12345", "output": "\"Twelve Thousand Three Hundred Forty Five\"", "explanation": "Thousands group."},
            {"input": "num = 0", "output": "\"Zero\"", "explanation": "Special case."},
        ],
        "testCases": [
            {"function": "numberToWords", "input": "123", "expectedOutput": "\"One Hundred Twenty Three\""},
            {"function": "numberToWords", "input": "12345", "expectedOutput": "\"Twelve Thousand Three Hundred Forty Five\""},
            {"function": "numberToWords", "input": "0", "expectedOutput": "\"Zero\""},
            {"function": "numberToWords", "input": "1", "expectedOutput": "\"One\""},
            {"function": "numberToWords", "input": "1000000", "expectedOutput": "\"One Million\""},
            {"function": "numberToWords", "input": "1000000000", "expectedOutput": "\"One Billion\""},
            {"function": "numberToWords", "input": "1000010", "expectedOutput": "\"One Million Ten\""},
            {"function": "numberToWords", "input": "20", "expectedOutput": "\"Twenty\""},
            {"function": "numberToWords", "input": "100", "expectedOutput": "\"One Hundred\""},
            {"function": "numberToWords", "input": "1000", "expectedOutput": "\"One Thousand\""},
        ],
        "tags": ["math", "string", "recursion"],
    },
    # ─── 63 ───
    {
        "slug": "range-sum-query",
        "title": "Range Sum Query – Immutable",
        "difficulty": "easy",
        "description": (
            "Given an integer array, answer multiple sum queries efficiently. "
            "Each query asks for the sum of elements between indices left and right (inclusive). "
            "Precompute a prefix sum array so each query runs in O(1) time."
        ),
        "starterCode": "class RangeSumQuery:\n    def __init__(self, nums: list):\n        pass\n    def sumRange(self, left: int, right: int) -> int:\n        pass",
        "examples": [
            {"input": "nums = [-2,0,3,-5,2,-1]; sumRange(0,2); sumRange(2,5); sumRange(0,5)", "output": "1, -1, -3", "explanation": "Prefix sums used."},
            {"input": "nums = [1]; sumRange(0,0)", "output": "1", "explanation": "Single element."},
            {"input": "nums = [1,2,3,4,5]; sumRange(1,3)", "output": "9", "explanation": "2+3+4=9."},
        ],
        "testCases": [
            {"function": "RangeSumQuery", "input": "[-2,0,3,-5,2,-1]; sumRange(0,2)", "expectedOutput": "1"},
            {"function": "RangeSumQuery", "input": "[-2,0,3,-5,2,-1]; sumRange(2,5)", "expectedOutput": "-1"},
            {"function": "RangeSumQuery", "input": "[-2,0,3,-5,2,-1]; sumRange(0,5)", "expectedOutput": "-3"},
            {"function": "RangeSumQuery", "input": "[1]; sumRange(0,0)", "expectedOutput": "1"},
            {"function": "RangeSumQuery", "input": "[1,2,3,4,5]; sumRange(1,3)", "expectedOutput": "9"},
            {"function": "RangeSumQuery", "input": "[1,2,3,4,5]; sumRange(0,4)", "expectedOutput": "15"},
            {"function": "RangeSumQuery", "input": "[5,10,15]; sumRange(0,1)", "expectedOutput": "15"},
            {"function": "RangeSumQuery", "input": "[5,10,15]; sumRange(1,2)", "expectedOutput": "25"},
            {"function": "RangeSumQuery", "input": "[0,0,0]; sumRange(0,2)", "expectedOutput": "0"},
            {"function": "RangeSumQuery", "input": "[-1,-2,-3]; sumRange(0,2)", "expectedOutput": "-6"},
        ],
        "tags": ["array", "prefix-sum", "design"],
    },
    # ─── 64 ───
    {
        "slug": "bitwise-and-range",
        "title": "Bitwise AND of Number Range",
        "difficulty": "medium",
        "description": (
            "Given two integers left and right representing a range [left, right], "
            "return the bitwise AND of all numbers in that range. "
            "Observe that bits that differ between left and right will always produce 0 after AND-ing all values — "
            "find the common left prefix."
        ),
        "starterCode": "def rangeBitwiseAnd(left: int, right: int) -> int:\n    pass",
        "examples": [
            {"input": "left = 5, right = 7", "output": "4", "explanation": "5&6&7=4."},
            {"input": "left = 0, right = 0", "output": "0", "explanation": "Single value 0."},
            {"input": "left = 1, right = 2147483647", "output": "0", "explanation": "Full range, all bits differ."},
        ],
        "testCases": [
            {"function": "rangeBitwiseAnd", "input": "5, 7", "expectedOutput": "4"},
            {"function": "rangeBitwiseAnd", "input": "0, 0", "expectedOutput": "0"},
            {"function": "rangeBitwiseAnd", "input": "1, 2147483647", "expectedOutput": "0"},
            {"function": "rangeBitwiseAnd", "input": "5, 5", "expectedOutput": "5"},
            {"function": "rangeBitwiseAnd", "input": "6, 7", "expectedOutput": "6"},
            {"function": "rangeBitwiseAnd", "input": "8, 9", "expectedOutput": "8"},
            {"function": "rangeBitwiseAnd", "input": "1, 1", "expectedOutput": "1"},
            {"function": "rangeBitwiseAnd", "input": "3, 4", "expectedOutput": "0"},
            {"function": "rangeBitwiseAnd", "input": "0, 1", "expectedOutput": "0"},
            {"function": "rangeBitwiseAnd", "input": "10, 12", "expectedOutput": "8"},
        ],
        "tags": ["bit-manipulation"],
    },
    # ─── 65 ───
    {
        "slug": "container-most-water-3d",
        "title": "Largest Rectangle in Grid",
        "difficulty": "hard",
        "description": (
            "Given a binary matrix of '0' and '1', find the largest rectangle containing only 1s and return its area. "
            "Build a histogram from each row using the rows above, "
            "then apply the largest rectangle in histogram algorithm on each row."
        ),
        "starterCode": "def maximalRectangle(matrix: list) -> int:\n    pass",
        "examples": [
            {"input": "matrix = [[\"1\",\"0\",\"1\",\"0\",\"0\"],[\"1\",\"0\",\"1\",\"1\",\"1\"],[\"1\",\"1\",\"1\",\"1\",\"1\"],[\"1\",\"0\",\"0\",\"1\",\"0\"]]", "output": "6", "explanation": "6-cell rectangle in the bottom-middle."},
            {"input": "matrix = [[\"0\"]]", "output": "0", "explanation": "No ones."},
            {"input": "matrix = [[\"1\"]]", "output": "1", "explanation": "Single one."},
        ],
        "testCases": [
            {"function": "maximalRectangle", "input": "[[\"1\",\"0\",\"1\",\"0\",\"0\"],[\"1\",\"0\",\"1\",\"1\",\"1\"],[\"1\",\"1\",\"1\",\"1\",\"1\"],[\"1\",\"0\",\"0\",\"1\",\"0\"]]", "expectedOutput": "6"},
            {"function": "maximalRectangle", "input": "[[\"0\"]]", "expectedOutput": "0"},
            {"function": "maximalRectangle", "input": "[[\"1\"]]", "expectedOutput": "1"},
            {"function": "maximalRectangle", "input": "[[\"1\",\"1\"]]", "expectedOutput": "2"},
            {"function": "maximalRectangle", "input": "[[\"1\"],[\"1\"]]", "expectedOutput": "2"},
            {"function": "maximalRectangle", "input": "[[\"0\",\"1\"],[\"1\",\"0\"]]", "expectedOutput": "1"},
            {"function": "maximalRectangle", "input": "[[\"1\",\"1\"],[\"1\",\"1\"]]", "expectedOutput": "4"},
            {"function": "maximalRectangle", "input": "[[\"1\",\"0\"],[\"1\",\"0\"]]", "expectedOutput": "2"},
            {"function": "maximalRectangle", "input": "[[\"0\",\"0\"],[\"0\",\"0\"]]", "expectedOutput": "0"},
            {"function": "maximalRectangle", "input": "[[\"1\",\"1\",\"1\"],[\"1\",\"1\",\"1\"]]", "expectedOutput": "6"},
        ],
        "tags": ["array", "stack", "matrix", "monotonic-stack", "dynamic-programming"],
    },
    # ─── 66 ───
    {
        "slug": "min-cost-tickets",
        "title": "Minimum Cost Tickets",
        "difficulty": "medium",
        "description": (
            "A traveler plans to travel on certain days of the year (1-365). "
            "Train passes are available for 1 day ($costs[0]), 7 days ($costs[1]), or 30 days ($costs[2]). "
            "Given an array of travel days and the three costs, return the minimum total cost to cover all travel days."
        ),
        "starterCode": "def minCostTickets(days: list, costs: list) -> int:\n    pass",
        "examples": [
            {"input": "days = [1,4,6,7,8,20], costs = [2,7,15]", "output": "11", "explanation": "Buy 1-day on day1, 7-day on day4, 1-day on day20."},
            {"input": "days = [1,2,3,4,5,6,7,8,9,10,30,31], costs = [2,7,15]", "output": "17", "explanation": "30-day on day1, 1-day on day30."},
            {"input": "days = [1], costs = [2,7,15]", "output": "2", "explanation": "Single day, cheapest ticket."},
        ],
        "testCases": [
            {"function": "minCostTickets", "input": "[1,4,6,7,8,20], [2,7,15]", "expectedOutput": "11"},
            {"function": "minCostTickets", "input": "[1,2,3,4,5,6,7,8,9,10,30,31], [2,7,15]", "expectedOutput": "17"},
            {"function": "minCostTickets", "input": "[1], [2,7,15]", "expectedOutput": "2"},
            {"function": "minCostTickets", "input": "[1,2,3], [2,7,15]", "expectedOutput": "6"},
            {"function": "minCostTickets", "input": "[1,2,3,4,5,6,7], [2,7,15]", "expectedOutput": "7"},
            {"function": "minCostTickets", "input": "[1,7,14,21,28], [2,7,15]", "expectedOutput": "10"},
            {"function": "minCostTickets", "input": "[1,365], [2,7,15]", "expectedOutput": "4"},
            {"function": "minCostTickets", "input": "[1,2,3,4,5], [5,10,20]", "expectedOutput": "20"},
            {"function": "minCostTickets", "input": "[1,2], [3,5,9]", "expectedOutput": "6"},
            {"function": "minCostTickets", "input": "[1,2,3,4,5,6,7,8,9,10], [1,10,20]", "expectedOutput": "10"},
        ],
        "tags": ["dynamic-programming", "array"],
    },
    # ─── 67 ───
    {
        "slug": "valid-sudoku",
        "title": "Valid Sudoku",
        "difficulty": "medium",
        "description": (
            "Determine if a partially filled 9x9 Sudoku board is valid. "
            "A valid board means: each row, each column, and each of the nine 3x3 sub-boxes "
            "contains the digits 1-9 without repetition. Empty cells are represented by '.'. "
            "Do not need to solve it — just validate."
        ),
        "starterCode": "def isValidSudoku(board: list) -> bool:\n    pass",
        "examples": [
            {"input": "board = standard valid sudoku", "output": "True", "explanation": "All constraints satisfied."},
            {"input": "board = board with duplicate 8 in row", "output": "False", "explanation": "Row constraint violated."},
            {"input": "board = board with duplicate in box", "output": "False", "explanation": "3x3 box constraint violated."},
        ],
        "testCases": [
            {"function": "isValidSudoku", "input": "valid 9x9 board", "expectedOutput": "True"},
            {"function": "isValidSudoku", "input": "board with row duplicate", "expectedOutput": "False"},
            {"function": "isValidSudoku", "input": "board with column duplicate", "expectedOutput": "False"},
            {"function": "isValidSudoku", "input": "board with box duplicate", "expectedOutput": "False"},
            {"function": "isValidSudoku", "input": "empty board (all dots)", "expectedOutput": "True"},
            {"function": "isValidSudoku", "input": "single digit board", "expectedOutput": "True"},
            {"function": "isValidSudoku", "input": "board with all 9s in first row", "expectedOutput": "False"},
            {"function": "isValidSudoku", "input": "board with duplicate in 3rd box", "expectedOutput": "False"},
            {"function": "isValidSudoku", "input": "board with one filled valid cell", "expectedOutput": "True"},
            {"function": "isValidSudoku", "input": "board with duplicate in last column", "expectedOutput": "False"},
        ],
        "tags": ["array", "hash-table", "matrix"],
    },
    # ─── 68 ───
    {
        "slug": "design-twitter",
        "title": "Design Twitter Feed",
        "difficulty": "medium",
        "description": (
            "Design a simplified Twitter that supports: postTweet(userId, tweetId), "
            "getNewsFeed(userId) which returns the 10 most recent tweet IDs from the user and their followees, "
            "follow(followerId, followeeId), and unfollow(followerId, followeeId). "
            "Tweets should appear in most-recent-first order. Use a heap for efficient top-10 retrieval."
        ),
        "starterCode": "class Twitter:\n    def __init__(self):\n        pass\n    def postTweet(self, userId: int, tweetId: int) -> None:\n        pass\n    def getNewsFeed(self, userId: int) -> list:\n        pass\n    def follow(self, followerId: int, followeeId: int) -> None:\n        pass\n    def unfollow(self, followerId: int, followeeId: int) -> None:\n        pass",
        "examples": [
            {"input": "postTweet(1,5); getNewsFeed(1)", "output": "[5]", "explanation": "User 1 sees their own tweet."},
            {"input": "postTweet(1,5); follow(1,2); postTweet(2,6); getNewsFeed(1)", "output": "[6,5]", "explanation": "Most recent first."},
            {"input": "postTweet(1,5); follow(1,2); postTweet(2,6); unfollow(1,2); getNewsFeed(1)", "output": "[5]", "explanation": "After unfollow."},
        ],
        "testCases": [
            {"function": "Twitter", "input": "postTweet(1,5); getNewsFeed(1)", "expectedOutput": "[5]"},
            {"function": "Twitter", "input": "postTweet(1,5); follow(1,2); postTweet(2,6); getNewsFeed(1)", "expectedOutput": "[6,5]"},
            {"function": "Twitter", "input": "postTweet(1,5); follow(1,2); postTweet(2,6); unfollow(1,2); getNewsFeed(1)", "expectedOutput": "[5]"},
            {"function": "Twitter", "input": "getNewsFeed(1)", "expectedOutput": "[]"},
            {"function": "Twitter", "input": "follow(1,2); getNewsFeed(1)", "expectedOutput": "[]"},
            {"function": "Twitter", "input": "postTweet(1,1); postTweet(1,2); getNewsFeed(1)", "expectedOutput": "[2,1]"},
            {"function": "Twitter", "input": "postTweet(1,1); follow(2,1); getNewsFeed(2)", "expectedOutput": "[1]"},
            {"function": "Twitter", "input": "follow(1,1); postTweet(1,5); getNewsFeed(1)", "expectedOutput": "[5]"},
            {"function": "Twitter", "input": "postTweet(1,5); postTweet(1,3); getNewsFeed(1)", "expectedOutput": "[3,5]"},
            {"function": "Twitter", "input": "follow(1,2); unfollow(1,2); postTweet(2,7); getNewsFeed(1)", "expectedOutput": "[]"},
        ],
        "tags": ["design", "heap", "hash-table", "linked-list"],
    },
    # ─── 69 ───
    {
        "slug": "reconstruct-itinerary",
        "title": "Reconstruct Itinerary",
        "difficulty": "hard",
        "description": (
            "Given a list of airline tickets represented as [from, to] pairs, reconstruct the itinerary in order. "
            "All tickets must be used exactly once. The itinerary must begin with 'JFK'. "
            "If multiple valid itineraries exist, return the one with the smallest lexical order. "
            "Use Hierholzer's algorithm for Eulerian paths."
        ),
        "starterCode": "def findItinerary(tickets: list) -> list:\n    pass",
        "examples": [
            {"input": "tickets = [[\"MUC\",\"LHR\"],[\"JFK\",\"MUC\"],[\"SFO\",\"SJC\"],[\"LHR\",\"SFO\"]]", "output": "[\"JFK\",\"MUC\",\"LHR\",\"SFO\",\"SJC\"]", "explanation": "Complete itinerary."},
            {"input": "tickets = [[\"JFK\",\"SFO\"],[\"JFK\",\"ATL\"],[\"SFO\",\"ATL\"],[\"ATL\",\"JFK\"],[\"ATL\",\"SFO\"]]", "output": "[\"JFK\",\"ATL\",\"JFK\",\"SFO\",\"ATL\",\"SFO\"]", "explanation": "Lexicographically smallest."},
            {"input": "tickets = [[\"JFK\",\"KUL\"],[\"JFK\",\"NRT\"],[\"NRT\",\"JFK\"]]", "output": "[\"JFK\",\"NRT\",\"JFK\",\"KUL\"]", "explanation": "NRT before KUL lexicographically."},
        ],
        "testCases": [
            {"function": "findItinerary", "input": "[[\"MUC\",\"LHR\"],[\"JFK\",\"MUC\"],[\"SFO\",\"SJC\"],[\"LHR\",\"SFO\"]]", "expectedOutput": "[\"JFK\",\"MUC\",\"LHR\",\"SFO\",\"SJC\"]"},
            {"function": "findItinerary", "input": "[[\"JFK\",\"SFO\"],[\"JFK\",\"ATL\"],[\"SFO\",\"ATL\"],[\"ATL\",\"JFK\"],[\"ATL\",\"SFO\"]]", "expectedOutput": "[\"JFK\",\"ATL\",\"JFK\",\"SFO\",\"ATL\",\"SFO\"]"},
            {"function": "findItinerary", "input": "[[\"JFK\",\"KUL\"],[\"JFK\",\"NRT\"],[\"NRT\",\"JFK\"]]", "expectedOutput": "[\"JFK\",\"NRT\",\"JFK\",\"KUL\"]"},
            {"function": "findItinerary", "input": "[[\"JFK\",\"A\"],[\"A\",\"JFK\"]]", "expectedOutput": "[\"JFK\",\"A\",\"JFK\"]"},
            {"function": "findItinerary", "input": "[[\"JFK\",\"B\"],[\"JFK\",\"A\"],[\"B\",\"A\"],[\"A\",\"B\"]]", "expectedOutput": "[\"JFK\",\"A\",\"B\",\"A\",\"B\"]"},
            {"function": "findItinerary", "input": "[[\"JFK\",\"ATL\"]]", "expectedOutput": "[\"JFK\",\"ATL\"]"},
            {"function": "findItinerary", "input": "[[\"JFK\",\"A\"],[\"A\",\"B\"],[\"B\",\"JFK\"]]", "expectedOutput": "[\"JFK\",\"A\",\"B\",\"JFK\"]"},
            {"function": "findItinerary", "input": "[[\"JFK\",\"ATL\"],[\"ATL\",\"JFK\"],[\"JFK\",\"SFO\"]]", "expectedOutput": "[\"JFK\",\"ATL\",\"JFK\",\"SFO\"]"},
            {"function": "findItinerary", "input": "[[\"JFK\",\"B\"],[\"B\",\"JFK\"],[\"JFK\",\"A\"],[\"A\",\"JFK\"]]", "expectedOutput": "[\"JFK\",\"A\",\"JFK\",\"B\",\"JFK\"]"},
            {"function": "findItinerary", "input": "[[\"JFK\",\"C\"],[\"C\",\"A\"],[\"A\",\"B\"],[\"B\",\"C\"],[\"C\",\"B\"],[\"B\",\"A\"]]", "expectedOutput": "valid eulerian path from JFK"},
        ],
        "tags": ["graph", "dfs", "eulerian-path", "backtracking"],
    },
    # ─── 70 ───
    {
        "slug": "minimum-height-trees",
        "title": "Minimum Height Trees",
        "difficulty": "medium",
        "description": (
            "A tree can be rooted at any node. The height is the number of edges in the longest path to a leaf. "
            "For a given undirected tree of n nodes, find all nodes that when chosen as root minimize the tree height. "
            "Return all such root values. Use topological leaf-trimming (like peeling an onion)."
        ),
        "starterCode": "def findMinHeightTrees(n: int, edges: list) -> list:\n    pass",
        "examples": [
            {"input": "n = 4, edges = [[1,0],[1,2],[1,3]]", "output": "[1]", "explanation": "Node 1 is the center."},
            {"input": "n = 6, edges = [[3,0],[3,1],[3,2],[3,4],[5,4]]", "output": "[3,4]", "explanation": "Two central nodes."},
            {"input": "n = 1, edges = []", "output": "[0]", "explanation": "Single node."},
        ],
        "testCases": [
            {"function": "findMinHeightTrees", "input": "4, [[1,0],[1,2],[1,3]]", "expectedOutput": "[1]"},
            {"function": "findMinHeightTrees", "input": "6, [[3,0],[3,1],[3,2],[3,4],[5,4]]", "expectedOutput": "[3,4]"},
            {"function": "findMinHeightTrees", "input": "1, []", "expectedOutput": "[0]"},
            {"function": "findMinHeightTrees", "input": "2, [[0,1]]", "expectedOutput": "[0,1]"},
            {"function": "findMinHeightTrees", "input": "3, [[0,1],[0,2]]", "expectedOutput": "[0]"},
            {"function": "findMinHeightTrees", "input": "5, [[0,1],[0,2],[0,3],[3,4]]", "expectedOutput": "[0,3]"},
            {"function": "findMinHeightTrees", "input": "7, [[0,1],[1,2],[1,3],[2,4],[3,5],[4,6]]", "expectedOutput": "[1,2]"},
            {"function": "findMinHeightTrees", "input": "4, [[0,1],[1,2],[2,3]]", "expectedOutput": "[1,2]"},
            {"function": "findMinHeightTrees", "input": "3, [[0,1],[1,2]]", "expectedOutput": "[1]"},
            {"function": "findMinHeightTrees", "input": "5, [[0,1],[1,2],[2,3],[3,4]]", "expectedOutput": "[2]"},
        ],
        "tags": ["graph", "bfs", "topological-sort"],
    },
    # ─── 71–100 ───
    {
        "slug": "candy-distribution",
        "title": "Candy Distribution",
        "difficulty": "hard",
        "description": (
            "Children stand in a row, each with a rating. Distribute candies so every child gets at least one, "
            "and children with a higher rating than their neighbour get more candies. "
            "Return the minimum total number of candies needed. "
            "Use two greedy passes — left to right then right to left."
        ),
        "starterCode": "def candy(ratings: list) -> int:\n    pass",
        "examples": [
            {"input": "ratings = [1,0,2]", "output": "5", "explanation": "Give [2,1,2] candies."},
            {"input": "ratings = [1,2,2]", "output": "4", "explanation": "Give [1,2,1] candies."},
            {"input": "ratings = [1]", "output": "1", "explanation": "One child."},
        ],
        "testCases": [
            {"function": "candy", "input": "[1,0,2]", "expectedOutput": "5"},
            {"function": "candy", "input": "[1,2,2]", "expectedOutput": "4"},
            {"function": "candy", "input": "[1]", "expectedOutput": "1"},
            {"function": "candy", "input": "[1,2,3,4,5]", "expectedOutput": "15"},
            {"function": "candy", "input": "[5,4,3,2,1]", "expectedOutput": "15"},
            {"function": "candy", "input": "[1,3,2,2,1]", "expectedOutput": "7"},
            {"function": "candy", "input": "[1,2,1]", "expectedOutput": "4"},
            {"function": "candy", "input": "[1,1,1]", "expectedOutput": "3"},
            {"function": "candy", "input": "[3,2,1,2,3]", "expectedOutput": "11"},
            {"function": "candy", "input": "[1,2,3,2,1]", "expectedOutput": "9"},
        ],
        "tags": ["greedy", "array"],
    },
    {
        "slug": "alien-dictionary",
        "title": "Alien Dictionary",
        "difficulty": "hard",
        "description": (
            "A new alien language uses English letters but in an unknown order. "
            "You are given a sorted list of words in this language. "
            "Derive the alphabetical order of the alien alphabet by comparing adjacent words. "
            "Return a string of unique characters in the correct order, or empty string if invalid."
        ),
        "starterCode": "def alienOrder(words: list) -> str:\n    pass",
        "examples": [
            {"input": "words = [\"wrt\",\"wrf\",\"er\",\"ett\",\"rftt\"]", "output": "\"wertf\"", "explanation": "Derived ordering."},
            {"input": "words = [\"z\",\"x\"]", "output": "\"zx\"", "explanation": "z comes before x."},
            {"input": "words = [\"z\",\"x\",\"z\"]", "output": "\"\"", "explanation": "Cycle detected."},
        ],
        "testCases": [
            {"function": "alienOrder", "input": "[\"wrt\",\"wrf\",\"er\",\"ett\",\"rftt\"]", "expectedOutput": "\"wertf\""},
            {"function": "alienOrder", "input": "[\"z\",\"x\"]", "expectedOutput": "\"zx\""},
            {"function": "alienOrder", "input": "[\"z\",\"x\",\"z\"]", "expectedOutput": "\"\""},
            {"function": "alienOrder", "input": "[\"abc\",\"ab\"]", "expectedOutput": "\"\""},
            {"function": "alienOrder", "input": "[\"a\"]", "expectedOutput": "\"a\""},
            {"function": "alienOrder", "input": "[\"a\",\"b\",\"c\"]", "expectedOutput": "\"abc\""},
            {"function": "alienOrder", "input": "[\"ab\",\"adc\"]", "expectedOutput": "contains b before d"},
            {"function": "alienOrder", "input": "[\"ba\",\"bc\",\"ac\",\"ca\"]", "expectedOutput": "b before a, a before c"},
            {"function": "alienOrder", "input": "[\"aa\",\"ab\"]", "expectedOutput": "contains a and b"},
            {"function": "alienOrder", "input": "[\"z\",\"z\"]", "expectedOutput": "\"z\""},
        ],
        "tags": ["graph", "topological-sort", "bfs", "dfs", "string"],
    },
    {
        "slug": "cut-wood-binary-search",
        "title": "Cut Wood to Length",
        "difficulty": "medium",
        "description": (
            "A lumberjack wants to cut pieces of wood into equal lengths to get k pieces total. "
            "The lumberjack can set the saw blade to any height h and cuts all trees taller than h, "
            "collecting the excess. Given tree heights and k, find the maximum h that yields at least k pieces. "
            "Use binary search on the answer."
        ),
        "starterCode": "def cutWood(heights: list, k: int) -> int:\n    pass",
        "examples": [
            {"input": "heights = [20,15,10,17], k = 7", "output": "15", "explanation": "At h=15: collect 5+0+0+2=7."},
            {"input": "heights = [4,42,40,26,46], k = 20", "output": "36", "explanation": "At h=36: collect correct amount."},
            {"input": "heights = [1,2,3], k = 3", "output": "1", "explanation": "Collect one from each."},
        ],
        "testCases": [
            {"function": "cutWood", "input": "[20,15,10,17], 7", "expectedOutput": "15"},
            {"function": "cutWood", "input": "[4,42,40,26,46], 20", "expectedOutput": "36"},
            {"function": "cutWood", "input": "[1,2,3], 3", "expectedOutput": "1"},
            {"function": "cutWood", "input": "[10,10,10], 3", "expectedOutput": "7"},
            {"function": "cutWood", "input": "[100], 50", "expectedOutput": "50"},
            {"function": "cutWood", "input": "[5,5,5,5], 4", "expectedOutput": "4"},
            {"function": "cutWood", "input": "[1,1,1,1], 2", "expectedOutput": "0"},
            {"function": "cutWood", "input": "[100,200,300], 3", "expectedOutput": "200"},
            {"function": "cutWood", "input": "[1,2,3,4,5], 5", "expectedOutput": "2"},
            {"function": "cutWood", "input": "[3,6,9], 6", "expectedOutput": "3"},
        ],
        "tags": ["binary-search", "greedy", "array"],
    },
    {
        "slug": "matrix-diagonal-traverse",
        "title": "Matrix Diagonal Traverse",
        "difficulty": "medium",
        "description": (
            "Given an m x n matrix, return all elements in diagonal order — "
            "traverse from the top-right to bottom-left on even diagonals, "
            "and bottom-left to top-right on odd diagonals (or vice versa). "
            "Return a flat array of elements in this zigzag diagonal order."
        ),
        "starterCode": "def diagonalTraverse(mat: list) -> list:\n    pass",
        "examples": [
            {"input": "mat = [[1,2,3],[4,5,6],[7,8,9]]", "output": "[1,2,4,7,5,3,6,8,9]", "explanation": "Diagonal order."},
            {"input": "mat = [[1,2],[3,4]]", "output": "[1,2,3,4]", "explanation": "2x2 diagonal."},
            {"input": "mat = [[1]]", "output": "[1]", "explanation": "Single element."},
        ],
        "testCases": [
            {"function": "diagonalTraverse", "input": "[[1,2,3],[4,5,6],[7,8,9]]", "expectedOutput": "[1,2,4,7,5,3,6,8,9]"},
            {"function": "diagonalTraverse", "input": "[[1,2],[3,4]]", "expectedOutput": "[1,2,3,4]"},
            {"function": "diagonalTraverse", "input": "[[1]]", "expectedOutput": "[1]"},
            {"function": "diagonalTraverse", "input": "[[1,2,3]]", "expectedOutput": "[1,2,3]"},
            {"function": "diagonalTraverse", "input": "[[1],[2],[3]]", "expectedOutput": "[1,2,3]"},
            {"function": "diagonalTraverse", "input": "[[1,2],[3,4],[5,6]]", "expectedOutput": "[1,2,3,5,4,6]"},
            {"function": "diagonalTraverse", "input": "[[1,2,3],[4,5,6]]", "expectedOutput": "[1,2,4,5,3,6]"},
            {"function": "diagonalTraverse", "input": "[[1,2,3,4]]", "expectedOutput": "[1,2,3,4]"},
            {"function": "diagonalTraverse", "input": "[[1,2,3],[4,5,6],[7,8,9],[10,11,12]]", "expectedOutput": "16 elements in diagonal order"},
            {"function": "diagonalTraverse", "input": "[[1,2],[3,4],[5,6],[7,8]]", "expectedOutput": "[1,2,3,5,4,6,7,8]"},
        ],
        "tags": ["matrix", "array", "simulation"],
    },
    {
        "slug": "prison-cells-after-n-days",
        "title": "Prison Cells After N Days",
        "difficulty": "medium",
        "description": (
            "There are 8 prison cells in a row, each either occupied (1) or vacant (0). "
            "Each day, a cell becomes occupied if its two neighbours were the same the previous day, "
            "otherwise it becomes vacant. The first and last cells always become vacant. "
            "Given the initial state and n days, return the state after n days. "
            "Detect the cycle to handle large n."
        ),
        "starterCode": "def prisonAfterNDays(cells: list, n: int) -> list:\n    pass",
        "examples": [
            {"input": "cells = [0,1,0,1,1,0,0,1], n = 7", "output": "[0,0,1,1,0,0,0,0]", "explanation": "After 7 days."},
            {"input": "cells = [1,0,0,1,0,0,1,0], n = 1000000000", "output": "[0,0,1,1,1,1,1,0]", "explanation": "Cycle detected."},
            {"input": "cells = [1,1,0,1,1,0,1,1], n = 6", "output": "[0,1,0,0,1,0,0,0]", "explanation": "After 6 days."},
        ],
        "testCases": [
            {"function": "prisonAfterNDays", "input": "[0,1,0,1,1,0,0,1], 7", "expectedOutput": "[0,0,1,1,0,0,0,0]"},
            {"function": "prisonAfterNDays", "input": "[1,0,0,1,0,0,1,0], 1000000000", "expectedOutput": "[0,0,1,1,1,1,1,0]"},
            {"function": "prisonAfterNDays", "input": "[1,1,0,1,1,0,1,1], 6", "expectedOutput": "[0,1,0,0,1,0,0,0]"},
            {"function": "prisonAfterNDays", "input": "[0,0,0,0,0,0,0,0], 1", "expectedOutput": "[0,0,0,0,0,0,0,0]"},
            {"function": "prisonAfterNDays", "input": "[1,0,1,0,1,0,1,0], 1", "expectedOutput": "[0,0,0,0,0,0,0,0]"},
            {"function": "prisonAfterNDays", "input": "[0,1,0,1,1,0,0,1], 1", "expectedOutput": "[0,1,1,0,0,0,0,0]"},
            {"function": "prisonAfterNDays", "input": "[1,1,1,1,0,0,0,0], 2", "expectedOutput": "[0,1,1,0,0,0,0,0]"},
            {"function": "prisonAfterNDays", "input": "[0,0,0,0,1,1,1,0], 3", "expectedOutput": "[0,0,0,0,0,1,0,0]"},
            {"function": "prisonAfterNDays", "input": "[1,0,0,1,0,0,1,0], 1", "expectedOutput": "[0,0,0,1,0,0,1,0]"},
            {"function": "prisonAfterNDays", "input": "[0,1,0,1,1,0,0,1], 256", "expectedOutput": "cycle-based result"},
        ],
        "tags": ["array", "hash-table", "simulation"],
    },
    {
        "slug": "stone-game-dp",
        "title": "Stone Game",
        "difficulty": "medium",
        "description": (
            "Alex and Lee play a game with piles of stones in a row. "
            "On each turn the current player takes the entire leftmost or rightmost pile. "
            "Alex always goes first. Both play optimally. "
            "Given the piles array (always even length, total is odd so no tie), "
            "return True if Alex wins — Alex always wins, can you prove it mathematically?"
        ),
        "starterCode": "def stoneGame(piles: list) -> bool:\n    pass",
        "examples": [
            {"input": "piles = [5,3,4,5]", "output": "True", "explanation": "Alex wins with optimal play."},
            {"input": "piles = [3,7,2,3]", "output": "True", "explanation": "Alex always wins."},
            {"input": "piles = [1,2]", "output": "True", "explanation": "Alex takes 2."},
        ],
        "testCases": [
            {"function": "stoneGame", "input": "[5,3,4,5]", "expectedOutput": "True"},
            {"function": "stoneGame", "input": "[3,7,2,3]", "expectedOutput": "True"},
            {"function": "stoneGame", "input": "[1,2]", "expectedOutput": "True"},
            {"function": "stoneGame", "input": "[1,100,1,100]", "expectedOutput": "True"},
            {"function": "stoneGame", "input": "[2,8,1,3]", "expectedOutput": "True"},
            {"function": "stoneGame", "input": "[6,2,3,4,5,5]", "expectedOutput": "True"},
            {"function": "stoneGame", "input": "[1,1]", "expectedOutput": "True"},
            {"function": "stoneGame", "input": "[10,1,1,10]", "expectedOutput": "True"},
            {"function": "stoneGame", "input": "[5,7,9,3]", "expectedOutput": "True"},
            {"function": "stoneGame", "input": "[100,2,4,100]", "expectedOutput": "True"},
        ],
        "tags": ["dynamic-programming", "math", "greedy", "game-theory"],
    },
    {
        "slug": "surrounded-regions",
        "title": "Surrounded Regions",
        "difficulty": "medium",
        "description": (
            "Given an m x n board of 'X' and 'O', capture all regions surrounded by 'X'. "
            "A region is captured by flipping all 'O's into 'X's. "
            "An 'O' region is NOT captured if it is connected to a border 'O'. "
            "Use DFS/BFS from the border to mark safe 'O's, then flip the rest."
        ),
        "starterCode": "def solve(board: list) -> None:\n    pass",
        "examples": [
            {"input": "board = [[\"X\",\"X\",\"X\",\"X\"],[\"X\",\"O\",\"O\",\"X\"],[\"X\",\"X\",\"O\",\"X\"],[\"X\",\"O\",\"X\",\"X\"]]", "output": "[[\"X\",\"X\",\"X\",\"X\"],[\"X\",\"X\",\"X\",\"X\"],[\"X\",\"X\",\"X\",\"X\"],[\"X\",\"O\",\"X\",\"X\"]]", "explanation": "Bottom O touches border so safe."},
            {"input": "board = [[\"X\"]]", "output": "[[\"X\"]]", "explanation": "No O to capture."},
            {"input": "board = [[\"O\"]]", "output": "[[\"O\"]]", "explanation": "Border O, not captured."},
        ],
        "testCases": [
            {"function": "solve", "input": "[[\"X\",\"X\",\"X\",\"X\"],[\"X\",\"O\",\"O\",\"X\"],[\"X\",\"X\",\"O\",\"X\"],[\"X\",\"O\",\"X\",\"X\"]]", "expectedOutput": "bottom O preserved"},
            {"function": "solve", "input": "[[\"X\"]]", "expectedOutput": "[[\"X\"]]"},
            {"function": "solve", "input": "[[\"O\"]]", "expectedOutput": "[[\"O\"]]"},
            {"function": "solve", "input": "[[\"O\",\"O\"],[\"O\",\"O\"]]", "expectedOutput": "all O preserved"},
            {"function": "solve", "input": "[[\"X\",\"X\"],[\"X\",\"O\"]]", "expectedOutput": "border O preserved"},
            {"function": "solve", "input": "[[\"X\",\"O\",\"X\"],[\"O\",\"X\",\"O\"],[\"X\",\"O\",\"X\"]]", "expectedOutput": "center O captured"},
            {"function": "solve", "input": "[[\"O\",\"X\",\"X\"],[\"X\",\"O\",\"X\"],[\"X\",\"X\",\"O\"]]", "expectedOutput": "border Os safe, center captured"},
            {"function": "solve", "input": "[[\"X\",\"X\",\"X\"],[\"X\",\"O\",\"X\"],[\"X\",\"X\",\"X\"]]", "expectedOutput": "[[\"X\",\"X\",\"X\"],[\"X\",\"X\",\"X\"],[\"X\",\"X\",\"X\"]]"},
            {"function": "solve", "input": "[[\"O\",\"O\",\"O\"],[\"O\",\"X\",\"O\"],[\"O\",\"O\",\"O\"]]", "expectedOutput": "all O preserved"},
            {"function": "solve", "input": "[[\"X\",\"O\",\"X\"],[\"O\",\"O\",\"O\"],[\"X\",\"O\",\"X\"]]", "expectedOutput": "all O preserved via border"},
        ],
        "tags": ["graph", "dfs", "bfs", "matrix", "union-find"],
    },
    {
        "slug": "pacific-atlantic-water",
        "title": "Pacific Atlantic Water Flow",
        "difficulty": "medium",
        "description": (
            "Rain water can flow to adjacent cells (4 directions) with equal or lower height. "
            "Given an m x n grid of heights, find all cells from which water can flow to both the Pacific Ocean "
            "(top/left border) and the Atlantic Ocean (bottom/right border). "
            "Use reverse BFS/DFS from each border."
        ),
        "starterCode": "def pacificAtlantic(heights: list) -> list:\n    pass",
        "examples": [
            {"input": "heights = [[1,2,2,3,5],[3,2,3,4,4],[2,4,5,3,1],[6,7,1,4,5],[5,1,1,2,4]]", "output": "[[0,4],[1,3],[1,4],[2,2],[3,0],[3,1],[4,0]]", "explanation": "7 cells can reach both oceans."},
            {"input": "heights = [[1]]", "output": "[[0,0]]", "explanation": "Single cell touches both."},
            {"input": "heights = [[1,2],[4,3]]", "output": "[[0,1],[1,0],[1,1]]", "explanation": "Three cells."},
        ],
        "testCases": [
            {"function": "pacificAtlantic", "input": "[[1,2,2,3,5],[3,2,3,4,4],[2,4,5,3,1],[6,7,1,4,5],[5,1,1,2,4]]", "expectedOutput": "7 cells"},
            {"function": "pacificAtlantic", "input": "[[1]]", "expectedOutput": "[[0,0]]"},
            {"function": "pacificAtlantic", "input": "[[1,2],[4,3]]", "expectedOutput": "[[0,1],[1,0],[1,1]]"},
            {"function": "pacificAtlantic", "input": "[[1,1],[1,1]]", "expectedOutput": "all 4 cells"},
            {"function": "pacificAtlantic", "input": "[[1,2,3],[8,9,4],[7,6,5]]", "expectedOutput": "[[0,2],[1,1],[1,2],[2,0],[2,1],[2,2]]"},
            {"function": "pacificAtlantic", "input": "[[3,3,3],[3,1,3],[0,2,4]]", "expectedOutput": "cells reaching both"},
            {"function": "pacificAtlantic", "input": "[[1,2],[2,1]]", "expectedOutput": "[[0,1],[1,0]]"},
            {"function": "pacificAtlantic", "input": "[[10,10,10],[10,1,10],[10,10,10]]", "expectedOutput": "border cells"},
            {"function": "pacificAtlantic", "input": "[[1,3],[3,1]]", "expectedOutput": "[[0,1],[1,0]]"},
            {"function": "pacificAtlantic", "input": "[[5,5],[5,5]]", "expectedOutput": "all 4 cells"},
        ],
        "tags": ["graph", "dfs", "bfs", "matrix"],
    },
    {
        "slug": "accounts-merge",
        "title": "Accounts Merge",
        "difficulty": "medium",
        "description": (
            "Each account is a list of strings where the first element is the account name, "
            "and the rest are email addresses belonging to that account. "
            "Two accounts belong to the same person if they share a common email. "
            "Merge all accounts of the same person, sort emails, and return the merged accounts. "
            "Use Union-Find or DFS."
        ),
        "starterCode": "def accountsMerge(accounts: list) -> list:\n    pass",
        "examples": [
            {"input": "accounts = [[\"John\",\"johnsmith@mail.com\",\"john_newyork@mail.com\"],[\"John\",\"johnsmith@mail.com\",\"john00@mail.com\"],[\"Mary\",\"mary@mail.com\"],[\"John\",\"johnnybravo@mail.com\"]]", "output": "3 accounts", "explanation": "First two Johns merged."},
            {"input": "accounts = [[\"Gabe\",\"Gabe0@m.co\",\"Gabe3@m.co\",\"Gabe1@m.co\"],[\"Kevin\",\"Kevin3@m.co\",\"Kevin5@m.co\"],[\"Ethan\",\"Ethan5@m.co\",\"Ethan4@m.co\"],[\"Hanzo\",\"Hanzo3@m.co\",\"Hanzo1@m.co\"],[\"Fern\",\"Fern5@m.co\",\"Fern1@m.co\"]]", "output": "5 accounts", "explanation": "No merging needed."},
            {"input": "accounts = [[\"a\",\"a@a.com\"],[\"b\",\"b@b.com\"]]", "output": "2 accounts", "explanation": "No shared emails."},
        ],
        "testCases": [
            {"function": "accountsMerge", "input": "[[\"John\",\"a@a.com\",\"b@b.com\"],[\"John\",\"a@a.com\"]]", "expectedOutput": "1 merged account"},
            {"function": "accountsMerge", "input": "[[\"a\",\"a@a.com\"],[\"b\",\"b@b.com\"]]", "expectedOutput": "2 accounts"},
            {"function": "accountsMerge", "input": "[[\"John\",\"a@a.com\"],[\"John\",\"b@b.com\"]]", "expectedOutput": "2 accounts"},
            {"function": "accountsMerge", "input": "[[\"John\",\"a@a.com\"],[\"John\",\"a@a.com\",\"b@b.com\"],[\"John\",\"b@b.com\"]]", "expectedOutput": "1 merged account"},
            {"function": "accountsMerge", "input": "[[\"a\",\"1@m\"],[\"b\",\"2@m\"],[\"c\",\"1@m\",\"2@m\"]]", "expectedOutput": "1 merged account"},
            {"function": "accountsMerge", "input": "[[\"Mary\",\"m@m.com\"]]", "expectedOutput": "1 account"},
            {"function": "accountsMerge", "input": "[[\"a\",\"x@m\"],[\"a\",\"y@m\"],[\"a\",\"x@m\",\"y@m\"]]", "expectedOutput": "1 merged account"},
            {"function": "accountsMerge", "input": "[[\"A\",\"a@a.com\",\"b@b.com\"],[\"B\",\"b@b.com\",\"c@c.com\"],[\"C\",\"c@c.com\"]]", "expectedOutput": "1 chain merged"},
            {"function": "accountsMerge", "input": "[[\"A\",\"a@a.com\"],[\"B\",\"b@b.com\"],[\"C\",\"c@c.com\"]]", "expectedOutput": "3 accounts"},
            {"function": "accountsMerge", "input": "[[\"a\",\"x@m\",\"y@m\"],[\"b\",\"z@m\"],[\"c\",\"y@m\",\"z@m\"]]", "expectedOutput": "1 merged account"},
        ],
        "tags": ["graph", "union-find", "dfs", "sorting", "string"],
    },
    {
        "slug": "word-search-ii",
        "title": "Word Search II",
        "difficulty": "hard",
        "description": (
            "Given an m x n board of characters and a list of words, "
            "return all words that can be found in the board. "
            "Words are formed by sequentially adjacent cells (horizontally or vertically), "
            "and no cell may be reused within one word. "
            "Use a Trie to prune the search space efficiently."
        ),
        "starterCode": "def findWords(board: list, words: list) -> list:\n    pass",
        "examples": [
            {"input": "board = [[\"o\",\"a\",\"a\",\"n\"],[\"e\",\"t\",\"a\",\"e\"],[\"i\",\"h\",\"k\",\"r\"],[\"i\",\"f\",\"l\",\"v\"]], words = [\"oath\",\"pea\",\"eat\",\"rain\"]", "output": "[\"eat\",\"oath\"]", "explanation": "Two words found."},
            {"input": "board = [[\"a\",\"b\"],[\"c\",\"d\"]], words = [\"abcd\"]", "output": "[]", "explanation": "Path not possible."},
            {"input": "board = [[\"a\"]], words = [\"a\"]", "output": "[\"a\"]", "explanation": "Single cell."},
        ],
        "testCases": [
            {"function": "findWords", "input": "[[\"o\",\"a\",\"a\",\"n\"],[\"e\",\"t\",\"a\",\"e\"],[\"i\",\"h\",\"k\",\"r\"],[\"i\",\"f\",\"l\",\"v\"]], [\"oath\",\"pea\",\"eat\",\"rain\"]", "expectedOutput": "[\"eat\",\"oath\"]"},
            {"function": "findWords", "input": "[[\"a\",\"b\"],[\"c\",\"d\"]], [\"abcd\"]", "expectedOutput": "[]"},
            {"function": "findWords", "input": "[[\"a\"]], [\"a\"]", "expectedOutput": "[\"a\"]"},
            {"function": "findWords", "input": "[[\"a\"]], [\"b\"]", "expectedOutput": "[]"},
            {"function": "findWords", "input": "[[\"a\",\"b\"],[\"a\",\"a\"]], [\"aba\",\"baa\",\"bab\",\"aaab\",\"aaa\",\"aaaa\",\"aaba\"]", "expectedOutput": "multiple found"},
            {"function": "findWords", "input": "[[\"a\",\"b\"],[\"c\",\"d\"]], [\"ab\",\"cb\",\"ad\",\"bd\",\"ac\",\"ca\",\"da\",\"bc\",\"db\",\"adcb\"]", "expectedOutput": "multiple found"},
            {"function": "findWords", "input": "[[\"a\",\"a\"]], [\"aaa\"]", "expectedOutput": "[]"},
            {"function": "findWords", "input": "[[\"a\",\"b\",\"c\"],[\"d\",\"e\",\"f\"]], [\"abc\",\"def\"]", "expectedOutput": "[\"abc\",\"def\"]"},
            {"function": "findWords", "input": "[[\"o\",\"a\"],[\"t\",\"h\"]], [\"oath\"]", "expectedOutput": "[\"oath\"]"},
            {"function": "findWords", "input": "[[\"a\",\"b\"],[\"c\",\"d\"]], [\"ac\",\"bd\"]", "expectedOutput": "[\"ac\",\"bd\"]"},
        ],
        "tags": ["trie", "dfs", "backtracking", "matrix"],
    },
    {
        "slug": "jump-game-min-jumps",
        "title": "Jump Game Min Jumps",
        "difficulty": "medium",
        "description": (
            "Given an integer array where each element is the maximum jump from that position, "
            "return the minimum number of jumps to reach the last index. "
            "It is guaranteed you can always reach the last index. "
            "Use a greedy approach tracking the current reach and the farthest reachable position."
        ),
        "starterCode": "def minJumps(nums: list) -> int:\n    pass",
        "examples": [
            {"input": "nums = [2,3,1,1,4]", "output": "2", "explanation": "Jump 1 step to index 1, then 3 steps to end."},
            {"input": "nums = [2,3,0,1,4]", "output": "2", "explanation": "Same minimum jumps."},
            {"input": "nums = [1,1,1,1]", "output": "3", "explanation": "Jump one step at a time."},
        ],
        "testCases": [
            {"function": "minJumps", "input": "[2,3,1,1,4]", "expectedOutput": "2"},
            {"function": "minJumps", "input": "[2,3,0,1,4]", "expectedOutput": "2"},
            {"function": "minJumps", "input": "[1,1,1,1]", "expectedOutput": "3"},
            {"function": "minJumps", "input": "[1]", "expectedOutput": "0"},
            {"function": "minJumps", "input": "[10,1,1,1]", "expectedOutput": "1"},
            {"function": "minJumps", "input": "[1,2,1,1,1]", "expectedOutput": "3"},
            {"function": "minJumps", "input": "[3,2,1,1,4]", "expectedOutput": "2"},
            {"function": "minJumps", "input": "[1,1]", "expectedOutput": "1"},
            {"function": "minJumps", "input": "[5,9,3,2,1,0,2,3,3,1,0,0]", "expectedOutput": "3"},
            {"function": "minJumps", "input": "[2,1,2,1,1]", "expectedOutput": "2"},
        ],
        "tags": ["greedy", "array", "dynamic-programming", "bfs"],
    },
    {
        "slug": "binary-tree-right-view",
        "title": "Binary Tree Right Side View",
        "difficulty": "medium",
        "description": (
            "Imagine standing to the right of a binary tree and looking leftward. "
            "You can see exactly one node per level — the rightmost node at each depth. "
            "Given the tree root, return the values of the nodes visible from the right side, "
            "from top to bottom. Use BFS level order traversal."
        ),
        "starterCode": "class TreeNode:\n    def __init__(self, val=0, left=None, right=None):\n        self.val = val\n        self.left = left\n        self.right = right\n\ndef rightSideView(root) -> list:\n    pass",
        "examples": [
            {"input": "root = [1,2,3,null,5,null,4]", "output": "[1,3,4]", "explanation": "Rightmost node per level."},
            {"input": "root = [1,null,3]", "output": "[1,3]", "explanation": "Right child visible."},
            {"input": "root = []", "output": "[]", "explanation": "Empty tree."},
        ],
        "testCases": [
            {"function": "rightSideView", "input": "[1,2,3,null,5,null,4]", "expectedOutput": "[1,3,4]"},
            {"function": "rightSideView", "input": "[1,null,3]", "expectedOutput": "[1,3]"},
            {"function": "rightSideView", "input": "[]", "expectedOutput": "[]"},
            {"function": "rightSideView", "input": "[1]", "expectedOutput": "[1]"},
            {"function": "rightSideView", "input": "[1,2]", "expectedOutput": "[1,2]"},
            {"function": "rightSideView", "input": "[1,null,2]", "expectedOutput": "[1,2]"},
            {"function": "rightSideView", "input": "[1,2,3,4]", "expectedOutput": "[1,3,4]"},
            {"function": "rightSideView", "input": "[1,2,3,null,null,4]", "expectedOutput": "[1,3,4]"},
            {"function": "rightSideView", "input": "[3,9,20,null,null,15,7]", "expectedOutput": "[3,20,7]"},
            {"function": "rightSideView", "input": "[1,2,3,4,5,6,7]", "expectedOutput": "[1,3,7]"},
        ],
        "tags": ["tree", "bfs", "dfs", "binary-tree"],
    },
    {
        "slug": "find-leaves-binary-tree",
        "title": "Find Leaves of Binary Tree",
        "difficulty": "medium",
        "description": (
            "Collect leaf nodes from a binary tree layer by layer: first collect all leaves, "
            "remove them, then collect the new leaves, and so on until the tree is empty. "
            "Return a list of lists, where each inner list contains the leaf values at each collection step. "
            "Use DFS with height calculation."
        ),
        "starterCode": "class TreeNode:\n    def __init__(self, val=0, left=None, right=None):\n        self.val = val\n        self.left = left\n        self.right = right\n\ndef findLeaves(root) -> list:\n    pass",
        "examples": [
            {"input": "root = [1,2,3,4,5]", "output": "[[4,5,3],[2],[1]]", "explanation": "Leaves collected in rounds."},
            {"input": "root = [1]", "output": "[[1]]", "explanation": "Single node is a leaf."},
            {"input": "root = [1,2]", "output": "[[2],[1]]", "explanation": "Two rounds."},
        ],
        "testCases": [
            {"function": "findLeaves", "input": "[1,2,3,4,5]", "expectedOutput": "[[4,5,3],[2],[1]]"},
            {"function": "findLeaves", "input": "[1]", "expectedOutput": "[[1]]"},
            {"function": "findLeaves", "input": "[1,2]", "expectedOutput": "[[2],[1]]"},
            {"function": "findLeaves", "input": "[1,2,3]", "expectedOutput": "[[2,3],[1]]"},
            {"function": "findLeaves", "input": "[1,null,2]", "expectedOutput": "[[2],[1]]"},
            {"function": "findLeaves", "input": "[1,2,null,3]", "expectedOutput": "[[3],[2],[1]]"},
            {"function": "findLeaves", "input": "[1,2,3,4,null,5]", "expectedOutput": "[[4,5,3],[2],[1]]"},
            {"function": "findLeaves", "input": "[5,3,8,1,4,7,9]", "expectedOutput": "[[1,4,7,9],[3,8],[5]]"},
            {"function": "findLeaves", "input": "[1,2,3,4,5,6,7]", "expectedOutput": "[[4,5,6,7],[2,3],[1]]"},
            {"function": "findLeaves", "input": "[1,2,null,3,null,4]", "expectedOutput": "[[4],[3],[2],[1]]"},
        ],
        "tags": ["tree", "dfs", "binary-tree"],
    },
    {
        "slug": "number-of-ways-to-decode",
        "title": "Number of Ways to Decode II",
        "difficulty": "hard",
        "description": (
            "Extend the decode ways problem to support wildcard '*' which represents digits 1-9. "
            "Count the total number of ways to decode the string. "
            "Return the count modulo 10^9 + 7. "
            "Use dynamic programming with careful handling of '*' cases."
        ),
        "starterCode": "def numDecodings(s: str) -> int:\n    pass",
        "examples": [
            {"input": "s = \"*\"", "output": "9", "explanation": "9 single-digit options."},
            {"input": "s = \"1*\"", "output": "18", "explanation": "10 two-digit combos + 9 separate."},
            {"input": "s = \"2*\"", "output": "15", "explanation": "11-19 single pair + 21-26 two pairs."},
        ],
        "testCases": [
            {"function": "numDecodings", "input": "\"*\"", "expectedOutput": "9"},
            {"function": "numDecodings", "input": "\"1*\"", "expectedOutput": "18"},
            {"function": "numDecodings", "input": "\"2*\"", "expectedOutput": "15"},
            {"function": "numDecodings", "input": "\"0\"", "expectedOutput": "0"},
            {"function": "numDecodings", "input": "\"**\"", "expectedOutput": "96"},
            {"function": "numDecodings", "input": "\"1\"", "expectedOutput": "1"},
            {"function": "numDecodings", "input": "\"*1\"", "expectedOutput": "11"},
            {"function": "numDecodings", "input": "\"*0\"", "expectedOutput": "2"},
            {"function": "numDecodings", "input": "\"*12\"", "expectedOutput": "6"},
            {"function": "numDecodings", "input": "\"1*2\"", "expectedOutput": "7"},
        ],
        "tags": ["dynamic-programming", "string"],
    },
    {
        "slug": "median-two-sorted-arrays",
        "title": "Median of Two Sorted Arrays",
        "difficulty": "hard",
        "description": (
            "Given two sorted arrays nums1 and nums2, return the median of the combined sorted array. "
            "The overall run time must be O(log(m+n)). "
            "Use binary search to partition both arrays such that left halves contain exactly half the total elements."
        ),
        "starterCode": "def findMedianSortedArrays(nums1: list, nums2: list) -> float:\n    pass",
        "examples": [
            {"input": "nums1 = [1,3], nums2 = [2]", "output": "2.0", "explanation": "Combined [1,2,3], median 2."},
            {"input": "nums1 = [1,2], nums2 = [3,4]", "output": "2.5", "explanation": "Combined [1,2,3,4], median (2+3)/2."},
            {"input": "nums1 = [0,0], nums2 = [0,0]", "output": "0.0", "explanation": "All zeros."},
        ],
        "testCases": [
            {"function": "findMedianSortedArrays", "input": "[1,3], [2]", "expectedOutput": "2.0"},
            {"function": "findMedianSortedArrays", "input": "[1,2], [3,4]", "expectedOutput": "2.5"},
            {"function": "findMedianSortedArrays", "input": "[0,0], [0,0]", "expectedOutput": "0.0"},
            {"function": "findMedianSortedArrays", "input": "[], [1]", "expectedOutput": "1.0"},
            {"function": "findMedianSortedArrays", "input": "[2], []", "expectedOutput": "2.0"},
            {"function": "findMedianSortedArrays", "input": "[1,3], [2,4]", "expectedOutput": "2.5"},
            {"function": "findMedianSortedArrays", "input": "[1,2,3], [4,5,6]", "expectedOutput": "3.5"},
            {"function": "findMedianSortedArrays", "input": "[1,3,5], [2,4,6]", "expectedOutput": "3.5"},
            {"function": "findMedianSortedArrays", "input": "[1,2], [3,4,5,6]", "expectedOutput": "3.5"},
            {"function": "findMedianSortedArrays", "input": "[1], [2,3,4,5]", "expectedOutput": "3.0"},
        ],
        "tags": ["array", "binary-search", "divide-and-conquer"],
    },
    {
        "slug": "regular-expression-match",
        "title": "Regular Expression Matching",
        "difficulty": "hard",
        "description": (
            "Implement regular expression matching with '.' (matches any single character) "
            "and '*' (matches zero or more of the preceding element). "
            "The matching must cover the entire input string. "
            "Given strings s and p, return True if s matches pattern p. "
            "Use dynamic programming."
        ),
        "starterCode": "def isMatch(s: str, p: str) -> bool:\n    pass",
        "examples": [
            {"input": "s = \"aa\", p = \"a\"", "output": "False", "explanation": "Pattern can't match both a's."},
            {"input": "s = \"aa\", p = \"a*\"", "output": "True", "explanation": "a* matches two a's."},
            {"input": "s = \"ab\", p = \".*\"", "output": "True", "explanation": ".* matches any string."},
        ],
        "testCases": [
            {"function": "isMatch", "input": "\"aa\", \"a\"", "expectedOutput": "False"},
            {"function": "isMatch", "input": "\"aa\", \"a*\"", "expectedOutput": "True"},
            {"function": "isMatch", "input": "\"ab\", \".*\"", "expectedOutput": "True"},
            {"function": "isMatch", "input": "\"aab\", \"c*a*b\"", "expectedOutput": "True"},
            {"function": "isMatch", "input": "\"mississippi\", \"mis*is*p*.\"", "expectedOutput": "False"},
            {"function": "isMatch", "input": "\"\", \"\"", "expectedOutput": "True"},
            {"function": "isMatch", "input": "\"\", \"a*\"", "expectedOutput": "True"},
            {"function": "isMatch", "input": "\"a\", \".\"", "expectedOutput": "True"},
            {"function": "isMatch", "input": "\"a\", \"a.\"", "expectedOutput": "False"},
            {"function": "isMatch", "input": "\"abc\", \"a.c\"", "expectedOutput": "True"},
        ],
        "tags": ["dynamic-programming", "string", "recursion"],
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
