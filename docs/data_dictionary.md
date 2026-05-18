# Data dictionary

## `synthetic_patients.csv`

| Field | Meaning |
|---|---|
| patient_id | Synthetic identifier such as `SP000001` |
| arrival_time_min | Minutes from start of synthetic day |
| pathway_id | Synthetic pathway label |
| acuity_level | Synthetic urgency/severity class from 1 to 5 |
| no_show_probability | Synthetic no-show probability |
| emergency_flag | Synthetic emergency insertion indicator |

## `synthetic_services.csv`

| Field | Meaning |
|---|---|
| patient_id | Synthetic patient identifier |
| station_id | Synthetic service station |
| sequence_order | Pathway step order |
| planned_start_min | Planned start time in minutes |
| service_duration_min | Synthetic service duration |
| resource_id | Synthetic resource identifier |

## `synthetic_resources.csv`

| Field | Meaning |
|---|---|
| resource_id | Synthetic resource identifier |
| station_id | Assigned station |
| capacity | Synthetic capacity |
| resource_type | staff, equipment, or room |

## `synthetic_pathways.csv`

| Field | Meaning |
|---|---|
| pathway_id | Synthetic pathway label |
| station_sequence | Ordered station sequence, separated by `>` |
| clinical_group | Synthetic workflow group |
