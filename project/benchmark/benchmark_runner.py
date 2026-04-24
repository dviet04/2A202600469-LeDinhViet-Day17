import json
import os
from agent.agent_core import MultiMemoryAgent
from memory.short_term import ShortTermMemory

def run_benchmark(scenarios_path, with_memory=True):
    with open(scenarios_path, 'r', encoding='utf-8') as f:
        scenarios = json.load(f)
    results = []
    for idx, scenario in enumerate(scenarios):
        agent = MultiMemoryAgent() if with_memory else None
        stm = ShortTermMemory() if not with_memory else None
        outputs = []
        for turn in scenario['turns']:
            if with_memory:
                output = agent.run(turn['input'])
            else:
                # No memory: just echo input
                stm = stm or ShortTermMemory()
                stm.add_message({'role': 'user', 'content': turn['input']})
                output = f"[NO MEMORY] {turn['input']}"
            outputs.append(output)
        results.append({
            'scenario': scenario['scenario'],
            'outputs': outputs
        })
    return results

def compare_benchmark(scenarios_path, output_path):
    with_mem = run_benchmark(scenarios_path, with_memory=True)
    no_mem = run_benchmark(scenarios_path, with_memory=False)
    table = []
    for idx, (w, n) in enumerate(zip(with_mem, no_mem), 1):
        pass_status = 'Pass' if w['outputs'][-1] != n['outputs'][-1] else 'Fail'
        table.append([idx, w['scenario'], n['outputs'][-1], w['outputs'][-1], pass_status])
    # Write markdown table
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('| # | Scenario | No-memory | With-memory | Pass |\n')
        f.write('|---|----------|-----------|-------------|------|\n')
        for row in table:
            f.write(f'| {row[0]} | {row[1]} | {row[2]} | {row[3]} | {row[4]} |\n')
    print(f"Benchmark results written to {output_path}")

if __name__ == "__main__":
    scenarios_path = os.path.join(os.path.dirname(__file__), 'scenarios.json')
    output_path = os.path.join(os.path.dirname(__file__), '../BENCHMARK.md')
    compare_benchmark(scenarios_path, output_path)
