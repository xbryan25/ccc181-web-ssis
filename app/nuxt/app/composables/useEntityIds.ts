type UseCollegeCodesResponse = {
  collegeCode: string[];
}

type UseProgramCodesResponse = {
  collegeCode: string;
  programCodes: string[];
}

export function useEntityIds(entityType: string){

  const { $apiFetch } = useNuxtApp();

  return $apiFetch<UseCollegeCodesResponse[] | UseProgramCodesResponse[]>(`/api/${entityType}/identifiers`, {
    method: 'GET',
    credentials: 'include',
  });
};

