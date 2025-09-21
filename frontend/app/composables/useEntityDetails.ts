

export function useEntityDetails(entityType: string, entityId: string){
  const apiUrl = import.meta.env.VITE_API_URL;

  return $fetch(`${apiUrl}/api/${entityType}/${entityId}`, {
    method: 'GET',
  });
};

