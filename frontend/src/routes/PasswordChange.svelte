<script>
  import { push } from 'svelte-spa-router';
  import Error from '../components/Error.svelte';
  import fastapi from '../lib/api';
  import { access_token, user_id, username, is_login } from '../lib/store';

  let password = '';
  let password1 = '';
  let password2 = '';
  let error = { detail: [] };

  function change(event) {
    event.preventDefault();

    let url = '/api/account/change';
    let params = {
      account_id: $user_id,
      password: password,
      password1: password1,
      password2: password2,
    };

    fastapi(
      'post',
      url,
      params,
      (json) => {
        error = { detail: [] };
        $access_token = '';
        $user_id = 0;
        $username = '';
        $is_login = false;
        push('/account-login');
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
      <h4 class="card-title text-center mb-3">비밀번호 변경</h4>
      <Error {error} />
      <form method="post">
        <div class="form-floating mb-2">
          <input type="password" class="form-control" id="password" placeholder="password" bind:value="{password}" />
          <label for="password">기존 비밀번호</label>
        </div>
        <div class="form-floating mb-2">
          <input type="password" class="form-control" id="password1" placeholder="password1" bind:value="{password1}" />
          <label for="password1">새 비밀번호</label>
        </div>
        <div class="form-floating mb-2">
          <input type="password" class="form-control" id="password2" placeholder="password2" bind:value="{password2}" />
          <label for="password2">새 비밀번호 확인</label>
        </div>
        <button type="submit" class="btn btn-outline-success" on:click="{change}">변경</button>
      </form>
    </div>
  </div>
</div>
