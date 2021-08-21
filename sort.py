import numpy as np
import random

def bubbleSort(array):

    n = len(array)

    for i in range(1, n):
        for j in range(n-i):
            yield [(0, array, {j:"red", j+1:"red"})]
            if (array[j] > array[j+1]):
                array[j], array[j+1] = array[j+1], array[j]
                yield [(0, array, {j:"red", j+1:"red"})]
    
    yield None

def selectionSort(array):

    n = len(array)

    for i in range(n-1):
        minIndex = i
        for j in range(i+1, n):
            yield [(0, array, {minIndex:"red", j:"red", i:"orange"})]
            if (array[minIndex] > array[j]):
                minIndex = j
        array[i], array[minIndex] = array[minIndex], array[i]
        yield [(0, array, {minIndex:"red", i:"orange"})]
        
    yield None

def insertionSort(array):

    n = len(array)

    for i in range(1, n):
        for j in range(i, 0, -1):
            yield [(0, array, {j:"red", j-1:"red"})]
            if (array[j] < array[j-1]):
                array[j], array[j-1] = array[j-1], array[j]
                yield [(0, array, {j:"red", j-1:"red"})]
            else:
                break

    yield None

def mergeSort(array, begin=None, end=None):

    n = len(array)

    isFirst = False

    if (begin == None):
        begin = 0
        isFirst = True
    if (end == None):
        end = n-1
        isFirst = True
    
    if (begin < end):
        leftEnd = (begin+end) // 2
        rightBegin = leftEnd + 1

        if (begin != leftEnd):
            yield from mergeSort(array, begin, leftEnd)
            yield from mergeSort(array, rightBegin, end)
        
        temp = np.zeros(end - begin + 1)

        i = 0

        left = begin
        right = rightBegin

        while (left <= leftEnd and right <= end):

            yield [(0, array, {left:"red", right:"red"}), (begin, temp, {i-1:"lightgreen"})]

            if (array[left] <= array[right]):
                temp[i] = array[left]
                array[left] = 0
                i += 1
                left += 1

                yield [(0, array, {right:"red"}), (begin, temp, {i-1:"lightgreen"})]
            else:
                temp[i] = array[right]
                array[right] = 0
                i += 1
                right += 1

                yield [(0, array, {left:"red"}), (begin, temp, {i-1:"lightgreen"})]
        
        if (left <= leftEnd):
            while (left <= leftEnd):

                yield [(0, array, {left:"red"}), (begin, temp, {i-1:"lightgreen"})]

                temp[i] = array[left]
                array[left] = 0

                yield [(0, array, dict()), (begin, temp, {i:"lightgreen"})]

                i += 1
                left += 1

        else:
            while (right <= end):

                yield [(0, array, {right:"red"}), (begin, temp, {i-1:"lightgreen"})]

                temp[i] = array[right]
                array[right] = 0

                yield [(0, array, dict()), (begin, temp, {i:"lightgreen"})]

                i += 1
                right += 1

        for i in range(len(temp)):
            array[begin+i] = temp[i]

    if (isFirst):
        yield None

def bogoSort(array):
    
    n = len(array)

    while (True):
        isSorted = True
        for i in range(n-1):
            if (array[i] > array[i+1]):
                isSorted = False
                break
        
        if (isSorted):
            break

        yield [(0, array, dict())]
        random.shuffle(array)
    
    yield None