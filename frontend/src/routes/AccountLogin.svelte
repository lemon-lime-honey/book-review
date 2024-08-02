<script>
  import { push } from 'svelte-spa-router';
  import Error from '../components/Error.svelte';
  import fastapi from '../lib/api';
  import { access_token, user_id, username, is_login } from '../lib/store';

  let login_username = '';
  let login_password = '';
  let error = { detail: [] };

  function login(event) {
    event.preventDefault();

    let url = '/api/account/login';
    let params = {
      username: login_username,
      password: login_password,
    };

    fastapi(
      'login',
      url,
      params,
      (json) => {
        error = { detail: [] };
        $access_token = json.access_token;
        $user_id = json.user_id;
        $username = json.username;
        $is_login = true;
        push('/');
      },
      (err_json) => {
        error = err_json;
      }
    );
  }
</script>

<div class="container d-flex justify-content-center">
  <div class="card w-75">
    <div class="card-body">
      <h4 class="card-title text-center mb-3">로그인</h4>
      <Error {error} />
      <form method="post">
        <div class="form-floating mb-2">
          <input type="text" class="form-control" id="username" placeholder="username" bind:value="{login_username}" />
          <label for="username">아이디</label>
        </div>
        <div class="form-floating mb-2">
          <input
            type="password"
            class="form-control"
            id="password"
            placeholder="password"
            bind:value="{login_password}"
          />
          <label for="password">비밀번호</label>
        </div>
        <button type="submit" class="btn btn-outline-success" on:click="{login}">로그인</button>
      </form>
    </div>
  </div>
</div>
