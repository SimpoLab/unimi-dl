class WrongSelectionError(Exception):
    pass


def multi_select(entries: list, entries_text: list = None, selection_text: str = "\nYour selection: ") -> list:
    if not entries_text:
        entries_text = entries
    elif len(entries_text) != len(entries):
        raise ValueError("entries and entries_text must have the same length")

    for i, item in enumerate(entries_text):
        print("%d.\t%s" % (i+1, item))
    bad_choice = True
    extremes = []
    sel_indexes = set()
    while bad_choice:
        bad_choice = False

        menu_input = input(selection_text)
        ranges = menu_input.strip().split(",")
        if len(ranges) == 1 and ranges[0] == "":
            return []
        for rang in ranges:
            extremes = rang.split("-")
            if not 1 <= len(extremes) <= 2:
                bad_choice = True
            try:
                extremes = [int(n)-1 for n in extremes]
            except ValueError:
                bad_choice = True

        if not bad_choice:
            if len(extremes) == 1:
                extremes.append(extremes[0])  # type: ignore
            sel_indexes.update(range(extremes[0], extremes[1]+1))  # type: ignore

            try:
                return [entries[i] for i in sel_indexes]
            except IndexError:
                bad_choice = True
        else:
            extremes = []
            sel_indexes = set()

    return []
