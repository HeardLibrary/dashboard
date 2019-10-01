# Heard Library Dashboard

The goal of this project is to create a Dashboard for the Heard Library.

Note: current data are fake and for development purposes only.

## Repo structure

```
├── README.md                  : Description of this repository
├── LICENSE                    : GNU General Public License v3.0 for repo
├── data                       : CSV and JSON data sources for dashboard
├── lambdas                    : scripts for current projects
│   ├──                        : 
│   │
│   └── zips                   : directory for zipped lambda packages ready for CLI upload
│ 
├── python                     : Python scripts (desktop)
    └── process_files_desktop.py     : script to load CSV data from desktop drive to GitHub repo
└── stateMachines              : Amazon State Language (ASL) code describing state machines
    └── .json     : state machine for overall workflow
```


----
Revised 2019-10-01

