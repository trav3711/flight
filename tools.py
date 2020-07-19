def binarySearch (arr, l, r, x):
    try:
        # Check base case
        if r >= l:

            mid = l + (r - l) // 2

            element = str(arr[mid])

            # If element is present at the middle itself
            if element == x:
                print(mid)
                return mid

            # If element is smaller than mid, then it
            # can only be present in left subarray
            elif element > x:
                return binarySearch(arr, l, mid-1, x)

            # Else the element can only be present
            # in right subarray
            else:
                return binarySearch(arr, mid + 1, r, x)

        else:
            # Element is not present in the array
            return -1
    except:
        print(f"this is the problem: {mid}")
