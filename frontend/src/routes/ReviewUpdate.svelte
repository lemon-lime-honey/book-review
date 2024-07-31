<script>
  import { push } from 'svelte-spa-router';
  import Error from '../components/Error.svelte';
  import fastapi from '../lib/api';

  export let params = {};
  const review_id = params.review_id;

  let subject = '';
  let book = '';
  let content = '';
  let error = { detail: [] };

  fastapi('get', '/api/review/detail/' + review_id, {}, (json) => {
    subject = json.subject;
    book = json.book;
    content = json.content;
  });

  function update_review(event) {
    event.preventDefault();
    let url = '/api/review/update/' + review_id;
    let params = {
      review_id: review_id,
      subject: subject,
      book: book,
      content: content,
    };

    fastapi(
      'put',
      url,
      params,
      (json) => {
        push('/review-detail/' + review_id);
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
      <h4 class="card-title mb-3 text-center">후기 수정</h4>
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
          <textarea class="form-control" placeholder="content" id="content" style="height: 200px" bind:value="{content}"
          ></textarea>
          <label for="content">내용</label>
        </div>
        <button class="btn btn-outline-success" on:click="{update_review}">등록</button>
      </form>
    </div>
  </div>
</div>
