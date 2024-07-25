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
      console.log(review_list);
    });
  }

  get_review_list(0);
</script>

<div class="container">
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
              <h2 class="card-title text-truncate">{review.subject}</h2>
              <h5 class="card-subtitle">{review.book}</h5>
              <div class="d-flex justify-content-between align-items-center">
                <p class="card-text m-0 mt-2">
                  {dayjs(review.created_at).fromNow()}
                </p>
                <p class="card-text text-secondary">{review.author.username}</p>
              </div>
              <div class="position-absolute top-0 end-0">
                <span>{review.like_accounts.length}</span>
                <Icon icon="material-symbols:thumbs-up-down" />
                <span>{review.dislike_accounts.length}</span>
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
