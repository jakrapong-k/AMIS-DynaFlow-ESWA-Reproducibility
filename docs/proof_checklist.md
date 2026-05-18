# ESWA proof and repository checklist

## Repository

- [ ] Repository is public.
- [ ] Repository URL matches the manuscript.
- [ ] README is complete.
- [ ] LICENSE is present.
- [ ] CITATION.cff is present.
- [ ] `requirements.txt` or `environment.yml` is present.
- [ ] Training/evaluation scripts are present.
- [ ] Configuration files are present for QI-MOGA, GAT-MAPPO, and TFT.
- [ ] Fixed seeds are documented.
- [ ] Synthetic data and data schemas are included.
- [ ] Privacy statement is included.
- [ ] No real patient data are included.
- [ ] No API keys, database credentials, or EHR/HIS credentials are included.

## Manuscript/proof risk terms

Search the proof and repository for the following terms before publication:

- `2^n classical solutions`
- `implicit parallel exploration`
- `quantum hardware`
- `quantum circuit`
- `superposition-based chromosome` in any misleading context

Use the scientifically safer phrasing:

> probabilistic amplitude-based chromosome representation maintaining probability distributions over candidate scheduling states.
