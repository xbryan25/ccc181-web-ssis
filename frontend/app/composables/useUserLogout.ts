
type UserLogoutResponse = {
    messageTitle: string
    message: string
}

export function useUserLogout(){
  const apiUrl = import.meta.env.VITE_API_URL;

  return $fetch<UserLogoutResponse>(`${apiUrl}/api/user/logout`, {
    method: 'POST',
    credentials: 'include',
  });
};