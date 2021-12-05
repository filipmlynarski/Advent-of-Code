import sys
sys.dont_write_bytecode = True
from utils import *

puzzle = list(map(int, open('puzzle/23.in').read().split(',')))


def run(my_id: int):
    network_que[my_id].append(my_id)

    def get_param(offset, mode, writes=False):
        ret = None
        if mode == '0':
            ret = puzzle_[pointer + offset]  # position mode
        elif mode == '1':
            ret = pointer + offset  # immediate mode
        elif mode == '2':
            ret = base + puzzle_[pointer + offset]  # relative mode
        return ret if writes else puzzle_[ret]

    puzzle_ = defaultdict(int, dict(enumerate(puzzle)))
    pointer = 0
    base = 0
    while True:
        mode_3, mode_2, mode_1, *opcode = f'{puzzle_[pointer]:0>5}'
        opcode = int(''.join(opcode))
        if opcode == 99:
            return

        reads_1 = get_param(1, mode_1)
        reads_2 = get_param(2, mode_2)
        writes_1 = get_param(1, mode_1, writes=True)
        writes_3 = get_param(3, mode_3, writes=True)
        pointer += [4, 4, 2, 2, 3, 3, 4, 4, 2][opcode-1]

        output = None
        if opcode == 1:
            puzzle_[writes_3] = reads_1 + reads_2
        elif opcode == 2:
            puzzle_[writes_3] = reads_1 * reads_2
        elif opcode == 3:
            read = -1
            if my_id in network_que:
                read = network_que[my_id].pop(0)
                if not network_que[my_id]:
                    network_que.pop(my_id)
            puzzle_[writes_1] = read
        elif opcode == 4:
            output = reads_1
        elif opcode == 5:
            if reads_1:
                pointer = reads_2
        elif opcode == 6:
            if not reads_1:
                pointer = reads_2
        elif opcode == 7:
            puzzle_[writes_3] = int(reads_1 < reads_2)
        elif opcode == 8:
            puzzle_[writes_3] = int(reads_1 == reads_2)
        elif opcode == 9:
            base += reads_1

        yield output


network_que = defaultdict(list)
sending = defaultdict(list)
network = [(id_, run(id_)) for id_ in range(50)]
list(next(computer) for _, computer in network)  # invoke generators
NAT_task = None
NAT_history = set()
part_1 = None
part_2 = None
count = 0
while part_2 is None:
    for id_, computer in network:
        NIC_output = next(computer)
        if NIC_output:
            sending[id_].append(NIC_output)
            if len(sending[id_]) == 3:
                task = sending.pop(id_)
                if task[0] == 255:
                    NAT_task = task[1], task[2]
                    if part_1 is None:
                        part_1 = task[2]
                        time_print(part_1)
                else:
                    network_que[task[0]].extend(task[1:])

    if not network_que and not sending and NAT_task:
        # waits for 100 empty cycles before dispatching NAT task (ugly but works)
        count += 1
        if count < 80:
            continue
        count = 0
        if NAT_task[1] in NAT_history:
            part_2 = NAT_task[1]
            time_print(part_2)
        NAT_history.add(NAT_task[1])
        network_que[0].extend(NAT_task)
