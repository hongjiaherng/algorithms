from copy import deepcopy
import math

class Sort:

    def insertion_sort(self, input):
        """
        Insertion sort

        Time complexity : 
            average and worst case : O(n^2)
            best case : O(n)

        Parameters
        ----------
        input : python list
            unsorted array
        """
        output = deepcopy(input)

        for i in range(1, len(output)):
            key = output[i]
            j = i - 1

            while j >= 0 and key < output[j]:
                output[j + 1] = output[j]
                j -= 1

            output[j + 1] = key

        return output

    def bubble_sort(self, input):
        """
        Bubble sort

        Time complexity : 
            average & worst case : O(n^2)
            best case : O(n)
        
        Parameters
        ----------
        input : python list
            unsorted array
        """
        # Create a duplicate of input array
        output = deepcopy(input)
        
        # Bubble sort
        for i in range(len(output) - 1, -1, -1):

            for j in range(1, i + 1):

                if output[j - 1] > output[j]:
                    temp = output[j - 1]
                    output[j - 1] = output[j]
                    output[j] = temp

        return output
    
    def counting_sort(self, input, by_placevalue=False, place_val=1):
        """
        Counting sort 
        
        Time complexity : 
            Best, worst, and average : O(n+k)
        
        - Stable sort -> this implementation is stable, i.e. the relative order of keys with equal value is preserved here
        - Don't support negative number in the array.
        - Support sorting based on place value (make it usable within radix sort)

        Parameters
        ----------
        input : python list
            unsorted array
        by_placevalue : boolean
            set True if wanting to sort based on place value (use for Radix Sort)
        place_val : int
            set place value digit (e.g., 1, 10, 100, 1000, ...) if wanting to sort based on place value (use for Radix Sort)
        """
        # Get max value in input array
        k = max(input) if not by_placevalue else 9

        # Initialize output and count array
        output = [None for i in range(len(input))]
        count = [0 for i in range(k+1)]

        # Count the occurance of each key, e.g., count[3] contains the occurance count of key number 3)
        for i in range(len(input)):
            key = input[i] if not by_placevalue else input[i] // place_val % 10
            count[key] += 1

        # Make every element the cumulative of previous elements, then count[key] - 1 is now telling the location of key in output array)
        for i in range(1, len(count)):
            count[i] += count[i-1]

        # Loop through the input array from behind
        for i in range(len(input) - 1, -1, -1):

            # Get the new index location of each key
            key = input[i] if not by_placevalue else input[i] // place_val % 10
            new_loc = count[key] - 1

            # Set the key to the new index location in output array
            output[new_loc] = input[i]

            # Decrement the count of key to tell the new location of the same key
            count[key] -= 1

        return output

    def radix_sort(self, input):
        """
        Radix sort 
        
        Time complexity : 
            Best, worst, and average case : O(d(n+k))

        - Utilizes counting sort internally for each place value's sort

        Parameters
        ----------
        input : python list
            unsorted array
        """
        # Make a deepcopy of input for cleaner code
        output = deepcopy(input)
        
        # Get maximum element
        k = max(input)

        # Apply counting sort to sort elements based on place value.
        place = 1
        
        # Apply counting sort to sort elements based on place value (i.e., starts from 1-digit, 10-digit, ...)
        while k // place > 0:
            output = self.counting_sort(output, by_placevalue=True, place_val=place)
            place *= 10

        return output

    def bucket_sort(self, input):
        """
        Bucket sort for whole numbers (>= 0)
        
        Time complexity : 
            Average and best case : O(n)
            Worst case : O(n^2)

        - Utilizes insertion sort internally for sorting elements in each bucket
        - Used when input is uniformly distributed over a range

        Parameters
        ----------
        input : python list
            unsorted array
        """

        n = len(input)
        output = []

        # Initialize a list of buckets in which each bucket contains an array
        buckets = [list() for i in range(n)]
        divider = math.ceil(max(input) / n)

        # Insert elements into their respective buckets
        for i in range(n):
            bucket_index = math.floor(input[i] / divider)
            buckets[bucket_index].append(input[i])

        # Sort the elements of each bucket
        for i in range(n):
            buckets[i] = self.insertion_sort(buckets[i])
        
        # Concatenate every bucket
        for bucket in buckets:
            for item in bucket:
                output.append(item)
        
        return output


    def floatnum_bucket_sort(self, input):
        """
        Bucket sort for real numbers ranged from 0 - 1
        
        Time complexity : 
            Average and best case : O(n)
            Worst case : O(n^2)

        - Utilizes insertion sort internally for sorting elements in each bucket
        - Used when input is uniformly distributed over a range

        Parameters
        ----------
        input : python list
            unsorted array
        """

        n = len(input)
        output = []
        buckets = [list() for i in range(n)]

        # Insert elements into their respective buckets
        for i in range(n):
            bucket_index = math.floor(n * input[i])
            buckets[bucket_index].append(input[i])

        # Sort the elements of each bucket
        for i in range(n):
            buckets[i] = self.insertion_sort(buckets[i])
        
        # Concatenate every bucket
        for bucket in buckets:
            for item in bucket:
                output.append(item)

        return output


    def shell_sort(self, input):
        """
        Shell sort
        
        Time complexity : 
            Worst case : O(n^r)  # r = 2 in this implementation, r is the number we divide the gap size with
            Best case : O(n log n)

        - Generalized version of insertion sort. It first sorts elements that are far apart 
        from each other and successively reduce the gap between the elements to be sorted.
        - The gap between the elements is reduced based on the sequence, n/2, n/4, ..., 1

        Parameters
        ----------
        input : python list
            unsorted array
        """
        output = deepcopy(input)
        n = len(input)

        # Iterate through gap sequence of n/2, n/4, ..., 1
        gap = n // 2
        while gap > 0:

            # Perform gapped insertion sort using current gap size
            for i in range(gap, n):
                key = output[i]
                j = i - gap
                
                while j >= 0 and key < output[j]:
                    output[j + gap] = output[j]
                    j -= gap
                output[j + gap] = key

            gap //= 2

        return output
        