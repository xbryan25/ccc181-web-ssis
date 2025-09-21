import type { Student, Program, College } from "~/types";

type EditEntityResponse = {
    message: string
}

export function useEditEntityDetails(entityType: string, entityDetails: Student | Program | College, selectedEntity: string){
  const apiUrl = import.meta.env.VITE_API_URL;


  return $fetch<EditEntityResponse>(`${apiUrl}/api/${entityType}/${selectedEntity}`, {
    method: 'PUT',
    body: {
      entityDetails
    },
  });
};