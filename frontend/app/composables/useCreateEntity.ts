import type { Student, Program, College } from "~/types";

type CreateEntityResponse = {
    message: string
}

export function useCreateEntity(entityType: string, entityDetails: Student | Program | College){
  const apiUrl = import.meta.env.VITE_API_URL;

  return $fetch<CreateEntityResponse>(`${apiUrl}/api/${entityType}/`, {
    method: 'POST',
    body: {
      entityDetails
    },
  });
};