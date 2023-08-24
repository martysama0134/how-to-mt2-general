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

def GetGroupsOf(egr, fnc):
    group_iterator = EterGroupIterator(egr)
    return filter(fnc, group_iterator)



class EterGroupReader(object):
    def __init__(self):
        self.stackIndex = 0
        self.groupStack = {}
        self.groupRoot = EterGroupNode("root")
        self.currentGroupNode = [self.groupRoot]
        if ENABLE_COMMENTS_PRESERVATION:
            self.lastNode = self.currentGroupNode[-1] # Used only for preserving comments


    def GetGroups(self, skipRoot=False):
        return EterGroupIterator(self, skipRoot=skipRoot)


    def GetGroupsOf(self, fnc, skipRoot=False):
        group_iterator = EterGroupIterator(self, skipRoot=skipRoot)
        return filter(fnc, group_iterator)


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

        for elem in group.dataList:
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

            for elem in group.dataList:
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


    def FindNode(self, *args):
        """
        Find a node in the hierarchy by specifying a variable number of arguments representing the path.

        :param args: Variable arguments representing the path to the node.
        :return: The found node or None if not found.
        """
        node = self.groupRoot  # Start from the root

        for key in args:
            if key in node.dataDict:
                node = node.dataDict[key]
            else:
                return None  # Key not found, return None

        return node



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

        self.dataDict = {}
        self.dataList = []

    def SetData(self, key, value):
        self.dataDict[key] = value
        self.dataList.append(value)



class EterGroupIterator:
    def __init__(self, egr, skipRoot = False):
        self.egr = egr
        if skipRoot:
            self.stack = list(egr.groupRoot.dataList)  # Initialize with children of root
        else:
            self.stack = [egr.groupRoot]

    def __iter__(self):
        return self

    def __next__(self):
        while self.stack:
            group = self.stack.pop()
            if isinstance(group, EterGroupNode):
                for elem in group.dataList:
                    if isinstance(elem, EterGroupNode):
                        self.stack.append(elem)
                return group
        raise StopIteration



class MobDropItemHelper(EterGroupReader):
    def AddNewItemToGroup():
        pass

    def GetGroupsOfMetins(self):
        return self.GetGroupsOf(lambda group: 'mob' in group.dataDict and 8000 <= group.dataDict['mob'].value[0] <= 8999)
        # def fnc(group):
        #     if 'mob' in group.dataDict:
        #         mob_value = group.dataDict['mob'].value[0]
        #         return 8000 <= mob_value <= 8999
        #     return False
        # return self.GetGroupsOf(fnc)



def GetGroupHighestIndex(group):
    return max(GetGroupIndexKeys(group), default=None)


def GetGroupIndexKeys(group):
    return [int(key) for key in group.dataDict.keys() if key.isdigit()]


def GetGroupIndexKeysFromDataList(group):
    return [int(elem.key) for elem in group.dataList if elem.key.isdigit()]


def CheckValidContinuousGroupIndex(group):
    # Convert keys to integers and sort them
    int_keys = sorted(map(int, GetGroupIndexKeysFromDataList(group)))

    # Check for contiguous and unique keys
    for i, key in enumerate(int_keys[:-1]):
        if key + 1 != int_keys[i + 1]:
            return False, key

    return True, 0


if __name__ == "__main__":
    pass
    # egr = EterGroupReader()
    # egr.LoadFromFile('sample.txt')
    # egr.PrintTree()
    # egr.SaveToFile('sample-out.txt')

    # if True: # find node and print it
    #     egr = EterGroupReader()
    #     egr.LoadFromFile('sample.txt')
    #     node = egr.FindNode("ApplyNumSettings", "Default", "basis")
    #     if node:
    #         print("node {} found with value {}".format(node.key, node.value))
    #     # egr.PrintTree(egr.groupRoot.dataDict["BodyChest"])
    #     # print(egr.groupRoot.dataDict["BodyChest"].dataDict["Vnum"].value)
    #     # egr.groupRoot.dataDict["BodyChest"].dataList

    # if True: # find node and edit it
    #     egr = EterGroupReader()
    #     egr.LoadFromFile('sample.txt')
    #     node = egr.FindNode("ApplyNumSettings", "Default", "basis")
    #     if node:
    #         node.value = [11, 22, 33, 44, 55, 66]
    #     egr.SaveToFile('sample-out.txt')

    # if True: # load alternative groups
    #     egr = EterGroupReader()
    #     egr.LoadFromFile('event.txt')
    #     egr.SaveToFile('event-out.txt')

    #     egr = EterGroupReader()
    #     egr.LoadFromFile('dragon_soul_table.txt')
    #     egr.SaveToFile('dragon_soul_table-out.txt')

    #     egr = EterGroupReader()
    #     egr.LoadFromFile('dst_commented.txt')
    #     egr.SaveToFile('dst_commented-out.txt')

    #     egr = EterGroupReader()
    #     egr.LoadFromFile('mob_drop_item.txt')
    #     egr.SaveToFile('mob_drop_item-out.txt')

    # if True: # iter all groups and sub groups
    #     egr = EterGroupReader()
    #     egr.LoadFromFile('sample.txt')

    #     # Create an instance of the iterator
    #     group_iterator = EterGroupIterator(egr, skipRoot=True)

    #     # Iterate over all groups using a lambda or function
    #     for group in group_iterator:
    #         print(f"Group Name: {group.name}")

    # if True: # load mob_drop_item and print only the metins
    #     egr = MobDropItemHelper()
    #     egr.LoadFromFile('mob_drop_item.txt')
    #     for group in egr.GetGroupsOfMetins():
    #         egr.PrintTree(group)
    #         print("HIGHEST", GetGroupHighestIndex(group))
    #     egr.SaveToFile('mob_drop_item-out.txt')

    # if True: # load mob_drop_item and check for errors
    #     egr = MobDropItemHelper()
    #     egr.LoadFromFile('mob_drop_item.txt')
    #     for group in egr.GetGroups(skipRoot=True):
    #         valid, found = CheckValidContinuousGroupIndex(group)
    #         if not valid:
    #             egr.PrintTree(group)
    #             print(f"NOT VALID: Error at group '{group.name}' index {found}")
    #             break
    #     egr.SaveToFile('mob_drop_item-out.txt')

    # if True: # load mob_drop_item and manipulate it
    #     egr = MobDropItemHelper()
    #     egr.LoadFromFile('mob_drop_item.txt')
    #     for group in egr.GetGroupsOfMetins():
    #         egr.PrintTree(group)
    #     egr.SaveToFile('mob_drop_item-out.txt')


