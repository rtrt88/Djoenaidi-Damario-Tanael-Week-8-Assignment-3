# CrewAI Mini Assignment - Student Subscription Plan

## 1) Business problem
This project looks at a simple business question: should a small coffee shop launch a student subscription plan?  
The crew analyzes student demand, business viability, and execution risk, then gives a final recommendation (launch now, pilot first, or do not launch).

## 2) How the 3 agents work together
The crew runs in sequence. First, the **Market Researcher** studies student behavior and identifies demand drivers and barriers. Next, the **Business Analyst** uses that output as context to compare low/base/high adoption scenarios and decide if the plan is commercially sensible. Finally, the **Report Writer** uses both previous outputs to create an owner-ready business report with a clear decision, weekly action plan, and KPIs. This setup makes the workflow logical: insights -> analysis -> final decision report.

## 3) Setup and run
1. (Optional) Create and activate a virtual environment.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create your env file:
   ```bash
   cp .env.example .env
   ```
4. Open `.env` and fill in your real API values.
5. Run:
   ```bash
   python crew.py
   ```

The final result is printed in the terminal.

## 4) Challenges and how they were solved
- **Challenge:** Making agent roles different enough for the rubric.  
  **Solution:** I rewrote each role with clear professional scope (consumer research, commercial analysis, executive reporting), plus measurable goals and behavior-focused backstories.
- **Challenge:** Making task dependencies explicit.  
  **Solution:** Task 2 uses `context=[task_1]`, and Task 3 uses `context=[task_1, task_2]`, so each step clearly builds on earlier outputs.
- **Challenge:** Getting strong, gradable outputs.  
  **Solution:** I used structured expected outputs (specific sections and counts) so results are easier to evaluate.

## 5) One thing I would change with more time
I would add a small input data file (sample student survey + basic sales numbers) so the analysis is grounded in fixed data and gives more repeatable outputs across runs.
