def remove_duplicate(p):
    checker = []
    for i in range (len(set(p))):
        if p[i] in checker:
            continue
        checker.append(p[i])
    return checker