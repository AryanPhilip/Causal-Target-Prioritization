from __future__ import annotations

from ctpc.core.types import DiseaseSummary


UC_DISEASE = DiseaseSummary(
    id="MONDO:0005101",
    label="Ulcerative colitis",
    synonyms=["UC", "Inflammatory bowel disease, ulcerative colitis"],
)

RANKING_FIXTURES = [
    {
        "target_id": "ENSG00000162594",
        "target_symbol": "IL23R",
        "target_name": "Interleukin 23 receptor",
        "association_evidence": 96.0,
        "clinical_support": 84.0,
        "chemical_support": 70.0,
        "tractability": 60.0,
        "confidence_modifier": 3.7,
        "serious_event_count": 220,
        "warning_flag": False,
        "supporting_evidence": [
            {
                "source": "opentargets",
                "source_record_id": "ot-uc-il23r-genetics",
                "title": "Strong target-disease association",
                "detail": "Open Targets convergence highlights genetics and pathway support.",
            },
            {
                "source": "clinicaltrials",
                "source_record_id": "NCT05507294",
                "title": "Late-stage clinical activity",
                "detail": "Ulcerative colitis trial activity supports translational relevance.",
            },
        ],
        "risk_evidence": [
            {
                "source": "openfda",
                "source_record_id": "fda-uc-il23r-2025",
                "title": "Moderate serious adverse event burden",
                "detail": "Mapped ingredient signals place IL23R programs in the medium penalty band.",
            }
        ],
        "linked_compounds": [
            {"chembl_id": "CHEMBL4297425", "name": "Mirikizumab", "modality": "antibody"},
            {"chembl_id": "CHEMBL4152864", "name": "Risankizumab", "modality": "antibody"},
        ],
        "linked_trials": [
            {
                "nct_id": "NCT05507294",
                "title": "Mirikizumab in moderate to severe ulcerative colitis",
                "phase": "Phase 3",
                "status": "Completed",
            }
        ],
        "safety_signals": [
            {
                "source": "openfda",
                "ingredient": "mirikizumab",
                "serious_event_count": 220,
                "warning_flag": False,
                "detail": "Serious-event burden remains visible but below the high-risk band.",
            }
        ],
    },
    {
        "target_id": "ENSG00000162434",
        "target_symbol": "JAK1",
        "target_name": "Janus kinase 1",
        "association_evidence": 84.0,
        "clinical_support": 84.0,
        "chemical_support": 76.0,
        "tractability": 68.0,
        "confidence_modifier": 4.0,
        "serious_event_count": 180,
        "warning_flag": True,
        "supporting_evidence": [
            {
                "source": "clinicaltrials",
                "source_record_id": "NCT03739866",
                "title": "Strong clinical maturity",
                "detail": "JAK1-linked programs show extensive ulcerative colitis trial evidence.",
            },
            {
                "source": "chembl",
                "source_record_id": "CHEMBL-JAK1-UC",
                "title": "Deep compound landscape",
                "detail": "Multiple potent compounds support tractability and precedence.",
            },
        ],
        "risk_evidence": [
            {
                "source": "openfda",
                "source_record_id": "fda-uc-jak1-2025",
                "title": "Meaningful safety burden",
                "detail": "Serious-event volume and warnings push JAK1 into a visible safety penalty band.",
            }
        ],
        "linked_compounds": [
            {"chembl_id": "CHEMBL3989989", "name": "Upadacitinib", "modality": "small molecule"},
            {"chembl_id": "CHEMBL4594618", "name": "Filgotinib", "modality": "small molecule"},
        ],
        "linked_trials": [
            {
                "nct_id": "NCT03739866",
                "title": "Upadacitinib induction study in ulcerative colitis",
                "phase": "Phase 3",
                "status": "Completed",
            }
        ],
        "safety_signals": [
            {
                "source": "openfda",
                "ingredient": "upadacitinib",
                "serious_event_count": 180,
                "warning_flag": True,
                "detail": "Warnings and serious-event burden create a meaningful safety discount.",
            }
        ],
    },
    {
        "target_id": "ENSG00000232810",
        "target_symbol": "TNF",
        "target_name": "Tumor necrosis factor",
        "association_evidence": 70.0,
        "clinical_support": 90.0,
        "chemical_support": 68.0,
        "tractability": 82.0,
        "confidence_modifier": 4.5,
        "serious_event_count": 110,
        "warning_flag": True,
        "supporting_evidence": [
            {
                "source": "clinicaltrials",
                "source_record_id": "NCT00036439",
                "title": "Established clinical precedent",
                "detail": "TNF inhibition remains a validated clinical mechanism in UC.",
            },
            {
                "source": "chembl",
                "source_record_id": "CHEMBL-TNF-UC",
                "title": "Rich modality support",
                "detail": "Compound and biologic support make TNF highly tractable.",
            },
        ],
        "risk_evidence": [
            {
                "source": "openfda",
                "source_record_id": "fda-uc-tnf-2025",
                "title": "Moderate warning burden",
                "detail": "Post-market signals apply a medium safety penalty.",
            }
        ],
        "linked_compounds": [
            {"chembl_id": "CHEMBL1201606", "name": "Infliximab", "modality": "antibody"},
            {"chembl_id": "CHEMBL1201580", "name": "Adalimumab", "modality": "antibody"},
        ],
        "linked_trials": [
            {
                "nct_id": "NCT00036439",
                "title": "Infliximab maintenance study in ulcerative colitis",
                "phase": "Phase 3",
                "status": "Completed",
            }
        ],
        "safety_signals": [
            {
                "source": "openfda",
                "ingredient": "infliximab",
                "serious_event_count": 110,
                "warning_flag": True,
                "detail": "Post-market warnings keep TNF-directed programs in the medium band.",
            }
        ],
    },
]

SOURCE_STATUS_FIXTURES = [
    {
        "source": "opentargets",
        "last_successful_ingest_at": "2026-03-29T18:00:00Z",
        "freshness_hours": 30,
        "row_count": 182,
        "mapping_coverage": 0.99,
        "validation_status": "healthy",
    },
    {
        "source": "chembl",
        "last_successful_ingest_at": "2026-03-28T21:00:00Z",
        "freshness_hours": 51,
        "row_count": 244,
        "mapping_coverage": 0.94,
        "validation_status": "healthy",
    },
    {
        "source": "clinicaltrials",
        "last_successful_ingest_at": "2026-03-29T14:00:00Z",
        "freshness_hours": 34,
        "row_count": 37,
        "mapping_coverage": 0.91,
        "validation_status": "healthy",
    },
    {
        "source": "openfda",
        "last_successful_ingest_at": "2026-03-27T08:00:00Z",
        "freshness_hours": 88,
        "row_count": 48,
        "mapping_coverage": 0.76,
        "validation_status": "warning",
    },
]
