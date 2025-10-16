
type DeleteEntityResponse = {
    message: string
}

export function useDeleteEntity(entityType: string, entityId: string){
  const apiUrl = import.meta.env.VITE_API_URL;

  return $fetch<DeleteEntityResponse>(`${apiUrl}/api/${entityType}/${entityId}`, {
    method: 'DELETE',
    credentials: 'include',
  });
};