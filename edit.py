def edit_sentence():    
    with open("0419.txt", "r", encoding="utf-8") as f:
        with open("e0419.txt", "w", encoding="utf-8") as g:
            for row in f:
                line = row.rstrip().split(" ")
                line.insert(2, line[1][14: 16])
                line.insert(2, line[1][12: 14])
                line.insert(2, line[1][8: 10])
                line.insert(2, line[1][4:8])
                line.insert(2, line[1][:4])
                del line[1]
            print(line)
            


with open("0419.txt", "r", encoding="utf-8") as f:
    with open("e0419.txt", "w", encoding="utf-8") as g:
        for row in f:
            line = row.rstrip().split(" ")
            for i in range(16, 8, -2):
                line.insert(2, line[1][i-2:i])
            line.insert(2, line[1][4:8])
            line.insert(2, line[1][:4])
            del line[1]
        print(line)
    
# if "  " in sen:
#     sen.replace("  ", " ")
# s_list = sen.rstrip().split(" ")
# for i in range(16, 7, -1):
#     s_list.insert(2, s_list[1][i-2:i])
# s_list.insert(2, s_list[1][4:8])
# s_list.insert(2, s_list[1][:4])
# del s_list[1]
# return s_list