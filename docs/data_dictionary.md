# Data dictionary

## `sample_patients.csv`

| Field | Meaning |
|---|---|
| patient_id | Sample identifier such as `P000001` |
| arrival_time_min | Minutes from start of sample-data day |
| pathway_id | Sample pathway label |
| acuity_level | Sample urgency/severity class from 1 to 5 |
| no_show_probability | Sample no-show probability |
| emergency_flag | Sample emergency insertion indicator |

## `sample_services.csv`

| Field | Meaning |
|---|---|
| patient_id | Sample patient identifier |
| station_id | Sample service station |
| sequence_order | Pathway step order |
| planned_start_min | Planned start time in minutes |
| service_duration_min | Sample service duration |
| resource_id | Sample resource identifier |

## `sample_resources.csv`

| Field | Meaning |
|---|---|
| resource_id | Sample resource identifier |
| station_id | Assigned station |
| capacity | Sample capacity |
| resource_type | staff, equipment, or room |

## `sample_pathways.csv`

| Field | Meaning |
|---|---|
| pathway_id | Sample pathway label |
| station_sequence | Ordered station sequence, separated by `>` |
| clinical_group | Sample-data workflow group |
