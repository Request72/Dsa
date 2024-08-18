def reverse_in_intervals(head, k):
    n = len(head)
    result = []
    
    for i in range(0, n, k):
        chunk = head[i:i + k]
        if len(chunk) < k:
            result.extend(chunk)
        else:
            result.extend(chunk[::-1])
    
    return result

head = [1, 2, 3, 4, 5]
k = 2
print(reverse_in_intervals(head, k))
