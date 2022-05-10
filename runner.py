from sort.sorting import Sort
from string_match.matcher import Matcher

# sort = Sort(verbose=True)

# arr = [154, 56, 77, 134, 186, 56, 94, 24, 13, 83, 95, 143]
# Bubble sort's driver code
# arr = [5, 1, 12, -5, 16]
# sort.bubble_sort(arr)

# Insertion sort's driver code
# arr = [5, 1, 12, -5, 16]
# sort.insertion_sort(arr)

# Counting sort's
# arr = [4, 1, 3, 4, 3]
# sort.counting_sort(arr)

# Radix sort's
# arr = [154, 56, 77, 134, 186, 56, 94, 24, 13, 83, 95, 143]
# sort.radix_sort(arr)

# Bucket sort's
# arr = [154, 56, 77, 134, 186, 56, 94, 24, 13, 83, 95, 143, 0]
# print(sort.bucket_sort(arr))

# arr = [.78, .17, .39, .26, .72, .12, .32, .16, .94, .86]
# print(sort.floatnum_bucket_sort(arr))

# Shell sort's
# arr = [154, 56, 77, 134, 186, 56, 94, 24]
# print(sort.shell_sort(arr))

match = Matcher(verbose=True)

# Rabin-Karp Matcher
# match.rabin_karp_matcher("3141592653589793", "26535", R=10, Q=997)
# match.rabin_karp_matcher("3141592653589793", "26535", R=10, Q=7)
# match.rabin_karp_matcher("algorisfunalgoisgreat", "algo", R=256, Q=1759)

# Knuth-Morris-Pratt Matcher
match.knuth_morris_pratt_matcher(text="onionionspl", pattern="onions")
