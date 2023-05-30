import os

def LoadTable(filename = "locale_string.txt"):
    print("Loading the file {}".format(filename))
    lang_table = {}

    toggleOriginal = False
    stringOriginal = ""
    errorsInLines = False
    # Open and read the file
    with open('locale_string.txt', 'rb') as f1:
        for line in f1.readlines():
            line = line.strip()
            #skip empty
            if not line:
                continue
            if not (line.startswith(b'"') and line.endswith(b'";')):
                # try to save the lines that only have ; missing
                if not (line.startswith(b'"') and line.endswith(b'"')):
                    print("strange line: {}".format(line))
                    errorsInLines = True
                    continue
                print("recovering line with ';' missing: {}".format(line))
                line+=b';'
            #toggle
            toggleOriginal = not toggleOriginal
            foundString = line[1:-2]
            if toggleOriginal:
                stringOriginal = foundString
            else:
                lang_table[stringOriginal] = foundString
    return lang_table, errorsInLines


def PrintTable(lang_table):
    for key, value in lang_table.items():
        print(f'{key} : {value}')


# Function to recursively find .cpp and .h files and replace strings
def replace_strings_in_files(directory, lang_table):
    print("Replacing the strings inside {}".format(directory))
    for dirpath, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            if filename.endswith('.cpp') or filename.endswith('.h'):
                filepath = os.path.join(dirpath, filename)
                with open(filepath, 'rb') as f1:
                    content = f1.read()

                # Replace strings based on lang_table
                for original, translated in lang_table.items():
                    content = content.replace(original, translated)

                # Write the replaced content back to the file
                with open(filepath, 'wb') as f1:
                    f1.write(content)


if __name__ == '__main__':
    filename = "locale_string.txt"
    lang_table, errorsInLines = LoadTable(filename)

    # Print the lang_table to check the result
    # PrintTable(lang_table)

    # Replace Translations
    if not errorsInLines:
        replace_strings_in_files('Srcs/Server', lang_table)
    else:
        print("Can't replace the strings until you fix your {}".format(filename))
