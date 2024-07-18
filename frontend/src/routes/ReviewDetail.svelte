<script>
  import { link, push } from 'svelte-spa-router';
  import fastapi from '../lib/api';
  import moment from 'moment/min/moment-with-locales';
  import { username } from '../lib/store';

  moment.locale('ko');

  export let params = {};

  let review_id = params.review_id;
  let review = { author: {}, comments: [] };

  function get_review() {
    fastapi('get', '/api/review/detail/' + review_id, {}, (json) => {
      review = json;
    });
  }

  get_review();

  function delete_review(_review_id) {
    if (window.confirm('정말로 삭제하시겠습니까?')) {
      let url = '/api/review/delete';
      let params = {
        review_id: _review_id,
      };

      fastapi('delete', url, params, (json) => {
        push('/');
      });
    }
  }
</script>

<div class="container">
  <div class="card border-light col-12 col-md-6 offset-md-3">
    <div class="card-header bg-transparent p-4">
      <h3 class="card-title">{review.subject}</h3>
      <h5 class="card-subtitle">{review.book}</h5>
      <div class="d-flex justify-content-between align-items-center mt-2">
        <p class="mb-0">{review.author.username}</p>
        <p class="small mb-0">
          {moment(review.created_at).format('YY.MM.DD hh:mm')} 작성 {#if review.updated_at}
            | {moment(review.updated_at).format('YY.MM.DD hh:mm')} 수정
          {/if}
        </p>
      </div>
    </div>
    <div class="card-body p-4">
      <p class="card-text">{review.content}</p>
    </div>
    {#if review.author.username == $username}
      <hr />
      <div class="text-end mb-3">
        <button class="btn btn-sm btn-danger" on:click="{() => delete_review(review.id)}">삭제</button>
        <a use:link href="/review-update/{review.id}" class="btn btn-sm btn-success">수정</a>
      </div>
    {/if}
    <div class="card-footer bg-transparent p-4">
      {#if review.comments}
        {#each review.comments as comment}
          {comment.content}
        {/each}
      {:else}
        <p>아직 댓글이 없어요</p>
      {/if}
    </div>
  </div>
</div>
