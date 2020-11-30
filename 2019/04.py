start, end = list(map(int, '153517-630395'.split('-')))

ans_1 = 0
ans_2 = 0
for password in map(str, range(start, end)):
    nums = list(map(int, password))
    if any(num_1 > num_2 for num_1, num_2 in zip(nums, nums[1:])):
        continue

    batch = 1
    p1_ok = False
    p2_ok = False
    for prev, char in zip(password, password[1:]):
        if prev == char:
            batch += 1
        else:
            if batch != 1:
                p1_ok = True
                if batch == 2:
                    p2_ok = True
                    break
            batch = 1
    else:
        if batch != 1:
            p1_ok = True
            p2_ok = batch == 2

    ans_1 += p1_ok or p2_ok
    ans_2 += p2_ok

print(ans_1)
print(ans_2)
