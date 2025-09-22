type UseEntityIdsResponse = {
    entityIds: {label: string}[]
}

export function useEntityIds(entityType: string){

  const apiUrl = import.meta.env.VITE_API_URL;

  return $fetch<UseEntityIdsResponse>(`${apiUrl}/api/${entityType}/identifiers`, {
    method: 'GET'
  });
};

