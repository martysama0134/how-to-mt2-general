# eter-group-parser

It loads and resave Eter Group files. It can also manipulate and repair them.

Example of a loaded file:

```
ScriptType: ['RaceDataScript']
BaseModelFileName: "d:/ymir work/pc/warrior/warrior_novice.GR2"
Group CorDraconis(Mystical):
    Vnum: [51506]
    1: [115000, 1, 1]
    2: [125000, 1, 1]
    3: [135000, 1, 1]
    4: [145000, 1, 1]
    5: [155000, 1, 1]
    6: [165000, 1, 1]

Group BodyChest:
    Vnum: [71203]
    1: [50401, 1, 1]
    2: [50402, 1, 1]
    3: [50403, 1, 1]
    4: [50404, 1, 1]
    5: [50405, 1, 1]

Group MentalChest:
    Vnum: [71205]
    1: [50416, 1, 1]
    2: [50417, 1, 1]
    3: [50418, 1, 1]
    4: [50419, 1, 1]
    5: [50420, 1, 1]

Group Cung_Mok:
    type: ['drop']
    mob: [151]
    1: [71151, 1, 100]
    2: [71151, 1, 100]
    3: [71151, 1, 100]
    4: [71151, 1, 100]
    5: [71151, 1, 100]
    6: [71299, 1, 50]
    7: [71740, 2, 50]
    8: [1, 20000, 50]
    9: [1, 30000, 30]

Group ApplyNumSettings:
    Group Default:
        basis: [1, 1, 1, 2, 2, 3]
        add_min: [0, 0, 0, 0, 0, 0]
        add_max: [0, 1, 2, 2, 3, 3]

    Group NotSoDefault:
        basis: [1, 2, 3, 4, 5]
        add_min: [5, 4, 3, 2, 1]
        add_max: [11, 3, 5, 7, 22]

    Group MixedTypes:
        1: ['MAX_SP', 500]
        2: ['RESIST_WIND', 10]
        3: ['ENCHANT_WIND', 10]


Group HairData:
    PathName: "d:/ymir Work/pc/warrior/"
    HairDataCount: [999]
    Group HairData00:
        HairIndex: [0]
        Model: "hair/hair_1_1.gr2"
        SourceSkin: "hair/hair_1_1.dds"
        TargetSkin: "warrior_hair_01.dds"

    Group HairData01:
        HairIndex: [1]
        Model: "hair/hair_1_1.gr2"
        SourceSkin: "hair/hair_1_1.dds"
        TargetSkin: "warrior_hair_01_white.dds"

    Group HairData02:
        HairIndex: [2]
        Model: "hair/hair_1_1.gr2"
        SourceSkin: "hair/hair_1_1.dds"
        TargetSkin: "warrior_hair_01_gold.dds"
```


Examples:

```py
    if True: # load, print, and save
        egr = EterGroupReader()
        egr.LoadFromFile('sample.txt')
        egr.PrintTree()
        egr.SaveToFile('sample-out.txt')

    if True: # find node and print it
        egr = EterGroupReader()
        egr.LoadFromFile('sample.txt')
        node = egr.FindNode("ApplyNumSettings", "Default", "basis")
        if node:
            print("node {} found with value {}".format(node.key, node.value))

    if True: # find node and edit it
        egr = EterGroupReader()
        egr.LoadFromFile('sample.txt')
        node = egr.FindNode("ApplyNumSettings", "Default", "basis")
        if node:
            node.value = [11, 22, 33, 44, 55, 66]
        egr.SaveToFile('sample-out.txt')

    if True: # iter all groups and sub groups
        egr = EterGroupReader()
        egr.LoadFromFile('sample.txt')

        # Create an instance of the iterator
        group_iterator = EterGroupIterator(egr, skipRoot=True)

        # Iterate over all groups using a lambda or function
        for group in group_iterator:
            print(f"Group Name: {group.name}")

    if True: # load mob_drop_item and print only the metins
        egr = MobDropItemHelper()
        egr.LoadFromFile('mob_drop_item.txt')
        for group in egr.GetGroupsOfMetins():
            egr.PrintTree(group)
            print("HIGHEST", GetGroupHighestIndex(group))
        egr.SaveToFile('mob_drop_item-out.txt')

    if True: # load mob_drop_item and add a red potion in the metin drops
        egr = MobDropItemHelper()
        egr.LoadFromFile('mob_drop_item.txt')
        for group in egr.GetGroupsOfMetinsAndDrop():
            egr.AddIndexElement(group, [27001, 1, 6.6])
            egr.PrintTree(group)
        egr.SaveToFile('mob_drop_item-out.txt')

    if True: # load mob_drop_item and add a red potion in vnum list
        egr = MobDropItemHelper()
        egr.LoadFromFile('mob_drop_item.txt')
        for group in egr.GetGroupsOf(lambda group: IsVnumInListGroup(group, [101, 105, 1059])):
            egr.AddIndexElement(group, [27001, 1, 6.6])
            egr.PrintTree(group)
        egr.SaveToFile('mob_drop_item-out.txt')

    if True: # load mob_drop_item and check for errors
        egr = MobDropItemHelper()
        egr.LoadFromFile('mob_drop_item.txt')
        for group in egr.GetGroups():
            valid, found = CheckValidContinuousGroupIndex(group)
            if not valid:
                egr.PrintTree(group)
                print(f"NOT VALID: Error at group '{group.name}' index {found}")
                break
        egr.SaveToFile('mob_drop_item-out.txt')

    if True: # load mob_drop_item and repair for index errors
        egr = MobDropItemHelper()
        egr.LoadFromFile('mob_drop_item.txt')
        for group in egr.GetGroups():
            RepairContinuousGroupIndex(group)
        egr.SaveToFile('mob_drop_item-out.txt')

```
