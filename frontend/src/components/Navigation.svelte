<script>
  import { link } from 'svelte-spa-router';
  import { access_token, username, is_login } from '../lib/store';

  function logout(event) {
    event.preventDefault();
    $access_token = '';
    $username = '';
    $is_login = false;
  }
</script>

<nav class="navbar navbar-expand-lg bg-body-tertiary mb-4">
  <div class="container-fluid">
    <a href="/" class="navbar-brand">BOOK</a>
    <button
      class="navbar-toggler"
      type="button"
      data-bs-toggle="collapse"
      data-bs-target="#navbar"
      aria-controls="navbar"
      aria-expanded="false"
      aria-label="Toggle navigation"
    >
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbar">
      <ul class="navbar-nav me-auto mb-2 mb-lg-0">
        {#if $is_login == true}
          <li class="nav-item">
            <a use:link href="/review-create" class="nav-link">후기 작성</a>
          </li>
          <li class="nav-item"><a use:link href="/account-login" class="nav-link" on:click="{logout}">로그아웃</a></li>
        {:else}
          <li class="nav-item">
            <a use:link href="/account-create" class="nav-link">회원가입</a>
          </li>
          <li class="nav-item">
            <a use:link href="/account-login" class="nav-link">로그인</a>
          </li>
        {/if}
      </ul>
    </div>
  </div>
</nav>
