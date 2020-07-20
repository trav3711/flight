from math import acos, cos, sin, radians

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

def stringSort(arr):
    for item in arr:
        item = str(item)
        arr.sort()
        return 0

def dist_func(x1, y1, x2, y2):
    #d = r * arccos((siny1 * siny2) + (cosy1 * cosy2 * cosΔx))
    r = 6378.137

    x1 = radians(x1)
    y1 = radians(y1)
    x2 = radians(x2)
    y2 = radians(y2)

    dy=y2-y1

    dist = r * acos((sin(x1)*sin(x2)) + (cos(x1)*cos(x2)*cos(dy)))

    return dist
