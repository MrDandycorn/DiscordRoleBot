def form(num, arr):
    if abs(num) % 10 == 1:
        return arr[0]
    if abs(num) % 10 > 4:
        return arr[2]
    return arr[1]