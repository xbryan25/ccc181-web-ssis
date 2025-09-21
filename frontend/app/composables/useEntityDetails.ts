import type { Student, Program, College } from "~/types";

type EntityTypeMap = {
  students: Student
  programs: Program
  colleges: College
}

export function useEntityDetails<T extends keyof EntityTypeMap>(
  entityType: T,
  entityId: string
): Promise<EntityTypeMap[T]> {
  const apiUrl = import.meta.env.VITE_API_URL

  return $fetch<EntityTypeMap[T]>(`${apiUrl}/api/${entityType}/${entityId}`, {
    method: 'GET',
  })
}

