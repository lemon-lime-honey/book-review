<script>
  import Navigation from './components/Navigation.svelte';
  import Router from 'svelte-spa-router';
  import Index from './routes/Index.svelte';
  import AccountCreate from './routes/AccountCreate.svelte';
  import AccountLogin from './routes/AccountLogin.svelte';

  const routes = {
    '/': Index,
    '/account-create': AccountCreate,
    '/account-login': AccountLogin,
  };
</script>

<Navigation />
<Router {routes} />
