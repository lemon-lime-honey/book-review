<script>
  import DOMPurify from 'dompurify';
  import { marked } from 'marked';
  import { markedEmoji } from 'marked-emoji';
  import { push } from 'svelte-spa-router';
  import Error from '../components/Error.svelte';
  import fastapi from '../lib/api';
  import { options } from '../lib/emoji';

  let username = '';
  let password1 = '';
  let password2 = '';
  let email = '';
  let birthday = '2000-01-01';
  let summary = '';
  let error = { detail: [] };

  marked.use(markedEmoji(options));

  function post_account(event) {
    event.preventDefault();

    let url = '/api/account/create';
    let params = {
      username: DOMPurify.sanitize(username),
      password1: DOMPurify.sanitize(password1),
      password2: DOMPurify.sanitize(password2),
      email: DOMPurify.sanitize(email),
      birthday: DOMPurify.sanitize(birthday),
      summary: DOMPurify.sanitize(summary),
    };

    fastapi(
      'post',
      url,
      params,
      (json) => {
        push('/account-login');
      },
      (err_json) => {
        console.log(birthday);
        error = err_json;
      }
    );
  }
</script>

<div class="container d-flex justify-content-center">
  <div class="card w-75">
    <div class="card-body">
      <h4 class="card-title mb-3 text-center">회원가입</h4>
      <Error {error} />
      <form method="post">
        <div class="form-floating mb-2">
          <input type="text" class="form-control" id="username" placeholder="usename" bind:value="{username}" />
          <label for="username">아이디</label>
        </div>
        <div class="form-floating mb-2">
          <input type="text" class="form-control" id="email" placeholder="email" bind:value="{email}" />
          <label for="email">이메일</label>
        </div>
        <div class="d-flex justify-content-between">
          <div class="form-floating mb-2 me-1 flex-grow-1">
            <input
              type="password"
              class="form-control"
              id="password1"
              placeholder="password"
              bind:value="{password1}"
            />
            <label for="password1">비밀번호</label>
          </div>
          <div class="form-floating mb-2 ms-1 flex-grow-1">
            <input
              type="password"
              class="form-control"
              id="password2"
              placeholder="password"
              bind:value="{password2}"
            />
            <label for="password1">비밀번호 확인</label>
          </div>
        </div>
        <div class="input-group mb-2">
          <span class="input-group-text">생년월일</span>
          <input type="date" class="form-control" bind:value="{birthday}" />
        </div>
        <div class="d-flex mb-2" style="height: 200px;">
          <textarea
            class="form-control w-50 h-100 me-2"
            aria-label="자기소개"
            bind:value="{summary}"
            placeholder="자기소개"
          ></textarea>
          <div class="border border-secondary-subtle w-50 p-1 preview">{@html marked(summary)}</div>
        </div>
        <button class="btn btn-outline-success" on:click="{post_account}">가입</button>
      </form>
    </div>
  </div>
</div>
