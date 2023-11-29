import { ApolloClient, ApolloProvider, InMemoryCache } from '@apollo/client';
import { Auth0Provider } from '@auth0/auth0-react';
import 'mapbox-gl/dist/mapbox-gl.css';
import React from 'react';
import ReactDOM from 'react-dom/client';
import { RouterProvider, createBrowserRouter } from 'react-router-dom';
import Home from './Home.tsx';
import RootLayout from './RootLayout.tsx';
import './index.css';
import { auth0Config, graphqlApiUrl } from './utils/helper.tsx';

const router = createBrowserRouter([
  {
    path: '/',
    element: <RootLayout />,
    children: [
      {
        index: true,
        element: <Home />,
      },
    ],
  },
]);

const client = new ApolloClient({
  uri: graphqlApiUrl(),
  cache: new InMemoryCache(),
});

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <Auth0Provider
      {...auth0Config()}
      authorizationParams={{
        redirect_uri: window.location.origin,
      }}
    >
      <ApolloProvider client={client}>
        <RouterProvider router={router} />
      </ApolloProvider>
    </Auth0Provider>
  </React.StrictMode>
);
