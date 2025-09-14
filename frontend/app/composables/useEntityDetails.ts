

export function useEntityDetails(entityType: string, entityId: string){
  const apiUrl = import.meta.env.VITE_API_URL;

  return useFetch(`${apiUrl}/api/${entityType}/`, {
    method: 'GET',
    params: {
      entityId
    },
  });
};

