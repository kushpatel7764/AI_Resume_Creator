def string_to_array(string):
    stripped_string = string.strip()
    array = []
    for item in stripped_string.split(','):
        # Remove white space the append to array
        array.append(item.strip())
    return array

def array_to_string(array):
    # array is an array of tuples
    string = ''
    for i, item in enumerate(array):
        if len(array) == i + 1:
            string += str(item[0])
        else:
            string += str(item[0]) + ", "
    return string