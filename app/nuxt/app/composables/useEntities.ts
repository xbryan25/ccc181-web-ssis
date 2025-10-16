import type { Student, Program, College } from "~/types";

type UseEntitiesResponse = {
    entities: Student[] | Program[] | College[]
}

export function useEntities(entityType: string, 
                            options?: {
                                rowsPerPage?: number, 
                                pageNumber?: number, 
                                searchValue?: string, 
                                searchBy?: string, 
                                searchType?: string, 
                                sortField?: string, 
                                sortOrder?: string
                            }){

  const apiUrl = import.meta.env.VITE_API_URL;

  return $fetch<UseEntitiesResponse>(`${apiUrl}/api/${entityType}/`, {
    method: 'GET',
    credentials: 'include',
    query: {
      ...(options || {})
    },
  });
};

