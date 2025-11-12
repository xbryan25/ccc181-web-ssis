
type DeleteEntityResponse = {
    message: string
}

export function useDeleteEntity(entityType: string, entityId: string){
  const { $apiFetch } = useNuxtApp();

  return $apiFetch<DeleteEntityResponse>(`/api/${entityType}/${entityId}`, {
    method: 'DELETE',
    credentials: 'include',
  });
};