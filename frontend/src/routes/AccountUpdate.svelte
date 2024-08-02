<script>
  import DOMPurify from 'dompurify';
  import { marked } from 'marked';
  import { markedEmoji } from 'marked-emoji';
  import { link, push } from 'svelte-spa-router';
  import Error from '../components/Error.svelte';
  import fastapi from '../lib/api';
  import { options } from '../lib/emoji';
  import { user_id, username } from '../lib/store';

  let usrname = '';
  let email = '';
  let birthday = '2000-01-01';
  let summary = '';
  let error = { detail: [] };

  fastapi('get', '/api/account/get/' + $username, {}, (json) => {
    usrname = json.username;
    email = json.email;
    birthday = json.birthday;
    summary = json.summary;
  });

  marked.use(markedEmoji(options));

  function update_account(event) {
    event.preventDefault();

    let url = '/api/account/update';
    let params = {
      id: $user_id,
      username: DOMPurify.sanitize(usrname),
      email: DOMPurify.sanitize(email),
      birthday: DOMPurify.sanitize(birthday),
      summary: DOMPurify.sanitize(summary),
    };

    fastapi(
      'put',
      url,
      params,
      (json) => {
        push('/');
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
      <h4 class="card-title mb-3 text-center">회원정보 수정</h4>
      <Error {error} />
      <form method="post">
        <div class="form-floating mb-2">
          <input type="text" class="form-control" id="username" placeholder="usename" bind:value="{usrname}" />
          <label for="username">아이디</label>
        </div>
        <div class="form-floating mb-2">
          <input type="text" class="form-control" id="email" placeholder="email" bind:value="{email}" />
          <label for="email">이메일</label>
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
        <div class="d-flex justify-content-between">
          <button class="btn btn-outline-success" on:click="{update_account}">저장</button>
          <a use:link href="/password-change" class="btn btn-outline-warning">비밀번호 변경</a>
        </div>
      </form>
    </div>
  </div>
</div>
