
type RefreshAccessTokenResponse = {
    accessTokenExpiresAt: number
}

export function useRefreshAccessToken(){
	const { $apiFetch } = useNuxtApp();

	return $apiFetch<RefreshAccessTokenResponse>(`/api/user/refresh`, {
		method: 'POST',
		credentials: 'include',
	});
};