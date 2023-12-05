from utils import *

sys.dont_write_bytecode = True

current_day = __file__.split('/')[-1].split('.')[0]
puzzle = open(f'puzzle/{current_day}.in').read()

blueprints = {}
for line in puzzle.splitlines():
    blueprint_id = int(line.split()[1][:-1])
    costs = {}
    for sentence in line.split(': ')[1].split('. '):
        words = sentence.split()
        costs[words[1]] = {}
        raw_costs = sentence.split('costs ')[1]
        for raw_cost in raw_costs.split(' and '):
            amount, material = raw_cost.split()
            material = material.strip('.')
            costs[words[1]][material] = int(amount)
    print(costs)
    blueprints[blueprint_id] = costs


def can_purchase(game_state: dict, robot_cost: dict) -> dict | bool:
    game_state_copy = deepcopy(game_state)
    for material_type, material_cost in robot_cost.items():
        game_state_copy['ores'][material_type] -= material_cost
        if game_state_copy['ores'][material_type] < 0:
            return False
    return game_state_copy


def get_next_games(game_state: dict, game_costs: dict) -> list[dict]:
    no_move_game = deepcopy(game_state.copy())
    for material_type, n_robots in no_move_game['robots'].items():
        no_move_game['ores'][material_type] += n_robots
    # no_move_game = {
    #     'ores': defaultdict(int, {ore: game_state['ores'][ore] + game_state['robots'][ore] for ore in game_state['ores']}),
    #     'robots': defaultdict(int, {robot: game_state['robots'][robot] for robot in game_state['robots']}),
    # }
    ret = [no_move_game]

    last_batch = [game_state]
    while True:
        new_batch = []
        for last_game in last_batch:
            for robot_material, robot_cost in game_costs.items():
                if new_game_state := can_purchase(last_game, robot_cost):
                    new_game_state['robots'][robot_material] += 1
                    new_batch.append(new_game_state)
        if not new_batch:
            return ret
        ret.extend(new_batch)
        last_batch = new_batch


best = -1
for blueprint_id, costs in blueprints.items():
    print(costs)
    games = [{'robots': defaultdict(int, {'ore': 1}), 'ores': defaultdict(int)}]
    for minute in range(16):
        next_games = []
        for game in games:
            next_games.extend(get_next_games(game, costs))
        games = next_games
        games.sort(key=lambda x: sum(x['ores'].values()))
        games = games[:1_000]
        print(f'{minute=}', len(games))

    print()
    print(games[0])
    print(games[-1])

    print('geode:', max(game['ores']['geode'] for game in games))
    print()
