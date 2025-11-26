
type DeleteEntityResponse = {
    message: string
}

export function useDeleteEntity(entityType: string, entityIds: Set<string>){
  const { $apiFetch } = useNuxtApp();

  return $apiFetch<DeleteEntityResponse>(`/api/${entityType}`, {
    method: 'DELETE',
    credentials: 'include',
    body: { entityIds: Array.from(entityIds) }
  });
};