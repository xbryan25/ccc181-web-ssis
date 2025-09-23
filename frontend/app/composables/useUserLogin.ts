
type UserLoginResponse = {
    message: string
    accessToken: string
    username: string
}

export function useUserLogin(email: string, password: string){
  const apiUrl = import.meta.env.VITE_API_URL;

  return $fetch<UserLoginResponse>(`${apiUrl}/api/user/login`, {
    method: 'POST',
    body: {
      email,
      password
    },
  });
};