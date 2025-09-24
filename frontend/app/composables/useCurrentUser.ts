
type CurrentUserResponse = {
    username: string
}

export async function useCurrentUser() {
  const apiUrl = import.meta.env.VITE_API_URL;

  return $fetch<CurrentUserResponse>(`${apiUrl}/api/user/me`, {
    method: 'GET',
    credentials: 'include',
  });
}