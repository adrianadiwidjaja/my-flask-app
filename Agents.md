# AGENT.md

## Purpose
This agent is responsible for executing prompts, running system commands, and maintaining a clear, auditable log of all its actions.

## Setup Instructions
1. **Run Initialization Script**
   - Upon startup, execute the `setup.sh` script to configure the project environment.
   - Command:
     ```bash
     bash setup.sh
     ```

2. **Action Execution**
   - For each task or prompt provided, the agent must:
     - Execute the required commands (e.g., bash commands, scripts, utilities).
     - Log each executed command and a brief description of the action into `logging.txt`.

3. **Logging Format**
   - Each entry in `logging.txt` must include:
     - **Timestamp** (ISO 8601 format)
     - **Action Summary** (brief description)
     - **Exact Command Executed**
   - Example entry:
     ```
     [2025-04-28T15:32:05Z] - Initialized virtual environment
     Command: python3 -m venv venv
     ```

4. **Summary at Completion**
   - After completing all assigned tasks, append a **final summary section** in `logging.txt` that briefly describes:
     - Total number of actions
     - Any errors encountered
     - Overall success status

## Example Workflow
```bash
# Step 1: Initialization
bash setup.sh

# Step 2: Execute task
<run prompt instructions>
<log action details>

# Step 3: Final summary
<append summary to logging.txt>
