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

  function get_review_list() {
    let url = '/api/review/list';

    fastapi('get', url, {}, (json) => {
      review_list = json;
    });
  }

  get_review_list();
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
</div>
