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

  const { $apiFetch } = useNuxtApp();

  return $apiFetch<EntityTypeMap[T]>(`/api/${entityType}/${entityId}`, {
    method: 'GET',
    credentials: 'include',
  })
}

