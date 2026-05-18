#!/usr/bin/env python
"""Test the new execution strategy system"""
import requests
import json
import time

BASE_URL = 'http://localhost:5000'

def test_function_problem():
    """Test function-based problem (Two Sum)"""
    print("\n=== Testing Function-Based Problem (Two Sum) ===")
    
    # Login
    login_resp = requests.post(f'{BASE_URL}/auth/login', json={
        'email': 'test@example.com',
        'password': 'test1234'
    })
    token = login_resp.json().get('token') or login_resp.json().get('access_token')
    if not token:
        print(f"Login failed: {login_resp.json()}")
        return
    
    # Get project ID
    projects_resp = requests.get(f'{BASE_URL}/projects', headers={
        'Authorization': f'Bearer {token}'
    })
    project_id = projects_resp.json()[0]['id']
    
    # Run code
    run_resp = requests.post(f'{BASE_URL}/submissions/run', 
        headers={
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        },
        json={
            'problemSlug': 'two-sum',
            'projectId': project_id,
            'code': '''def solution(nums, target):
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []'''
        }
    )
    
    result = run_resp.json()
    print(f"Status: {result.get('status')}")
    print(f"Passed: {result.get('passedTests')}/{result.get('totalTests')}")
    if result.get('errorOutput'):
        print(f"Error: {result.get('errorOutput')}")
    return result.get('status') == 'accepted'


def test_class_problem():
    """Test class-based problem (Range Sum Query)"""
    print("\n=== Testing Class-Based Problem (Range Sum Query) ===")
    
    # Login
    login_resp = requests.post(f'{BASE_URL}/auth/login', json={
        'email': 'test@example.com',
        'password': 'test1234'
    })
    token = login_resp.json().get('token') or login_resp.json().get('access_token')
    
    # Get project ID
    projects_resp = requests.get(f'{BASE_URL}/projects', headers={
        'Authorization': f'Bearer {token}'
    })
    projects = projects_resp.json()
    if isinstance(projects, dict):
        project_id = projects.get('id')
    else:
        project_id = projects[0]['id']
    
    # Run code
    run_resp = requests.post(f'{BASE_URL}/submissions/run', 
        headers={
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        },
        json={
            'problemSlug': 'range-sum-query',
            'projectId': project_id,
            'code': '''class RangeSumQuery:
    def __init__(self, nums):
        self.prefix = [0]
        for num in nums:
            self.prefix.append(self.prefix[-1] + num)
    
    def sumRange(self, left, right):
        return self.prefix[right + 1] - self.prefix[left]'''
        }
    )
    
    result = run_resp.json()
    print(f"Status: {result.get('status')}")
    print(f"Passed: {result.get('passedTests')}/{result.get('totalTests')}")
    if result.get('errorOutput'):
        print(f"Error: {result.get('errorOutput')}")
    return result.get('status') == 'accepted'


if __name__ == '__main__':
    print("Testing New Execution Strategy System")
    print("=" * 50)
    
    func_ok = test_function_problem()
    time.sleep(2)
    class_ok = test_class_problem()
    
    print("\n" + "=" * 50)
    print("SUMMARY:")
    print(f"  Function-based: {'✓ PASS' if func_ok else '✗ FAIL'}")
    print(f"  Class-based: {'✓ PASS' if class_ok else '✗ FAIL'}")
