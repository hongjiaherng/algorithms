from copy import deepcopy

class Sort:
    def __init__(self, verbose=False):
        self.set_verbosity(verbose)

    def set_verbosity(self, verbose=False):
        self.__verbose = verbose
        self.__verboseprint = print if self.__verbose else lambda *a, **k:None

    def bubble_sort(self, input):
        """
        Bubble sort
        
        Parameters
        ----------
        input : python list
            unsorted array
        """
        # Create a duplicate of input array
        output = deepcopy(input)

        self.__verboseprint(f"input : {input}")

        # Bubble sort
        for i in range(len(output) - 1, -1, -1):
            self.__verboseprint(f"i = {i} : ")
            for j in range(1, i + 1):
                self.__verboseprint(f"\tj = {j} : {output}")
                if output[j - 1] > output[j]:
                    temp = output[j - 1]
                    output[j - 1] = output[j]
                    output[j] = temp

        self.__verboseprint(f"output : {output}")
        return output
    
    def counting_sort(self, input, k):
        """
        Counting sort (stable sorting - The relative order of keys with equal value is preserved here)
        
        Don't support negative number in the array.

        Parameters
        ----------
        input : python list
            unsorted array
        k : int
            max value in unsorted array
        """

        # Initialize output and count array
        output = [None for i in range(len(input))]
        count = [0 for i in range(k+1)]

        self.__verboseprint(f"input : {input}")
        self.__verboseprint(f"output : {output} \t (initialization)")
        self.__verboseprint(f"count : {count} \t (initialization)")

        # Count the occurance of each key, e.g., count[3] contains the occurance count of key number 3)
        for i in range(len(input)):
            key = input[i]
            count[key] += 1
        
        self.__verboseprint(f"count : {count} \t (count the occurance of each key, e.g., count[3] contains the occurance count of number 3)")

        # Make every element the cumulative of previous elements, then count[key] - 1 is now telling the location of key in output array)
        for i in range(1, len(count)):
            count[i] += count[i-1]

        self.__verboseprint(f"count : {count} \t (make every element the cumulative of previous elements, count[key] - 1 is now telling the location of key in output array)")

        # Loop through the input array from behind
        for i in range(len(input) - 1, -1, -1):

            # Get the new index location of each key
            key = input[i]
            new_loc = count[key] - 1

            self.__verboseprint(f"i = {i}, key = {key}")
            self.__verboseprint(f"\tnew location of key : index {new_loc} \t (determined by count[key] - 1)")
            self.__verboseprint(f"\tcount : {count} \t (before decrement count of key = {key})")

            # Set the key to the new index location in output array
            output[new_loc] = key

            # Decrement the count of key to tell the new location of the same key
            count[key] -= 1

            self.__verboseprint(f"\tcount : {count} \t (after decrement count of key = {key})")
            self.__verboseprint(f"\toutput : {output} \t (key = {key} is inserted into index {new_loc})")

        self.__verboseprint(f"output : {output}")
        return output


# Bubble sort's driver code
# arr = [5, 1, 12, -5, 16]
sort = Sort(verbose=False)
# sort.bubble_sort(arr)

# Counting sort's
arr = [4, 1, 3, 4, 3]
sort.counting_sort(arr, k=max(arr))