# Problem Set 4A
# Name: <your name here>
# Collaborators:
# Time Spent: x:xx

def get_permutations(sequence):
    '''
    Enumerate all permutations of a given string

    sequence (string): an arbitrary string to permute. Assume that it is a
    non-empty string.  

    You MUST use recursion for this part. Non-recursive solutions will not be
    accepted.

    Returns: a list of all permutations of sequence

    Example:
    >>> get_permutations('abc')
    ['abc', 'acb', 'bac', 'bca', 'cab', 'cba']

    Note: depending on your implementation, you may return the permutations in
    a different order than what is listed here.
    '''

    #Base case
    seq_list = list(sequence)
    if len(seq_list) == 0:
        return []
    elif len(seq_list) == 1:
        return [seq_list]
    else:
        l = []
        for i in range(len(seq_list)):
            element = seq_list[i]
            restElement = seq_list[:i] + seq_list[i+1:] #list of the rest of elements
            for p in get_permutations(restElement):
                l.append([element]+ p )

    return l






if __name__ == '__main__':
#    #EXAMPLE
#    example_input = 'abc'
#    print('Input:', example_input)
#    print('Expected Output:', ['abc', 'acb', 'bac', 'bca', 'cab', 'cba'])
#    print('Actual Output:', get_permutations(example_input))
    
#    # Put three example test cases here (for your sanity, limit your inputs
#    to be three characters or fewer as you will have n! permutations for a 
#    sequence of length n)
    example_input ='abc'

    print('Input: ', example_input)
    print('Output: ', get_permutations(example_input))
