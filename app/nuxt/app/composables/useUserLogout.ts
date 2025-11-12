
type UserLogoutResponse = {
    messageTitle: string
    message: string
}

export function useUserLogout(){
  const { $apiFetch } = useNuxtApp();

  return $apiFetch<UserLogoutResponse>(`/api/user/logout`, {
    method: 'POST',
    credentials: 'include',
  });
};