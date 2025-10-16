
type UseEntitiesResponse = {
    totalCount: number
}

export function useEntitiesCount(entityType: string, 
                                  options?: {
                                    searchValue?: string, 
                                    searchBy?: string, 
                                    searchType?: string,
                                    filterBy?: Record<string, string | number>
                                }){

  const apiUrl = import.meta.env.VITE_API_URL;

  return $fetch<UseEntitiesResponse>(`${apiUrl}/api/${entityType}/total-count`, {
    method: 'GET',
    credentials: 'include',
    query: {
      ...(options || {}),
    },
  });
};

