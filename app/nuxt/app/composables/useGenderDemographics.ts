

type GenderDemographicsResponse = {
    count: number,
    gender: string,
}

export function useGenderDemographics(filterBy?: Record<string, string | number>){
  const { $apiFetch } = useNuxtApp();

  return $apiFetch<GenderDemographicsResponse[]>(`/api/students/gender-demographics`, {
    method: 'GET',
    credentials: 'include',
    query: {
      ...(filterBy || {}),
    },
  });
};