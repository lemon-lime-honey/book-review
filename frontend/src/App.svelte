<script>
  import Navigation from './components/Navigation.svelte';
  import Router from 'svelte-spa-router';
  import Index from './routes/Index.svelte';
  import AccountCreate from './routes/AccountCreate.svelte';
  import AccountLogin from './routes/AccountLogin.svelte';
  import AccountProfile from './routes/AccountProfile.svelte';
  import AccountMatch from './routes/AccountMatch.svelte';
  import AccountUpdate from './routes/AccountUpdate.svelte';
  import PasswordChange from './routes/PasswordChange.svelte';
  import PasswordReset from './routes/PasswordReset.svelte';
  import ReviewCreate from './routes/ReviewCreate.svelte';
  import ReviewDetail from './routes/ReviewDetail.svelte';
  import ReviewUpdate from './routes/ReviewUpdate.svelte';
  import CommentUpdate from './routes/CommentUpdate.svelte';

  const routes = {
    '/': Index,
    '/account-create': AccountCreate,
    '/account-login': AccountLogin,
    '/account-profile/:username': AccountProfile,
    '/account-match': AccountMatch,
    '/account-update': AccountUpdate,
    '/password-change': PasswordChange,
    '/password-reset/': PasswordReset,
    '/review-create': ReviewCreate,
    '/review-detail/:review_id': ReviewDetail,
    '/review-update/:review_id': ReviewUpdate,
    '/comment-update/:comment_id': CommentUpdate,
  };
</script>

<Navigation />
<Router {routes} />
