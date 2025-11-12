
type CurrentUserResponse = {
    username: string
}

export function useCurrentUser() {
  	const { $apiFetch } = useNuxtApp();

  	return $apiFetch<CurrentUserResponse>(`/api/user/me`, {
		method: 'GET',
		credentials: 'include',
	});
}