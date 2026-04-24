# Multi-Memory Agent - Benchmark Report

## Executive Summary

- **Report Generated**: 2026-04-25 01:24:52
- **Total Scenarios**: 10
- **Total Turns Executed**: 43
- **Memory Stack Tested**: Short-term, Profile, Episodic, Semantic
- **Final Profile Fields**: 1
- **Total Episodes Logged**: 6

## Scenario Execution Summary

| # | Scenario | Turns | Profile Fields | Episodes Created | Status |
|---|----------|-------|----------------|------------------|--------|
| 1 | Store initial user profile (long-term seed) | 3 | 1 | 0 | PASS |
| 2 | Recall profile after unrelated conversation | 4 | 0 | 0 | PASS |
| 3 | Overwrite preference with conflict | 4 | 0 | 0 | PASS |
| 4 | Episodic memory with multiple events | 5 | 0 | 4 | PASS |
| 5 | Episodic vs long-term distinction | 3 | 0 | 5 | PASS |
| 6 | Semantic retrieval with FAQ and follow-up | 3 | 0 | 0 | PASS |
| 7 | Combine semantic knowledge with personal context | 3 | 0 | 6 | PASS |
| 8 | Long context trimming with important early fact | 10 | 0 | 0 | PASS |
| 9 | Implicit recall from long-term memory | 3 | 0 | 0 | PASS |
| 10 | Chained reasoning + memory + overwrite check | 5 | 0 | 0 | PASS |

## Memory Stack Impact

### Profile Memory (Long-term User Data)

**Final Profile State**:
- name: Linh

### Episodic Memory (Event/Task Logs)

**Total Episodes Logged**: 6

**Sample Events**:
- completed task A (Session: ac1b2d85...)
- completed task B (Session: a45cff1b...)
- went for lunch (Session: 2c04360b...)
- completed task C (Session: 98437846...)
- went to the gym (Session: a6a7e124...)

## Detailed Scenario Analysis

### Scenario 1: Store initial user profile (long-term seed)

**Description**: 

**Execution**:
- Turns executed: 3
- Profile fields updated: 1
- Episodes created: 0

**Profile Updates**:
- name: Linh

### Scenario 2: Recall profile after unrelated conversation

**Description**: 

**Execution**:
- Turns executed: 4
- Profile fields updated: 0
- Episodes created: 0

### Scenario 3: Overwrite preference with conflict

**Description**: 

**Execution**:
- Turns executed: 4
- Profile fields updated: 0
- Episodes created: 0

### Scenario 4: Episodic memory with multiple events

**Description**: 

**Execution**:
- Turns executed: 5
- Profile fields updated: 0
- Episodes created: 4

### Scenario 5: Episodic vs long-term distinction

**Description**: 

**Execution**:
- Turns executed: 3
- Profile fields updated: 0
- Episodes created: 5

### Scenario 6: Semantic retrieval with FAQ and follow-up

**Description**: 

**Execution**:
- Turns executed: 3
- Profile fields updated: 0
- Episodes created: 0

### Scenario 7: Combine semantic knowledge with personal context

**Description**: 

**Execution**:
- Turns executed: 3
- Profile fields updated: 0
- Episodes created: 6

### Scenario 8: Long context trimming with important early fact

**Description**: 

**Execution**:
- Turns executed: 10
- Profile fields updated: 0
- Episodes created: 0

### Scenario 9: Implicit recall from long-term memory

**Description**: 

**Execution**:
- Turns executed: 3
- Profile fields updated: 0
- Episodes created: 0

### Scenario 10: Chained reasoning + memory + overwrite check

**Description**: 

**Execution**:
- Turns executed: 5
- Profile fields updated: 0
- Episodes created: 0

## Key Achievements

✓ **10/10 scenarios executed successfully**
✓ **Profile memory**: Captured 1 user attributes
✓ **Episodic memory**: Logged 6 significant events
✓ **Memory isolation**: Each scenario ran with fresh memory state
✓ **Background saving**: Memory updates persisted via threading

