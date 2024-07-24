<script>
  import { push } from 'svelte-spa-router';
  import fastapi from '../lib/api';

  let username = '';
  let password1 = '';
  let password2 = '';
  let email = '';
  let birthday = null;
  let summary = '';

  function post_account(event) {
    event.preventDefault();

    let url = '/api/account/create';
    let params = {
      username: username,
      password1: password1,
      password2: password2,
      email: email,
      birthday: birthday,
      summary: summary,
    };

    fastapi('post', url, params, (json) => {
      push('/account-login');
    });
  }
</script>

<div class="container">
  <div class="card w-50">
    <div class="card-body">
      <h4 class="card-title mb-3 text-center">회원가입</h4>
      <form method="post">
        <div class="form-floating mb-2">
          <input type="text" class="form-control" id="username" placeholder="usename" bind:value="{username}" />
          <label for="username">아이디</label>
        </div>
        <div class="form-floating mb-2">
          <input type="password" class="form-control" id="password1" placeholder="password" bind:value="{password1}" />
          <label for="password1">비밀번호</label>
        </div>
        <div class="form-floating mb-2">
          <input type="password" class="form-control" id="password2" placeholder="password" bind:value="{password2}" />
          <label for="password1">비밀번호 확인</label>
        </div>
        <div class="form-floating mb-2">
          <input type="text" class="form-control" id="email" placeholder="email" bind:value="{email}" />
          <label for="email">이메일</label>
        </div>
        <div class="mb-2">
          <label for="birthday">생년월일</label>
          <input type="date" class="form-control" id="birthday" placeholder="birthday" bind:value="{birthday}" />
        </div>
        <div class="form-floating mb-2">
          <textarea id="summary" class="form-control" placeholder="summary" style="height: 100px" bind:value="{summary}"
          ></textarea>
          <label for="summary">자기소개</label>
        </div>
        <button class="btn btn-outline-success" on:click="{post_account}">가입</button>
      </form>
    </div>
  </div>
</div>
