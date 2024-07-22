<script>
  import fastapi from '../lib/api';
  import { link } from 'svelte-spa-router';
  import dayjs from 'dayjs';
  import 'dayjs/locale/ko';
  import relativeTime from 'dayjs/plugin/relativeTime';

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
            <a use:link href="/review-detail/{review.id}" class="text-reset link-underline link-underline-opacity-0">
              <h4 class="card-title text-truncate">{review.subject}</h4>
              <div class="d-flex justify-content-between align-items-center">
                <h6 class="card-subtitle">{review.book}</h6>
                <p class="card-text text-secondary">{review.author.username}</p>
              </div>
              <p>
                {dayjs(review.created_at).fromNow()}
              </p>
            </a>
          </div>
        </div>
      {/each}
    {/if}
  </div>
</div>
