<script>
  import { link, push } from 'svelte-spa-router';
  import fastapi from '../lib/api';
  import { is_login, user_id } from '../lib/store';
  import dayjs from 'dayjs';
  import 'dayjs/locale/ko';
  import relativeTime from 'dayjs/plugin/relativeTime';
  import Icon, { _api } from '@iconify/svelte';

  dayjs.extend(relativeTime);
  dayjs.locale('ko');

  export let params = {};

  let review_id = params.review_id;
  let review = { author: {}, like_accounts: [], dislike_accounts: [] };
  let comment_list = [];
  let comment_flag = [];
  let review_flag = 0;
  let content = '';
  let size = 10;
  let page = 0;
  let total = 0;
  $: total_page = Math.ceil(total / size);

  function get_review() {
    fastapi('get', '/api/review/detail/' + review_id, {}, (json) => {
      comment_flag = [];
      review = json;
      for (let i = 0; i < review.comments.length; i++) {
        comment_flag.push(chk_like_comment(i));
      }
      chk_like_review();
      get_comment_list(page);
    });
  }

  function get_comment_list(_page) {
    let url = '/api/comment/list/' + review_id;
    let params = { page: _page, size: size };

    fastapi('get', url, { review_id: review_id }, (json) => {
      comment_list = json.comment_list;
      page = _page;
      total = json.total;
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

  function like_review() {
    let url = '/api/review/like';
    let params = {
      review_id: review.id,
    };

    fastapi('post', url, params, (json) => {
      get_review();
    });
  }

  function dislike_review() {
    let url = '/api/review/dislike';
    let params = {
      review_id: review.id,
    };

    fastapi('post', url, params, (json) => {
      get_review();
    });
  }

  function like_comment(comment_id) {
    let url = '/api/comment/like';
    let params = {
      comment_id: comment_id,
    };

    fastapi('post', url, params, (json) => {
      get_review();
    });
  }

  function dislike_comment(comment_id) {
    let url = '/api/comment/dislike';
    let params = {
      comment_id: comment_id,
    };

    fastapi('post', url, params, (json) => {
      get_review();
    });
  }

  function chk_like_review() {
    if (!$is_login) return;

    for (let i = 0; i < review.like_accounts.length; i++) {
      if (review.like_accounts[i].username == $user_id) {
        review_flag = 1;
        return;
      }
    }

    for (let i = 0; i < review.dislike_accounts.length; i++) {
      if (review.dislike_accounts[i].username == $user_id) {
        review_flag = 2;
        return;
      }
    }

    review_flag = 0;
    return;
  }

  function chk_like_comment(idx) {
    if (!$is_login) return;

    let comment = review.comments[idx];

    if (typeof comment !== 'undefined') {
      for (let i = 0; i < comment.like_accounts.length; i++) {
        if (comment.like_accounts[i].username == $user_id) {
          return 1;
        }
      }
    }

    if (typeof comment !== 'undefined') {
      for (let i = 0; i < comment.dislike_accounts.length; i++) {
        if (comment.dislike_accounts[i].username == $user_id) {
          return 2;
        }
      }
    }

    return 0;
  }
</script>

<div class="container">
  <div class="card border-light col-12 col-md-6 offset-md-3">
    <div class="card-header bg-transparent p-4">
      <div class="position-relative">
        <h3 class="card-title">{review.subject}</h3>
        <div class="position-absolute top-0 end-0">
          {#if review.author.username == $user_id}
            <a use:link href="/review-update/{review.id}" class="btn p-0">
              <Icon icon="material-symbols:edit" />
            </a>
            <button class="btn p-0 ps-1" on:click="{() => delete_review(review.id)}">
              <Icon icon="material-symbols:delete-outline" />
            </button>
          {/if}
        </div>
      </div>

      <h5 class="card-subtitle">{review.book}</h5>
      <div class="d-flex justify-content-between align-items-center mt-2">
        <a
          use:link
          href="/account-profile/{review.author.username}"
          class="mb-0 text-reset link-underline link-underline-opacity-0"
        >
          {review.author.username}
        </a>
        <p class="small mb-0">
          {dayjs(review.created_at).format('YY.MM.DD hh:mm')} 작성 {#if review.updated_at}
            | {dayjs(review.updated_at).format('YY.MM.DD hh:mm')} 수정
          {/if}
        </p>
      </div>
    </div>
    <div class="card-body p-4">
      <p class="card-text">{review.content}</p>
    </div>
    <hr />
    <div class="text-center mb-3 align-items-center">
      <div class="text-center d-flex align-items-center justify-content-center">
        <button
          class="btn border-0"
          on:click="{() => like_review()}"
          disabled="{review_flag === 2 || !$is_login || $user_id == review.author.username ? true : false}"
        >
          <span>{review.like_accounts.length}</span>
          <Icon icon="{review_flag === 1 ? 'material-symbols:thumb-up' : 'material-symbols:thumb-up-outline'}" />
        </button>
        <button
          class="btn border-0"
          on:click="{() => dislike_review()}"
          disabled="{review_flag === 1 || !$is_login || $user_id == review.author.username ? true : false}"
        >
          <Icon icon="{review_flag === 2 ? 'material-symbols:thumb-down' : 'material-symbols:thumb-down-outline'}" />
          <span>{review.dislike_accounts.length}</span>
        </button>
      </div>
    </div>
    <hr />
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
            {#each comment_list as comment, i}
              <tr>
                <td class="text-break w-75">
                  {comment.content}
                </td>
                <td class="align-middle flex position-relative">
                  <div class="flex">
                    <div class="text-center">
                      <a
                        use:link
                        href="/account-profile/{comment.author.username}"
                        class="mb-0 link-underline link-underline-opacity-0 text-reset"
                      >
                        {comment.author.username}
                      </a>
                    </div>
                    <p class="text-body-secondary mb-0 text-center" style="font-size: 0.65rem">
                      {#if comment.updated_at}
                        {dayjs(comment.updated_at).format('YY.MM.DD hh:mm')}
                      {:else}
                        {dayjs(comment.created_at).format('YY.MM.DD hh:mm')}
                      {/if}
                    </p>
                  </div>
                  <div class="d-flex align-items-center justify-content-center">
                    <div class="flex">
                      <button
                        class="btn btn-sm border-0"
                        on:click="{() => like_comment(comment.id)}"
                        disabled="{comment_flag[i] === 2 || !$is_login || $user_id == comment.author.username
                          ? true
                          : false}"
                      >
                        <Icon
                          icon="{comment_flag[i] === 1
                            ? 'material-symbols:thumb-up'
                            : 'material-symbols:thumb-up-outline'}"
                        />
                        <span style="font-size: 0.7rem">
                          {comment.like_accounts.length}
                        </span>
                      </button>
                    </div>
                    <div>
                      <button
                        class="btn btn-sm border-0"
                        on:click="{() => dislike_comment(comment.id)}"
                        disabled="{comment_flag[i] === 1 || !$is_login || $user_id == comment.author.username
                          ? true
                          : false}"
                      >
                        <Icon
                          icon="{comment_flag[i] === 2
                            ? 'material-symbols:thumb-down'
                            : 'material-symbols:thumb-down-outline'}"
                        />
                        <span style="font-size: 0.7rem">
                          {comment.dislike_accounts.length}
                        </span>
                      </button>
                    </div>
                  </div>
                  <span class="position-absolute top-0 end-0 d-flex">
                    {#if comment.author.username == $user_id}
                      <a use:link href="/comment-update/{comment.id}" class="btn btn-sm p-0">
                        <Icon icon="material-symbols:edit" width="0.7rem" height="0.7rem" />
                      </a>
                      <button class="btn btn-sm p-0 ps-1" on:click="{() => delete_comment(comment.id)}">
                        <Icon icon="material-symbols:delete-outline" width="0.7rem" height="0.7rem" />
                      </button>
                    {/if}
                  </span>
                </td>
              </tr>
            {/each}
          </tbody>
        </table>
        <ul class="pagination pagination-sm justify-content-center align-items-center">
          <li class="page-item {page <= 0 && 'disabled'}">
            <button class="page-link" on:click="{() => get_comment_list(page - 1)}">
              <Icon icon="material-symbols:keyboard-double-arrow-left" />
            </button>
          </li>
          {#each Array(total_page) as _, loop_page}
            {#if loop_page >= page - 5 && loop_page <= page + 5}
              <li class="page-item {loop_page === page && 'active'}">
                <button on:click="{() => get_comment_list(loop_page)}" class="page-link">{loop_page + 1}</button>
              </li>
            {/if}
          {/each}
          <li class="page-item {page >= total_page - 1 && 'disabled'}">
            <button on:click="{() => get_comment_list(page + 1)}" class="page-link">
              <Icon icon="material-symbols:keyboard-double-arrow-right" />
            </button>
          </li>
        </ul>
      {:else}
        <p>아직 댓글이 없어요</p>
      {/if}
    </div>
  </div>
</div>
