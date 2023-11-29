export function auth0Config(): { domain: string; clientId: string } {
  return {
    domain: process.env.VITE_AUTH0_DOMAIN!,
    clientId: process.env.VITE_AUTH0_CLIENT_ID!,
  };
}

export function backendApiUrl(): string {
  return process.env.VITE_REACT_APP_API_URL!;
}

export function graphqlApiUrl(): string {
  return backendApiUrl() + '/graphql';
}
