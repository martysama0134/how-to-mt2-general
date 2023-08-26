#!/usr/local/bin/python3
# Copyright (c) 2023, martysama0134
# All rights reserved.
# MIT License

"""EterGroupParser
A Python script to parse, manipulate, and automatically repair Eter Group files.
"""

__author__		= "martysama0134"
__copyright__	= "Copyright (c) 2023 martysama0134"
__date__		= "2023-08-24"
__license__		= "MIT License"
__version__		= "3.0"
__url__         = "https://github.com/martysama0134/how-to-mt2-general/tree/master/eter-group-parser"
__description__ = "A Python script to parse, manipulate, and automatically repair Eter Group files."

import re

ENABLE_NEXT_GROUP_PADDING = False
ENABLE_COMMENTS_PRESERVATION = True
ENABLE_AUTO_INCREMENT_FIX = True


def GetIndent(n = 1, delimiter = '\t', padding = 1):
    return n * (delimiter * padding)

def GetSpaceIndent(n):
    return GetIndent(n, delimiter=' ', padding=4)

def GetGroupsOf(egr, fnc):
    group_iterator = EterGroupIterator(egr)
    return filter(fnc, group_iterator)



class EterGroupReader(object):
    """EterGroupReader
    You can fully load and resave any Eter Group files like mob_drop_item.txt, warrior_m.msm, dragon_soul_table.txt, and quite more.

    It also preserves the comments made with '#' in their correct place, except for the comments in the root below other Groups.
    """

    def __init__(self):
        self.stackIndex = 0
        self.groupStack = {}
        self.groupRoot = EterGroupNode("root")
        self.currentGroupNode = [self.groupRoot]
        if ENABLE_COMMENTS_PRESERVATION:
            self.lastNode = self.currentGroupNode[-1] # Used only for preserving comments


    def GetGroups(self, skipRoot=True):
        return EterGroupIterator(self, skipRoot=skipRoot)


    def GetGroupsOf(self, fnc, skipRoot=True):
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
        self.key = str(key)
        self.value = value



class EterGroupNode(EterNode):
    def __init__(self, name=''):
        super().__init__(name)

        self.dataDict = {}
        self.dataList = []

    def SetData(self, key, value):
        self.dataDict[str(key)] = value
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
    """MobDropItemHelper
    You can handle mob_drop_item.txt with special functions.
    """
    def GetGroupsOfMetins(self):
        return GetGroupsOfMetins(self)

    def GetGroupsOfMetinsAndDrop(self):
        return GetGroupsOfMetinsAndDrop(self)

    def AddIndexElement(self, group, data):
        AddIndexElement(group, data)



def AddIndexElement(group, data):
    highest = str(GetGroupHighestIndex(group) + 1)
    elem = EterElemNode()
    elem.SetName(highest)
    elem.SetIndex(group.index)
    elem.SetParent(group)
    elem.SetData(highest, data)
    group.SetData(highest, elem)


def GetGroupsOfMetinsAndDrop(egr):
    return egr.GetGroupsOf(lambda group: IsTypeDropGroup(group) and IsMetinGroup(group))


def GetGroupsOfMetins(egr):
    return egr.GetGroupsOf(lambda group: IsMetinGroup(group))


def IsTypeGroup(group, type_to_check):
    return 'type' in group.dataDict and group.dataDict['type'].value[0] == type_to_check


def IsTypeDropGroup(group):
    return IsTypeGroup(group, 'drop')


def IsTypeKillGroup(group):
    return IsTypeGroup(group, 'kill')


def IsMetinGroup(group):
    return IsVnumInRangeGroup(group, 8000, 8999)


def IsVnumInListGroup(group, vnum_list):
    return 'mob' in group.dataDict and group.dataDict['mob'].value[0] in vnum_list


def IsVnumInRangeGroup(group, min_vnum, max_vnum):
    return 'mob' in group.dataDict and min_vnum <= group.dataDict['mob'].value[0] <= max_vnum


def GetGroupHighestIndex(group):
    return max(GetGroupIndexKeys(group), default=0)


def GetGroupIndexKeys(group):
    return [int(key) for key in group.dataDict.keys() if key.isdigit()]


def GetGroupIndexKeysFromDataList(group):
    return [int(elem.key) for elem in group.dataList if isinstance(elem, EterElemNode) and elem.key.isdigit()]

def GetGroupIndexNodeFromDataList(group):
    return [elem for elem in group.dataList if isinstance(elem, EterElemNode) and elem.key.isdigit()]


def CheckValidContinuousGroupIndex(group, repair=False):
    # Convert keys to integers and sort them
    int_keys = sorted(map(int, GetGroupIndexKeysFromDataList(group)))

    # Check for contiguous and unique keys
    for i, key in enumerate(int_keys[:-1]):
        if key + 1 != int_keys[i + 1]:
            return False, key

    return True, 0


def RepairContinuousGroupIndex(group):
    # Convert keys to integers and sort them
    int_keys = sorted(map(int, GetGroupIndexKeysFromDataList(group)))
    if not int_keys:
        print(f"group {group.name} has no index list")
        return

    needs_repair = False
    # Check for contiguous and unique keys
    for i, key in enumerate(int_keys):
        if i + 1 != key:
            needs_repair = True

    if needs_repair:
        group.dataDict = {}
        print(f"reparing group {group.name}")
        for i, node in enumerate(GetGroupIndexNodeFromDataList(group)):
            old_key = node.key
            new_key = str(i + 1)
            group.dataDict[new_key] = node
            node.key = new_key
            if old_key != new_key:
                print(old_key, "->", new_key)


