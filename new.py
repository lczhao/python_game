# you can use print for debugging purposes, e.g.
# print "this is a debug message"

def solution(K, A):
    A.sort();
    gotCounter = 0;
    findList = [];
    i = 0;
    while i < len(A):
        j = i + 1;
        occur = 1;
        while j < len(A) and A[j] == A[i]:
            occur += 1;
            j += 1;
        findList.append((A[i], occur));
        i = j;
    print(findList);
    print(A);
    for i in findList:
        lookfor = K - i[0];
        f = binarySearch(lookfor, A);
        if f != -1:
            print("lookfor: " , lookfor, ", ", i[0], ", " , i[1], ", ", f);
            gotCounter += i[1];
    
    return gotCounter;

def binarySearch(k, a):
    mid = int(len(a) / 2);
    if len(a) == 0: return -1;
    if k == a[mid]:
        return mid;
    if k < a[mid]:
        return binarySearch(k, a[:mid]);
    if k > a[mid]:
        return binarySearch(k, a[mid + 1:]);
        
solution(6, [1, 8, -3, 0, 1, 3, -2, 4, 5])