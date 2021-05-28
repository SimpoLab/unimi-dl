class WrongSelectionError(Exception):
    pass


def multi_select(entries: list, text: str = "\nYour selection: ") -> list:
    for i, item in enumerate(entries):
        print("%d.\t%s" % (i+1, item))
    menu_input = input(text)

    ranges = menu_input.strip().split(",")
    sel_indexes = set()
    for rang in ranges:
        extremes = rang.split("-")
        if not 1 <= len(extremes) <= 2:
            raise WrongSelectionError
        try:
            extremes = [int(n)-1 for n in extremes]
        except ValueError:
            raise WrongSelectionError
        if len(extremes) == 1:
            extremes.append(extremes[0])
        sel_indexes.update(range(extremes[0], extremes[1]+1))

    try:
        return [entries[i] for i in sel_indexes]
    except IndexError:
        raise WrongSelectionError
