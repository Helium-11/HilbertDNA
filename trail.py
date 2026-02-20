from tex_to_dna import dna_to_text
import json

with open("storage/metadata.json") as f:
    metadata = json.load(f)

dna = metadata["c3ad8000-03ea-4c8f-ad1e-490241de5a73"]["dna"]

print(dna_to_text(dna))
