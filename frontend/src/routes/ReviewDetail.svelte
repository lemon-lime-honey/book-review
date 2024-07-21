<script>
  import { link, push } from 'svelte-spa-router';
  import fastapi from '../lib/api';
  import moment from 'moment/min/moment-with-locales';
  import { is_login, username } from '../lib/store';

  moment.locale('ko');

  export let params = {};

  let review_id = params.review_id;
  let review = { author: {}, comments: [] };
  let content = '';

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

  function post_comment(event) {
    event.preventDefault();

    let url = '/api/comment/create/' + review_id;
    let params = { content: content };

    fastapi('post', url, params, (json) => {
      content = '';
      get_review();
    });
  }

  function delete_comment(comment_id) {
    if (window.confirm('정말로 삭제하시겠습니까?')) {
      let url = '/api/comment/delete';
      let params = {
        comment_id: comment_id,
      };

      fastapi('delete', url, params, (json) => {
        get_review();
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
    <hr />
    {#if review.author.username == $username}
      <div class="text-end mb-3">
        <button class="btn btn-sm btn-danger" on:click="{() => delete_review(review.id)}">삭제</button>
        <a use:link href="/review-update/{review.id}" class="btn btn-sm btn-success">수정</a>
      </div>
      <hr />
    {/if}
    {#if $is_login}
      <form method="post" class="mb-3">
        <div class="d-flex justify-content-between">
          <input type="text" class="form-control me-1" bind:value="{content}" />
          <input type="submit" class="btn btn-outline-primary btn-sm" on:click="{post_comment}" value="등록" />
        </div>
      </form>
    {:else}
      <p class="text-center">비회원은 댓글을 작성할 수 없습니다</p>
    {/if}

    <div class="card-footer bg-transparent p-2">
      {#if review.comments}
        <table class="table table-borderless table-hover align-middle">
          <tbody>
            {#each review.comments as comment}
              <tr>
                <td class="text-break w-75">{comment.content}</td>
                <td class="align-middle">
                  <div class="flex">
                    <p class="mb-0">{comment.author.username}</p>
                    <p class="text-body-secondary mb-0" style="font-size: 0.75rem">
                      {#if comment.updated_at}
                        {moment(comment.updated_at).format('YY.MM.DD hh:mm')}
                      {:else}
                        {moment(comment.created_at).format('YY.MM.DD hh:mm')}
                      {/if}
                    </p>
                  </div>
                </td>
                <td class="px-0">
                  {#if review.author.username == $username}
                    <a use:link href="/comment-update/{comment.id}" class="btn btn-sm btn-outline-success mb-1">수정</a>
                    <button class="btn btn-sm btn-outline-danger" on:click="{() => delete_comment(comment.id)}">
                      삭제
                    </button>
                  {:else}
                    <div class="flex">
                      <button class="btn btn-sm mb-1">u</button>
                      <button class="btn btn-sm">d</button>
                    </div>
                  {/if}
                </td>
              </tr>
            {/each}
          </tbody>
        </table>
      {:else}
        <p>아직 댓글이 없어요</p>
      {/if}
    </div>
  </div>
</div>
