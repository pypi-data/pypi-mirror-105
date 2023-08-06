"""This is a function called nester which provides one function called print_lol
which prints lists that may or may not include nested lists"""
def print_lol(item_list, level):
    """Takes the argument the_listwhich is any python list
each item is recursively printed onto its own line. A second argument
called level sets the indentations to use"""
    for each_item in item_list:
        if isinstance(each_item, list):
            print_lol(each_item, level+1)
        else:
            for tab_stop in range(level):
                print("\t", end=")
            print(each_item)
