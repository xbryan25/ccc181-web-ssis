export interface Program {
  programCode: string;
  programName: string;
  collegeCode: string;
};

export interface ProgramFormState {
  programCode: string;
  programName: string;
  collegeCode: { label: string };
}