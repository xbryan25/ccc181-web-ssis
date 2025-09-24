import type { H3Event } from 'h3'

type CurrentUserResponse = {
    username: string
}

export async function useCurrentUser(loadType: string, event?: H3Event | null) {
  const apiUrl = import.meta.env.VITE_API_URL;

  // If loadType === 'server', it is run during SSR
  // else, run during client

  if (loadType === 'server'){
    return $fetch<CurrentUserResponse>(`${apiUrl}/api/user/me`, {
      headers: {
        cookie: event?.node.req.headers.cookie || ''
      },
    })
  } else {
    return $fetch<CurrentUserResponse>(`${apiUrl}/api/user/me`, {
        method: 'GET',
        credentials: 'include',
    });
  }
}