import type { YearLevel, Gender } from "./";

export interface Student {
  idNumber: string;
  firstName: string;
  lastName: string;
  yearLevel: YearLevel;
  gender: Gender;
  avatarUrl: string;
  programCode: string;
};

export interface StudentFormState {
  idNumber: string;
  firstName: string;
  lastName: string;
  yearLevel: { label: YearLevel };
  gender: { label: Gender };
  programCode: { label: string };
}