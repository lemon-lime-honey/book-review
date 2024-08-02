<script>
  import { push } from 'svelte-spa-router';
  import Error from '../components/Error.svelte';
  import fastapi from '../lib/api';

  let error = { detail: [] };
  let username = '';
  let email = '';

  function match_account(event) {
    event.preventDefault();

    let url = '/api/account/match';
    let params = {
      username: username,
      email: email,
    };

    fastapi(
      'post',
      url,
      params,
      (json) => {
        error = { detail: [] };
        let qParams = new URLSearchParams({ account_id: json.id }).toString();
        const next_url = `/password-reset?${qParams}`;

        push(next_url);
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
      <h4 class="card-title text-center mb-3">계정 확인</h4>
      <Error {error} />
      <form method="post">
        <div class="form-floating mb-2">
          <input type="text" class="form-control" id="username" placeholder="username" bind:value="{username}" />
          <label for="username">아이디</label>
        </div>
        <div class="form-floating mb-2">
          <input type="text" class="form-control" id="email" placeholder="email" bind:value="{email}" />
          <label for="email">이메일</label>
        </div>
        <button type="submit" class="btn btn-outline-success" on:click="{match_account}">완료</button>
      </form>
    </div>
  </div>
</div>
