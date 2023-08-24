#!/usr/local/bin/python3
# EterGroupParser - A Python script to parse and manipulate EterPack Group files.
# Copyright (c) 2023 martysama0134
# MIT License

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
                self.currentNode[-1].SetData(groupName, group)

                self.currentNode.append(group)

            elif line.startswith('{'):
                pass #stack incremental moved to group init

            elif line.startswith('}'):
                self.groupStack[self.stackIndex] = False
                self.stackIndex -= 1
                self.currentNode.pop()

            else:
                key, value = self.GetValueFromLine(line)
                elem = EterElemNode()
                elem.SetName(key)
                elem.SetIndex(self.stackIndex)
                elem.SetParent(self.currentNode[-1])
                elem.SetData(key, value)
                self.currentNode[-1].SetData(key, elem)
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
            indent = ' '*4*level
            print('{}Group {}:'.format(indent, group.name))

        for key, elem in group.data.items():
            if isinstance(elem, EterGroupNode):
                self.PrintTree(elem, level + 1)
                print("")
            else:
                indent = ' '*4*(level + 1)
                print('{}{}: {}'.format(indent, elem.key, elem.value))

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
                    if isinstance(elem.value, list):
                        elem.value = "\t".join(str(elem2) for elem2 in elem.value)
                    indent2 = '\t'*1*(level + 1)
                    generatedLines.append('{}{}\t{}'.format(indent2, elem.key, elem.value))

            if isinstance(group, EterGroupNode) and level >= 0:
                generatedLines.append('{}}}'.format(indent))

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
        self.comments = []

    def SetName(self, name):
        self.name = name

    def SetIndex(self, index):
        self.index = index

    def SetParent(self, parent):
        self.parent = parent


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
