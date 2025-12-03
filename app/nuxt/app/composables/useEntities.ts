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
                                filterByGender?: string,
                                filterByYearLevel?: string,
                                filterByProgramCode?: string,
                                sortField?: string, 
                                sortOrder?: string
                            }){

  const { $apiFetch } = useNuxtApp();

  return $apiFetch<UseEntitiesResponse>(`/api/${entityType}/`, {
    method: 'GET',
    credentials: 'include',
    query: {
      ...(options || {})
    },
  });
};

