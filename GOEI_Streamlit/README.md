# GOEI Streamlit Dashboard

Local Python prototype of the GOIP platform described in the attached GOEI V3 revised proposal.
Arabic default, English toggle, seven sections, sample regional CSV, transparent opportunity scoring,
skill matching, policy simulation, JSON scenario save/load, and CSV export.

## Windows quick start
1. Install Python 3.11 or newer. Select “Add python.exe to PATH” during installation.
2. Extract this ZIP completely. Open the extracted GOEI_Streamlit folder.
3. Double-click run_windows.bat. Internet is required for the initial package installation.
4. Keep the terminal open. The dashboard opens at http://localhost:8501.
5. Press Ctrl+C in the terminal to stop it.

## PowerShell manual steps
Open PowerShell in the extracted folder containing app.py:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run app.py
```

If `py` is unavailable, use `python -m venv .venv` for the first command.
No virtual-environment activation or execution-policy change is needed.
The leading `.\` is important in PowerShell.

## Command Prompt
```cmd
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe -m streamlit run app.py
```

## macOS / Linux
```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m streamlit run app.py
```

## Data and paths
The included data/regions.csv prevents the missing regions.csv error. Data paths are resolved
relative to core.py, so starting the app from another directory works too.
Regional percentages, historical variations and SME scores are invented demonstration data.
No API keys, n8n, Zapier, paid services or external data connections are used.
Once dependencies are installed, the local dashboard needs no internet connection.

## Model scope
- Opportunity score: weighted sum of employment, poverty resilience, skills, digital and SME scores.
  Components are bounded to 0–100. Demonstration weights are 25/25/20/15/15 percent.
- Matching: required-skills overlap; roles are samples, not live vacancies.
- Simulation: illustrative budget-effect formulas, not trained AI or causal inference.
  Allocations must total 100 percent. Coefficients need empirical calibration.
- Aggregates: simple regional means, not population-weighted estimates.
- Proposal targets are preserved as proposed ambitions. Funding is not secured.
- JSON downloads save scenarios as files on your computer; reload them on the simulator page.
  Allocation and budget load from JSON. Region/year remain the sidebar selections.
No personal data, automatic funding decisions or institutional endorsement is implied.

## Files
app.py — Streamlit UI
core.py — data validation and demonstration calculations
data/regions.csv — bundled sample dataset
requirements.txt — Python packages
.streamlit/config.toml — green theme and telemetry disabled
run_windows.bat — Windows launcher
README.md — these instructions
