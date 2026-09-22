def remove_duplicate(p):
    checker = []
    for item in p:
        if item not in checker:
            checker.append(item)
    return checker