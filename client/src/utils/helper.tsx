function requiredEnvVar(name: string): string {
  console.log(import.meta.env);

  const value = import.meta.env[name];

  if (!value) {
    throw new Error(`env variable ${name} is required!`);
  }

  return value;
}

export function auth0Config(): { domain: string; clientId: string } {
  return {
    domain: requiredEnvVar('VITE_AUTH0_DOMAIN'),
    clientId: requiredEnvVar('VITE_AUTH0_CLIENT_ID'),
  };
}

export function backendApiUrl(): string {
  return requiredEnvVar('VITE_AUTH0_DOMAIN');
}
