


def ContArraySum(value,total):
    if len(value)<2:
        return False
    seen = set()
    getval = set()
    for i in value:
        target = total -i
        if target not in seen:
            seen.add(i)

        else:
            getval.add((min(i,target),max(i,target)))
    print('\n'.join(map(str,list(getval))))


ContArraySum([1,3,3,2,2],4)