

export function useEntityDetails(entityType: string, entityId: string){
  const apiUrl = import.meta.env.VITE_API_URL;

  return useFetch(`${apiUrl}/api/${entityType.slice(0, -1)}/`, {
    method: 'GET',
    params: {
      entityId
    },
  });
};

