from django.test import TestCase

# Create your tests here.

# create sample dict
sample_dict = {
    'a': 1,
    'b': 2,
    'c': 3}

# run for in dict
for key, value in sample_dict.items():
    print(key, value)
    