def CreateGroupNode(parent, func):
    # If the group does not exist, create a new one
    new_group = EterGroupNode()
    func(new_group)

    new_group.SetIndex(parent.index + 1)
    new_group.SetParent(parent)

    parent.SetData(new_group.name, new_group)
    return new_group


def CreateMobDropGroup(egr, mob_vnum, type_value):
    parent = egr.groupRoot
    def custom_func(group):
        new_elem2 = EterElemNode()
        new_elem2.SetData('type', [type_value])
        group.SetData('type', new_elem2)

        new_elem1 = EterElemNode()
        new_elem1.SetData('mob', [mob_vnum])
        group.SetData('mob', new_elem1)
        group.SetName(f"Mob{mob_vnum}Type{type_value.capitalize()}")
        group.SetParent(parent)

    return CreateGroupNode(parent, custom_func)


def FindOrCreateGroup(egr, condition_func, create_func):
    # Check if a group satisfying the condition already exists
    for group in egr.GetGroups():
        if condition_func(group):
            return group  # Group already exists, return it

    # If the group does not exist, create a new one using the provided create_func
    new_group = create_func()

    return new_group


def FindOrCreateMobDropGroup(egr, mob_vnum, type_value):
    condition_func = lambda group: 'mob' in group.dataDict and 'type' in group.dataDict and \
                                   group.dataDict['mob'].value[0] == mob_vnum and group.dataDict['type'].value[0] == type_value

    create_func = lambda: CreateMobDropGroup(egr, mob_vnum, type_value)

    return FindOrCreateGroup(egr, condition_func, create_func)



class RaceDataHelper(EterGroupReader):
    """RaceDataHelper
    You can handle any .msm with special functions.
    """
    def ReplaceShapeIndexValue(self, old_value, new_value):
        ReplaceShapeIndexValue(self, old_value, new_value)



def ReplaceShapeIndexValue(egr, old_value, new_value):
    for group in egr.GetGroups():
        for elem in group.dataList:
            if isinstance(elem, EterElemNode) and elem.key == 'ShapeIndex' and elem.value[0] == old_value:
                elem.value[0] = new_value



if __name__ == "__main__":
    pass
    # if True: # load, print, and save
    #     egr = EterGroupReader()
    #     egr.LoadFromFile('sample.txt')
    #     egr.PrintTree()
    #     egr.SaveToFile('sample-out.txt')

    # if True: # find node and print it
    #     egr = EterGroupReader()
    #     egr.LoadFromFile('sample.txt')
    #     node = egr.FindNode("ApplyNumSettings", "Default", "basis")
    #     if node:
    #         print("node {} found with value {}".format(node.key, node.value))

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

    # if True: # load mob_drop_item and add a red potion in the metin drops
    #     egr = MobDropItemHelper()
    #     egr.LoadFromFile('mob_drop_item.txt')
    #     for group in egr.GetGroupsOfMetinsAndDrop():
    #         egr.AddIndexElement(group, [27001, 1, 6.6])
    #         egr.PrintTree(group)
    #     egr.SaveToFile('mob_drop_item-out.txt')

    # if True: # load mob_drop_item and add a red potion in vnum list
    #     egr = MobDropItemHelper()
    #     egr.LoadFromFile('mob_drop_item.txt')
    #     for group in egr.GetGroupsOf(lambda group: IsVnumInListGroup(group, [101, 105, 1059])):
    #         egr.AddIndexElement(group, [27001, 1, 6.6])
    #         egr.PrintTree(group)
    #     egr.SaveToFile('mob_drop_item-out.txt')

    # if True: # load mob_drop_item and check for errors
    #     egr = MobDropItemHelper()
    #     egr.LoadFromFile('mob_drop_item.txt')
    #     for group in egr.GetGroups():
    #         valid, found = CheckValidContinuousGroupIndex(group)
    #         if not valid:
    #             egr.PrintTree(group)
    #             print(f"NOT VALID: Error at group '{group.name}' index {found}")
    #             break
    #     egr.SaveToFile('mob_drop_item-out.txt')

    # if True: # load mob_drop_item and repair for index errors
    #     egr = MobDropItemHelper()
    #     egr.LoadFromFile('mob_drop_item.txt')
    #     for group in egr.GetGroups():
    #         RepairContinuousGroupIndex(group)
    #     egr.SaveToFile('mob_drop_item-out.txt')

    # if True: # load mob_drop_item and manipulate it
    #     egr = MobDropItemHelper()
    #     egr.LoadFromFile('mob_drop_item.txt')
    #     for group in egr.GetGroupsOfMetins():
    #         egr.PrintTree(group)
    #     egr.SaveToFile('mob_drop_item-out.txt')

    # if True: # load mob_drop_item and search / create a node
    #     egr = MobDropItemHelper()
    #     egr.LoadFromFile('mob_drop_item.txt')
    #     group = FindOrCreateMobDropGroup(egr, 691, "limit")
    #     egr.AddIndexElement(group, [27001, 11, 6.12])
    #     egr.AddIndexElement(group, [27002, 22, 12.34])
    #     egr.AddIndexElement(group, [27003, 33, 18.56])
    #     egr.PrintTree(group)
    #     egr.SaveToFile('mob_drop_item-out.txt')

    if True: #load a .msm and search a specific costume
        egr = RaceDataHelper()
        egr.LoadFromFile('assassin_m.msm')
        egr.ReplaceShapeIndexValue(44114, 44115)
        egr.SaveToFile('assassin_m-out.msm')

