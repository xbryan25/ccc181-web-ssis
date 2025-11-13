import type { ProgramFormState, CollegeFormState } from "~/types";

type EditEntityResponse = {
    message: string
}

export function useEditEntityDetails(entityType: string, options: { entityDetails?: ProgramFormState | CollegeFormState; studentFormData?: FormData }, selectedEntity: string){
  const { $apiFetch } = useNuxtApp();

 return $apiFetch<EditEntityResponse>(`/api/${entityType}/${selectedEntity}`, {
    method: 'PATCH',
    credentials: 'include',
    body: options.entityDetails ?? options.studentFormData 
  });
};