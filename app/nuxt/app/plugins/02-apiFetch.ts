import type { FetchOptions } from 'ofetch';

type NitroFetchMethod =
  | 'GET' | 'POST' | 'PUT' | 'DELETE' | 'PATCH' | 'OPTIONS' | 'HEAD'
  | 'get' | 'post' | 'put' | 'delete' | 'patch' | 'options' | 'head';

let refreshPromise: Promise<void> | null = null;

export default defineNuxtPlugin((nuxtApp) => {
  const baseURL = import.meta.env.VITE_API_URL;

  // Wrapper for automatic refresh
  const fetchWithRefresh = async <T = any>(
    url: string,
    options?: FetchOptions
  ): Promise<T> => {
    try {

      const method = (options?.method?.toUpperCase() ?? 'GET') as NitroFetchMethod;

      return await $fetch<T>(`${baseURL}${url}`, {
        ...options,
        method,
      });
    } catch (err: any) {
      // If 401, refresh token and retry
      const status = err?.response?.status;
      if (status === 401) {
        if (!refreshPromise) {
          refreshPromise = (async () => {
            await $fetch(`${baseURL}/api/user/refresh`, {
              method: 'POST',
              credentials: 'include',
            });
          })().finally(() => (refreshPromise = null));
        }

        await refreshPromise;

        // Retry the original request
        const method = (options?.method?.toUpperCase() ?? 'GET') as NitroFetchMethod;

        return await $fetch.raw<T>(`${baseURL}${url}`, {
          ...options,
          method,
          credentials: 'include',
        }).then(res => res._data as T); // unwrap raw response
      }

      throw err;
    }
  };

  // Provide globally
  nuxtApp.provide('apiFetch', fetchWithRefresh);
});