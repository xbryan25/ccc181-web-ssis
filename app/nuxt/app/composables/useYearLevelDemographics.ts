

type YearLevelDemographicsResponse = {
    count: number,
    yearLevel: string,
}

export function useYearLevelDemographics(filterBy?: Record<string, string | number>){
  const { $apiFetch } = useNuxtApp();

  return $apiFetch<YearLevelDemographicsResponse[]>(`/api/students/year-level-demographics`, {
    method: 'GET',
    credentials: 'include',
    query: {
      ...(filterBy || {}),
    },
  });
};