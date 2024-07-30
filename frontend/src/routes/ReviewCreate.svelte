<script>
  import { push } from 'svelte-spa-router';
  import Error from '../components/Error.svelte';
  import fastapi from '../lib/api';

  let subject = '';
  let book = '';
  let content = '';
  let error = { detail: [] };

  function post_review(event) {
    event.preventDefault();
    let url = '/api/review/create';
    let params = {
      subject: subject,
      book: book,
      content: content,
    };

    fastapi(
      'post',
      url,
      params,
      (json) => {
        push('/');
      },
      (err_json) => {
        error = err_json;
      }
    );
  }
</script>

<div class="container">
  <div class="card w-50">
    <div class="card-body">
      <h4 class="card-title mb-3 text-center">후기 작성</h4>
      <Error {error} />
      <form method="post">
        <div class="form-floating mb-2">
          <input type="text" class="form-control" id="subject" placeholder="subject" bind:value="{subject}" />
          <label for="subject">제목</label>
        </div>
        <div class="form-floating mb-2">
          <input type="text" class="form-control" id="book" placeholder="book" bind:value="{book}" />
          <label for="book">책 제목</label>
        </div>
        <div class="form-floating mb-2">
          <textarea class="form-control" placeholder="content" id="content" style="height: 100px" bind:value="{content}"
          ></textarea>
          <label for="content">내용</label>
        </div>
        <button class="btn btn-outline-success" on:click="{post_review}">등록</button>
      </form>
    </div>
  </div>
</div>
