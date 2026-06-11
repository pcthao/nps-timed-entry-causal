## Did Timed Entry Reduce Crowding at Rocky Mountain National Park?

##### Overview

National Parks across the United States have experienced record visitation growth, creating challenges around traffic congestion, parking availability, trail crowding, and visitor experience. In response, several parks have implemented reservation-based access systems.

This project evaluates whether Rocky Mountain National Park’s timed-entry reservation system reduced visitor crowding using a synthetic control causal inference approach.

Instead of comparing visitation before and after implementation, I estimate a counterfactual:

**What would RMNP visitation have looked like if timed entry had never been introduced?**

A synthetic version of RMNP was constructed using a weighted combination of comparable National Parks that did not implement major access restrictions.

##### Research Question
Did timed entry reduced peak-season crowding at Rocky Mountain NP? 
Specically:
- Did peak-season visitation decline after timed entry?
- Were changes larger than expected compared with similar parks?
- Did time entry redistribute visitation or reduced overall demand?

Data: NPS Monthly Recreation Visitation Statistics 

##### Methods:

Syntehtic Control Model



Project Sctructure: 

notebooks/
├── 01_data_collection.ipynb
├── 02_intervention_database.ipynb
├── 03_donor_selection.ipynb
├── 04_exploratory_analysis.ipynb
├── 05_synthetic_control.ipynb
├── 06_model_validation.ipynb
└── 07_results_and_insights.ipynb
