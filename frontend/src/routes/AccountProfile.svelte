<script>
  import { link } from 'svelte-spa-router';
  import relativeTime from 'dayjs/plugin/relativeTime';
  import fastapi from '../lib/api';
  import { user_id } from '../lib/store';
  import dayjs from 'dayjs';
  import 'dayjs/locale/ko';
  import Icon from '@iconify/svelte';

  export let params = {};

  dayjs.extend(relativeTime);
  dayjs.locale('ko');

  let username = params.username;
  let account = { following: [], followers: [] };
  let reviews = [];
  let comments = [];
  let review_size = 5;
  let review_page = 0;
  let review_total = 0;
  let comment_size = 5;
  let comment_page = 0;
  let comment_total = 0;
  let is_following = false;

  $: total_review_page = Math.ceil(review_total / review_size);
  $: total_comment_page = Math.ceil(comment_total / comment_size);

  function get_profile() {
    fastapi('get', '/api/account/get/' + username, {}, (json) => {
      account = json;
      chk_follow();
      get_reviews(0);
      get_comments(0);
    });
  }

  get_profile();

  function get_reviews(_review_page) {
    fastapi(
      'get',
      '/api/account/reviews',
      { account_id: account.id, page: _review_page, size: review_size },
      (json) => {
        reviews = json.review_list;
        review_page = _review_page;
        review_total = json.total;
      }
    );
  }

  function get_comments(_comment_page) {
    fastapi(
      'get',
      '/api/account/comments',
      { account_id: account.id, page: _comment_page, size: comment_size },
      (json) => {
        comments = json.comment_list;
        comment_page = _comment_page;
        comment_total = json.total;
      }
    );
  }

  function chk_follow() {
    is_following = false;
    if ($user_id == 0) return;
    account.followers.forEach((follower) => {
      if (follower.id === $user_id) {
        is_following = true;
        return;
      }
    });
    return;
  }

  function follow() {
    fastapi('post', '/api/account/follow', { account_id: account.id }, (json) => {
      get_profile();
    });
  }
</script>

<div class="container">
  <div class="card border-light col-12 col-md-8 col-lg-6 offset-md-2 offset-lg-3">
    <div class="card-header bg-transparent p-0">
      <div class="px-4 pt-4 d-flex justify-content-between align-items-center">
        <p class="h3">{account.username}</p>
        {#if is_following}
          <button
            on:click="{() => follow()}"
            class="btn btn-warning"
            disabled="{$user_id == 0 || $user_id === account.id ? true : false}"
          >
            언팔로우
          </button>
        {:else}
          <button
            on:click="{() => follow()}"
            class="btn btn-success"
            disabled="{$user_id == 0 || $user_id === account.id ? true : false}"
          >
            팔로우
          </button>
        {/if}
      </div>
      <hr class="p-0" />
      <div class="card-subtitle px-4 pb-4">
        <span>팔로우 {account.followers.length}</span>
        <span>팔로잉 {account.following.length}</span>
      </div>
      <p class="px-4 pb-3">{account.summary}</p>
    </div>
    <div class="card-body p-0">
      <ul class="nav nav-tabs pt-3" id="profile-tab" role="tablist">
        <li class="nav-item" role="presentation">
          <button
            class="nav-link active"
            id="review-tab"
            data-bs-toggle="tab"
            data-bs-target="#review-tab-pane"
            type="button"
            role="tab"
            aria-controls="review-tab-pane"
            aria-selected="true">작성한 후기</button
          >
        </li>
        <li class="nav-item" role="presentation">
          <button
            class="nav-link"
            id="comment-tab"
            data-bs-toggle="tab"
            data-bs-target="#comment-tab-pane"
            type="button"
            role="tab"
            aria-controls="comment-tab-pane"
            aria-selected="false">작성한 댓글</button
          >
        </li>
      </ul>
      <div class="tab-content" id="myTabContent">
        <div
          class="tab-pane fade show active"
          id="review-tab-pane"
          role="tabpanel"
          aria-labelledby="review-tab"
          tabindex="0"
        >
          {#if reviews}
            {#each reviews as review}
              <div class="card mx-1 my-2">
                <div class="card-body">
                  <a
                    use:link
                    href="/review-detail/{review.id}"
                    class="text-reset link-underline link-underline-opacity-0"
                  >
                    <div class="card-title">{review.subject}</div>
                    <div class="card-text text-truncate">{review.content}</div>
                    <div class="d-flex justify-content-between">
                      <div class="card-subtitle">{review.book}</div>
                      <div class="card-subtitle">
                        {review.updated_at
                          ? dayjs(review.updated_at).format('YY.MM.DD')
                          : dayjs(review.created_at).format('YY.MM.DD')}
                      </div>
                    </div>
                  </a>
                </div>
              </div>
            {/each}
            <ul class="pagination pagination-sm justify-content-center align-items-center">
              <li class="page-item {review_page <= 0 && 'disabled'}">
                <button class="page-link" on:click="{() => get_reviews(review_page - 1)}">
                  <Icon icon="material-symbols:keyboard-double-arrow-left" />
                </button>
              </li>
              {#each Array(total_review_page) as _, loop_page}
                {#if loop_page >= review_page - 5 && loop_page <= review_page + 5}
                  <li class="page-item {loop_page === review_page && 'active'}">
                    <button on:click="{() => get_reviews(loop_page)}" class="page-link">{loop_page + 1}</button>
                  </li>
                {/if}
              {/each}
              <li class="page-item {review_page >= total_review_page - 1 && 'disabled'}">
                <button on:click="{() => get_reviews(review_page + 1)}" class="page-link">
                  <Icon icon="material-symbols:keyboard-double-arrow-right" />
                </button>
              </li>
            </ul>
          {/if}
        </div>
        <div class="tab-pane fade" id="comment-tab-pane" role="tabpanel" aria-labelledby="comment-tab" tabindex="0">
          {#if comments}
            {#each comments as comment}
              <div class="card mx-1 my-2">
                <div class="card-body">
                  <a
                    use:link
                    href="/review-detail/{comment.review_id}"
                    class="text-reset link-underline link-underline-opacity-0"
                  >
                    <div class="card-text text-truncate">{comment.content}</div>
                    <div class="card-subtitle text-end">
                      {comment.updated_at
                        ? dayjs(comment.updated_at).format('YY.MM.DD')
                        : dayjs(comment.created_at).format('YY.MM.DD')}
                    </div>
                  </a>
                </div>
              </div>
            {/each}
            <ul class="pagination pagination-sm justify-content-center align-items-center">
              <li class="page-item {comment_page <= 0 && 'disabled'}">
                <button class="page-link" on:click="{() => get_comments(comment_page - 1)}">
                  <Icon icon="material-symbols:keyboard-double-arrow-left" />
                </button>
              </li>
              {#each Array(total_comment_page) as _, loop_page}
                {#if loop_page >= comment_page - 5 && loop_page <= comment_page + 5}
                  <li class="page-item {loop_page === comment_page && 'active'}">
                    <button on:click="{() => get_comments(loop_page)}" class="page-link">{loop_page + 1}</button>
                  </li>
                {/if}
              {/each}
              <li class="page-item {comment_page >= total_comment_page - 1 && 'disabled'}">
                <button on:click="{() => get_comments(comment_page + 1)}" class="page-link">
                  <Icon icon="material-symbols:keyboard-double-arrow-right" />
                </button>
              </li>
            </ul>
          {/if}
        </div>
      </div>
    </div>
  </div>
</div>
