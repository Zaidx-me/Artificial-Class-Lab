# AI Coding IDE Benchmarking Assignment - Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Benchmark 10 modern AI coding IDEs by building the same minimal Python program in each, then create a handwritten report with pros/cons and final ranking.

**Architecture:** Phased approach - setup all IDEs first, then execute the same small Python task (~15-20 min each), collect data, analyze, and write report. Fast to complete - ~6 hours total.

**Tech Stack:** Python 3 + pytest (minimal, no frameworks needed)

**Spec:** assignment_01/task-spec.md (to be created)

## Global Constraints

- Same task specification used for ALL 10 IDEs (no changes mid-experiment)
- Time limit: 20 minutes per IDE maximum (hard stop)
- Use only Python standard library + pytest
- Record timing from first prompt to working program
- Note setup time (install/config) separately for each IDE
- All code saved in implementations/ folder

---

## The 10 IDEs (Final Selection)

| # | Folder | IDE | Type |
|---|--------|-----|------|
| 1 | 01-cursor | Cursor | Standalone VS Code fork |
| 2 | 02-windsurf | Windsurf | Standalone VS Code fork |
| 3 | 03-trae | Trae | Standalone VS Code fork |
| 4 | 04-zed | Zed AI | Native Rust GUI IDE |
| 5 | 05-replit | Replit | Cloud browser IDE |
| 6 | 06-vscode-copilot | VS Code + Copilot | Editor + Extension |
| 7 | 07-vscode-cline | VS Code + Cline | Editor + Autonomous Agent |
| 8 | 08-claude-code | Claude Code | CLI Agent |
| 9 | 09-aider | Aider | Terminal Agent |
| 10 | 10-codeium | Codeium | Editor + Extension |

---

## Phase 1: Project Setup (~30 min)

### Task 1: Create Repository Structure

**Files:**
- Create: `assignment_01/README.md`
- Create: `assignment_01/task-spec.md`
- Create: `assignment_01/benchmark-data/raw-results.csv`
- Create: `assignment_01/benchmark-data/scoring-rubric.md`

- [ ] **Step 1: Clone/update your repo**

```bash
cd /path/to/your/workspace
git clone https://github.com/zaidx-me/artificial-class-lab.git
cd artificial-class-lab
git checkout -b assignment-01
```

- [ ] **Step 2: Create folder structure**

```bash
mkdir -p assignment_01/{ide-setup-notes,implementations,benchmark-data}
mkdir -p assignment_01/implementations/{01-cursor,02-windsurf,03-trae,04-zed,05-replit,06-vscode-copilot,07-vscode-cline,08-claude-code,09-aider,10-codeium}
```

- [ ] **Step 3: Create task-spec.md**

The EXACT same task given to all 10 IDEs:

```markdown
# Benchmark Task: Student Grades Manager (Python)

Build a Python CLI program called `grades.py` with:

## Requirements
1. Read student records from a text file `students.txt` (format per line: `Name,Mark1,Mark2,Mark3`)
2. For each student, compute:
   - Average mark
   - Highest mark
   - Letter grade (A: >=85, B: >=70, C: >=60, D: >=50, F: <50)
3. Print results as a neatly formatted table
4. Show class statistics: overall average, highest scorer name, lowest scorer name
5. Handle invalid lines gracefully (skip them, print a warning)

## Files
- `grades.py` - main program
- `test_grades.py` - 3 unit tests with pytest
- `students.txt` - sample data (provide at least 5 students)

## Sample Input (students.txt)
```
Ali,78,85,90
Sara,62,70,55
Hamza,92,88,95
Ayesha,45,50,48
Bilal,70,73,69
```

## Example Output
```
Name        Average   Highest   Grade
--------------------------------------
Ali         84.33     90        B
Sara        62.33     70        C
Hamza       91.67     95        A
Ayesha      47.67     50        F
Bilal       70.67     73        C

Class Stats:
Overall Average: 71.33
Top Scorer: Hamza (91.67)
Lowest Scorer: Ayesha (47.67)
```
```

- [ ] **Step 4: Create scoring-rubric.md**

```markdown
# Scoring Rubric

## Metrics (1-10 scale unless noted)

### 1. Task Completion Time
- 0-10 min = 10/10
- 10-15 min = 8/10
- 15-20 min = 6/10
- Did not finish in 20 min = 2/10

### 2. AI Accuracy
Score how well AI suggestions performed:
- 10: All suggestions correct and useful
- 8: Most correct, few minor fixes needed
- 6: Mixed - several wrong suggestions
- 4: Mostly wrong, had to write most myself
- 2: AI actively harmful, disabled it

### 3. Features Completed (%)
- % of 5 requirements from task-spec completed correctly

### 4. Code Quality
- Follows conventions (PEP8): 3 pts
- Readable, clear naming: 3 pts
- Correct error handling: 2 pts
- Efficient/simple solution: 2 pts
- Total: 10 pts

### 5. Setup Difficulty (1-5, lower is easier)
- 1: Install and ready in < 2 min
- 3: Some config needed (API key, account)
- 5: Complex setup, multiple issues

### Scoring Formula
Composite = (Time x 0.25) + (AI Accuracy x 0.20) + (Features % / 10 x 0.25) + (Code Quality x 0.30)
```

