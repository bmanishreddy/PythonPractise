def comon_elements(list1,list2):
    commonlist = []

    p1 = 0
    p2 = 0

    while p1 < len(list1) and p2 < len(list2):
        print("values in p1 and p2 ",p1,p2)
        if list1[p1] == list2[p2]:
            commonlist.append(list1[p1])
            p1 += 1
            p2 += 1
        elif list1[p1] > list2[p2]:
            p2 += 1
        else:
            p1 += 1
    return commonlist


print(comon_elements([1,2,4,4,5,6],[1,2,3,4,5,6,6,6]))