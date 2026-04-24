#!/usr/bin/env python
# Test detect_profile_update
import sys
sys.path.insert(0, '.')

from utils.helpers import detect_profile_update, extract_episode

print("Test 1: detect_profile_update")
result = detect_profile_update("My name is John and I'm a developer")
print(f"Result: {result}")
print(f"Type: {type(result)}")

print("\nTest 2: extract_episode")
result2 = extract_episode("I went to Paris yesterday")
print(f"Result: {result2}")
