from sorting import Sort

sort = Sort(verbose=True)

arr = [154, 56, 77, 134, 186, 56, 94, 24, 13, 83, 95, 143]
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
print(sort.shell_sort(arr))
