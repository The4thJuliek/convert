# To be used to export and convert annotations from INCEpTION.
# Hard install: python -m pip install dkpro-cassis 
# Export the annotations from INCEpTION using the XMI format.

import json
from cassis import *

# Load TypeSystem and CAS
with open('typesystem.xml', 'rb') as f:
    typesystem = load_typesystem(f)

#Insert filename.xmi
with open('admin.xmi', 'rb') as f:
    cas = load_cas_from_xmi(f, typesystem=typesystem)


def cas_to_conllu(cas):
    conllu_lines = []
    sentence_id = 1  # Starting with the first sentence ID

    # Create mappings for custom layer annotations by offsets
    dict_deaf_map = {
        (ann.begin, ann.end): ";".join(ann.DictionaryDefinitionDEAF.elements)
        for ann in cas.select("webanno.custom.DictDEAF") if ann.DictionaryDefinitionDEAF
    }
    dict_hindley_map = {
        (ann.begin, ann.end): ";".join(ann.DictionaryDefinition.elements)
        for ann in cas.select("webanno.custom.DictHindley") if ann.DictionaryDefinition
    }
    trotter_glossary_map = {
        (ann.begin, ann.end): ";".join(ann.TrotterDefinition.elements)
        for ann in cas.select("webanno.custom.TrotterGlossary") if ann.TrotterDefinition
    }
    named_entity_map = {
        (ann.begin, ann.end): ann.value if hasattr(ann, "value") and ann.value else "_"
        for ann in cas.select("de.tudarmstadt.ukp.dkpro.core.api.ner.type.NamedEntity")
    }

    # Extract Token Annotations and align with definitions
    for token in cas.select("de.tudarmstadt.ukp.dkpro.core.api.segmentation.type.Token"):
        # Align definitions with token offsets
        dict_deaf_def = dict_deaf_map.get((token.begin, token.end), "_")
        dict_hindley_def = dict_hindley_map.get((token.begin, token.end), "_")
        trotter_def = trotter_glossary_map.get((token.begin, token.end), "_")
        named_entity = named_entity_map.get((token.begin, token.end), "_")

        # Add the row
        conllu_lines.append(
            f"{sentence_id}\t{token.get_covered_text()}\t{token.lemma.value if token.lemma else '_'}\t"
            f"{token.pos.coarseValue if token.pos else '_'}\t"
            f"{token.pos.PosValue if token.pos else '_'}\t_\t0\troot\t_\t"
            f"{dict_deaf_def}\t{dict_hindley_def}\t{trotter_def}\t{named_entity}"
        )

    conllu_lines.append("")  # Add a blank line between sentences
    return "\n".join(conllu_lines)


def cas_to_json(cas):
    annotations = []

    # Extract Token Annotations
    for token in cas.select("de.tudarmstadt.ukp.dkpro.core.api.segmentation.type.Token"):
        annotation = {
            "type": "Token",
            "begin": token.begin,
            "end": token.end,
            "text": token.get_covered_text(),
            "lemma": token.lemma.value if token.lemma else None,
            "upos": token.pos.coarseValue if token.pos else None,
            "xpos": token.pos.PosValue if token.pos else None
        }
        annotations.append(annotation)

    # Extract DictDEAF Annotations
    for dict_deaf in cas.select("webanno.custom.DictDEAF"):
        dictionary_definition = (
            ";".join(dict_deaf.DictionaryDefinitionDEAF.elements)
            if dict_deaf.DictionaryDefinitionDEAF else None
        )
        annotation = {
            "type": "DictDEAF",
            "begin": dict_deaf.begin,
            "end": dict_deaf.end,
            "text": dict_deaf.get_covered_text(),
            "DictionaryDefinitionDEAF": dictionary_definition
        }
        annotations.append(annotation)

    # Extract DictHindley Annotations
    for dict_hindley in cas.select("webanno.custom.DictHindley"):
        dictionary_definition = (
            ";".join(dict_hindley.DictionaryDefinition.elements)
            if dict_hindley.DictionaryDefinition else None
        )
        annotation = {
            "type": "DictHindley",
            "begin": dict_hindley.begin,
            "end": dict_hindley.end,
            "text": dict_hindley.get_covered_text(),
            "DictionaryDefinition": dictionary_definition
        }
        annotations.append(annotation)

    # Extract TrotterGlossary Annotations
    for trotter_glossary in cas.select("webanno.custom.TrotterGlossary"):
        trotter_definition = (
            ";".join(trotter_glossary.TrotterDefinition.elements)
            if trotter_glossary.TrotterDefinition else None
        )
        annotation = {
            "type": "TrotterGlossary",
            "begin": trotter_glossary.begin,
            "end": trotter_glossary.end,
            "text": trotter_glossary.get_covered_text(),
            "TrotterDefinition": trotter_definition
        }
        annotations.append(annotation)

    # Extract NamedEntity Annotations
    for named_entity in cas.select("de.tudarmstadt.ukp.dkpro.core.api.ner.type.NamedEntity"):
        annotation = {
            "type": "NamedEntity",
            "begin": named_entity.begin,
            "end": named_entity.end,
            "text": named_entity.get_covered_text(),
            "value": named_entity.value if hasattr(named_entity, "value") else None
        }
        annotations.append(annotation)

    return annotations


