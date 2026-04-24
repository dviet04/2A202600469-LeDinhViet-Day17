#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Benchmark Runner: Execute 10 scenarios and log memory/history
"""
import json
import os
import sys
import time
from datetime import datetime

# Add project to path
sys.path.insert(0, os.path.dirname(__file__))

from agent.agent_core import MultiMemoryAgent, call_openai_llm


def setup_fresh_memory():
    """Reset memory files for fresh benchmark run"""
    profile_path = "data/profile.json"
    episodic_path = "data/episodic.json"
    
    # Reset files
    with open(profile_path, 'w', encoding='utf-8') as f:
        json.dump({"default_user": {}}, f, indent=2)
    
    with open(episodic_path, 'w', encoding='utf-8') as f:
        json.dump([], f, indent=2)


def load_memory_state():
    """Load current memory state"""
    memory_state = {
        "profile": {},
        "episodic": []
    }
    
    try:
        with open('data/profile.json', 'r', encoding='utf-8') as f:
            memory_state["profile"] = json.load(f)
    except:
        pass
    
    try:
        with open('data/episodic.json', 'r', encoding='utf-8') as f:
            memory_state["episodic"] = json.load(f)
    except:
        pass
    
    return memory_state


def run_scenario_with_memory(scenario):
    """Run scenario with memory enabled"""
    agent = MultiMemoryAgent()
    outputs = []
    
    for turn_idx, turn in enumerate(scenario['turns'], 1):
        try:
            response = agent.run(turn['input'])
            outputs.append({
                "turn": turn_idx,
                "input": turn['input'],
                "output": response[:200],  # Truncate for brevity
                "timestamp": datetime.now().isoformat()
            })
        except Exception as e:
            outputs.append({
                "turn": turn_idx,
                "input": turn['input'],
                "output": f"[ERROR: {str(e)}]",
                "timestamp": datetime.now().isoformat()
            })
        time.sleep(0.5)  # Rate limit API calls
    
    # Capture memory state after scenario
    memory_state = load_memory_state()
    
    return {
        "outputs": outputs,
        "memory_state": memory_state
    }


class NoMemoryAgent:
    """Simple baseline agent without memory"""
    
    def run(self, input_text):
        """Just call LLM without memory context"""
        prompt = f"User: {input_text}\n\nRespond helpfully."
        try:
            return call_openai_llm(prompt)
        except:
            return "[Error]"


def run_scenario_no_memory(scenario):
    """Run scenario without memory (baseline)"""
    agent = NoMemoryAgent()
    outputs = []
    
    for turn_idx, turn in enumerate(scenario['turns'], 1):
        try:
            response = agent.run(turn['input'])
            outputs.append({
                "turn": turn_idx,
                "input": turn['input'],
                "output": response[:200],  # Truncate for brevity
                "timestamp": datetime.now().isoformat()
            })
        except Exception as e:
            outputs.append({
                "turn": turn_idx,
                "input": turn['input'],
                "output": f"[ERROR]",
                "timestamp": datetime.now().isoformat()
            })
        time.sleep(0.5)  # Rate limit API calls
    
    return {"outputs": outputs}


def run_benchmark():
    """Main benchmark function"""
    scenarios_path = "benchmark/scenarios.json"
    history_path = "benchmark/benchmark_history.json"
    
    # Load scenarios
    with open(scenarios_path, 'r', encoding='utf-8') as f:
        scenarios = json.load(f)
    
    print(f"\n{'='*70}")
    print("BENCHMARK: Multi-Memory Agent (10 Scenarios)")
    print(f"{'='*70}")
    print(f"Total Scenarios: {len(scenarios)}")
    print(f"Start time: {datetime.now().isoformat()}\n")
    
    # Run all scenarios
    history = []
    
    for idx, scenario in enumerate(scenarios, 1):
        print(f"[Scenario {idx}/{len(scenarios)}] {scenario['scenario']}")
        print(f"  Turns: {len(scenario['turns'])}")
        
        # Reset memory for each scenario
        setup_fresh_memory()
        
        # Run WITH memory
        print(f"  Running WITH memory...")
        with_mem_result = run_scenario_with_memory(scenario)
        print(f"  Running WITH memory... ✓")
        
        # Run WITHOUT memory
        print(f"  Running WITHOUT memory...")
        no_mem_result = run_scenario_no_memory(scenario)
        print(f"  Running WITHOUT memory... ✓")
        
        # Combine results
        scenario_result = {
            "scenario_id": idx,
            "scenario_name": scenario['scenario'],
            "description": scenario.get('description', ''),
            "turns_count": len(scenario['turns']),
            "no_memory": no_mem_result,
            "with_memory": with_mem_result
        }
        
        history.append(scenario_result)
        print()
    
    # Save history
    with open(history_path, 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=2)
    
    print(f"{'='*70}")
    print(f"✓ Benchmark completed!")
    print(f"History saved: {history_path}")
    print(f"Total scenarios run: {len(history)}")
    print(f"End time: {datetime.now().isoformat()}")
    print(f"{'='*70}\n")
    
    return history


if __name__ == "__main__":
    os.chdir(os.path.dirname(__file__))
    run_benchmark()
