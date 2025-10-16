
type UserSignupResponse = {
    messageTitle: string
    message: string
}

export function useUserSignup(username: string, email: string, password: string){
  const apiUrl = import.meta.env.VITE_API_URL;

  return $fetch<UserSignupResponse>(`${apiUrl}/api/user/signup`, {
    method: 'POST',
    body: {
      username,
      email,
      password
    },
  });
};