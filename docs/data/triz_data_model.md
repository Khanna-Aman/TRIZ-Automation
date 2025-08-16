# TRIZ Data Model

## Entities
- triz_principle(id, name, description)
- triz_parameter(id, name, description)
- triz_matrix_link(improving_param, worsening_param, principle_id)

## Usage
- Lookup principles by parameter pair
- Store full 40 principles and 39 parameters

## Import
- See services/triz/import_triz_matrix.py
- Input formats: JSON (principles, parameters) and CSV (matrix)

