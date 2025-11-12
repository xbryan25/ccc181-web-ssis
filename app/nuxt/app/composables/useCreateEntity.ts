import type { Student, Program, College } from "~/types";

type CreateEntityResponse = {
    message: string
}

export function useCreateEntity(entityType: string, entityDetails: Student | Program | College){
  const { $apiFetch } = useNuxtApp();

  return $apiFetch<CreateEntityResponse>(`/api/${entityType}/`, {
    method: 'POST',
    credentials: 'include',
    body: {
      entityDetails
    },
  });
};