# 
# Define a function named all_equal that takes a list and checks whether all elements in the list are the same. 
# For example, calling all_equal([1, 1, 1]) should return True.

# My shit incorrect solution
def all_equal(arr):
    arr = list(arr)
    # Originally there was a loop here
    if arr == arr:
        return True
    else: 
        return False

print(all_equal([1, 1, 1]))
print(all_equal([1, 1, 0]))

def all_equal(lst):
    # Check if list empty
    if not lst:
        return True
    first_elem = lst[0]
    
    # So I was right there is a loop
    for elem in lst:
        if elem != first_elem:
            return False
    return True

# The 7 lines of code I failed to write.
def all_equal(lst):
    if not lst:
        return True
    first_elem = lst[0]
    for elem in lst:
        if elem != first_elem:
            return False
    return True

print(all_equal([1, 1, 1]))  # Should return True
print(all_equal([1, 2, 1]))  # Should return False
print(all_equal([])) # Return True if empty