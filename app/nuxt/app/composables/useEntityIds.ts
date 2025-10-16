type UseCollegeCodesResponse = {
  collegeCode: string[];
}

type UseProgramCodesResponse = {
  collegeCode: string;
  programCodes: string[];
}

export function useEntityIds(entityType: string){

  const apiUrl = import.meta.env.VITE_API_URL;

  return $fetch<UseCollegeCodesResponse[] | UseProgramCodesResponse[]>(`${apiUrl}/api/${entityType}/identifiers`, {
    method: 'GET',
    credentials: 'include',
  });
};

