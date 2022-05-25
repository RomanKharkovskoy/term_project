y = [0, 1, 1, 1, 1, 1, 1, 0]
x1 = [1, 1, 1, 1, 1, 1, 1, 0]
x2 = [0, 1, 1, 1, 1, 1, 1, 1]
x3 = [1, 1, 1, 1, 1, 1, 1, 1]
x4 = [0, 0, 0, 0, 0, 0, 0, 0]
x5 = [0, 1, 1, 1, 0, 1, 1, 1, 1, 1]
frame_array = x5
frame_array_cur = [[0, 0]]
max_vr = 0


print(frame_array)
frame_array.insert(0, 0)
frame_array.insert(len(frame_array), 0)
print(frame_array)


for x in range(1,len(frame_array)):
    if (frame_array[x-1] == 0 and frame_array[x] == 1):
        frame_array_cur.append([x, x])
    if (frame_array[x-1] == 1 and frame_array[x] == 0):
        frame_array_cur[len(frame_array_cur)-1][1] = x-1
print(frame_array_cur)
if len(frame_array_cur) != 1:
    for x in range(len(frame_array_cur)):
        cur_vr = frame_array_cur[x][1] - frame_array_cur[x][0]
        if max_vr < cur_vr:
            max_vr = cur_vr
            res = frame_array_cur[x]
    res[0] = res[0] - 1
    res[1] = res[1] - 1
    print(res)
    print(res[1] - res[0] + 1)
else:
    res = [0, 0]
    print(res)