def cas_to_tsv(cas):
    tsv_lines = []
    # Header for the TSV file
    tsv_lines.append("Type\tBegin\tEnd\tText\tLemma\tUPOS\tXPOS\tDictDEAF\tDictHindley\tTrotterGlossary\tNamedEntity")

    # Create mappings for custom layer annotations by offsets
    dict_deaf_map = {
        (ann.begin, ann.end): ";".join(ann.DictionaryDefinitionDEAF.elements)
        for ann in cas.select("webanno.custom.DictDEAF") if ann.DictionaryDefinitionDEAF
    }
    dict_hindley_map = {
        (ann.begin, ann.end): ";".join(ann.DictionaryDefinition.elements)
        for ann in cas.select("webanno.custom.DictHindley") if ann.DictionaryDefinition
    }
    trotter_glossary_map = {
        (ann.begin, ann.end): ";".join(ann.TrotterDefinition.elements)
        for ann in cas.select("webanno.custom.TrotterGlossary") if ann.TrotterDefinition
    }
    named_entity_map = {
        (ann.begin, ann.end): ann.value if hasattr(ann, "value") and ann.value else "_"
        for ann in cas.select("de.tudarmstadt.ukp.dkpro.core.api.ner.type.NamedEntity")
    }

    # Extract Token Annotations and align with definitions
    for token in cas.select("de.tudarmstadt.ukp.dkpro.core.api.segmentation.type.Token"):
        # Align definitions with token offsets
        dict_deaf_def = dict_deaf_map.get((token.begin, token.end), "_")
        dict_hindley_def = dict_hindley_map.get((token.begin, token.end), "_")
        trotter_def = trotter_glossary_map.get((token.begin, token.end), "_")
        named_entity = named_entity_map.get((token.begin, token.end), "_")

        # Add the row
        tsv_lines.append(
            f"Token\t{token.begin}\t{token.end}\t{token.get_covered_text()}\t"
            f"{token.lemma.value if token.lemma else '_'}\t"
            f"{token.pos.coarseValue if token.pos else '_'}\t"
            f"{token.pos.PosValue if token.pos else '_'}\t"
            f"{dict_deaf_def}\t{dict_hindley_def}\t{trotter_def}\t{named_entity}"
        )

    return "\n".join(tsv_lines)


# Generate CONLLU data
conllu_output = cas_to_conllu(cas)
with open('annotations_with_named_entities.conllu', 'w', encoding='utf-8') as f:
    f.write(conllu_output)

# Generate JSON data
annotations = cas_to_json(cas)
with open('annotations_with_named_entities.json', 'w', encoding='utf-8') as f:
    json.dump(annotations, f, ensure_ascii=False, indent=4)

# Generate TSV data
tsv_output = cas_to_tsv(cas)
with open('annotations_with_named_entities.tsv', 'w', encoding='utf-8') as f:
    f.write(tsv_output)

print("Annotations saved successfully!")
