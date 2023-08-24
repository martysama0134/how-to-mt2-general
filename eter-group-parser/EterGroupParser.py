#!/usr/local/bin/python3
# EterGroupParser - A Python script to parse and manipulate EterPack Group files.
# Copyright (c) 2023 martysama0134
# MIT License

import re

ENABLE_NEXT_GROUP_PADDING = False
ENABLE_COMMENTS_PRESERVATION = True


def GetIndent(n = 1, delimiter = '\t', padding = 1):
    return n * (delimiter * padding)

def GetSpaceIndent(n):
    return GetIndent(n, delimiter=' ', padding=4)



class EterGroupReader(object):
    def __init__(self):
        self.stackIndex = 0
        self.groupStack = {}
        self.groupRoot = EterGroupNode("root")
        self.currentGroupNode = [self.groupRoot]
        if ENABLE_COMMENTS_PRESERVATION:
            self.lastNode = self.currentGroupNode[-1] # Used only for preserving comments


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
                if ENABLE_COMMENTS_PRESERVATION:
                    self.lastNode.AddComment(line)
                continue

            elif line.lower().startswith('group'):
                self.stackIndex += 1
                self.groupStack[self.stackIndex] = True

                groupName = self.GetGroupNameFromLine(line)
                # print(groupName)

                group = EterGroupNode()
                group.SetName(groupName)
                group.SetIndex(self.stackIndex)
                group.SetParent(self.currentGroupNode[-1])
                self.currentGroupNode[-1].SetData(groupName, group)

                self.currentGroupNode.append(group)
                self.lastNode = group

            elif line.startswith('{'):
                pass #stack incremental moved to group init

            elif line.startswith('}'):
                self.groupStack[self.stackIndex] = False
                self.stackIndex -= 1
                self.currentGroupNode.pop()
                self.lastNode = self.currentGroupNode[-1]

            else:
                key, value = self.GetValueFromLine(line)
                elem = EterElemNode()
                elem.SetName(key)
                elem.SetIndex(self.stackIndex)
                elem.SetParent(self.currentGroupNode[-1])
                elem.SetData(key, value)
                self.currentGroupNode[-1].SetData(key, elem)
                self.lastNode = elem
                # print(key, value)


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

            # Check if the word is an integer
            if isinstance(value, list):
                value = [int(elem) if elem.isdigit() else elem for elem in value]

            return key, value

        return None, None


    def PrintTree(self, group = None, level = 0):
        if not group:
            group = self.groupRoot
            level = level - 1
        else:
            print('{}Group {}:'.format(GetSpaceIndent(level), group.name))

        for key, elem in group.data.items():
            if isinstance(elem, EterGroupNode):
                self.PrintTree(elem, level + 1)
                if ENABLE_NEXT_GROUP_PADDING:
                    print("")
            else:
                print('{}{}: {}'.format(GetSpaceIndent(level + 1), elem.key, elem.value))


    def GenerateTree(self):
        generatedLines = []

        def ProcessTree(group = None, level = 0):
            if not group:
                group = self.groupRoot
                level = level - 1
            else:
                generatedLines.append('{}Group\t{}'.format(GetIndent(level), group.name))
                generatedLines.append('{}{{'.format(GetIndent(level)))

            if ENABLE_COMMENTS_PRESERVATION:
                for comment in group.comments:
                    generatedLines.append('{}{}'.format(GetIndent(level + 1), comment))

            for key, elem in group.data.items():
                if isinstance(elem, EterGroupNode):
                    ProcessTree(elem, level + 1)
                    if ENABLE_NEXT_GROUP_PADDING:
                        generatedLines.append("")
                else:
                    if isinstance(elem.value, list):
                        elem.value = "\t".join(str(elem2) for elem2 in elem.value)

                    generatedLines.append('{}{}\t{}'.format(GetIndent(level + 1), elem.key, elem.value))
                    if ENABLE_COMMENTS_PRESERVATION:
                        for comment in elem.comments:
                            generatedLines.append('{}{}'.format(GetIndent(level + 1), comment))

            if isinstance(group, EterGroupNode) and level >= 0:
                generatedLines.append('{}}}'.format(GetIndent(level)))

        ProcessTree()
        return "\n".join(generatedLines)


    def SaveToFile(self, filename):
        with open(filename, "w") as f:
            f.write(self.GenerateTree())



class EterNode(object):
    def __init__(self, name=''):
        self.name = name or "NONAME_{}".format(id(self))
        self.index = 0
        self.parent = None
        if ENABLE_COMMENTS_PRESERVATION:
            self.comments = []

    def SetName(self, name):
        self.name = name

    def SetIndex(self, index):
        self.index = index

    def SetParent(self, parent):
        self.parent = parent

    if ENABLE_COMMENTS_PRESERVATION:
        def AddComment(self, comment):
            self.comments.append(comment)



class EterElemNode(EterNode):
    def __init__(self, name=''):
        super().__init__(name)

        self.key = ''
        self.value = ''

    def SetData(self, key, value):
        self.key = key
        self.value = value



class EterGroupNode(EterNode):
    def __init__(self, name=''):
        super().__init__(name)

        self.data = {}

    def SetData(self, key, value):
        self.data[key] = value



if __name__ == "__main__":
    egr = EterGroupReader()
    egr.LoadFromFile('sample.txt')
    egr.PrintTree()
    egr.SaveToFile('sample-out.txt')
