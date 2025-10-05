
type RefreshAccessTokenResponse = {
    accessTokenExpiresAt: number
}

export function useRefreshAccessToken(){
  const apiUrl = import.meta.env.VITE_API_URL;

	return $fetch<RefreshAccessTokenResponse>(`${apiUrl}/api/user/refresh`, {
    method: 'POST',
    credentials: 'include',
  });
};