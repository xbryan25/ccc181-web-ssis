
type UseEntitiesResponse = {
    totalCount: number
}

export function useEntitiesCount(entityType: string, 
                                  options?: {
                                    searchValue?: string, 
                                    searchBy?: string, 
                                    searchType?: string,
                                    filterByGender?: string,
                                    filterByYearLevel?: string,
                                    filterByProgramCode?: string,
                                    filterBy?: Record<string, string | number>
                                }){

  const { $apiFetch } = useNuxtApp();

  return $apiFetch<UseEntitiesResponse>(`/api/${entityType}/total-count`, {
    method: 'GET',
    credentials: 'include',
    query: {
      ...(options || {}),
    },
  });
};

