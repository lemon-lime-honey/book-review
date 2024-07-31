<script>
  import fastapi from '../lib/api';
  import { link } from 'svelte-spa-router';
  import dayjs from 'dayjs';
  import 'dayjs/locale/ko';
  import relativeTime from 'dayjs/plugin/relativeTime';
  import Icon from '@iconify/svelte';

  dayjs.extend(relativeTime);
  dayjs.locale('ko');

  let review_list = [];
  let size = 12;
  let page = 0;
  let total = 0;
  $: total_page = Math.ceil(total / size);

  function get_review_list(_page) {
    let url = '/api/review/list';
    let params = { page: _page, size: size };

    fastapi('get', url, params, (json) => {
      review_list = review_list.concat(json.review_list);
      page = _page;
      total = json.total;
      hideSpinner();
    });
  }

  get_review_list(0);

  function hideSpinner() {
    document.getElementById('spinner').style.display = 'none';
  }
</script>

<div class="container">
  <div class="d-flex justify-content-center mt-5" style="height: 100%;">
    <div class="spinner-border" role="status" id="spinner">
      <span class="visually-hidden">Loading...</span>
    </div>
  </div>
  <div class="row row-cols-1 row-cols-md-2 row-cols-lg-4">
    {#if review_list}
      {#each review_list as review}
        <div class="col card border-light">
          <div class="card-body">
            <a
              use:link
              href="/review-detail/{review.id}"
              class="text-reset link-underline link-underline-opacity-0 position-relative"
            >
              <div class="position-absolute top-0 end-0">
                <Icon icon="material-symbols:mode-comment" />
                <span>{review.comments.length}</span>
                <Icon icon="material-symbols:thumb-up" />
                <span>{review.like_accounts.length}</span>
                <Icon icon="material-symbols:thumb-down" />
                <span>{review.dislike_accounts.length}</span>
              </div>
              <h2 class="card-title text-truncate mt-4 pt-3">{review.subject}</h2>
              <h5 class="card-subtitle text-truncate py-2">{review.book}</h5>
              <div class="d-flex justify-content-between align-items-center pb-3">
                <p class="card-text m-0 mt-2">
                  {dayjs(review.created_at).fromNow()}
                </p>
                <p class="card-text text-secondary">{review.author.username}</p>
              </div>
            </a>
          </div>
        </div>
      {/each}
    {/if}
  </div>
  {#if review_list && page < total_page - 1}
    <div class="d-flex justify-content-center">
      <button on:click="{() => get_review_list(page + 1)}" class="btn text-center">
        <Icon icon="material-symbols:more-vert" width="2em" height="2em" />
      </button>
    </div>
  {/if}
</div>
