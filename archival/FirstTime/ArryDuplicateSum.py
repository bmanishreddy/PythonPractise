def rotation(list1,list2):
    if len(list1) != len(list2):
        return False
    key = list1[0]
    key_index = 0
    for i in range(len(list2)):
        if list2[i] == key:
            key_index = i

            break

    if key_index == 0:
        return False

    for x in range(len(list1)):
        l2index = (key_index+x) % len(list1)

        if list1[x] != list2[l2index]:
            return False

    return True


print(rotation([1,2,3,4,5,6,7],[4,5,6,7,1,2,3]))
