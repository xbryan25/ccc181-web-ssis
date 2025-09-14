import type { Student, Program, College } from "~/types";

type EditEntityResponse = {
    message: string
}

export function useEditEntityDetails(entityType: string, entityDetails: Student | Program | College){
  const apiUrl = import.meta.env.VITE_API_URL;

  return useFetch<EditEntityResponse>(`${apiUrl}/api/${entityType}`, {
    method: 'PUT',
    body: {
      entityDetails
    },
  });
};