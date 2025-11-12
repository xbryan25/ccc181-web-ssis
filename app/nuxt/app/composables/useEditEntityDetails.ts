import type { Student, Program, College } from "~/types";

type EditEntityResponse = {
    message: string
}

export function useEditEntityDetails(entityType: string, entityDetails: Student | Program | College, selectedEntity: string){
  const { $apiFetch } = useNuxtApp();

  return $apiFetch<EditEntityResponse>(`/api/${entityType}/${selectedEntity}`, {
    method: 'PATCH',
    credentials: 'include',
    body: {
      entityDetails
    },
  });
};