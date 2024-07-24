<script>
  import fastapi from '../lib/api';
  import { user_id } from '../lib/store';

  export let params = {};

  let username = params.username;
  let account = { following: [], followers: [] };
  let reviews = [];
  let comments = [];
  let is_following = false;

  function get_profile() {
    fastapi('get', '/api/account/get/' + username, {}, (json) => {
      account = json;
      chk_follow();
    });
  }

  get_profile();

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
  <div class="card border-light col-12 col-md-6 offset-md-3">
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
          {#if account.reviews}
            {#each account.reviews as review}
              {review.subject}
            {/each}
          {/if}
        </div>
        <div class="tab-pane fade" id="comment-tab-pane" role="tabpanel" aria-labelledby="comment-tab" tabindex="0">
          {#if account.comments}
            {#each account.comments as comment}
              {comment.content}
            {/each}
          {/if}
        </div>
      </div>
    </div>
  </div>
</div>
