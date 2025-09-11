export interface Student {
  idNumber: string;
  firstName: string;
  lastName: string;
  yearLevel: "1st" | "2nd" | "3rd" | "4th" | "4th+";
  gender: "Male" | "Female" | "Others" | "Prefer not to say";
  programCode: string;
};
