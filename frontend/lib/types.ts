export type EvidenceItem = {
  source: string;
  sourceRecordId: string;
  title: string;
  detail: string;
};

export type TargetScorecard = {
  targetId: string;
  targetSymbol: string;
  targetName: string;
  diseaseId: string;
  diseaseName: string;
  overallScore: number;
  percentile: number;
  profile: string;
  freshnessDays: number;
  confidenceLabel: string;
  components: {
    associationEvidence: number;
    clinicalSupport: number;
    chemicalSupport: number;
    tractability: number;
    confidenceModifier: number;
    safetyPenalty: number;
  };
  explanation: {
    summary: string;
    supportingEvidence: EvidenceItem[];
    riskEvidence: EvidenceItem[];
  };
};

export type SourceStatus = {
  source: string;
  lastSuccessfulIngestAt: string;
  freshnessHours: number;
  rowCount: number;
  mappingCoverage: number;
  validationStatus: string;
};

export type DiseaseSummary = {
  id: string;
  label: string;
  synonyms: string[];
};

export type TargetDetail = {
  targetId: string;
  targetSymbol: string;
  targetName: string;
  diseaseId: string;
  diseaseName: string;
  scorecard: TargetScorecard;
  linkedCompounds: {
    chemblId: string;
    name: string;
    modality: string;
  }[];
  linkedTrials: {
    nctId: string;
    title: string;
    phase: string;
    status: string;
  }[];
  safetySignals: {
    source: string;
    ingredient: string;
    seriousEventCount: number;
    warningFlag: boolean;
    detail: string;
  }[];
};
