// <reference types="vite/client" />
interface ImportMetaEnv {
  VITE_REACT_APP_API_URL: string;
  VITE_AUTH0_CLIENT_ID: string;
  VITE_AUTH0_DOMAIN: string;
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}
