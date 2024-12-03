from utils import *

sys.dont_write_bytecode = True

current_day = __file__.split('/')[-1].split('.')[0]
puzzle = open(f'puzzle/{current_day}.in').read()

instructions, network = puzzle.split('\n\n')
nodes = {}
for line in network.splitlines():
    line = line.replace('(', '').replace(')', '').replace(' =', ',')
    line = line.split(', ')
    nodes[line[0]] = {"L": line[1], "R": line[2]}

# part 1
step = 0
current = "AAA"
while current != "ZZZ":
    current = nodes[current][instructions[step % len(instructions)]]
    step += 1
time_print(step)

# part 2
currents = [node for node in nodes if node.endswith("A")]
offsets = []
cycles = []
for current in currents:
    step = 0
    seen = set()
    seen_list = [current]
    while (current, step % len(instructions)) not in seen:
        seen.add((current, step))
        current = nodes[current][instructions[step % len(instructions)]]
        step += 1
        seen_list.append(current)

    Z_node = next(node for node in seen_list if node.endswith('Z'))
    first_index_in_cycle = seen_list.index(seen_list[-1])
    offsets.append(seen_list.index(Z_node))
    cycles.append(step - first_index_in_cycle)

# Explanation: https://chatgpt.com/share/6748bc5a-0c80-800d-8607-a55d00bb9322
x = offsets[0]
lcm = cycles[0]
for i in range(1, len(offsets)):
    a, m = offsets[i], cycles[i]
    # Adjust x to satisfy the next congruence
    while x % m != a % m:
        x += lcm
    # Update the lcm for the combined cycle
    lcm = (lcm * m) // math.gcd(lcm, m)
time_print(x)
