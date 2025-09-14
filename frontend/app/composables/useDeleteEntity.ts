
type DeleteEntityResponse = {
    message: string
}

export function useDeleteEntity(entityType: string, entityId: string){
  const apiUrl = import.meta.env.VITE_API_URL;

  return useFetch<DeleteEntityResponse>(`${apiUrl}/api/${entityType.slice(0, -1)}`, {
    method: 'DELETE',
    body: {
      entityId
    },
  });
};