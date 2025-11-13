import type { StudentFormState, ProgramFormState, CollegeFormState } from "~/types";

type EditEntityResponse = {
    message: string
}

export function useEditEntityDetails(entityType: string, entityDetails: StudentFormState | ProgramFormState | CollegeFormState, selectedEntity: string){
  const { $apiFetch } = useNuxtApp();

  return $apiFetch<EditEntityResponse>(`/api/${entityType}/${selectedEntity}`, {
    method: 'PATCH',
    credentials: 'include',
    body: {
      entityDetails
    },
  });
};