- [ ] **Step 5: Create raw-results.csv template**

```csv
IDE,Type,Setup_Time_Min,Task_Time_Min,AI_Accuracy_1_10,Features_Completed_Pct,Code_Quality_1_10,Setup_Difficulty_1_5,Notable_Observations
Cursor,Standalone Fork,,,,,,,
Windsurf,Standalone Fork,,,,,,,
Trae,Standalone Fork,,,,,,,
Zed AI,Native GUI IDE,,,,,,,
Replit,Cloud Browser IDE,,,,,,,
VS Code + Copilot,Editor + Ext,,,,,,,
VS Code + Cline,Editor + Agent,,,,,,,
Claude Code,CLI Agent,,,,,,,
Aider,CLI Agent,,,,,,,
Codeium,Editor + Ext,,,,,,,
```

- [ ] **Step 6: Commit**

```bash
git add assignment_01/
git commit -m "feat: setup assignment_01 structure and task specification"
```

---

## Phase 2: IDE Installation (~1-2 hours)

### Task 2: Install and Document All 10 IDEs

**Files:**
- Create: `assignment_01/ide-setup-notes/01-cursor.md` (and 9 more)

**Instructions:** For each IDE, create a markdown file documenting:
1. Installation steps
2. First-time configuration
3. Account/login required (yes/no)
4. Pricing (free tier limits)
5. Time taken to install and configure

- [ ] **Step 1: Install Cursor**

```bash
paru -S --noconfirm cursor-bin
```

- [ ] **Step 2: Install Windsurf**

```bash
paru -Ss windsurf   # find package name, then:
paru -S --noconfirm windsurf
```

- [ ] **Step 3: Install Trae**

```bash
paru -Ss trae   # or download installer from https://trae.ai
```

- [ ] **Step 4: Install Zed AI**

```bash
sudo pacman -S zed        # if not in repos:
paru -S --noconfirm zed-editor
# sign in (Settings -> Accounts) to enable Zed AI assistant
```

- [ ] **Step 5: Install Replit**

```bash
# browser-based - no install. Just open https://replit.com and sign in
```

- [ ] **Step 6: Install VS Code + Copilot extension**

```bash
code --install-extension GitHub.copilot
# sign in with GitHub (free with Student Pack)
```

- [ ] **Step 7: Install VS Code + Cline extension**

```bash
code --install-extension saoudrizwan.claude-dev
# needs an API key (Claude/OpenAI) in Cline settings
```

- [ ] **Step 8: Install Claude Code (CLI)**

```bash
npm install -g @anthropic-ai/claude-code
# requires Anthropic API key (set ANTHROPIC_API_KEY)
```

- [ ] **Step 9: Install Aider (terminal)**

```bash
pip install aider-chat
# requires API key (set OPENAI_API_KEY or ANTHROPIC_API_KEY)
```

- [ ] **Step 10: Install Codeium extension**

```bash
code --install-extension Codeium.codeium
# free tier, no credit card
```

- [ ] **Step 11: Commit all setup notes**

```bash
git add assignment_01/ide-setup-notes/
git commit -m "feat: document installation and setup for all 10 IDEs"
```

---

## Phase 3: Benchmark Execution (~3-4 hours total)

### Task 3: Execute Benchmark in Each IDE

**Instructions:** For each IDE, run the exact same procedure:

- [ ] **Step 1: Start timer**

Note start time. Open the IDE, create `grades.py` in that IDE's project folder.

- [ ] **Step 2: Provide task specification**

Ask the AI: "Build the program described in task-spec.md" (paste the task-spec content).

- [ ] **Step 3: Monitor and record**

- Count helpful vs unhelpful AI suggestions
- Note what the AI got right/wrong
- Track time waiting vs writing code
- Note any errors and how they were resolved

- [ ] **Step 4: Test the program**

```bash
python3 grades.py
pytest test_grades.py
```

- [ ] **Step 5: Stop at 20 min mark (hard stop)**

Record total time. Score the IDE: fill in CSV row.

- [ ] **Step 6: Save implementation**

Copy working code to that IDE's `implementations/NN-xxx/` folder.

- [ ] **Step 7: Commit**

```bash
git add assignment_01/implementations/01-cursor/
git commit -m "feat: Cursor benchmark - [time] min"
```

**Benchmark order (10 x 20 min):**
1. Cursor
2. Windsurf
3. Trae
4. Zed AI
5. Replit
6. VS Code + Copilot
7. VS Code + Cline
8. Claude Code
9. Aider
10. Codeium

---

## Phase 4: Data Analysis (~1 hour)

### Task 4: Analyze Benchmark Results

