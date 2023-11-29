export function auth0Config(): { domain: string; clientId: string } {
  return {
    domain: import.meta.env.VITE_AUTH0_DOMAIN!,
    clientId: import.meta.env.VITE_AUTH0_CLIENT_ID!,
  };
}

export function backendApiUrl(): string {
  return import.meta.env.VITE_REACT_APP_API_URL!;
}

export function graphqlApiUrl(): string {
  return backendApiUrl() + '/graphql';
}
