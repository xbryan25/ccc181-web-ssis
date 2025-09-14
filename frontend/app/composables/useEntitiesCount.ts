
type UseEntitiesResponse = {
    entitiesCount: number
}

export function useEntitiesCount(entityType: string, 
                                options?: {
                                    searchValue?: string, 
                                    searchBy?: string, 
                                    searchType?: string,
                                }){

  const apiUrl = import.meta.env.VITE_API_URL;

  return useFetch<UseEntitiesResponse>(`${apiUrl}/api/${entityType}/count`, {
    method: 'GET',
    query: {
      ...(options || {})
    },
  });
};

