<script>
  import { push, querystring } from 'svelte-spa-router';
  import Error from '../components/Error.svelte';
  import fastapi from '../lib/api';

  let password1 = '';
  let password2 = '';
  let error = { detail: [] };

  let param = new URLSearchParams($querystring);

  function reset(event) {
    event.preventDefault();

    let url = '/api/account/reset';
    let params = {
      account_id: param.get('account_id'),
      password1: password1,
      password2: password2,
    };

    fastapi(
      'post',
      url,
      params,
      (json) => {
        error = { detail: [] };
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
      <h4 class="card-title text-center mb-3">비밀번호 재설정</h4>
      <Error {error} />
      <form method="post">
        <div class="form-floating mb-2">
          <input type="password" class="form-control" id="password1" placeholder="password1" bind:value="{password1}" />
          <label for="password1">비밀번호</label>
        </div>
        <div class="form-floating mb-2">
          <input type="password" class="form-control" id="password2" placeholder="password2" bind:value="{password2}" />
          <label for="password2">비밀번호 확인</label>
        </div>
        <button type="submit" class="btn btn-outline-success" on:click="{reset}">재설정</button>
      </form>
    </div>
  </div>
</div>
