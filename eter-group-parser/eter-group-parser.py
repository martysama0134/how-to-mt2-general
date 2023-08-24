# martysama0134 & ChatGPT - 2023
import re


class EterGroupReader(object):
    def __init__(self):
        self.stackIndex = 0
        self.groupStack = {}
        self.groupRoot = EterGroupNode("root")
        self.currentNode = [self.groupRoot]

    def LoadFromFile(self, filename):
        with open(filename, "r") as f:
            return self.LoadFromData(f.read())

    def LoadFromData(self, data):
        lines = data.split("\n")
        for line in lines:
            line = line.strip()

            if not line:
                continue

            elif line.startswith('#'):
                continue

            elif line.lower().startswith('group'):
                self.stackIndex += 1
                self.groupStack[self.stackIndex] = True

                groupName = self.GetGroupNameFromLine(line)
                # print(groupName)

                group = EterGroupNode()
                group.SetName(groupName)
                group.SetIndex(self.stackIndex)
                group.SetParent(self.currentNode[-1])
                self.currentNode[-1].data[groupName] = group

                self.currentNode.append(group)

            elif line.startswith('{'):
                pass #stack incremental moved to group init

            elif line.startswith('}'):
                self.groupStack[self.stackIndex] = False
                self.stackIndex -= 1
                self.currentNode.pop()

            else:
                key, value = self.GetValueFromLine(line)
                self.currentNode[-1].data[key] = value
                # print(value)

    def GetGroupNameFromLine(self, line):
        match = re.search(r'Group\s+(.+)', line, re.IGNORECASE)
        return match.group(1).strip() if match else 'NONAME'

    def GetValueFromLine(self, line):
        # Split the line into words while preserving double-quoted strings
        words = re.findall(r'(?:"[^"]*"|[^\s"])+', line)

        if len(words) >= 2:
            key = words[0]
            value = words[1:]

            # Handle values within double quotes
            if len(value) == 1 and value[0].startswith('"') and value[0].endswith('"'):
                value = value[0]#[1:-1]

            # Convert numeric strings to integers
            if all(part.isdigit() for part in value):
                value = [int(item) for item in value]  # Convert to int list
                # if len(value) == 1:
                #     value = value[0]
            else:
                value = ''.join(value)  # Concatenate strings with spaces

            return key, value

        return None, None

    def PrintTree(self, group = None, level = 0):
        if not group:
            group = self.groupRoot
            level = level - 1
        else:
            indent = ' '*4*level
            print('{}Group {}:'.format(indent, group.name))

        for key, elem in group.data.items():
            if isinstance(elem, EterGroupNode):
                self.PrintTree(elem, level + 1)
                print("")
            else:
                indent = ' '*4*(level + 1)
                print('{}{}: {}'.format(indent, key, elem))

    def GenerateTree(self):
        generatedLines = []
        def ProcessTree(group = None, level = 0):
            if not group:
                group = self.groupRoot
                level = level - 1
            else:
                indent = '\t'*1*level
                generatedLines.append('{}Group\t{}'.format(indent, group.name))
                generatedLines.append('{}{{'.format(indent))

            for key, elem in group.data.items():
                if isinstance(elem, EterGroupNode):
                    ProcessTree(elem, level + 1)
                    generatedLines.append("")
                else:
                    if isinstance(elem, list):
                        elem = "\t".join(str(elem2) for elem2 in elem)
                    indent2 = '\t'*1*(level + 1)
                    generatedLines.append('{}{}\t{}'.format(indent2, key, elem))

            if isinstance(group, EterGroupNode) and level >= 0:
                generatedLines.append('{}}}'.format(indent))

        ProcessTree()
        return "\n".join(generatedLines)

    def SaveToFile(self, filename):
        with open(filename, "w") as f:
            f.write(self.GenerateTree())
        pass


class EterGroupNode(object):
    def __init__(self, name = ''):
        self.data = {}
        self.name = name if name else "NONAME_{}".format(id(self))
        self.index = 0
        self.parent = None

    def SetName(self, name):
        self.name = name

    def SetIndex(self, index):
        self.index = index

    def SetParent(self, parent):
        self.parent = parent


if __name__ == "__main__":
    egr = EterGroupReader()
    egr.LoadFromFile('sample.txt')
    egr.PrintTree()
    egr.SaveToFile('sample-out.txt')
