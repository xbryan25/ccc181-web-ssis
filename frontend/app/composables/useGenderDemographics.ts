

type GenderDemographicsResponse = {
    count: number,
    gender: string,
}

export function useGenderDemographics(){
  const apiUrl = import.meta.env.VITE_API_URL;

  return $fetch<GenderDemographicsResponse[]>(`${apiUrl}/api/students/gender-demographics`, {
    method: 'GET',
    credentials: 'include',

  });
};