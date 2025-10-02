

type YearLevelDemographicsResponse = {
    count: number,
    yearLevel: string,
}

export function useYearLevelDemographics(){
  const apiUrl = import.meta.env.VITE_API_URL;

  return $fetch<YearLevelDemographicsResponse[]>(`${apiUrl}/api/students/year-level-demographics`, {
    method: 'GET',
    credentials: 'include',

  });
};