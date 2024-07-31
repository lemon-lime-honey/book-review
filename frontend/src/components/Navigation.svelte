<script>
  import { link } from 'svelte-spa-router';
  import { access_token, user_id, is_login } from '../lib/store';

  function logout(event) {
    event.preventDefault();
    $access_token = '';
    $user_id = 0;
    $is_login = false;
  }
</script>

<nav class="navbar bg-info-subtle mb-4">
  <div class="container-fluid">
    <a href="/" class="navbar-brand ms-3">BOOK</a>
    <div class="me-3">
      {#if $is_login == true}<a use:link href="/account-login" class="nav-link" on:click="{logout}">로그아웃</a>
      {:else}
        <div class="d-flex">
          <a use:link href="/account-create" class="nav-link me-2">회원가입</a>
          <a use:link href="/account-login" class="nav-link ms-2">로그인</a>
        </div>
      {/if}
    </div>
  </div>
</nav>
