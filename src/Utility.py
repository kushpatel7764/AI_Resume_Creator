def string_to_array(string):
    stripped_string = string.strip()
    array = []
    for item in stripped_string.split(','):
        #Remove white space the append to array
        array.append(item.strip())
    return array