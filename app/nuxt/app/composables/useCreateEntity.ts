
import type { ProgramFormState, CollegeFormState } from "~/types";

type CreateEntityResponse = {
    message: string
}

export function useCreateEntity(entityType: string, options: { entityDetails?: ProgramFormState | CollegeFormState; studentFormData?: FormData }){
  const { $apiFetch } = useNuxtApp();

  return $apiFetch<CreateEntityResponse>(`/api/${entityType}/`, {
    method: 'POST',
    credentials: 'include',
    body: options.entityDetails ?? options.studentFormData 
  });
};