**Files:**
- Modify: `assignment_01/benchmark-data/raw-results.csv`
- Create: `assignment_01/benchmark-data/ranking-table.md`
- Create: `assignment_01/benchmark-data/analysis.md`

- [ ] **Step 1: Calculate composite scores in the CSV**

Add a `Composite_Score` column to the CSV.

- [ ] **Step 2: Create ranking table**

```markdown
| Rank | IDE | Composite | Time (min) | AI Accuracy | Features % | Code Quality |
|------|-----|-----------|------------|-------------|------------|--------------|
| 1    | ... | ...       | ...        | ...         | ...        | ...          |
```

- [ ] **Step 3: Write analysis.md**

- Top 3 performers and why
- Bottom 3 and why
- Best for students (free tier)
- Best value for money
- Surprising findings

- [ ] **Step 4: Commit**

```bash
git add assignment_01/benchmark-data/
git commit -m "feat: complete benchmark analysis and ranking"
```

---

## Phase 5: Handwritten Report (~2-3 hours)

### Task 5: Write the Handwritten Report

**Instructions:** Use this outline to write pages by hand (estimate ~10-12 pages).

- [ ] **Step 1: Page 1 - Title Page**

- Assignment title: "Benchmarking 10 Modern AI Coding IDEs"
- Name: Muhammad Zaid, 5th Semester IT
- University: University of the Punjab, Lahore
- Date, Course (Artificial Intelligence)

- [ ] **Step 2: Pages 2-3 - Introduction**

- What are AI coding IDEs?
- Why benchmark them (motivation)
- Methodology summary (task, metrics, time limit)

- [ ] **Step 3: Pages 4-5 - IDE Profiles**

Brief description (2-3 lines each) for all 10 IDEs:
- Cursor, Windsurf, Trae, Zed AI, Replit, VS Code + Copilot, VS Code + Cline, Claude Code, Aider, Codeium

- [ ] **Step 4: Page 6 - Task Description**

- The Student Grades Manager task (brief)
- Tech: Python 3 + pytest
- 5 requirements

- [ ] **Step 5: Pages 7-8 - Results & Ranking**

- Copy the ranking table
- Show composite scores chart (draw by hand - bar chart works well)

- [ ] **Step 6: Pages 9-10 - Pros and Cons**

One short section per IDE:
- Pros (3-4 bullets)
- Cons (3-4 bullets)

- [ ] **Step 7: Page 11 - Final Ranking & Recommendation**

- Top 5 recommendation
- Best for students (free/cheap)
- Best for professionals
- Best value for money
- Final verdict

- [ ] **Step 8: Page 12 - Conclusion**

- Key learnings
- How AI IDEs changed your workflow
- Reference: GitHub repo (zaidx-me/artificial-class-lab/assignment_01)

- [ ] **Step 9: Save outline to repo**

Create `assignment_01/handwritten-report-outline.md` with this structure.

```bash
git add assignment_01/handwritten-report-outline.md
git commit -m "feat: add handwritten report outline"
```

---

## Phase 6: Submission (~30 min)

### Task 6: Prepare Submission

- [ ] **Step 1: Update README.md**

Assignment overview, links to each implementation, results, findings.

- [ ] **Step 2: Verify all commits**

```bash
git log --oneline -20
```

- [ ] **Step 3: Push to GitHub**

```bash
git push -u origin assignment-01
```

- [ ] **Step 4: Organize handwritten pages**

Number pages, add table of contents, draw bar/line charts by hand.

---

## Summary: Timeline (6-8 hours split over 1-2 days)

| Phase | What | Time |
|-------|------|------|
| 1 | Repo + task-spec + rubric | 30 min |
| 2 | Install all 10 IDEs + notes | 1-2 hours |
| 3 | Run benchmark x 10 (20 min each) | 3-4 hours |
| 4 | Analysis + ranking | 1 hour |
| 5 | Handwritten report | 2-3 hours |
| 6 | Push + submission prep | 30 min |
| **Total** | | **~6-8 hours (1 weekend day ok)** |

---

## Success Criteria

- [ ] All 10 IDEs benchmarked with working `grades.py` + tests
- [ ] CSV filled with all metrics per IDE
- [ ] Ranking table created and sorted by composite score
- [ ] Handwritten report complete (~12 pages)
- [ ] All code committed and pushed to GitHub
- [ ] README.md updated in assignment_01/

---

## Notes for Muhammad Zaid

1. **Hard time limit:** 20 minutes per IDE - if it doesn't finish, that's the data point.
2. **Same command every time:** Give each IDE the identical task prompt. No editing.
3. **Track everything:** 20 min is short; take notes as you go.
4. **Free tiers:** Use free tiers wherever possible (Copilot Student Pack, free Codeium/Trae/Windsurf tiers, etc.).
5. **Screenshots:** Grab 1-2 screenshots of each IDE in action for your report.
6. **The Data is the Report:** Even bad scores are interesting findings - write honestly.