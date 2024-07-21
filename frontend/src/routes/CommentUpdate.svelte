<script>
  import fastapi from '../lib/api';
  import { push } from 'svelte-spa-router';

  export let params = {};
  const comment_id = params.comment_id;

  let review_id = 0;
  let content = 0;

  fastapi('get', '/api/comment/detail/' + comment_id, {}, (json) => {
    review_id = json.review_id;
    content = json.content;
  });

  function update_comment(event) {
    event.preventDefault();
    let url = '/api/comment/update';
    let params = {
      comment_id: comment_id,
      content: content,
    };

    fastapi('put', url, params, (json) => {
      push('/review-detail/' + review_id);
    });
  }
</script>

<div class="container">
  <div class="card w-50">
    <div class="card-body">
      <h4 class="card-title mb-3 text-center">댓글 수정</h4>
      <form method="post">
        <div class="form-floating mb-2">
          <textarea class="form-control" placeholder="content" id="content" style="height: 100px" bind:value="{content}"
          ></textarea>
          <label for="content">내용</label>
        </div>
        <button class="btn btn-outline-success" on:click="{update_comment}">저장</button>
      </form>
    </div>
  </div>
</div>
