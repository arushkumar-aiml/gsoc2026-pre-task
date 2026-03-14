# GitHub Repository Intelligence Analyzer
### C2SI Pre-GSoC Task 2026 — Task 2
**Built by:** Arush Kumar  
**GitHub:** https://github.com/arushkumar-aiml

## Overview
A Python tool that analyzes multiple GitHub repositories 
and generates insights about their activity, complexity, 
and learning difficulty.

## Features
- Fetches real-time data from GitHub API
- Calculates Activity Score
- Estimates Complexity Score
- Classifies repositories as Beginner/Intermediate/Advanced
- Generates structured summary report
- Handles missing data and edge cases

## How to Run
1. Install requirements:
   pip install requests

2. Run the analyzer:
   python analyzer.py

## Sample Output
- Repository name and language
- Stars, Forks, Open Issues
- Activity Score
- Complexity Score  
- Difficulty Classification
- Summary of all repositories

## Scoring Formula
**Activity Score** = (Stars × 0.3) + (Forks × 0.3) + 
(Issues × 0.2) + (Commits × 0.1) + (Watchers × 0.1)

**Complexity Score** = Size score + Issues score + Language score

**Difficulty Classification:**
- Score 1-4 = Beginner
- Score 5-7 = Intermediate  
- Score 8+ = Advanced
