<script>
  import Router from 'svelte-spa-router';
  import AccountCreate from './routes/AccountCreate.svelte';
  import AccountLogin from './routes/AccountLogin.svelte';

  const routes = {
    '/account-create': AccountCreate,
    '/account-login': AccountLogin,
  };
</script>

<Router {routes} />
